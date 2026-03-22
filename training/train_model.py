import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load cleaned dataset
print("Loading cleaned dataset...")
data = pd.read_csv("dataset/cleaned_dataset.csv")

print("Total Records:", len(data))
print("Total Features:", len(data.columns))

# Label column (with space)
label_col = " Label"

# Separate features and labels
X = data.drop(label_col, axis=1)
y = data[label_col]

# Convert text labels to numbers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train-test split
print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train AI model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, n_jobs=-1)
model.fit(X_train, y_train)

# Test model
print("Evaluating model...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model/malware_model.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")

print("\n✅ AI Model trained and saved successfully!")
