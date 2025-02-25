import joblib

# Load the trained model
model = joblib.load("file path of trained model ") #eg:rf_logic_depth_model.joblib

# Predict depth
features ="ouput from feature_extractor.py"
predicted_depth = model.predict([features])[0]
print("Predicted Logic Depth:", predicted_depth)
