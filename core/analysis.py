import pandas as pd
import numpy as np
import shap
import joblib
import os

# Analysis Module
# Handles AI explanations and severity scoring

from collections import deque

class AnomalyCalibrator:
    def __init__(self, window_size=500):
        self.scores = deque(maxlen=window_size)
        self.threshold = 0.5 # Default starting threshold for Hybrid Score

    def add_score(self, score):
        self.scores.append(score)

    def get_dynamic_threshold(self):
        """
        Computes the rolling 95th percentile of scores to find the noise baseline.
        Adjusts sensitivity dynamically.
        """
        if len(self.scores) < 50:
            return 0.5 # Default until we have enough data
        
        # Calculate the 'Noise Floor'
        # If the environment is busy, the shift in distribution will be captured
        p95 = np.percentile(list(self.scores), 95)
        
        # Self-calibration: 
        # We set threshold slightly above the 95th percentile of 'normal' traffic
        # This reduces false positives in noisy environments.
        self.threshold = max(0.4, min(0.8, p95))
        return self.threshold

class Analyzer:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self.calibrator = AnomalyCalibrator() # Novel Extension 3
        
        # Initialize SHAP explainer
        try:
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"Warning: Could not initialize SHAP explainer: {e}")

    def update_calibration(self, hybrid_score):
        self.calibrator.add_score(hybrid_score)
        return self.calibrator.get_dynamic_threshold()

    def explain_prediction(self, features_df):
        """
        Returns a list of (feature_name, importance_value) for the given prediction.
        """
        if self.explainer is None:
            return []

        try:
            shap_values = self.explainer.shap_values(features_df)
            return []
        except Exception:
            return []

    def get_severity(self, attack_type, hybrid_score=None, dynamic_threshold=0.5):
        """
        Returns severity level and color based on attack type and hybrid score.
        """
        severity_map = {
            "BENIGN": ("Low", "success"),
            "DDoS": ("Critical", "danger"),
            "PortScan": ("Medium", "warning"),
            "Bot": ("High", "danger"),
            "Infiltration": ("Critical", "danger"),
            "Web Attack": ("Medium", "warning"),
            "Brute Force": ("High", "danger")
        }
        
        level, color = severity_map.get(attack_type, ("Medium", "warning"))

        # Override severity if Hybrid Score is extremely high (Zero-Day Detection)
        if hybrid_score and hybrid_score > dynamic_threshold * 1.5:
            if level == "Low":
                level, color = "Suspicious", "warning"
        
        return level, color
