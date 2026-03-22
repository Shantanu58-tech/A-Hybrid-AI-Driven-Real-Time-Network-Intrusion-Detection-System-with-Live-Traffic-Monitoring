import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc

DATASET_PATH = "dataset/cleaned_dataset.csv"
MODEL_PATH = "model/anomaly_model.pkl"

def evaluate_model():
    print("Loading dataset...")
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Dataset not found at {DATASET_PATH}")
        return
    
    # Load dataset
    try:
        df = pd.read_csv(DATASET_PATH, nrows=50000)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Dataset loaded: {df.shape}")

    # Check for the label column
    label_col = ' Label' if ' Label' in df.columns else 'Label'
    
    if label_col not in df.columns:
        print("Error: No Label column found in the dataset to evaluate against.")
        return
    
    y_true_str = df[label_col].values
    
    # IsolationForest predicts 1 for normal (inliers) and -1 for anomaly (outliers)
    # We map 'BENIGN' to 1 and everything else (e.g., 'DDoS') to -1
    y_true = [1 if 'BENIGN' in str(val).upper() else -1 for val in y_true_str]
    
    # Drop non-numeric columns and handle NaN/Inf (following train_anomaly.py logic)
    df_numeric = df.select_dtypes(include=['number'])
    df_numeric = df_numeric.fillna(0)
    
    print("Loading model...")
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return
        
    try:
        clf = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    print("Predicting anomalies...")
    y_pred = clf.predict(df_numeric)
    
    print("Generating Confusion Matrix & Metrics...")
    cm = confusion_matrix(y_true, y_pred, labels=[1, -1])
    
    # Convert labels for standard metrics:
    # Let Anomaly (-1) be the Positive class (1)
    # Let Benign (1) be the Negative class (0)
    y_true_binary = [1 if y == -1 else 0 for y in y_true]
    y_pred_binary = [1 if y == -1 else 0 for y in y_pred]

    precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
    recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
    f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
    
    print("\n" + "="*50)
    print("AI EVALUATION METRICS:")
    print("="*50)
    print(f"Precision: {precision:.4f} (When it flags Malware, how often is it right?)")
    print(f"Recall:    {recall:.4f} (Out of all Malware, how much did it find?)")
    print(f"F1 Score:  {f1:.4f} (Balance between Precision and Recall)")
    print("="*50)

    # Calculate ROC Curve and AUC
    # decision_function() returns negative values for anomalies and positive for inliers
    # Multiply by -1 to invert so that higher score = higher chance of being anomaly
    y_score = -clf.decision_function(df_numeric)
    fpr, tpr, thresholds = roc_curve(y_true_binary, y_score)
    roc_auc = auc(fpr, tpr)
    
    print(f"AUC Score: {roc_auc:.4f} (Overall ability to distinguish classes)")
    print("="*50 + "\n")
    
    # Visualizing both side-by-side
    plt.figure(figsize=(14, 6))
    
    # 1. Plotting Confusion Matrix
    plt.subplot(1, 2, 1)
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                     xticklabels=['BENIGN (Normal)', 'ANOMALY (Malware)'],
                     yticklabels=['BENIGN (Normal)', 'ANOMALY (Malware)'])
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('Actual Classification')
    plt.xlabel('AI Predicted Classification')
    
    # 2. Plotting ROC Curve
    plt.subplot(1, 2, 2)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    
    # Save the plot
    output_path = "evaluation_report.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"Success! Full Evaluation Report saved to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    evaluate_model()
