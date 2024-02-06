import sys
import os
sys.path.append(os.getcwd())
from mlops.entity import config_entity
from mlops.components import data_ingestion
from mlops.components import model_train
from mlops.components import model_to_bucket
import fire

def pipeline_initiate():
    training_pipeline_config=config_entity.TrainingPipelineConfig()
    data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config)
    print(data_ingestion_config.to_dict())
    data_ingestion_=data_ingestion.DataIngestion(data_ingestion_config)
    data_ingestion_artifact=data_ingestion_.initiate_data_ingestion()
    print("DATA INGESTION ARTIFACT")
    print(data_ingestion_artifact)

    model_training_config=config_entity.ModelTrainerConfig(training_pipeline_config)
    model_training_=model_train.ModelTrainer(model_trainer_config=model_training_config,data_ingestion_artifact=data_ingestion_artifact)
    model_training_artifact=model_training_.initiate_model_trainer()
    print("MODEL TRAINING ARTIFACT")
    print(model_training_artifact)

    model_pusher_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
    model_pusher_=model_to_bucket.ModelPusher(model_trainer_config=model_pusher_config)
    model_pusher_.initiate_model_pusher()
    return "Pipeline ran successfully"

# if __name__=="__main__":
#     fire.Fire(pipeline_initiate)