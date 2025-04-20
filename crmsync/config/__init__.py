from datetime import date
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict

from dotenv import load_dotenv

# Carga el archivo .env (por defecto busca el archivo en el directorio actual)
load_dotenv()


@dataclass
class SyncConfig:
    non_status_values: list = field(default_factory=lambda: ['Cancelación', 'Prospecto'])
    effective_date: date = field(default_factory=lambda: date(2025, 1, 1))
    non_broker: list = field(default_factory=lambda: ['Otro Broker'])
    
    def __post_init__(self):
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.name_db = os.getenv('DB_NAME')
        self.type = os.getenv('DB_TYPE')
        self.connector = os.getenv('DB_CONNECTOR')
        self.endpoint = os.getenv('ERPNEXT_HOST')
        self.api_key = os.getenv('ERPNEXT_API_KEY')
        self.api_secret = os.getenv('ERPNEXT_API_SECRET')
        self.address_mapping = self._load_mapping('address')
        self.contact_mapping = self._load_mapping('contact')
        self.customer_mapping = self._load_mapping('customer')
        self.item_mapping = self._load_mapping('item')
        
    def _load_mapping(self, filename: str) -> Dict[str, Any]:
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapping")
        filename = os.path.join(current_dir, f"{filename}.json")
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file) 
