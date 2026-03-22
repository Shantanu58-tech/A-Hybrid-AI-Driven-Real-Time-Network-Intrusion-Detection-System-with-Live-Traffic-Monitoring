
import joblib
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest

class MalwareDetector:
    def __init__(self, model_path="model/malware_model.pkl", encoder_path="model/label_encoder.pkl", anomaly_model_path="model/anomaly_model.pkl"):
        self.model = None
        self.encoder = None
        self.anomaly_detector = None
        self.feature_names = None
        
        self.load_models(model_path, encoder_path, anomaly_model_path)

    def load_models(self, model_path, encoder_path, anomaly_model_path):
        try:
            if os.path.exists(model_path):
                print(f"Loading Random Forest Model from {model_path}...")
                self.model = joblib.load(model_path)
                if hasattr(self.model, "feature_names_in_"):
                    self.feature_names = self.model.feature_names_in_
            else:
                print(f"Error: Model file {model_path} not found.")

            if os.path.exists(encoder_path):
                print(f"Loading Label Encoder from {encoder_path}...")
                self.encoder = joblib.load(encoder_path)

            if os.path.exists(anomaly_model_path):
                print(f"Loading Anomaly Detector from {anomaly_model_path}...")
                self.anomaly_detector = joblib.load(anomaly_model_path)
            else:
                print("Warning: Anomaly Detector model not found. Anomaly detection will be disabled until trained.")

        except Exception as e:
            print(f"Error loading models: {e}")

    def normalize_anomaly_score(self, raw_score):
        """
        Normalizes Isolation Forest score (usually -0.5 to 0.5) to a 0-1 range.
        Anomalies (< 0) will map closer to 1.0, Inliers (> 0) map closer to 0.0.
        """
        # Sigmoidal mapping: 1 / (1 + exp(10 * raw_score))
        # When raw_score is -0.5 (strong anomaly) -> ~0.99
        # When raw_score is 0.5 (strong inlier) -> ~0.01
        return 1 / (1 + np.exp(10 * raw_score))

    def calculate_hybrid_score(self, rf_confidence, if_score, traffic_volatility=1.0):
        """
        Confidence-Adaptive Fusion Engine
        Fuses RF Probability and IF Anomaly Score with dynamic weights.
        """
        # Normalize IF score: 0 (benign) to 1 (anomaly)
        norm_if = self.normalize_anomaly_score(if_score)
        
        # Adaptive Weights
        if traffic_volatility > 1.5:
            # High volatility: trust anomaly detection more (faster, outlier-focused)
            w1, w2 = 0.5, 0.5
        else:
            # Normal traffic: trust classification more (high-precision)
            w1, w2 = 0.8, 0.2
            
        return (w1 * rf_confidence) + (w2 * norm_if)

    def predict(self, packet_features, traffic_volatility=1.0):
        """
        Predicts if a packet is malware or benign.
        Returns: 
            - classification (str): "BENIGN" or Attack Type
            - hybrid_score (float): Combined Score (0 to 1, higher is more malicious)
            - confidence (float): Pure RF Probability
        """
        if not self.model:
            return "Unknown", 0.0, 0.0

        # Convert features to DataFrame
        df = pd.DataFrame([packet_features])
        
        # Ensure features match training data
        if self.feature_names is not None:
            df = df.reindex(columns=self.feature_names, fill_value=0)

        # 1. Random Forest Classification
        prediction_index = self.model.predict(df)[0]
        rf_confidence = np.max(self.model.predict_proba(df)[0])
        
        if self.encoder:
            attack_type = self.encoder.inverse_transform([prediction_index])[0]
        else:
            attack_type = str(prediction_index)

        # 2. Anomaly Detection (Isolation Forest)
        if_score = 0.0
        if self.anomaly_detector:
            try:
                # decision_function returns negative for outliers
                if_score = self.anomaly_detector.decision_function(df)[0]
            except Exception:
                pass

        # 3. Hybrid Fusion Logic (Novel Extension)
        hybrid_score = self.calculate_hybrid_score(rf_confidence, if_score, traffic_volatility)

        # To maintain compatibility with existing 'anomaly_score' display on dashboard,
        # we return the hybrid_score as the second value.
        return attack_type, hybrid_score, rf_confidence

    def get_feature_names(self):
        return self.feature_names

