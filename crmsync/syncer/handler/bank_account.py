from dataclasses import dataclass, field
import re
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler
from datetime import datetime

@dataclass
class BankAccount(DocTypeHandler):
    customer_name: str
    bank_name: Optional[str] = None
    bank_account_no: Optional[str] = None
    branch_code: Optional[str] = None
    card_number: Optional[str] = None
    card_verification_code: Optional[str] = None
    card_expiration_date: Optional[str] = None
    account_type: Optional[str] = None
    
    
    
    @classmethod
    def from_row(cls, row, mapping, customer_name, account_type, bank_name):
        return cls(
            customer_name=customer_name,
            bank_name=bank_name,
            bank_account_no=row.get(mapping["bank_account_no"]),
            branch_code=row.get(mapping["branch_code"]),
            card_number=row.get(mapping["card_number"]),
            card_verification_code=row.get(mapping["card_verification_code"]),
            card_expiration_date=row.get(mapping["card_expiration_date"]),
            account_type=account_type,
        )

    def __post_init__(self):
        self.doctype = "Bank Account"
        self.normalize_fields()
        self.normalize_and_sync()
    
    def normalize_fields(self):
        RE_NON_LETTER = re.compile(r'\D+')
        self.bank_account_no = RE_NON_LETTER.sub("", self.bank_account_no)
        self.branch_code = RE_NON_LETTER.sub("", self.branch_code)
        self.card_number = RE_NON_LETTER.sub("", self.card_number)
        
        if(self.account_type != "Bank"):
            self.card_verification_code = RE_NON_LETTER.sub("", self.card_verification_code).zfill(3)[:3]
            self.card_expiration_date = RE_NON_LETTER.sub("", self.card_expiration_date).zfill(4)[:4]
            month = self.card_expiration_date[:2]
            year = self.card_expiration_date[2:]
            self.card_expiration_date = f"20{year}-{month}-01"
                
    def get_filters(self):
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        if self.account_type == "Bank":
            return f"{self.bank_account_no[:4]} - {self.bank_name} - {self.customer_name}"
        else:
            return f"{self.card_number[:4]} - {self.bank_name} - {self.customer_name}"

    def build_data(self):
        data = {
            "account_name": self.customer_name,
            "bank": self.bank_name,
            "party_type": "Customer",
            "party": self.customer_name,
            "account_type": self.account_type
        }
        
        if self.account_type == "Bank":
            data["account_subtype"] = "Checking"
            data["branch_code"] = self.branch_code
            data["bank_account_no"] = self.bank_account_no
        else:           
            data["custom_card_number"] = self.card_number
            data["custom_card_verification_code"] = self.card_verification_code
            data["custom_expiration_date"] = self.card_expiration_date
        
        return data
