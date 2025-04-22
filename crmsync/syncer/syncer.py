import os
import json
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

                for contact_id, group in df.groupby("contact_id"):
                    pa = PolicyAssembler(self.config, contact_id, group)
                    df_issues = self.query_service.fetch_issues(uow, contact_id)
                    for _, ticket in df_issues.iterrows():
                        subject = ticket.loc["title"]
                        status = ticket.loc["status"]
                        raw_description = ticket.loc["description"]
                        raw_solution = ticket.loc["solution"]
                        pa.create_issue(subject, status, raw_description, raw_solution)


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


    @staticmethod
    def _convert_json_to_spacy(input_json: str, output_spacy: str, base_model: str = "es_core_news_lg"):
        """
        Convierte dataset.json a train.spacy o dev.spacy usando el modelo base de spaCy.
        """
        nlp = spacy.load(base_model, exclude=["tok2vec", "tagger", "parser"])
        db = DocBin()
        
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
        filename = os.path.join(current_dir, f"dataset.json")
        with open(filename, 'r', encoding='utf-8') as input_json:
            data = json.load(input_json) 
        
            for entry in data:
                doc = nlp.make_doc(entry["text"])
                ents = []
                for start, end, label in entry["entities"]:
                    span = doc.char_span(start, end, label=label)
                    if span:
                        ents.append(span)
                doc.ents = ents
                db.add(doc)
            db.to_disk(output_spacy)
            print(f"✅ Saved {output_spacy}")

    @staticmethod
    def _train_ner_model(dataset_path: str, output_dir: str = "model", config_path: str = "config.cfg"):
        """
        Inicializa config.cfg si no existe y entrena el modelo spaCy NER en CPU.
        """
        from pathlib import Path
        import subprocess

        # 1) Crear config.cfg si no existe
        if not Path(config_path).exists():
            subprocess.run([
                "python", "-m", "spacy", "init", "config", config_path,
                "--lang", "es", "--pipeline", "ner", "--optimize", "accuracy"
            ], check=True)

        # 2) Ejecutar entrenamiento en CPU (sin --gpu-id)
        cmd = [
            "python", "-m", "spacy", "train", config_path,
            "--output", output_dir,
            "--paths.train", "train.spacy",
            "--paths.dev", "dev.spacy",
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