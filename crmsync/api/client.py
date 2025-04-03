import json
import os
from typing import List

from api.models.account import Account
from api.models.product import Product
from pandas import Series

from crmsync.api.models.contact import Contact
from crmsync.api.models.policy import Policy


class PolicyAssembler:
    def __init__(self, row: Series):
        # Se asume que en cada registro existen los campos 'policy_id', 'policy_name'
        # y para el contacto: 'contactid', 'contact_name', 'contact_email'

        # Crear el objeto Contact a partir del registro.

        account = self.get_account(row)
        contacts: List[Contact] = self.get_contacts(row, account)
        self.update_account(contacts, account.id)
        product = self.get_product(row)

        self.get_policies(contacts, account.id, product.id)

        # policy.add_contact(contact)
        # Retornamos una lista de objetos Policy
        # return list(policy.values())

    def update_account(self, contacts: list[Contact], accountid):
        for contact in (c for c in contacts if c.data):
            # Actualiza solo si el accountid actual es distinto al nuevo
            if contact.account_name != accountid:
                contact.update(accountid)

    def get_account(self, row) -> Account:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "account_mapping.json")
        with open(file_path, "r", encoding="utf-8") as f:
            contact_mapping = json.load(f)

        for cfg in contact_mapping:
            # Si existe una clave "condition" y no se cumple, se salta este contacto.
            if "condition" in cfg and not row.get(cfg["condition"]):
                continue
            return Account(
                first_name=row.get(cfg["first_name"]),
                last_name=row.get(cfg["last_name"]),
                second_name=row.get(cfg["second_name"]),
                gender=row.get(cfg["gender"]),
                dob=row.get(cfg["dob"]),
                SSN=row.get(cfg["SSN"]),
                income=row.get(cfg["income"]),
                phone1=row.get(cfg["phone1"]),
                otherphone=row.get(cfg["otherphone"]),
                emergencyphone=row.get(cfg["emergencyphone"]),
                email1=row.get(cfg["email1"]),
                email2=row.get(cfg["email2"]),
                ship_street=row.get(cfg["ship_street"]),
                ship_pobox=row.get(cfg["ship_pobox"]),
                ship_city=row.get(cfg["ship_city"]),
                ship_state=row.get(cfg["ship_state"]),
                ship_code=row.get(cfg["ship_code"]),
            )

    def get_product(self, row: Series) -> Product:
        return Product(
            planid=row.get('cf_2035'),
            benefitid=row.get('cf_2203'),
        )

    def get_contacts(self, row: Series, account: Account) -> List[Contact]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "contacts_mapping.json")
        with open(file_path, "r", encoding="utf-8") as f:
            contact_mapping = json.load(f)

        contacts = []
        accountid = account.id

        for cfg in contact_mapping:
            # Si existe una clave "condition" y no se cumple, se salta este contacto.
            if "condition" in cfg and not row.get(cfg["condition"]):
                continue

            include_account = cfg.get("relationship") == "Owner"

            contacts.append(
                Contact(
                    first_name=row.get(cfg["first_name"]),
                    second_name=row.get(cfg["second_name"]),
                    last_name=row.get(cfg["last_name"]),
                    dob=row.get(cfg["dob"]),
                    ssn=row.get(cfg["ssn"]),
                    work=row.get(cfg["work"]),
                    gender=row.get(cfg["gender"]),
                    language=row.get(cfg["language"]),  # implement
                    account_name=accountid,
                    relationship=cfg["relationship"],
                    document=row.get(cfg["document"]),
                    mailing_street=row.get(cfg["ship_street"]),
                    mailing_pobox=row.get(cfg["ship_pobox"]),
                    mailing_city=row.get(cfg["ship_city"]),
                    mailing_state=row.get(cfg["ship_state"]),
                    mailing_code=row.get(cfg["ship_code"]),
                    apply=row.get(cfg["apply"]),
                    phone1=account.phone1 if include_account else None,
                    otherphone=account.otherphone if include_account else None,
                    emergencyphone=account.emergencyphone if include_account else None,
                    email1=account.email1 if include_account else None,
                    email2=account.email2 if include_account else None,
                )
            )
        return contacts

    def get_policies(self, contacts, accountid, productid) -> Policy:
        return Policy(
            contacts=contacts,
            accountid=accountid,
            productid=productid,
        )
