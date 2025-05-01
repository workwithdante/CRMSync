from dataclasses import dataclass, field
from datetime import datetime
from typing import List

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
        self.custom_consent = self.custom_consent if self.custom_consent not in ('Email Send', 'Email Resend') else "Email Sent"

        self.transaction_date = self.transaction_date if self.transaction_date != 'None' and self.transaction_date else self.delivery_date

        if self.transaction_date > self.delivery_date:
            self.transaction_date = self.delivery_date

    def get_filters(self):
        filters = []

        if self.customer_name:
            filters.append(["Sales Order", "customer", "=", self.customer_name])
        if self.delivery_date:
            filters.append(["Sales Order", "delivery_date", "=", self.delivery_date])
        if self.custom_expiry_date:
            filters.append(["Sales Order", "custom_expiry_date", "=", self.custom_expiry_date])
        if self.custom_ffm_app_id:
            filters.append(["Sales Order", "custom_ffm_app_id", "=", self.custom_ffm_app_id])
        if self.custom_subscriber_id:
            filters.append(["Sales Order", "custom_subscriber_id", "=", self.custom_subscriber_id])
        if self.custom_app_review:
            filters.append(["Sales Order", "custom_app_review", "=", self.custom_app_review])
        if self.custom_consent:
            filters.append(["Sales Order", "custom_consent", "=", self.custom_consent])
        if self.custom_renew:
            filters.append(["Sales Order", "custom_renew", "=", self.custom_renew])
        if self.transaction_date or self.delivery_date:
            filters.append(["Sales Order", "transaction_date", "=", self.transaction_date if self.broker != 'Otro Broker' else self.delivery_date])
        if self.item_name:
            filters.append(["Sales Order Item", "item_code", "=", self.item_name])
        if self.rate:
            filters.append(["Sales Order Item", "rate", "=", float(self.rate) if self.rate else 0.0])


        return filters

    def get_filters_child(self):
        return [
            {
                "childtable": "custom_dependents",
                "conditions": {
                    "contact": [contact.name for contact in self.contacts],
                    "relationship": [contact.relationship for contact in self.contacts],
                }
            }
        ] if self.contacts else []


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
                    "rate": float(self.rate) if self.rate else 0.0,
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
            "broker_name": self.broker if self.broker else "",
            "national_producer_number": broker_npn.get(self.broker, 0.0),
            "initial_date": self.delivery_date,
            "end_date": self.custom_expiry_date,
        })
        
        # Agregar entradas a custom_company_info si al menos un campo existe
        for contact in self.contacts:
            if contact.relationship:
                data.setdefault("custom_dependents", []).append({
                    "contact": contact.name if contact.name else "",
                    "first_name": contact.first_name if contact.first_name else "",
                    "middle_name": contact.middle_name if contact.middle_name else "",
                    "last_name": contact.last_name if contact.last_name else "",
                    "gender": contact.gender if contact.gender else "Male",
                    "day_of_birth": contact.day_of_birth if contact.day_of_birth else "",
                    "relationship": contact.relationship if contact.relationship else "",
                    "social_security_number": contact.social_security_number if contact.social_security_number else "",
                    "job_type": contact.job_type if contact.job_type else "",
                    "income": float(contact.income) if contact.income else 0.0,
                    "migratory_status": contact.migratory_status if contact.migratory_status else "",
                    "smoke": contact.smoke if contact.smoke else "",
                    "been_in_jail": contact.been_in_jail if contact.been_in_jail else "",
                    "coverage": contact.coverage if contact.coverage else "",
                    "language": contact.language if contact.language else "",
                })
            
            if any([contact.member_id, contact.user, contact.password]):
                data.setdefault("custom_company_info", []).append({
                    "contact": contact.name if contact.name else "",
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