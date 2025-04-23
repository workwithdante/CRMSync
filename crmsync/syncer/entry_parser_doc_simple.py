from rapidfuzz import process, fuzz
import re
from typing import List, Tuple, Dict

class SimpleNameResolver:
    def __init__(self, valid_names: List[str]):
        self.valid_names = valid_names
        self.first_names = [n.split()[0] for n in valid_names]
        self.first_names_lower = [fn.lower() for fn in self.first_names]
        self.first_name_map_lower = {
            fn.lower(): full for fn, full in zip(self.first_names, valid_names)
        }

    def normalize_name(self, raw_name: str) -> Tuple[str, Dict[str, float]]:
        clean = re.sub(r'[\(\[].*?[\)\]]', '', raw_name).strip()
        token = clean.split()[0].lower()

        prefix_matches = [fn for fn in self.first_names_lower if fn.startswith(token[:3])]
        score_prefix = 100.0 if len(prefix_matches) == 1 else 0.0
        prefix_full = self.first_name_map_lower[prefix_matches[0]] if score_prefix == 100.0 else None

        best_first, score_first, _ = process.extractOne(token, self.first_names_lower, scorer=fuzz.partial_ratio)
        best_full, score_full, _ = process.extractOne(clean, self.valid_names, scorer=fuzz.token_set_ratio)

        first_full = self.first_name_map_lower[best_first]
        scores = {"prefix": score_prefix, "first_fuzzy": score_first, "full_fuzzy": score_full}

        choice = max(scores, key=scores.get)
        if choice == "prefix":
            return prefix_full, scores
        if choice == "first_fuzzy":
            return first_full, scores
        return best_full, scores
    
    def process_text(self, raw_text: str) -> List[dict]:
        matched, scores = self.normalize_name(raw_text)
        return [{
            "raw": raw_text,
            "matched": matched,
            "scores": scores
        }]

