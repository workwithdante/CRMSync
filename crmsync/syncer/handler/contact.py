from dataclasses import dataclass, field
import re
from typing import List, Optional
from crmsync.syncer.handler.base import DocTypeHandler

@dataclass
class Contact(DocTypeHandler):
    customer_name: str
    relationship: str
    first_name: str
    middle_name: str
    coverage: str
    last_name: str
    gender: str
    day_of_birth: str
    social_security_number: str
    migratory_status: str
    job_type: Optional[str] = None
    income: Optional[str] = "0"
    language: Optional[str] = None
    smoke: Optional[str] = None
    been_in_jail: Optional[str] = None
    phone: Optional[str] = None
    mobile_no: Optional[str] = None
    email1: Optional[str] = None
    email2: Optional[str] = None
    member_id: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    document_type: Optional[List[str]] = field(default_factory=list)
    document_deadline: Optional[str] = None

    def __post_init__(self):
        self.doctype = "Contact"
        self.normalize_fields()
        self.normalize_and_sync()
        
    @classmethod
    def from_row(cls, row, cfg, customer_name):
        return cls(
            customer_name=customer_name,
            relationship='Spouse' if cfg['relationship'] == 'Spouse' else row.get(cfg["relationship"]),
            coverage=row.get(cfg["coverage"]),
            first_name=row.get(cfg["first_name"]),
            middle_name=row.get(cfg["middle_name"]),
            last_name=row.get(cfg["last_name"]),
            gender=row.get(cfg["gender"]),
            day_of_birth=row.get(cfg["day_of_birth"]),
            social_security_number=row.get(cfg["social_security_number"]),
            migratory_status=row.get(cfg["migratory_status"]),
            job_type=row.get(cfg["job_type"]),
            income=row.get(cfg["income"]),
            language=row.get(cfg["language"]),
            phone=row.get(cfg.get("phone")) if cfg['relationship'] == 'Owner' else None,
            mobile_no=row.get(cfg.get("mobile_no")) if cfg['relationship'] == 'Owner' else None,
            email1=row.get(cfg.get("email1")) if cfg['relationship'] == 'Owner' else None,
            email2=row.get(cfg.get("email2")) if cfg['relationship'] == 'Owner' else None,
            smoke=row.get(cfg["smoke"]),
            been_in_jail=row.get(cfg["been_in_jail"]),
            member_id=row.get(cfg["member_id"]),
            user=row.get(cfg["user"]),
            password=row.get(cfg["password"]),
        )
        
    def normalize_fields(self):        
        coverage_list = {
            "OBAMACARE": "Obamacare",
            "MEDICARE": "Medicare",
            "MEDICAID": "Medicaid",
            "NO APLICA": "Other",
        }
        
        self.coverage = coverage_list.get(self.coverage) if self.coverage else "Other"
            
        self.social_security_number = self.social_security_number.replace("-", "") if self.social_security_number else None
        
        document_list_in_spanish = {
            "CIUDADANO": "Passport",
            "ANTORCHA": "Notice of Action (I-797)",
            "NOTICIA DE ACCION": "Notice of Action (I-797)",
            "RESIDENTE": "Resident (I-551)",
            "ASILO POLITICO": "Refugee Travel (I-571)",
            "PERMISO DE TRABAJO": "Employment Authorization (I-766)",
            "VISA": "Visa (temporary I-551)",
            "PAROL": "Temporary (passport or I-94/I-94A)",
            "TPS": "Temporary (passport or I-821)",
            "PASAPORTE VIAJERO": "Foreign Passport",
            "I-20": "Nonimmigrant Student Status (I-20)",
            "I-94": "Alien number or I-94 number",
        }
        
        self.migratory_status = document_list_in_spanish.get(self.migratory_status)
        self.smoke =  'No' if self.smoke != "YES" else 'Yes'
        self.been_in_jail = 'No' if self.been_in_jail != "YES" else 'Yes'
        self.day_of_birth = self.day_of_birth.strftime("%Y-%m-%d") if self.day_of_birth else None
        
        self.gender = self.gender.capitalize() if self.gender else None
        self.language = self.language.capitalize() if self.language else None
        
        self.email1 = self.email1.lower() if self.email1 else None
        self.email2 = self.email2.lower() if self.email2 else None
        
        self.phone = re.sub(r'\D', '', self.phone) if self.phone else None
        self.mobile_no = re.sub(r'\D', '', self.mobile_no) if self.mobile_no else None
        
    def get_filters(self):
        return None

    def get_filters_child(self):
        return None
    
    def get_existing_name(self):
        return self.full_name()

    def build_data(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "custom_day_of_birth": self.day_of_birth,
            "gender": self.gender,
            "links": [
                {
                    "link_doctype": "Customer",
                    "link_name": self.customer_name,
                }
            ]
        }

        if self.social_security_number:
            clean_ssn = re.sub(r'\D', '', self.social_security_number).zfill(9) if self.social_security_number else None
            if len(clean_ssn) <= 9:
                data["custom_social_security_number"] = clean_ssn
            else:
                raise ValueError("Social Security Number must be 8 digits long.")
        
        if self.relationship == "Owner":
            data["is_primary_contact"] = 1
            data["is_billing_contact"] = 1

        email_list = [self.email1, self.email2]

        for i, email in enumerate(filter(None, email_list)):
            data.setdefault('email_ids', []).append({
                'email_id': email,
                'is_primary': 1 if i == 0 else 0
            })


        if self.phone or self.mobile_no:
            phone_entries = []

            if self.phone:
                phone_entries.append({
                    "phone": self.phone,
                    "is_primary_phone": 1,
                    "is_primary_mobile_no": 0
                })

            if self.mobile_no:
                phone_entries.append({
                    "phone": self.mobile_no,
                    "is_primary_phone": 0,
                    "is_primary_mobile_no": 1
                })

            data["phone_nos"] = phone_entries

        return data

    def full_name(self):
        return " ".join(filter(None, [self.first_name, self.middle_name, self.last_name])) + f"-{self.customer_name}"

