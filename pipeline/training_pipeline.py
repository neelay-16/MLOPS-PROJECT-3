from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from src.feature_store import RedisFeatureStore
from config.paths_config import *
from utils.common_functions import read_yaml  # Import this function

if __name__=="__main__":
    # Read the config file
    config = read_yaml(CONFIG_PATH)
    
    # Pass config to DataIngestion, not RAW_DIR
    data_ingestion = DataIngestion(config)
    data_ingestion.run()

    feature_store = RedisFeatureStore()

    data_processor = DataProcessing(TRAIN_FILE_PATH, TEST_FILE_PATH, feature_store)
    data_processor.run()

    feature_store = RedisFeatureStore()
    model_trainer = ModelTraining(feature_store)
    model_trainer.run()