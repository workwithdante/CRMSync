import json
import os
import logging
from typing import List

from pandas import Series

from crmsync.syncer.handler.customer import Customer
from crmsync.syncer.handler.contact import Contact
from syncer.handler.salesorder import SalesOrder
from crmsync.syncer.handler.address import Address
from crmsync.syncer.handler.item import Item
from crmsync.config import SyncConfig

logging.basicConfig(level=logging.INFO)

class PolicyAssembler:
    def __init__(self, config: SyncConfig, row: Series):
        self.config = config

        self.mapping = {
            "Customer": (Customer, self.config.customer_mapping),
            "Address": (Address, self.config.address_mapping),
            "Contact": (Contact, self.config.contact_mapping),
            "Item": (Item, self.config.item_mapping),
            "SalesOrder": (SalesOrder, None),  # reusa mapping de contacto para fechas
        }

        # Construcción y sincronización implícita desde __post_init__
        customer = self.instantiate("Customer", row)
        address = self.instantiate("Address", row, customer_name=customer.name)
        contacts = self.instantiate("Contact", row, customer_name=customer.name)
        item = self.instantiate("Item", row)

        self.instantiate(
            "SalesOrder",
            row,
            contacts=contacts,
            customer_name=customer.name,
            item_name=item.name,
            address_name=address.name
        )

        print("✅ Policy assembled successfully")

    def instantiate(self, key: str, row: Series, **extra_kwargs):
        cls, mapping_list = self.mapping[key]
        results = []
        
        if mapping_list:
            for mapping in mapping_list:
                if mapping.get("coverage") and not row.get(mapping["coverage"]):
                    continue

                instance = cls.from_row(row, mapping, **extra_kwargs)
                results.append(instance)

                if key not in {"Contact"}:
                    return instance
        else:
            instance = cls.from_row(row, **extra_kwargs)
            results.append(instance)

        return results if results else None
