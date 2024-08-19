import pandas as pd
import numpy as np

# Load your dataset
data = pd.read_csv(r'C:\author_file_path\original_dataset.csv')

# Function to generate a synthetic dataset preserving frequency distributions
def generate_synthetic_dataset(original_data, n_samples=None):
    if n_samples is None:
        n_samples = len(original_data)
    
    synthetic_data = original_data.sample(n=n_samples, replace=True, random_state=1)
    return synthetic_data

# Generate a synthetic dataset with the same number of rows as the original
synthetic_data = generate_synthetic_dataset(data)

# Save the synthetic dataset
synthetic_data.to_csv(r'user_file_path/synthetic_dataset.csv', index=False)

print("Synthetic dataset generated successfully!")
