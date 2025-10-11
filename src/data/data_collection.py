import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import yaml

def load_params(file_path: str) -> float:
    try:
        with open(file_path, 'r') as file:
            params = yaml.safe_load(file)
        return params['data_collection']['test_size']
    except Exception as e:
        raise Exception(f"Error loading parameters from {file_path}: {e}")

def load_data(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error loading data from {file_path}: {e}")

def split_data(data: pd.DataFrame, test_size: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        return train_test_split(data, test_size=test_size, random_state=42)
    except ValueError as e:
        raise ValueError(f"Error splitting data: {e}")

def save_data(df: pd.DataFrame, file_path: str) -> None:
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error saving data to {file_path}: {e}")

def main():
    try:
        # Load dataset
        data_path = r"C:\Users\HP\Documents\Data Science (Atomcamp)\Python\MLops\water_potability.csv"
        data = load_data(data_path)

        # Load parameters
        params_file_path = 'params.yaml'
        test_size = load_params(params_file_path)

        # Split data
        train_data, test_data = split_data(data, test_size)

        # Save outputs
        raw_data_path = os.path.join('data', 'raw')
        os.makedirs(raw_data_path, exist_ok=True)

        save_data(train_data, os.path.join(raw_data_path, 'train.csv'))
        save_data(test_data, os.path.join(raw_data_path, 'test.csv'))

        print("Data collection stage completed successfully!")

    except Exception as e:
        raise Exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
