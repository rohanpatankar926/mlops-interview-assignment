import os,sys
sys.path.append(os.getcwd())
from mlops.exception import CustomException
from datetime import datetime

FILE_NAME="main_data.csv"
TRAIN_FILE_PATH="train.csv"
TEST_FILE_PATH="test.csv"
DEV_FILE_PATH="dev.csv"
LABEL="label"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir=os.path.join("artifacts",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise CustomException(e,sys)


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="main"
            self.collection_name="main-data"
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_path=os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_PATH)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_PATH)
            self.dev_file_path=os.path.join(self.data_ingestion_dir,"dataset",DEV_FILE_PATH)
            self.test_size=0.25
        except Exception as e:
            raise CustomException(e,sys)

    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise CustomException(e,sys)

class ModelTrainerConfig(object):
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.bert_model = "distilbert-base-uncased"
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
            self.learning_rate = 5.0e-5
            self.max_epoch = 2
            self.batch_size = 16
        except Exception as e:
            raise CustomException(e,sys)
