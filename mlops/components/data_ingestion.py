import os,sys
sys.path.append(os.getcwd())
from mlops import utils
from mlops.entity import config_entity
from mlops.entity import artifacts_entity
from mlops.exception import CustomException
from loguru import logger as logging
import pandas as pd 
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig ):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)
            logging.info("Save data in feature store")

            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_path,index=False,header=True)


            logging.info("split dataset into train and test set")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            train_df_,dev_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Save df to feature store folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            dev_df.to_csv(path_or_buf=self.data_ingestion_config.dev_file_path,index=False,header=True)
            data_ingestion_artifact = artifacts_entity.DataIngestionArtifact(
                data_directory=self.data_ingestion_config.data_ingestion_dir,
                feature_store_file=self.data_ingestion_config.feature_store_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path,
                dev_file_path=self.data_ingestion_config.dev_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(error_message=e, error_detail=sys)
        

