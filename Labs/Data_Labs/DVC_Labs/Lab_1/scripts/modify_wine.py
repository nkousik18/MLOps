import os
import pandas as pd

# Base directory (one level up from 'scripts')
BASE_DIR = os.path.dirname(__file__)
data_path = os.path.join(BASE_DIR, "..", "data", "winequality-red.csv")

# Load dataset (semicolon delimited)
df = pd.read_csv(data_path, sep=";")

# Display initial shape and columns
print("Original shape:", df.shape)
print("Original columns:", list(df.columns))

# Example modification: categorize wine quality
def quality_label(x):
    if x >= 7:
        return "high"
    elif x >= 5:
        return "medium"
    else:
        return "low"

df["quality_label"] = df["quality"].apply(quality_label)

# Save the modified dataset to the same data folder
output_path = os.path.join(BASE_DIR, "..", "data", "winequality-red-modified.csv")
df.to_csv(output_path, index=False)

print(f"✅ Modified dataset saved to {output_path}")
print("New shape:", df.shape)
