import os
import re
import json
import spacy
from dateutil import parser as date_parser
from ftfy import fix_text
from rapidfuzz import process, fuzz
from typing import List, Tuple
from spacy.tokens import Span
from spacy.util import filter_spans
from spacy.language import Language

@Language.factory(
    "fuzzy_person_detector",
    default_config={"valid_names": [], "threshold": 75}
)
def create_fuzzy_person_detector(nlp, name, valid_names: List[str], threshold: int):
    """
    Crea un detector de personas difuso.

    Este componente de spaCy detecta entidades PERSON utilizando fuzzy matching.
    """
    first_names = [n.split()[0] for n in valid_names]
    first_lower = [fn.lower() for fn in first_names]

    def fuzzy_person_detector(doc):
        """
        Detecta entidades PERSON difusamente en un documento.
        """
        new_ents = list(doc.ents)
        for token in doc:
            text = token.text.lower()
            # Salta tokens muy cortos o numéricos
            if len(text) < 3 or not text.isalpha():
                continue
            # Elimina paréntesis o comentarios: "Juan(Debe doc)" -> "Juan"
            clean_text = re.sub(r'[\(\[].*?[\)\]]', '', token.text).strip()
            if not clean_text:
                continue
            # fuzzy match contra los nombres válidos
            best, score, _ = process.extractOne(
                clean_text.lower(), first_lower, scorer=fuzz.partial_ratio
            )
            if score >= threshold:
                span = Span(doc, token.i, token.i + 1, label="PERSON")
                new_ents.append(span)
        doc.ents = filter_spans(new_ents)
        return doc

    return fuzzy_person_detector

class EntryParserDocNER:
    """
    Parser de entradas de texto con NER (Named Entity Recognition).

    Esta clase utiliza spaCy para realizar NER y extraer información relevante de un texto.
    """
    def __init__(self, valid_names: List[str], model_path: str = None):
        """
        Inicializa el parser.

        Args:
            valid_names: lista de nombres completos válidos
            model_path: ruta al modelo spaCy (por defecto usa 'es_core_news_lg')
        """
        self.valid_names = valid_names
        self.first_names = [name.split()[0] for name in valid_names]
        self.first_names_lower = [fn.lower() for fn in self.first_names]
        self.first_name_map_lower = {fn.lower(): full for fn, full in zip(self.first_names, valid_names)}

        # Selecciona el modelo: entrenado o spaCy por defecto
        if model_path:
            ner_model_full_path = model_path
        else:
            # Por defecto usa modelo grande en español
            ner_model_full_path = "es_core_news_lg"

        self.nlp = spacy.load(ner_model_full_path, exclude=["tok2vec", "tagger", "parser"])

        # Añadir entity_ruler
        ruler = self.nlp.add_pipe(
            "entity_ruler", name="entity_ruler", before="ner",
            config={"overwrite_ents": True, "phrase_matcher_attr": "LOWER"}
        )
        patterns = []
        for full in valid_names:
            parts = full.split()
            first = parts[0]
            patterns.append({"label": "PERSON", "pattern": full})
            patterns.append({"label": "PERSON", "pattern": first})
            if len(parts) >= 2:
                init = parts[-1][0]
                patterns += [
                    {"label": "PERSON", "pattern": f"{first} {init}"},
                    {"label": "PERSON", "pattern": f"{first} {init}."}
                ]
        ruler.add_patterns(patterns)

        # Añadir fuzzy detector
        self.nlp.add_pipe(
            "fuzzy_person_detector", name="fuzzy_person_detector",
            before="entity_ruler",
            config={"valid_names": valid_names, "threshold": 75}
        )

        self._date_regex = re.compile(r"^\s*(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{2,4})\s+(.*)$")

    def normalize_name(self, raw_name: str) -> Tuple[str, dict]:
        """
        Normaliza un nombre.

        Args:
            raw_name (str): Nombre a normalizar.

        Returns:
            Tuple[str, dict]: Tupla con el nombre normalizado y los scores.
        """
        raw_name = re.sub(r'[\(\[].*?[\)\]]', '', raw_name).strip()
        token = raw_name.strip().split()[0].lower()
        prefix_matches = [fn for fn in self.first_names_lower if fn.startswith(token[:3])]
        score_prefix = 100.0 if len(prefix_matches) == 1 else 0.0
        prefix_full = self.first_name_map_lower[prefix_matches[0]] if len(prefix_matches) == 1 else None
        best_first_lower, score_first, _ = process.extractOne(
            token, self.first_names_lower, scorer=fuzz.partial_ratio
        )
        first_full = self.first_name_map_lower[best_first_lower]
        best_full, score_full, _ = process.extractOne(
            raw_name.strip(), self.valid_names, scorer=fuzz.token_set_ratio
        )
        scores = {"prefix": score_prefix, "first_fuzzy": score_first, "full_fuzzy": score_full}
        choice = max(scores, key=lambda k: scores[k])
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
        doc = self.nlp(raw_text)
        found = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                matched_name, scores = self.normalize_name(ent.text)
                found.append({
                    "raw": ent.text,
                    "matched": matched_name,
                    "scores": scores
                })
        return found
