import pandas as pd

# Load your dataset
data = pd.read_csv('user_file_path/synthetic_dataset.csv')

# Condition the dataset on the value "Traditional Survey" in the column 'Completion Mode'
conditioned_data = data[data['Completion Mode'] == 'Traditional Survey']

# Define a function to compute descriptive statistics
def compute_descriptive_stats(df, columns):
    stats = {}
    for column in columns:
        if column in df.columns:
            stats[column] = {
                'Median': df[column].median(),
                'Average': df[column].mean(),
                'IQR': df[column].quantile(0.75) - df[column].quantile(0.25),
                'Max': df[column].max(),
                'Min': df[column].min()
            }
        else:
            stats[column] = 'Column not found in the dataset'
    return stats

# Variables of interest
variables = ['RATING', 'Total Words per Respondent', 'Total Themes per Respondent', 'total_num_followups']

# Compute the descriptive statistics
descriptive_stats = compute_descriptive_stats(conditioned_data, variables)

# Print the results
for var, stats in descriptive_stats.items():
    print(f"Descriptive statistics for {var}:")
    if isinstance(stats, dict):
        for stat_name, value in stats.items():
            print(f"  {stat_name}: {value}")
    else:
        print(f"  {stats}")
    print()
