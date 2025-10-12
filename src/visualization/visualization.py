import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# === Setup ===
REPORT_DIR = os.path.join("reports")
FIG_DIR = os.path.join(REPORT_DIR, "figures")

# Create folders if not exist
os.makedirs(FIG_DIR, exist_ok=True)


# === Load Data and Model ===
def load_data(path: str) -> pd.DataFrame:
    """Load dataset from CSV."""
    try:
        print(f"Loading data from: {path}")
        return pd.read_csv(path)
    except Exception as e:
        raise Exception(f"Error loading data: {e}")


def load_model(path: str):
    """Load trained model."""
    try:
        print(f"Loading model from: {path}")
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise Exception(f"Error loading model: {e}")


# === Visualization Functions ===
def basic_visuals(data: pd.DataFrame):
    """Generate and save basic dataset visualizations."""

    # Histogram
    plt.figure(figsize=(15, 10))
    data.hist(figsize=(15, 10))
    plt.suptitle("Feature Distributions", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "histograms.png"))
    plt.close()

    # Pairplot
    sns.pairplot(data)
    plt.suptitle("Pairwise Relationships Between Features", fontsize=16)
    plt.savefig(os.path.join(FIG_DIR, "pairplot.png"))
    plt.close()

    # Correlation Heatmap
    plt.figure(figsize=(15, 10))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "correlation_heatmap.png"))
    plt.close()

    # Boxplots
    for column in data.select_dtypes(include=[np.number]).columns:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=data[column], color="skyblue")
        plt.title(f"Box plot of {column}", fontsize=14)
        plt.xlabel(column)
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, f"boxplot_{column}.png"))
        plt.close()

    # KDE plots (distribution by Potability)
    if "Potability" in data.columns:
        for column in data.select_dtypes(include=[np.number]).columns:
            plt.figure(figsize=(8, 4))
            sns.kdeplot(data=data, x=column, hue="Potability", fill=True)
            plt.title(f"Distribution of {column} by Potability", fontsize=14)
            plt.xlabel(column)
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, f"kde_{column}.png"))
            plt.close()

    # Scatter Plot between pH and Hardness
    if all(col in data.columns for col in ["ph", "Hardness", "Potability"]):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="ph", y="Hardness", hue="Potability", data=data, palette="Set1")
        plt.title("Scatter Plot: pH vs Hardness by Potability", fontsize=16)
        plt.xlabel("pH")
        plt.ylabel("Hardness")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, "scatter_ph_hardness.png"))
        plt.close()


# === Model Evaluation Visuals ===
def evaluation_visuals(model, data: pd.DataFrame):
    """Visualize and save model performance (actual vs predicted and metrics)."""
    if "Potability" not in data.columns:
        raise KeyError("The dataset must contain a 'Potability' column for evaluation visualization.")

    X_test = data.drop(columns=["Potability"])
    y_true = data["Potability"].dropna()
    X_test = X_test.loc[y_true.index]

    y_pred = model.predict(X_test)

    # Actual vs Predicted Comparison
    plt.figure(figsize=(8, 5))
    plt.scatter(range(len(y_true)), y_true, color="blue", label="Actual", alpha=0.6)
    plt.scatter(range(len(y_pred)), y_pred, color="red", label="Predicted", alpha=0.6)
    plt.title("Actual vs Predicted Potability", fontsize=16)
    plt.xlabel("Sample Index")
    plt.ylabel("Potability")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "actual_vs_predicted.png"))
    plt.close()

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Not Potable", "Potable"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "confusion_matrix.png"))
    plt.close()

    # Evaluation Metrics Visualization
    try:
        with open("reports/eval_metrics.json", "r") as f:
            metrics = json.load(f)
    except Exception as e:
        raise Exception(f"Error loading eval_metrics.json: {e}")

    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=metric_names, y=metric_values, palette="viridis")
    plt.title("Model Evaluation Metrics", fontsize=16)
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "evaluation_metrics.png"))
    plt.close()


# === Main Function ===
def main():
    try:
        # Paths
        model_path = os.path.join("models", "rf_model.pkl")
        test_path = os.path.join("data", "preprocessing", "test_processed.csv")

        # Load Data and Model
        data = load_data(test_path)
        model = load_model(model_path)

        # Generate Visuals
        print("Generating basic data visualizations...")
        basic_visuals(data)

        print("Generating evaluation visualizations...")
        evaluation_visuals(model, data)

        print(f"All visualizations saved in: {FIG_DIR}")

    except Exception as e:
        raise Exception(f"An error occurred in visualization.py: {e}")


if __name__ == "__main__":
    main()