import math
import os
import json
import random
import spacy
from spacy.tokens import DocBin

from crmsync.config import SyncConfig
from database.services.query import QueryService
from syncer.policy_assembler import PolicyAssembler
from crmsync.config.logging import setup_logging
from database.unit_of_work import UnitOfWork
from sqlalchemy.orm import sessionmaker
from crmsync.database.engine import get_engine

class Syncer:
    def __init__(self):
        engine = get_engine()
        if not engine:
            raise RuntimeError("Could not create engine")
        self.config = SyncConfig()
        self.query_service = QueryService(self.config)
        self.unit_of_work = UnitOfWork(lambda: sessionmaker(bind=engine)())

    def sync(self):
        logger = setup_logging()
        try:
            with self.unit_of_work as uow:
                version = self.query_service.validate_connection(uow)
                logger.info(f"Connected to VTigerCRM (version {version})")

                # 1) Fetch records
                df = self.query_service.fetch_records(uow)

                # 2) Entrenar el modelo NER de SpaCy
                #self._train_ner_model("model")

                for contact_id, group in df.groupby("contact_id"):
                    PolicyAssembler(self.config, contact_id, group)
                    """
                    df_issues = self.query_service.fetch_issues(uow, contact_id)
                    for _, ticket in df_issues.iterrows():
                        subject = ticket.loc["title"]
                        status = ticket.loc["status"]
                        raw_description = ticket.loc["description"]
                        raw_solution = ticket.loc["solution"]
                        pa.create_issue(subject, status, raw_description, raw_solution)
                    """


        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
        return True
    
    def recursive_join(self, query, join_list):
        """
        Función recursiva que añade JOINs a la consulta.

        :param query: Consulta base.
        :param join_list: Lista de tuplas (modelo, condición de join).
        :return: Consulta con los JOINs aplicados.
        """
        if not join_list:
            return query
        model, condition = join_list[0]
        new_query = query.join(model, condition)
        return self.recursive_join(new_query, join_list[1:])


    def _convert_json_to_spacy(self,
                            train_spacy: str = "train.spacy",
                            dev_spacy: str = "dev.spacy",
                            split_ratio: float = 0.8,
                            base_model: str = "es_core_news_lg"):
        """
        Convierte dataset.json en train.spacy y dev.spacy (dividido automáticamente).
        """
        nlp = spacy.load(base_model, exclude=["tok2vec", "tagger", "parser"])

        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model/dataset")
        filename = os.path.join(current_dir, "dataset.json")

        with open(filename, 'r', encoding='utf-8') as input_json:
            data = json.load(input_json)

        random.shuffle(data)  # Mezclar los datos antes de dividir

        # Dividir dataset según split_ratio
        split_point = math.ceil(len(data) * split_ratio)
        train_data = data[:split_point]
        dev_data = data[split_point:]

        def create_docbin(data_subset):
            db = DocBin()
            for entry in data_subset:
                doc = nlp.make_doc(entry["text"])
                ents = []
                for start, end, label in entry["entities"]:
                    span = doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)
                doc.ents = ents
                db.add(doc)
            return db

        # Crear y guardar train.spacy
        train_db = create_docbin(train_data)
        train_db.to_disk(train_spacy)
        print(f"✅ Saved {train_spacy} successfully (train set)")

        # Crear y guardar dev.spacy
        dev_db = create_docbin(dev_data)
        dev_db.to_disk(dev_spacy)
        print(f"✅ Saved {dev_spacy} successfully (dev set)")

    def _train_ner_model(self, output_dir: str = "model", config_path: str = "model/config.cfg"):
        from pathlib import Path
        import subprocess
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_full_dir = os.path.join(current_dir, output_dir)
        config_full_path = os.path.join(current_dir, config_path)
        train_spacy = os.path.join(current_dir, "model/dataset/train.spacy")
        dev_spacy = os.path.join(current_dir, "model/dataset/dev.spacy")

        # 1) Crear config.cfg si no existe
        if not Path(config_full_path).exists():
            self._convert_json_to_spacy(train_spacy=train_spacy, dev_spacy=dev_spacy, split_ratio=0.75)

            subprocess.run([
                "python", "-m", "spacy", "init", "config", config_path,
                "--lang", "es", "--pipeline", "ner", "--optimize", "accuracy"
            ], check=True)

        # 2) Ejecutar entrenamiento en CPU (sin --gpu-id) si no existe el directorio de salida
        model_full_dir = os.path.join(current_dir, output_dir, "model-best")
        if not Path(model_full_dir).exists():
            cmd = [
                "python", "-m", "spacy", "train", config_full_path,
                "--output", output_full_dir
            ]
            try:
                result = subprocess.run(cmd, check=True)
                print("✅ Training completed successfully on CPU\n")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print("❌ Training failed!")
                print("Exit code:", e.returncode)
                print("\n=== STDOUT ===")
                print(e.stdout or "<no stdout>")
                print("\n=== STDERR ===")
                print(e.stderr or "<no stderr>")
                raise