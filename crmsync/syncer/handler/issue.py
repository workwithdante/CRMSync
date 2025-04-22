from dataclasses import dataclass, field
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class Issue(DocTypeHandler):
    subject: str
    status: str
    date: str
    employee: str
    description: str
    customer_name: str
    
    @classmethod
    def from_row(cls, subject, status, date, employee, description, customer_name):
        return cls(
            subject=subject,
            status=status,
            date=date,
            employee=employee,
            description=description,
            customer_name=customer_name
        )

    def __post_init__(self):
        self.doctype = "Issue"
        self.normalize_fields()
        self.normalize_and_sync()

    def normalize_fields(self):
        issue_status = {
            "Open": "Open",
            "Closed": "Resolved",
            "In Progress": "Replied",
            "Wait For Response": "On Hold"
        }
        self.status = issue_status.get(self.status, "Open")
        
    def get_filters(self):
        return [
            ["Issue", "subject", "=", self.subject],
            ["Issue", "description", "=", self.description],
            ["Issue", "status", "=", self.status],
            ["Issue", "customer", "=", self.customer_name],
        ]
    
    def get_existing_name(self):
        return None

    def build_data(self):
        return {
            "subject": self.subject,
            "description": self.description,
            "priority": "Low",
            "status": self.status,
            "customer": self.customer_name,
        }
