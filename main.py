from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
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
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                 data_validation_artifact=data_validation_artifact)
        logger.info("Data Transformation Initiated!")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info('Data Transformation Completed!')
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifacts=data_transformation_artifact)
        logger.info('Model Trainer Initiated!')
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.info('Model Trainer Completed!')

    except Exception as e:
        raise NetworkSecurityException(e,sys)