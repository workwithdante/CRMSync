import re
from typing import Any, Dict, List
from collections import Counter

class DictComparator:
    """
    Comparador de diccionarios.

    Esta clase se encarga de comparar diccionarios y detectar las diferencias.
    """
    def __init__(self):
        """
        Inicializa el comparador.
        """
        self.comparators = {}

    def register(self, field: str, fn):
        """
        Registra una función de comparación especial para un campo.

        Args:
            field (str): Nombre del campo.
            fn: Función de comparación.
        """
        self.comparators[field] = fn

    def compare_dicts(self, new_data: Dict, existing_data: Dict) -> Dict:
        """
        Compara dos diccionarios y devuelve las diferencias.

        Args:
            new_data (Dict): Diccionario nuevo.
            existing_data (Dict): Diccionario existente.

        Returns:
            Dict: Diccionario con las diferencias.
        """
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
        """
        Normaliza un valor para la comparación.

        Args:
            value (Any): Valor a normalizar.

        Returns:
            Any: Valor normalizado.
        """
        if self._is_number(value):
            return float(value)
        return str(value).strip()

    def _is_number(self, value: Any) -> bool:
        """
        Verifica si un valor es un número.

        Args:
            value (Any): Valor a verificar.

        Returns:
            bool: True si el valor es un número, False en caso contrario.
        """
        return re.match(r'^-?\d+(?:\.\d+)?$', str(value)) is not None


    def compare_list_of_dicts(
        self,
        new_list: List[Dict[str, Any]],
        existing_list: List[Dict[str, Any]],
        keys: List[str],
        append: bool = False
    ) -> bool:
        """
        Compara dos listas de diccionarios y devuelve True si hay diferencias.

        Args:
            new_list (List[Dict[str, Any]]): Lista nueva.
            existing_list (List[Dict[str, Any]]): Lista existente.
            keys (List[str]): Lista de claves a comparar.
            append (bool): Indica si se deben agregar los elementos faltantes de la lista nueva a la existente.

        Returns:
            bool: True si hay diferencias, False en caso contrario.
        """
        if not isinstance(new_list, list) or not isinstance(existing_list, list):
            return True

        def is_significant(v: Any) -> bool:
            return v not in (None, '', 0, 0.0)

        def normalize(v: Any) -> Any:
            return v if is_significant(v) else None

        def clean_item(item: Dict[str, Any]) -> Dict[str, Any]:
            return {k: normalize(item.get(k)) for k in keys}

        # Paso 1: versiones “limpias”
        new_cleaned      = [clean_item(i) for i in new_list]
        existing_cleaned = [clean_item(i) for i in existing_list]

        # Paso 2: si append, fusionamos lo que falte en new_list
        if append:
            # 1) Set de tuplas ya existentes (usamos existing_cleaned)
            seen = {tuple(d.values()) for d in existing_cleaned}

            # 2) Snapshot de pares (cleaned, original) para iterar sin pisar new_list
            pairs = list(zip(new_cleaned, existing_list))

            # 3) Para cada par, añadimos el original si no lo habíamos visto
            for cleaned_dict, orig_item in pairs:
                tup = tuple(cleaned_dict.values())  # corresponde al orden de 'keys'
                if tup not in seen:
                    new_list.append(orig_item)       # mutamos new_list
                    new_cleaned.append(cleaned_dict) # mantenemos los cleaned sync
                    seen.add(tup)
                    print(f"➕ Appended: {tup}")

        # Paso 3: tu lógica de detección de diferencias
        for n_item in new_cleaned:
            if n_item not in existing_cleaned:
                similar = next(
                    (e for e in existing_cleaned if e.get("contact") == n_item.get("contact")),
                    None
                )
                print(f"➕ To add: {tuple(n_item.values())} (x1)")
                if similar:
                    diffs = {
                        k: (similar[k], n_item[k])
                        for k in keys
                        if similar.get(k) != n_item[k]
                    }
                    for field, (old, new) in diffs.items():
                        print(f"   ↪ Campo '{field}': '{old}' → '{new}'")
                return True

        for e_item in existing_cleaned:
            if e_item not in new_cleaned:
                print(f"➖ To remove: {tuple(e_item.values())} (x1)")
                return True

        return False
  
    def compare_items_with_names(self, new_items, existing_items, match_by="item_code"):
        """
        Compara dos listas de items y devuelve True si hay diferencias.

        Args:
            new_items (List[Dict[str, Any]]): Lista nueva.
            existing_items (List[Dict[str, Any]]): Lista existente.
            match_by (str): Campo a usar para la comparación.

        Returns:
            bool: True si hay diferencias, False en caso contrario.
        """
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
