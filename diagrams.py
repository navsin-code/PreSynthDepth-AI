import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import matplotlib.pyplot as plt


# Parse features
def parse_opencore_features(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
        # Unique inputs (bus widths, handle symbolic)
        inputs = set()
        for line in code.split('\n'):
            if 'input' in line and '[' in line:
                try:
                    range_str = line.split('[')[1].split(']')[0]
                    if ':' in range_str:
                        start, end = map(int, range_str.split(':'))
                        width = abs(start - end) + 1
                        inputs.add(width)
                    else:
                        inputs.add(1)
                except (ValueError, IndexError):
                    inputs.add(4)
        fan_in = sum(inputs) if inputs else max(code.count('['), 2)

        # Gate counts
        assign_code = ''.join(line for line in code.split('\n') if 'assign' in line)
        and_count = assign_code.count('&')
        or_count = assign_code.count('|')
        xor_count = assign_code.count('^')
        not_count = assign_code.count('~')
        shift_count = assign_code.count('<<') + assign_code.count('>>') + assign_code.count('<<<') + assign_code.count(
            '>>>')
        comp_count = assign_code.count('>') + assign_code.count('<') + assign_code.count('==')
        ternary_count = assign_code.count('?')
        total_gates = and_count + or_count + xor_count + not_count + shift_count + comp_count + ternary_count
        gate_mix = (and_count + or_count) / total_gates if total_gates > 0 else 1.0
        op_count = total_gates

        # Nesting
        nest_depth = assign_code.count('(') - assign_code.count(')')  # Balanced nesting
        if nest_depth < 0: nest_depth = 0  # Safety

        # Dependency chain (wires beyond outputs)
        dep_chain = code.count('wire') - 1 if code.count('wire') > 0 else 0

        # Register proximity (assume inputs from flops unless clear otherwise)
        reg_prox = 1 if "always @" in code else 1  # Keep 1 for consistency

    return [fan_in, op_count, nest_depth, dep_chain, gate_mix, reg_prox]


# Load and parse the module
file_path = "verilog file on local system"
features = parse_opencore_features(file_path)
print("Extracted Features:", features)

# Load model
model = joblib.load('model path')

# Predict depth
predicted_depth = model.predict([features])[0]
print("Predicted Logic Depth:", predicted_depth)

# Actual depth for comparison (hardcode or show manual trace)
actual_depth = "Calcuated manually"
print("Actual Logic Depth (manual):", actual_depth)

# Feature importance plot
feature_names = ["Fan-In", "Op Count", "Nest Depth", "Dep Chain", "Gate Mix", "Reg Prox"]
feature_importance = model.feature_importances_
plt.bar(feature_names, feature_importance)
plt.title("Feature Importance for Logic Depth Prediction")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Plot predicted vs. actual
plt.scatter([actual_depth], [predicted_depth], color='blue', label='Prediction vs Actual')
plt.plot([0, 3], [0, 3], 'r--', label='Perfect Prediction')
plt.xlabel("Actual Depth")
plt.ylabel("Predicted Depth")
plt.title("Prediction Accuracy")
plt.legend()
plt.grid(True)
plt.show()