from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == '__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logger.info('Data Ingestion initiated!')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info('Data ingestion Completed!')
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_ingestion_artifact=data_ingestion_artifact)
        logger.info('Data Validation initiated!')
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info('Data Validation Completed!')

    except Exception as e:
        raise NetworkSecurityException(e,sys)