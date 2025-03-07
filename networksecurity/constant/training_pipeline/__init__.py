"""
defining common variable for training pipeline
"""
TARGET_COLUMN = 'Result'
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME = 'phisingData.csv'
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = "test.csv"



"""defining data ingestion constant variable starts with DATA_INGESTION """

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "bilalahmad"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2