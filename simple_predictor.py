import pickle
import pandas as pd
import numpy as np
import os

class SimplePredictor:
    def __init__(self):
        # Find the most recent model
        artifact_dir = "artifact"
        artifact_folders = [f for f in os.listdir(artifact_dir) if os.path.isdir(os.path.join(artifact_dir, f))]
        artifact_folders.sort(reverse=True)
        
        latest_artifact = artifact_folders[0]
        model_path = os.path.join(artifact_dir, latest_artifact, "model_trainer", "trained_model", "model.pkl")
        
        # Load only the model
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    def predict(self, data_dict):
        # Create DataFrame with id column
        df = pd.DataFrame(data_dict)
        df['id'] = range(len(df))  # Add missing id column
        
        # Make prediction
        prediction = self.model.predict(df)
        return prediction