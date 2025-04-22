import logging
from typing import Dict, List, Tuple
from pandas import DataFrame
from syncer.entry_parser import EntryParserNER
from syncer.handler.issue import Issue
from syncer.handler.task import Task

from crmsync.syncer.handler.customer import Customer
from crmsync.syncer.handler.contact import Contact
from syncer.handler.salesorder import SalesOrder
from crmsync.syncer.handler.address import Address
from crmsync.syncer.handler.item import Item
from crmsync.config import SyncConfig

# at the very top of your file
import gc


logging.basicConfig(level=logging.INFO)

class PolicyAssembler:
    def __init__(self, config: SyncConfig, contact_id: str, rows: DataFrame):
        self.config = config
        self.contact_id = contact_id
        self.rows = rows
        
        self.valid_names = [
            "Jorge Devia", "Yesica Bedoya", "Yorlady Franco", "Luisa Buitrago",
            "Carolina Gomez", "Margarita Mesa", "Wendy Patiño", "Valentina Carvajal",
            "Karen Arias", "Julieth Loaiza", "Tatiana Betancourt", "Juan Ocampo",
            "Anyela Ospina", "Juan Alarcón", "Santiago Moncada", "Victoria Cuellar",
            "Ximena Cuenca", "Elizabeth Arias", "Yuliana Hidalgo", "Alejandra Paramo",
            "Yensi Cruz", "Adriana Infante", "Angela Manso", "Natalia Sierra",
            "Jennifer Arango", "Maira Santander", "Daniela Lopez", "Danna Suarez",
            "Karol Ramirez", "Yesica Ramirez", "Erika Castro", "Eliana Sanchez", "Eliana Gil",
            "Alejandro Ruiz", "Paula Bastidas", "Yuliana Perez", "Lilian Aristizabal"
        ]
        
        # 0) Instanciamos UNA SOLA VEZ el parser SpaCy+fuzzy
        self.parser = EntryParserNER(
            valid_names=self.valid_names,
            ner_model_path="model/model-best"
        )
        # Para acelerar: eliminar tok2vec (solo NER + ruler + custom)
        if "tok2vec" in self.parser.nlp.pipe_names:
            self.parser.nlp.remove_pipe("tok2vec")

        
        # Cachés internos
        # Key contacto: (first_name, last_name, day_of_birth)
        self._contact_cache: Dict[Tuple[str,str,str], Contact] = {}
        # Key dirección: (address_title, address_type, address_line1,
        #                  city, state, pincode, country)
        self._address_cache: Dict[Tuple[str,str,str,str,str,str,str], Address] = {}

        # 1) Crear el customer UNA VEZ (la primera fila)
        first_row = rows.iloc[0]
        # Supongo que Customer.from_row toma (row, mapping, **kwargs)
        customer = Customer.from_row(first_row, *self.config.customer_mapping)
        self.customer = customer

        # 2) Iterar todas las filas (órdenes)
        for _, row in rows.iterrows():
            # 2.1) Address con caché
            addr_map = self.config.address_mapping[0]  # asumo un solo mapping
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
                    address = Address.from_row(
                        row,
                        addr_map,
                        customer_name=customer.name
                    )
                    self._address_cache[addr_key] = address

            # 2.2) Contact(es) con caché
            contacts = []
            for mapping in self.config.contact_mapping:
                if not row.get(mapping["coverage"]):
                    continue

                fn = row.get(mapping["first_name"])
                ln = row.get(mapping["last_name"])
                dob = row.get(mapping["day_of_birth"])
                contact_key = (fn, ln, dob)

                if contact_key in self._contact_cache:
                    contact = self._contact_cache[contact_key]
                else:
                    contact = Contact.from_row(
                        row,
                        mapping,
                        customer_name=customer.name
                    )
                    self._contact_cache[contact_key] = contact

                contacts.append(contact)
            
            # 2.3) Item (siempre uno nuevo)
            item = Item.from_row(row, *self.config.item_mapping)

            # 2.4) SalesOrder para esta fila
            SalesOrder.from_row(
                row,
                contacts=contacts,
                customer_name=customer.name,
                item_name=item.name,
                address_name=address.name if address else None,
            )

        logging.info(
            f"✅ Policy assembled for contact {contact_id}: "
            f"{len(rows)} orders, "
            f"{len(self._contact_cache)} contacts, "
            f"{len(self._address_cache)} addresses created"
        )
        
    def create_issue(
        self,
        subject: str,
        status: str,
        raw_description: str,
        raw_solution: str,
    ):
        """
        Break raw_description into batches, parse each batch into issues, then
        for each issue spawn batched tasks if raw_solution is provided.
        """
        # batch‐parse the description into Issue objects
        self._create_issues_in_batches(subject, status, raw_description)

        # if there is a solution, batch‐create the tasks for all those issues
        if raw_solution:
            for issue in self._issued_issues:
                self._create_tasks_in_batches(issue.name, raw_solution)

        # once done, clear the issue list and collect
        del self._issued_issues
        gc.collect()

    def _create_issues_in_batches(
        self,
        subject: str,
        status: str,
        raw_description: str,
        batch_size: int = 50
    ):
        """Split raw_description into line‐batches, parse, and emit Issue.from_row."""
        lines = raw_description.splitlines()
        batch: list[str] = []
        self._issued_issues: list[Issue] = []

        for i, line in enumerate(lines, start=1):
            batch.append(line)
            if i % batch_size == 0:
                self._flush_issue_batch(subject, status, batch)

        # flush any remainder
        if batch:
            self._flush_issue_batch(subject, status, batch)

    def _flush_issue_batch(
        self,
        subject: str,
        status: str,
        batch: list[str]
    ):
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

        # free immediately
        del text
        batch.clear()
        gc.collect()

    def _create_tasks_in_batches(
        self,
        issue_name: str,
        raw_solution: str,
        batch_size: int = 50
    ):
        """Split raw_solution into line‐batches, parse, and emit Task.from_row."""
        lines = raw_solution.splitlines()
        batch: list[str] = []

        for i, line in enumerate(lines, start=1):
            batch.append(line)
            if i % batch_size == 0:
                self._flush_task_batch(issue_name, batch)

        if batch:
            self._flush_task_batch(issue_name, batch)

    def _flush_task_batch(
        self,
        issue_name: str,
        batch: list[str]
    ):
        text = "\n".join(batch)
        for chunk in self.parser.process_text(text):
            Task.from_row(
                subject="Follow‑up",
                employee=chunk["name"],
                issue_name=issue_name,
                description=chunk["description"].replace("\n", "<br>"),
            )
            logging.info(f"Created task for issue {issue_name}, assignee {chunk['name']}")

        # free immediately
        del text
        batch.clear()
        gc.collect()
