from mlops.exception import CustomException
from loguru import logger as logging
from mlops.entity.config_entity import ModelTrainerConfig
import sys
from model_utils import *

class ModelPusher(object):
    def __init__(self,model_trainer_config:ModelTrainerConfig):
        try:
            logging.info(f"{'>>>'*20} Model Pusher {'<<<'*20}")
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_model_pusher(self):
        logging.info("Model Pusher is initiated")
        model_saved_dir=self.model_trainer_config.model_trainer_dir
        upload_model_to_s3(s3_bucket=os.getenv("S3_BUCKET"),model_path=model_saved_dir)
