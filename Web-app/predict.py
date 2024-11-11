from tensorflow.keras.models import load_model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

import numpy as np

# Load model from HDF5 file
loaded_model_h5 = load_model("asset/activity_model.h5")
# Load dataset
df = pd.read_csv('asset/activity_recommendations.csv')

# Encoding categorical features
label_enc = LabelEncoder()
df['Location'] = label_enc.fit_transform(df['Location'])
df['Weather Condition'] = label_enc.fit_transform(df['Weather Condition'])
df['Recommended Activity'] = label_enc.fit_transform(df['Recommended Activity'])

# Separate features and target
X = df[['Temperature (°C)', 'Humidity (%)', 'Wind Speed (km/h)', 'Precipitation (%)', 'Location', 'Weather Condition']]
y = df['Recommended Activity']

# Scaling features
scaler = StandardScaler()
X = scaler.fit_transform(X)

def predict_activity(new_data):
    new_data = scaler.transform(new_data)

    # Predict
    predicted_activity = loaded_model_h5.predict(new_data)
    predicted_label = label_enc.inverse_transform([np.argmax(predicted_activity)])
    print(f"Recommended Activity: {predicted_label[0]}")
    return predicted_label[0]

    