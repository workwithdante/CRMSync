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
            """Convierte valores no-significativos a None, deja los demás intactos."""
            return v if is_significant(v) else None

        def identity(item: Dict[str, Any]):
            """Tupla de valores normalizados, en el orden de keys."""
            return tuple(normalize(item.get(k)) for k in keys)

        # Construye los Counters sobre las identidades normalizadas
        new_ids      = [identity(i) for i in new_list]
        existing_ids = [identity(i) for i in existing_list]

        new_counts      = Counter(new_ids)
        existing_counts = Counter(existing_ids)

        # 1) ¿Hay algo que agregar? (new tiene más de existing)
        for id_, cnt in new_counts.items():
            if cnt > existing_counts.get(id_, 0):
                print(f"To add (new > existing): {id_} count_diff={cnt-existing_counts.get(id_,0)}")
                return True

        # 2) ¿Hay algo que remover? (existing tiene más de new)
        for id_, cnt in existing_counts.items():
            if cnt > new_counts.get(id_, 0):
                print(f"To remove (existing > new): {id_} count_diff={cnt-new_counts.get(id_,0)}")
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