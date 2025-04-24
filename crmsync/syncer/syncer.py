import math
import os
import json
import random
from typing import Iterator
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

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

                for contact_id, group in tqdm(df.groupby("contact_id"), desc="Procesando contactos"):
                    PolicyAssembler(self.config, contact_id, group)
                    # Si deseas procesar tickets también, descomenta:
                    # df_issues = self.query_service.fetch_issues(uow, contact_id)
                    # for ticket in df_issues.itertuples(index=False):
                    #     pa.create_issue(ticket.title, ticket.status, ticket.description, ticket.solution)

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
        return True

    def recursive_join(self, query, join_list):
        if not join_list:
            return query
        model, condition = join_list[0]
        new_query = query.join(model, condition)
        return self.recursive_join(new_query, join_list[1:])

    def _convert_json_to_spacy(self, train_spacy="train.spacy", dev_spacy="dev.spacy", split_ratio=0.8, base_model="es_core_news_lg"):
        nlp = spacy.load(base_model, exclude=["tok2vec", "tagger", "parser"])

        dataset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model/dataset")
        filename = os.path.join(dataset_dir, "dataset.json")

        with open(filename, 'r', encoding='utf-8') as input_json:
            data = json.load(input_json)

        random.shuffle(data)
        split_point = math.ceil(len(data) * split_ratio)
        train_data, dev_data = data[:split_point], data[split_point:]

        def create_docbin(data_subset):
            db = DocBin()
            for entry in data_subset:
                doc = nlp.make_doc(entry["text"])
                ents = [
                    span for start, end, label in entry["entities"]
                    if (span := doc.char_span(start, end, label=label))
                ]
                doc.ents = ents
                db.add(doc)
            return db

        create_docbin(train_data).to_disk(train_spacy)
        print(f"✅ Saved {train_spacy} successfully (train set)")

        create_docbin(dev_data).to_disk(dev_spacy)
        print(f"✅ Saved {dev_spacy} successfully (dev set)")

    def _train_ner_model(self, output_dir="model", config_path="model/config.cfg"):
        from pathlib import Path
        import subprocess

        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_full_dir = os.path.join(current_dir, output_dir)
        config_full_path = os.path.join(current_dir, config_path)
        train_spacy = os.path.join(current_dir, "model/dataset/train.spacy")
        dev_spacy = os.path.join(current_dir, "model/dataset/dev.spacy")

        if not Path(config_full_path).exists():
            self._convert_json_to_spacy(train_spacy, dev_spacy, 0.75)
            subprocess.run([
                "python", "-m", "spacy", "init", "config", config_path,
                "--lang", "es", "--pipeline", "ner", "--optimize", "accuracy"
            ], check=True)

        model_full_dir = os.path.join(current_dir, output_dir, "model-best")
        if not Path(model_full_dir).exists():
            cmd = [
                "python", "-m", "spacy", "train", config_full_path,
                "--output", output_full_dir
            ]
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
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