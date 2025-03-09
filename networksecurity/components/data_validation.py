from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.utils.common import read_yaml, write_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

import os 
import sys

import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                  data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact =  data_ingestion_artifact
            self.schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def check_no_columns(self, df: pd.DataFrame) -> bool:
        try:
            base_no_column = len(self.schema_config['columns'])
            logger.info(f"Required number of columns:{base_no_column}")
            logger.info(f"Data frame has columns:{len(df.columns)}")
            if base_no_column == len(df.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


        
    def check_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, threshold = 0.05):
        try:
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found  = True

                report.update({col:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    }})
                
            drift_report_file_path = self.data_validation_config.driftreport_filename

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(filepath=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


        
    def initiate_data_validation(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # checking columns Len
            status = self.check_no_columns(df=train_df)
            if not status:
                logger.info('Error:train dataframe does not contain all columns')
            status = self.check_no_columns(df=test_df)
            if not status:
                logger.info('Error:test data does not contain all columns') 


            self.check_data_drift(train_df, test_df)
            dirpath = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dirpath, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header =True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path= self.data_validation_config.driftreport_filename

            )
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


        


