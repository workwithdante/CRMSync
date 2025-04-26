import logging
import gc
from tqdm import tqdm
from typing import Dict, Tuple
from polars import DataFrame
from syncer.entry_parser_doc_simple import SimpleNameResolver
from syncer.handler.issue import Issue
from syncer.handler.task import Task

from crmsync.syncer.handler.customer import Customer
from crmsync.syncer.handler.contact import Contact
from syncer.handler.salesorder import SalesOrder
from crmsync.syncer.handler.address import Address
from crmsync.syncer.handler.item import Item
from crmsync.config import SyncConfig

logging.basicConfig(level=logging.INFO)

class PolicyAssembler:
    def __init__(self, config: SyncConfig, contact_id: str, rows: DataFrame):
        self.config = config
        self.contact_id = contact_id
        self.rows = rows

        self._contact_cache: Dict[Tuple[str, str, str], Contact] = {}
        self._address_cache: Dict[Tuple[str, str, str, str], Address] = {}

        # 1) Crear el customer UNA VEZ (la primera fila)
        first_row = rows.iloc[0]     
        customer = Customer.from_row(first_row, *self.config.customer_mapping)
        self.customer = customer

        # Precargar mappings
        addr_map = self.config.address_mapping[0]

        # 2) Iterar todas las filas (órdenes)
        for _, row in rows.iterrows():
            # 2.1) Address con caché
            addr_key = (
                row.get(addr_map["street"]),
                row.get(addr_map["city"]),
                row.get(addr_map["state"]),
                row.get(addr_map["code"]),
            )

            address = None
            if addr_key != ('', '', '', ''):
                if addr_key in self._address_cache:
                    address = self._address_cache[addr_key]
                else:
                    address = Address.from_row(row, addr_map, customer_name=customer.name)
                    self._address_cache[addr_key] = address

            # 2.2) Contact(es) con caché
            contacts = []
            for mapping in self.config.contact_mapping:
                if row.get(mapping["coverage"]) == '' or (row.get(mapping["first_name"]) == '' and row.get(mapping["last_name"])) == '':
                    continue

                fn = row.get(mapping["first_name"])
                ln = row.get(mapping["last_name"])
                dob = row.get(mapping["day_of_birth"])
                contact_key = (fn, ln, dob)

                relations_in_spanish = {
                    "ABUELO(A)": "Grandparent",
                    "HERMANO(A)": "Sibling",
                    "HIJO(A)": "Child",
                    "NIETO(A)": "Grandchild",
                    "PADRE/MADRE": "Parent",
                    "SOBRINO(A)": "Cousin",
                    "SUEGRO(O)": "Parent-In-Law",
                    "TIO(A)": "Uncle/Aunt",
                    "HIJASTRO(A)": "Stepchild",
                    "CUÑADO(A)": "Nibling",
                    "OTRO": "Other",
                    "YERNO/NUERA": "Nibling",
                    "PRIMO(A)": "Cousin",
                }
                
                relationship = relations_in_spanish.get(row.get(mapping["relationship"]), mapping["relationship"])

                if mapping["relationship"] == "Owner":
                    relationship = "Owner"
                elif mapping["relationship"] == "Spouse":
                    relationship = "Spouse"
                else:
                    relationship = relations_in_spanish.get(row.get(mapping["relationship"]), "Other")

                if contact_key in self._contact_cache:
                    contact = self._contact_cache[contact_key]  
                else:
                    contact = Contact.from_row(row, mapping, customer_name=customer.name)
                    self._contact_cache[contact_key] = contact

                contact.relationship = relationship
                contacts.append(contact)

            # 2.3) Item
            item = Item.from_row(row, *self.config.item_mapping)

            # 2.4) Documentos asociados a contactos
            documents = {
                row.get(f"document_person_{i}"): row.get(f"document_name_{i}")
                for i in range(1, 6)
                if row.get(f"document_name_{i}", None) not in (None, '')
            }

            parser = None

            if documents or not contacts:
                valid_names = [c.name.split("-")[0] for c in self._contact_cache.values()]
                parser = SimpleNameResolver(valid_names=valid_names if valid_names else [self.customer.name])

            for doc_person, doc_type in documents.items():
                [chunk] = parser.process_text(doc_person)
                target_name = chunk.get("matched")

                contact = next((c for c in contacts if c.name.startswith(target_name)), None)
                if contact:
                    contact.document_type.append(doc_type)
                    contact.document_deadline = getattr(row, "document_deadline", None)
            
            if parser and not contacts and self._contact_cache:
                [chunk] = parser.process_text(row.get("subject", self.customer.name))
                target_name = chunk.get("matched")
                contact = next((c for c in self._contact_cache.values() if c.name.startswith(target_name)), None)
                contact.relationship = "Owner"
                contacts.append(contact)



            # 2.5) Crear SalesOrder
            SalesOrder.from_row(
                row,
                contacts=contacts,
                customer_name=customer.name,
                item_name=item.name,
                address_name=address.name if address else None,
            )

        tqdm.write(
            f"Policy assembled for contact {contact_id}: "
            f"{len(rows)} orders, "
            f"{len(self._contact_cache)} contacts, "
            f"{len(self._address_cache)} addresses created"
        )

    def create_issue(self, subject: str, status: str, raw_description: str, raw_solution: str):
        self._create_issues_in_batches(subject, status, raw_description)
        if raw_solution:
            for issue in self._issued_issues:
                self._create_tasks_in_batches(issue.name, raw_solution)
        del self._issued_issues
        gc.collect()

    def _create_issues_in_batches(self, subject: str, status: str, raw_description: str, batch_size: int = 50):
        lines = raw_description.splitlines()
        batch: list[str] = []
        self._issued_issues: list[Issue] = []

        for i, line in enumerate(lines, start=1):
            batch.append(line)
            if i % batch_size == 0:
                self._flush_issue_batch(subject, status, batch)

        if batch:
            self._flush_issue_batch(subject, status, batch)

    def _flush_issue_batch(self, subject: str, status: str, batch: list[str]):
        text = "\n".join(batch)
        for chunk in self.parser.process_text(text):
            issue = Issue.from_row(
                subject=subject,
                status=status,
                date=chunk["date"],
                employee=chunk["name"],
                description=chunk["description"].replace("\n", "<br>"),
                customer_name=self.customer.name,
            )
            logging.info(f"Created issue: {issue.name}")
            self._issued_issues.append(issue)

        del text
        batch.clear()
        gc.collect()

    def _create_tasks_in_batches(self, issue_name: str, raw_solution: str, batch_size: int = 50):
        lines = raw_solution.splitlines()
        batch: list[str] = []

        for i, line in enumerate(lines, start=1):
            batch.append(line)
            if i % batch_size == 0:
                self._flush_task_batch(issue_name, batch)

        if batch:
            self._flush_task_batch(issue_name, batch)

    def _flush_task_batch(self, issue_name: str, batch: list[str]):
        text = "\n".join(batch)
        for chunk in self.parser.process_text(text):
            Task.from_row(
                subject="Follow‑up",
                employee=chunk["name"],
                issue_name=issue_name,
                description=chunk["description"].replace("\n", "<br>"),
            )
            logging.info(f"Created task for issue {issue_name}, assignee {chunk['name']}")

        del text
        batch.clear()
        gc.collect()
