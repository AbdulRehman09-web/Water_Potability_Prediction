import numpy as np
import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from the given CSV file path."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Error loading data from {file_path}: {e}")

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values with the median of each column."""
    try:
        for column in df.columns:
            if df[column].isnull().any():
                missing_value = df[column].median()
                df[column] = df[column].fillna(missing_value)
        return df
    except Exception as e:
        raise Exception(f"Error filling missing values: {e}")

def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save processed DataFrame to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error saving data to {file_path}: {e}")

def main():
    try:
        raw_data_path = "./data/raw/"
        processed_data_path = "./data/preprocessing"  # ✅ fixed to match dvc.yaml

        # Load raw data
        train_data = load_data(os.path.join(raw_data_path, "train.csv"))
        test_data = load_data(os.path.join(raw_data_path, "test.csv"))

        # Handle missing values
        train_processed_data = handle_missing_values(train_data)
        test_processed_data = handle_missing_values(test_data)

        # Create output directory (if it doesn't exist)
        os.makedirs(processed_data_path, exist_ok=True)

        # Save processed data
        save_data(train_processed_data, os.path.join(processed_data_path, "train_processed.csv"))
        save_data(test_processed_data, os.path.join(processed_data_path, "test_processed.csv"))

        print("Data preprocessing completed successfully!")

    except Exception as e:
        raise Exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
