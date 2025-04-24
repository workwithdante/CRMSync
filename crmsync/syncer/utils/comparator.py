import re
from typing import Any, Dict, List
from collections import Counter

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

    def compare_list_of_dicts(
        self,
        new_list: List[Dict[str, Any]],
        existing_list: List[Dict[str, Any]],
        keys: List[str]
    ) -> bool:
        if not isinstance(new_list, list) or not isinstance(existing_list, list):
            return True

        def is_significant(v: Any) -> bool:
            return v not in (None, '', 0, 0.0)

        def normalize(v: Any) -> Any:
            return v if is_significant(v) else None

        def clean_item(item: Dict[str, Any]) -> Dict[str, Any]:
            return {k: normalize(item.get(k)) for k in keys}

        new_cleaned = [clean_item(i) for i in new_list]
        existing_cleaned = [clean_item(i) for i in existing_list]

        new_ids = [tuple(i.values()) for i in new_cleaned]
        existing_ids = [tuple(i.values()) for i in existing_cleaned]

        from collections import Counter
        new_counts = Counter(new_ids)
        existing_counts = Counter(existing_ids)

        # Mostrar diferencias campo por campo si hay nuevas entradas
        for n_item in new_cleaned:
            if n_item not in existing_cleaned:
                similar = next((e_item for e_item in existing_cleaned if e_item.get("contact") == n_item.get("contact")), None)
                if similar:
                    diffs = {
                        k: (similar[k], n_item[k])
                        for k in keys
                        if similar.get(k) != n_item.get(k)
                    }
                    print(f"➕ To add: {tuple(n_item.values())} (x1)")
                    for field, (old, new) in diffs.items():
                        print(f"   ↪ Campo '{field}': '{old}' → '{new}'")
                    return True
                else:
                    print(f"➕ To add: {tuple(n_item.values())} (x1)")
                    return True

        for e_item in existing_cleaned:
            if e_item not in new_cleaned:
                print(f"➖ To remove: {tuple(e_item.values())} (x1)")
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