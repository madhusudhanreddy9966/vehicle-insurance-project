import pickle
import pandas as pd
import numpy as np
from src.exception import MyException
from src.logger import logging
import sys
import os

class LocalVehicleDataClassifier:
    def __init__(self):
        """
        Local classifier that uses the most recent trained model
        """
        try:
            # Find the most recent artifact directory
            artifact_dir = "artifact"
            artifact_folders = [f for f in os.listdir(artifact_dir) if os.path.isdir(os.path.join(artifact_dir, f))]
            artifact_folders.sort(reverse=True)  # Get the most recent
            
            if not artifact_folders:
                raise Exception("No trained models found in artifact directory")
            
            latest_artifact = artifact_folders[0]
            self.model_path = os.path.join(artifact_dir, latest_artifact, "model_trainer", "trained_model", "model.pkl")
            self.preprocessor_path = os.path.join(artifact_dir, latest_artifact, "data_transformation", "transformed_object", "preprocessing.pkl")
            
            # Load model and preprocessor
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(self.preprocessor_path, 'rb') as f:
                self.preprocessor = pickle.load(f)
                
            logging.info(f"Loaded model from {self.model_path}")
            logging.info(f"Loaded preprocessor from {self.preprocessor_path}")
            
        except Exception as e:
            raise MyException(e, sys)
    
    def predict(self, dataframe):
        """
        Make prediction using local model
        """
        try:
            logging.info("Starting local prediction")
            
            # Transform the data using the preprocessor
            transformed_data = self.preprocessor.transform(dataframe)
            
            # Make prediction
            prediction = self.model.predict(transformed_data)
            
            logging.info(f"Prediction completed: {prediction}")
            return prediction
            
        except Exception as e:
            raise MyException(e, sys)