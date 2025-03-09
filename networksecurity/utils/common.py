from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import yaml
import sys, os
import numpy as np
import pickle

def read_yaml(filepath:str) -> dict:
    try:
        with open(filepath, 'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def write_yaml_file(content: object, filepath:str, replace:bool = False):
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok= True)
        with open(filepath, 'w') as f:
            yaml.dump(content,f)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

def save_object(file_path: str, obj: object) -> None:
    try:
        logger.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logger.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e