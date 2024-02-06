from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_directory: str
    feature_store_file:str
    train_file_path:str
    test_file_path:str
    dev_file_path: str


@dataclass
class ModelTrainerArtifact:
    model_path:str