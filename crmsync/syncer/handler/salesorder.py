from dataclasses import dataclass, field
from typing import List, Optional

from syncer.handler.contact import Contact
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class SalesOrder(DocTypeHandler):
    contacts: List[Contact]
    customer_name: str
    item_name: str
    customer_address: str
    delivery_date: str
    custom_expiry_date: str
    custom_subscriber_id: str
    custom_app_review: str
    custom_consent: str
    custom_renew: str
    custom_sales_person: str
    custom_sales_date: str
    custom_digitizer: str
    transaction_date: str
    custom_ffm_app_id: str
    rate: float
    
    @classmethod
    def from_row(cls, row, contacts: List[Contact], customer_name, item_name, address_name):
        # Campos que quieres mapear directamente desde el row
        direct_fields = [
            "transaction_date", "delivery_date", "custom_expiry_date",
            "custom_ffm_app_id", "custom_subscriber_id", "custom_app_review",
            "custom_consent", "custom_renew", "custom_sales_person",
            "custom_sales_date", "custom_digitizer", "rate"
        ]

        # Genera kwargs dinámicamente desde el row
        kwargs = {field: row.get(field) for field in direct_fields}

        # Agrega los otros campos manuales
        return cls(
            contacts=contacts,
            customer_name=customer_name,
            item_name=item_name,
            customer_address=address_name,
            **kwargs
        )

    def __post_init__(self):
        self.doctype = "Sales Order"
        self.normalize_fields()
        self.normalize_and_sync()
        
    def normalize_fields(self):
        self.custom_consent = self.custom_consent if self.custom_consent != 'Email Send' else "Email Sent"

    def get_filters(self):
        return [
            ["Sales Order", "customer", "=", self.customer_name],
            ["Sales Order", "delivery_date", "=", self.delivery_date],
            ["Sales Order", "custom_expiry_date", "=", self.custom_expiry_date],
            ["Sales Order", "status", "not in", ["Closed", "Cancelled"]],
        ]

    def get_existing_name(self):
        return None

    def build_data(self):
        data =  {
            "customer": self.customer_name,
            "company": 'Mabe Center',
            "delivery_date": self.delivery_date,
            "custom_expiry_date": self.custom_expiry_date,
            "custom_ffm_app_id": self.custom_ffm_app_id,
            "transaction_date": self.transaction_date,
            "custom_subscriber_id": self.custom_subscriber_id,
            "custom_app_review": self.custom_app_review,
            "custom_consent": self.custom_consent,
            #"custom_renew": self.custom_renew,
            #"custom_sales_person": self.custom_sales_person,
            "items": [
                {
                    "item_code": self.item_name,
                    "item_name": self.item_name,
                    "uom": "Nos",                
                    "conversion_factor": 1.0,    
                    "qty": 1.0,
                    "rate": self.rate,
                },
            ],
            "customer_address": self.customer_address,
        }
        
        # Agregar entradas a custom_company_info si al menos un campo existe
        for contact in self.contacts:
            if contact.relationship:
                data.setdefault("custom_dependents", []).append({
                    "contact": contact.name,
                    "first_name": contact.first_name,
                    "middle_name": contact.middle_name,
                    "last_name": contact.last_name,
                    "gender": contact.gender,
                    "day_of_birth": contact.day_of_birth,
                    "relationship": contact.relationship,
                    "social_security_number": contact.social_security_number,
                    "job_type": contact.job_type,
                    "income": contact.income,
                    "migratory_status": contact.migratory_status,
                    "smoke": contact.smoke,
                    "been_in_jail": contact.been_in_jail,
                    "coverage": contact.coverage,
                    "language": contact.language,
                })
            
            if any([contact.member_id, contact.user, contact.password]):
                data.setdefault("custom_company_info", []).append({
                    "contact": contact.name,
                    "member_id": contact.member_id,
                    "user": contact.user,
                    "password": contact.password,
                })

        return data