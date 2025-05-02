from dataclasses import dataclass, field
import re
from typing import Optional
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class BankAccount(DocTypeHandler):
    customer_name: str
    bank_account: Optional[str] = None
    bank_account_no: Optional[str] = None
    branch_code: Optional[str] = None
    card_account: Optional[str] = None
    card_number: Optional[str] = None
    card_verification_code: Optional[str] = None
    expiration_date: Optional[str] = None
    card_type: Optional[str] = None
    account_type: Optional[str] = None
    
    
    
    @classmethod
    def from_row(cls, row, mapping, customer_name, account_type, bank_account=None):
        return cls(
            customer_name=customer_name,
            bank_account=bank_account,
            bank_account_no=row.get(mapping["bank_account_no"]),
            branch_code=row.get(mapping["branch_code"]),
            card_account=row.get(mapping["card_account"]),
            card_number=row.get(mapping["card_number"]),
            card_verification_code=row.get(mapping["card_verification_code"]),
            expiration_date=row.get(mapping["expiration_date"]),
            card_type=row.get(mapping["card_type"]),
        )

    def __post_init__(self):
        self.doctype = "Bank Account"
        self.normalize_fields()
        self.normalize_and_sync()
    
    def normalize_fields(self):
        CARDS = {
            "VISA": "Visa Inc",
            "MASTERCARD": "Mastercard Incorporated",
            "AMERICAN EXPRESS": "American Express Company",
            "DISCOVERY": "Discover Financial Services",
        }

        self.card_account = CARDS.get(self.card_account, "")

    def get_filters(self):
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        if self.account_type == "Bank":
            return f"{self.bank_account_no[:4]} - {self.bank_account} - {self.customer_name}"
        else:
            return f"{self.card_number[:4]} - {self.card_account} - {self.customer_name}"

    def build_data(self):
        data = {
            "account_name": self.customer_name,
            "party_type": "Customer",
            "party": self.customer_name,
        }
        
        if self.bank_account:
            data["account_type"] = "Bank"
            data["bank"] = self.bank_account
            data["account_subtype"] = "Checking"
            data["branch_code"] = self.branch_code
            data["bank_account_no"] = self.bank_account_no
        elif self.card_account:
            if self.card_type == "Crédito":
                data["account_type"] = "Credit Card"
            elif self.card_type == "Débito":
                data["account_type"] = "Debit Card"
            else:
                return None
            
            data["bank"] = self.card_account
            data["custom_card_number"] = self.card_number
            data["custom_card_verification_code"] = self.card_verification_code
            data["custom_expiration_date"] = self.expiration_date
        else:
            return None
        
        return data
