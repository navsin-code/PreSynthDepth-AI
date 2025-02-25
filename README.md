# PreSynthDepth AI

## Overview
Welcome to `PreSynthDepth AI`, a machine learning solution that predicts combinational logic depth in Verilog RTL pre-synthesis to identify potential timing violations early in chip design. This project uses a Random Forest Regressor to analyze Verilog modules.It’s ideal for engineers and students working on small RTL designs, with plans to scale for deeper logic (depths 4–5) in future work.

The repository contains all code collaterals, including feature extraction, model training, and prediction scripts, written in Python using open-source libraries. This README guides you on setting up the environment, running the code, and understanding its use.

## Repository Contents
- feature_extractor.py: Extracts features (Fan-In, Op Count, etc.) from Verilog (.v) files.
- train_model.py: Trains a Random Forest model on a dataset, calculates MSE, and saves the model.
- predict_depth.py: Uses the trained model to predict logic depth for a given Verilog module’s features.
- combined_dataset.csv: Dataset of 56 Verilog modules with features and depths 0–3 (optional, for training).
- README.md: This file.

## Prerequisites
To run the code, ensure you have the following installed:

1)Python 3.8+: Available from [python.org](https://www.python.org/downloads/).
- Required Libraries:
  - pandas (for data handling)
  - numpy (for numerical operations)
  - scikit-learn (for Random Forest and metrics)
  - joblib (for model saving/loading)
  - matplotlib (for visualization, optional for feature importance)


Install these using pip:
`pip install pandas numpy scikit-learn joblib matplotlib`

## Environment Setup
1)Clone the Repository
`git clone https://github.com/your-username/pre-synth-depth-ai.git
cd pre-synth-depth-ai`

2)Install Dependencies: Run the pip command above to install required libraries. Ensure Python 3.8+ is installed and added to your PATH.

3)Prepare Verilog Files:
Save your Verilog modules (e.g., comparator_3bit.v) in a directory, or update file paths in the scripts (e.g., file_path in feature_extractor.py).

4)Prepare Dataset (Optional):
If using train_model.py, ensure combined_dataset.csv is in the same directory or update the path. This CSV should have headers: Fan-In, Op Count, Nest Depth, Dep Chain, Gate Mix, Reg Prox, Logic Depth.

## How to Run the Code
1)Feature Extraction (`feature_extractor.py`):Extract features from a Verilog file to analyze its logic depth.

Command:`python feature_extractor.py`

Steps:\
1.Update file_path in the script to point to your Verilog file (e.g., `verilog_modules/comparator_3bit.v`).\
2.Run the script to print features (e.g. [3, 6, 0, 0, 0.0, 1] for comparator_3bit).\
3.Features are returned as [Fan-In, Op Count, Nest Depth, Dep Chain, Gate Mix, Reg Prox].

2)Train the Model and Calculate MSE (`train_model.py`):Train the Random Forest model on your dataset, calculate MSE, and save the model.\
Command:`python train_model.py`\
Steps:\
1.Ensure `combined_dataset.csv` is in the same directory or update its path in the script.\
2.Run the script to train the model, print predictions, MSE, cross-validated MSE, feature importance, and save the model as `rf_logic_depth_model.joblib`.\
3.A bar chart of feature importance will also display.

3)Predict Logic Depth (`predict_depth.py`):Use the trained model to predict the logic depth for a given set of features.

Command:`python predict_depth.py`\
Steps:\
1.Ensure `rf_logic_depth_model.joblib` is in the same directory or update its path.
2.Update features in the script to match your Verilog module’s features (e.g. [3, 6, 0, 0, 0.0, 1] for comparator_3bit).
3.Run the script to print the predicted depth.

## Additional Information
1)Limitations: The current model is optimized for depths 0–3. For depths 4–5, it under-predicts as 3, indicating a need for an expanded dataset\
2)Dependencies: All libraries are open-source and standard (scikit-learn, pandas, etc.), ensuring portability across environments.\
3)File Paths: Update paths (e.g., ``file_path``, ``combined_dataset.csv``, ``rf_logic_depth_model.joblib``) to match your local setup or use relative paths for portability.\
4)Scalability: Future work includes scaling to depths 4–5 and beyond by retraining with an expanded dataset, integrating clock period data, and optimizing for larger IPs.




