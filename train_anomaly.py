
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Configuration
DATASET_PATH = "dataset/cleaned_dataset.csv"
MODEL_PATH = "model/anomaly_model.pkl"

def train_anomaly_model():
    print("Loading dataset...")
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return

    # Load dataset (limit rows to speed up if needed, e.g., 50k)
    try:
        df = pd.read_csv(DATASET_PATH, nrows=50000)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Dataset loaded: {df.shape}")

    # Use only benign traffic for training anomaly detector (Semi-supervised)
    # Assuming there's a 'Label' column. If not, we just train on everything (Unsupervised)
    label_col = ' Label' if ' Label' in df.columns else 'Label'
    if label_col in df.columns:
        print("Filtering for BENIGN traffic...")
        df = df[df[label_col].str.contains('BENIGN', case=False, na=False)]
        
    # Drop non-numeric columns
    df_numeric = df.select_dtypes(include=['number'])
    
    # Handle NaN/Inf
    df_numeric = df_numeric.fillna(0)
    
    print(f"Training Isolation Forest on {df_numeric.shape[0]} samples...")
    
    clf = IsolationForest(
        n_estimators=100, 
        contamination=0.01, # Associate ~1% as anomalies
        random_state=42, 
        n_jobs=-1
    )
    
    clf.fit(df_numeric)
    
    print("Saving model...")
    joblib.dump(clf, MODEL_PATH)
    print(f"Anomaly Detection Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_anomaly_model()
