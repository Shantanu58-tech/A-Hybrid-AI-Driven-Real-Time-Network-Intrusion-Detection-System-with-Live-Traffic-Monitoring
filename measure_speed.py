
import time
import joblib
import pandas as pd
import numpy as np

# Load the model
model = joblib.load("model/malware_model.pkl")
feature_names = model.feature_names_in_

# Generate a dummy packet matching the 10 features expected in capture
features = {
    " Destination Port": 80,
    " Flow Duration": 1,
    " Total Fwd Packets": 1,
    " Total Backward Packets": 0,
    "Total Length of Fwd Packets": 100,
    " Total Length of Bwd Packets": 0,
    " Fwd Packet Length Max": 100,
    " Fwd Packet Length Min": 100,
    " Fwd Packet Length Mean": 100,
    " Fwd Packet Length Std": 0
}

df = pd.DataFrame([features])
# Reindex like the detector does
df = df.reindex(columns=feature_names, fill_value=0)

# Measure time for 1000 predictions
start_time = time.time()
for _ in range(1000):
    model.predict(df)
end_time = time.time()

avg_time = (end_time - start_time) / 1000
print(f"Average detection time per packet: {avg_time*1000:.4f} ms")
