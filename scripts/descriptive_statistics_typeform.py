import pandas as pd

# Load your dataset
data = pd.read_csv('path/to/your/dataset.csv')

# Condition the dataset on the value "Typeform" in the column 'methodology'
conditioned_data = data[data['methodology'] == 'Typeform']

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
variables = ['RATING', 'COMPL_TIME_SEC', '# words / respondent', '# themes / respondent', '# total followups / respondent']

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
