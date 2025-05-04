from rapidfuzz import process, fuzz # Importa las clases process y fuzz del módulo rapidfuzz
import re # Importa el módulo re para el uso de expresiones regulares
from typing import List, Tuple, Dict # Importa las clases List, Tuple y Dict del módulo typing

class SimpleNameResolver:
    """
    Resolvedor de nombres simple.

    Esta clase se encarga de resolver nombres a partir de una lista de nombres válidos.
    """
    def __init__(self, valid_names: List[str]):
        """
        Constructor de la clase SimpleNameResolver.

        Args:
            valid_names (List[str]): Lista de nombres válidos.
        """
        # Lista de nombres válidos
        self.valid_names = valid_names
        # Lista de primeros nombres
        self.first_names = [n.split()[0] for n in valid_names]
        # Lista de primeros nombres en minúsculas
        self.first_names_lower = [fn.lower() for fn in self.first_names]
        # Mapeo de primeros nombres en minúsculas a nombres completos
        self.first_name_map_lower = {
            fn.lower(): full for fn, full in zip(self.first_names, valid_names)
        }

    def normalize_name(self, raw_name: str) -> Tuple[str, Dict[str, float]]:
        """
        Normaliza un nombre.

        Args:
            raw_name (str): Nombre a normalizar.

        Returns:
            Tuple[str, Dict[str, float]]: Tupla con el nombre normalizado y los scores.
        """
        # Elimina paréntesis y corchetes del nombre
        clean = re.sub(r'[\(\[].*?[\)\]]', '', raw_name).strip()
        # Obtiene el primer token del nombre en minúsculas
        token = clean.split()[0].lower()

        # Busca coincidencias de prefijos
        prefix_matches = [fn for fn in self.first_names_lower if fn.startswith(token[:3])]
        # Define el score del prefijo
        score_prefix = 100.0 if len(prefix_matches) == 1 else 0.0
        # Define el nombre completo del prefijo
        prefix_full = self.first_name_map_lower[prefix_matches[0]] if score_prefix == 100.0 else None

        # Obtiene el mejor primer nombre y el mejor nombre completo
        best_first, score_first, _ = process.extractOne(token, self.first_names_lower, scorer=fuzz.partial_ratio)
        best_full, score_full, _ = process.extractOne(clean, self.valid_names, scorer=fuzz.token_set_ratio)

        # Obtiene el nombre completo del primer nombre
        first_full = self.first_name_map_lower[best_first]
        # Define los scores
        scores = {"prefix": score_prefix, "first_fuzzy": score_first, "full_fuzzy": score_full}

        # Elige la mejor opción
        choice = max(scores, key=scores.get)
        # Retorna el nombre normalizado y los scores
        if choice == "prefix":
            return prefix_full, scores
        if choice == "first_fuzzy":
            return first_full, scores
        return best_full, scores
    
    def process_text(self, raw_text: str) -> List[dict]:
        """
        Procesa un texto.

        Args:
            raw_text (str): Texto a procesar.

        Returns:
            List[dict]: Lista de diccionarios con el texto original, el nombre coincidente y los scores.
        """
        # Normaliza el nombre
        matched, scores = self.normalize_name(raw_text)
        # Retorna el resultado
        return [{
            "raw": raw_text,
            "matched": matched,
            "scores": scores
        }]
