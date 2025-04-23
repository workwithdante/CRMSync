from dataclasses import dataclass, field
from typing import List, Optional

from syncer.handler.contact import Contact
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class SalesOrder(DocTypeHandler):
    contacts: List[Contact]
    customer_name: str
    item_name: str
    shipping_address_name: str
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
    broker: str
    
    @classmethod
    def from_row(cls, row, contacts: List[Contact], customer_name, item_name, address_name):
        # Campos que quieres mapear directamente desde el row
        direct_fields = [
            "transaction_date", "delivery_date", "custom_expiry_date",
            "custom_ffm_app_id", "custom_subscriber_id", "custom_app_review",
            "custom_consent", "custom_renew", "custom_sales_person",
            "custom_sales_date", "custom_digitizer", "rate", "broker"
        ]

        # Genera kwargs dinámicamente desde el row
        kwargs = {field: row.get(field) for field in direct_fields}

        # Agrega los otros campos manuales
        return cls(
            contacts=contacts,
            customer_name=customer_name,
            item_name=item_name,
            shipping_address_name=address_name,
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
            "company": 'Sierra Group',
            "delivery_date": self.delivery_date,
            "custom_expiry_date": self.custom_expiry_date,
            "custom_ffm_app_id": self.custom_ffm_app_id,
            "transaction_date": self.transaction_date if self.broker != 'Otro Broker' else self.delivery_date,
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
            "shipping_address_name": self.shipping_address_name if self.shipping_address_name else "",
            "territory": "United States",
            "customer_address": self.shipping_address_name if self.shipping_address_name else "",
        }
        
        if not self.shipping_address_name:
            data["shipping_address"] = ""
            data["address_display"] = ""
            
        broker_npn = {
            "Beatriz Sierra": 8602276,
            "Ana Daniella Corrales": 19011307,
            "Juan Ramirez": 4440000,
        }
            
        data.setdefault("custom_broker_info", []).append({
            "broker_name": self.broker,
            "national_producer_number": broker_npn.get(self.broker, 0.0),
            "initial_date": self.delivery_date,
            "end_date": self.custom_expiry_date,
        })
        
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
                    "member_id": contact.member_id if contact.member_id else "",
                    "user": contact.user if contact.user else "",
                    "password": contact.password if contact.password else "",
                })
            
            if contact.document_deadline:
                document_type = {
                    "Copia ss": "ssn",
                    "Negacion medicaid": "coverage",
                    "Prueba cambio de direccion": "coverage",
                    "Perdida de cobertura": "coverage",
                    "Prueba de ingresos": "income",
                    "Prueba migratoria": "migratory",
                    "Prueba no encarcelamiento": "coverage",
                    "Prueba Sep": "coverage",
                    "E. cobertura médica": "coverage",
                    "Prueba Ciudadanía": "citizenship",
                    "E. cobertura empleo": "coverage",
                }

                entry = {
                    "contact": contact.name,
                    "dateline": contact.document_deadline,
                }

                for doc_type in contact.document_type:
                    if key := document_type.get(doc_type):
                        entry[key] = 1

                data.setdefault("custom_documents", []).append(entry)

        return data