import re
from typing import Any, Dict, List


class DictComparator:
    def __init__(self):
        self.comparators = {}

    def register(self, field: str, fn):
        """Registrar una función de comparación especial para un campo."""
        self.comparators[field] = fn

    def compare_dicts(self, new_data: Dict, existing_data: Dict) -> Dict:
        changes = {
            k: v for k, v in new_data.items()
            if existing_data.get(k) != v
        }

        normalized_changes = {}
        for k, v in changes.items():
            if k in self.comparators:
                existing_val = existing_data.get(k, [])
                if self.comparators[k](v, existing_val):
                    normalized_changes[k] = v
            elif self._normalize_value(v) != self._normalize_value(existing_data.get(k)):
                normalized_changes[k] = v

        return normalized_changes

    def _normalize_value(self, value: Any):
        if self._is_number(value):
            return float(value)
        return str(value).strip()

    def _is_number(self, value: Any) -> bool:
        return re.match(r'^-?\d+(?:\.\d+)?$', str(value)) is not None

    def compare_list_of_dicts(self, new_list: List[Dict], existing_list: List[Dict], keys: List[str]) -> bool:
        if not isinstance(new_list, list) or not isinstance(existing_list, list):
            return True

        def is_significant(value: Any) -> bool:
            return value not in (None, '', 0, 0.0)

        for new_item in new_list:
            match_found = False
            for existing in existing_list:
                mismatches = {
                    k: (new_item.get(k), existing.get(k))
                    for k in keys
                    if is_significant(new_item.get(k)) and new_item.get(k) != existing.get(k)
                }
                if not mismatches:
                    match_found = True
                    break  # Encontró coincidencia, no hay que reportar
            if not match_found:
                print(f"No match for item: {new_item}")
                print(f"Mismatched fields: {mismatches}")
                return True

        return False
        
    def compare_items_with_names(self, new_items, existing_items, match_by="item_code"):
        if not isinstance(new_items, list) or not isinstance(existing_items, list):
            return True

        changes = []
        for new_item in new_items:
            matched = next(
                (ei for ei in existing_items if ei.get(match_by) == new_item.get(match_by)),
                None
            )
            if matched:
                # Copia el name del existente si coincide
                new_item["name"] = matched.get("name")

                # Verifica si alguno de los campos relevantes cambió
                for key in ["qty", "rate", "uom", "conversion_factor"]:
                    if str(new_item.get(key)) != str(matched.get(key)):
                        changes.append(new_item)
                        break
            else:
                # Es un ítem completamente nuevo
                changes.append(new_item)

        return bool(changes)  # si hay al menos uno con diferencias