import pandas as pd
import numpy as np
import re


file_path="/home/nassosliak/Desktop/avlsi/TDD/cadence/vc.csv"
data=pd.read_csv(file_path)
height=0.68
mean_value=1.3
target_indices=[]
sigmas=[]
vc_values=[]
print(data.columns)
print(data.iloc[:, 0])
for i in range(1,data.columns.size):
    max_value=(np.max(data.iloc[:, 1]))
    target_value = max_value * height
    closest_index = (np.abs(data.iloc[:, i] - target_value)).idxmin()
    sigmas.append(np.abs(data.iloc[closest_index, 0]-mean_value))
print(sigmas)
pattern = re.compile(r'Vc\s*(-?\d*\.?\d+([eE][-+]?\d+)?)')

#Extract vc values
for col in data.columns:
    match = pattern.search(col)
    if match:
        value_str = match.group(1)
        try:
            vc_values.append(float(value_str))
        except ValueError as e:
            print(f"Error converting '{value_str}' to float: {e}")

print("Extracted Vc values:", vc_values)


degree = 3
coefficients = np.polyfit(sigmas, vc_values, degree)

polynomial = np.poly1d(coefficients)
print(polynomial)
vcrange=(0,1)
sigma_range = np.linspace(min(sigmas), max(sigmas), 10)
vc_from_polynomial = polynomial(sigma_range)

print(f"Sigmas corresponding to Vc values within the range {vcrange}:")
filtered_sigmas = sigma_range[(vc_from_polynomial >= vcrange[0]) & (vc_from_polynomial <= vcrange[1])]
filtered_vcs = vc_from_polynomial[(vc_from_polynomial >= vcrange[0]) & (vc_from_polynomial <= vcrange[1])]

for sigma, vc in zip(filtered_sigmas, filtered_vcs):
    print(f"Sigma: {sigma}, Vc: {vc}")
print("Vr: ", mean_value)