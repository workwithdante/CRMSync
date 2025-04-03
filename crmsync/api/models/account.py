from dataclasses import dataclass, field
from typing import Optional

from api import client


@dataclass
class Account:
    id: Optional[str] = field(default=None, init=False)
    first_name: str
    last_name: str
    second_name: str
    gender: str
    dob: str
    SSN: str
    income: str
    phone1: str
    otherphone: str
    emergencyphone: str
    email1: str
    email2: str
    ship_street: str
    ship_pobox: str
    ship_city: str
    ship_state: str
    ship_code: str

    def __post_init__(self):
        # Paso 2: Producto hijo
        accountname = " ".join([name for name in [self.first_name, getattr(self, 'second_name', None), self.last_name] if name])
        query = f"SELECT * FROM Accounts WHERE accountname = '{accountname}' LIMIT 1"
        accountExits = next(iter(client.doQuery(query)), None)
        new_data = {
            "accountname": accountname,
            "phone": self.phone1,
            "otherphone": self.otherphone,
            "fax": "",
            "email1": self.email1,
            "email2": self.email2,
            "rating": "Active",
            "annual_revenue": self.income,
            "ship_street": self.ship_street,
            "ship_pobox": self.ship_pobox,
            "ship_city": self.ship_city,
            "ship_state": self.ship_state,
            "ship_code": self.ship_code,
            "ship_country": "United States",
        }
        if not accountExits:
            account = client.doCreate('Accounts', new_data)
        else:
            
            def normalize_value(value):
                try:
                    return float(value)  # Convierte números a float para comparación
                except (ValueError, TypeError):
                    return str(value).strip() 
    
            changes = {key: value for key, value in new_data.items() if accountExits.get(key) != value}
            
            normalized_changes = {
                k: v
                for k, v in changes.items()
                if normalize_value(v) != normalize_value(accountExits.get(k))
            }
            
            if normalized_changes:
                updated_data = {**accountExits, **normalized_changes} 
                client.doUpdate(updated_data)
                
            account = accountExits

        self.id = account['id']
