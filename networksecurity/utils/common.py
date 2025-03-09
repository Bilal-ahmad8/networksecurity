from networksecurity.exception.exception import NetworkSecurityException
import yaml
import sys, os


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