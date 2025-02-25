import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib
import os

# Load the dataset
data = pd.read_csv("Downloaded CSV File with correct path")
X = data[["Fan-In", "Op Count", "Nest Depth", "Dep Chain", "Gate Mix", "Reg Prox"]].values
y = data["Logic Depth"].values

# Split into training and testing sets (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Dataset size:", len(X), "Training size:", len(X_train), "Test size:", len(X_test))

# Initialize and train the model
model = RandomForestRegressor(
    n_estimators=200,  # More trees for robustness
    max_depth=5,      # Limit tree depth to avoid overfitting on small data
    min_samples_split=5,  # Minimum samples to split a node
    random_state=42    # For reproducibility
)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)
print("Predictions:", y_pred)
print("Actual:", y_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))

# Cross-validation for reliability
cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
print("Cross-Validated MSE (mean):", -cv_scores.mean())
print("Cross-Validated MSE (std):", cv_scores.std())

feature_names = ["Fan-In", "Op Count", "Nest Depth", "Dep Chain", "Gate Mix", "Reg Prox"]
feature_importance = model.feature_importances_

model_path = "model path on local directory"#.joblib extension
joblib.dump(model, model_path)

if os.path.exists(model_path):
    print(f"Model saved successfully at {model_path}")
else:
    print("Error: Model file not found!")