from dataclasses import dataclass
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class Task(DocTypeHandler):
    subject: str
    employee: str
    description: str
    issue_name: str
    
    @classmethod
    def from_row(cls, subject, employee, description, issue_name):
        return cls(
            subject=subject,
            employee=employee,
            description=description,
            issue_name=issue_name
        )

    def __post_init__(self):
        self.doctype = "Task"
        self.normalize_and_sync()
        
    def get_filters(self):
        return [
            ["Task", "subject", "=", self.subject],
            ["Task", "description", "=", self.description],
            ["Task", "issue", "=", self.issue_name],
        ]

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        return None

    def build_data(self):
        return {
            "subject": self.subject,
            "description": self.description,
            "priority": "Low",
            "status": "Completed",
            "issue": self.issue_name,
            "completed_by": self.employee,
            "completed_on": self.date
        }
