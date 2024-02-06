import os,sys
sys.path.append(os.getcwd())
from mlops.entity import config_entity
from mlops.entity import artifacts_entity
from mlops.exception import CustomException
from mlops.components.data_ingestion import DataIngestion

from loguru import logger as logging
import sys
from flair.data import Corpus
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.datasets import CSVClassificationCorpus
import mlflow
from mlflow.tracking import MlflowClient
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")
remote_Server_Uri = "http://127.0.0.1:8080"
mlflow.set_tracking_uri(remote_Server_Uri)
mlflow.set_experiment("test_experiment")

class CustomModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                    data_ingestion_artifact:artifacts_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer Initiated {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_model_trainer(self):
        with mlflow.start_run():
            data_folder = f"{self.data_ingestion_artifact.data_directory}/dataset"
            train_path = self.data_ingestion_artifact.train_file_path.split("/")[-1]
            test_path = self.data_ingestion_artifact.test_file_path.split("/")[-1]
            dev_path = self.data_ingestion_artifact.dev_file_path.split("/")[-1]
            column_name_map = {0: "text", 1: "label"}
            corpus: Corpus = CSVClassificationCorpus(data_folder=data_folder,
                                                    train_file=train_path,
                                                    dev_file=dev_path,
                                                    test_file=test_path,
                                                    column_name_map=column_name_map,
                                                    skip_header=True,
                                                    delimiter=',',
                                                    label_type=config_entity.LABEL)
            label_type = config_entity.LABEL
            label_dict = corpus.make_label_dictionary(label_type=label_type)
            document_embeddings = TransformerDocumentEmbeddings(self.model_trainer_config.bert_model, fine_tune=True)
            classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, label_type=label_type)
            trainer = ModelTrainer(classifier, corpus)
            trainer.fine_tune(self.model_trainer_config.model_trainer_dir,
                            learning_rate=self.model_trainer_config.learning_rate,
                            mini_batch_size=self.model_trainer_config.batch_size,
                            max_epochs=self.model_trainer_config.max_epoch)
            mlflow.log_params({
                'learning_rate': self.model_trainer_config.learning_rate,
                'batch_size': self.model_trainer_config.batch_size,
                'max_epochs': self.model_trainer_config.max_epoch
            })
            mlflow.pytorch.log_model(classifier, "model")
            model_trainer_artifact = artifacts_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_trainer_dir)
            mlflow.log_artifact(self.model_trainer_config.model_trainer_dir)
            logging.info(f"Model Trainer artifact --> {model_trainer_artifact}")
            return model_trainer_artifact

if __name__=="__main__":
    training_pipeline_config=config_entity.TrainingPipelineConfig()
    data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config)
    data_ingestion_artifact = DataIngestion(data_ingestion_config=data_ingestion_config).initiate_data_ingestion()
    model_training_config=config_entity.ModelTrainerConfig(training_pipeline_config)
    model_training_=CustomModelTrainer(model_trainer_config=model_training_config,data_ingestion_artifact=data_ingestion_artifact)
    model_training_artifact=model_training_.initiate_model_trainer()
    print("MODEL TRAINING ARTIFACT")
    print(model_training_artifact)
