from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.constant.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.common import save_numpy_array_data, save_object
import numpy as np
import pandas as pd
import sys, os
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def preprocessor_obj(self):
        try:
            ki = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logger.info(f'imputer instantiate with {DATA_TRANSFORMATION_IMPUTER_PARAMS} parameters!')
            pipeline = Pipeline([('imputer', ki)])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_data = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_data = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            train_feature_data = train_data.drop(columns=[TARGET_COLUMN], axis=1)
            train_y_data = train_data[TARGET_COLUMN]
            train_y_data.replace(-1,0)

            test_feature_data = test_data.drop(columns=[TARGET_COLUMN], axis=1)
            test_y_data = test_data[TARGET_COLUMN]
            test_y_data.replace(-1,0)

            preprocessor = self.preprocessor_obj()
            transformed_train_feature = preprocessor.fit_transform(train_feature_data)
            transformed_test_feature = preprocessor.transform(test_feature_data)

            train_arr = np.c_[transformed_train_feature, np.array(train_y_data)]
            test_arr = np.c_[transformed_test_feature, np.array(test_y_data)]

            save_numpy_array_data(self.data_transformation_config.data_train_transformation_dir, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.data_test_transformation_dir, array=test_arr)
            save_object(self.data_transformation_config.data_transformation_object_dir, obj=preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_data_path=self.data_transformation_config.data_train_transformation_dir,
                transformed_test_data_path= self.data_transformation_config.data_test_transformation_dir,
                transformed_object_path= self.data_transformation_config.data_transformation_object_dir
            )
            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)




