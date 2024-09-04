import pandas as pd
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Define the file path
file_path = r"C:\Users\l440\Downloads\final_data (2).csv"

# Load the dataset
df = pd.read_csv(file_path)

# Clean the column names by removing special characters and spaces
df.columns = df.columns.str.replace('?', '', regex=False).str.replace(' ', '_')

# Ensure categorical variables are treated as strings
df['VOICE'] = df['VOICE'].astype(str)
df['comparison_result'] = df['comparison_result'].astype(str)

# Create a contingency table
contingency_table = pd.crosstab(df['VOICE'], df['comparison_result'])

# Print the contingency table
print("Contingency Table:")
print(contingency_table)

# Perform the Chi-Square Test of Independence or Fisher's Exact Test
chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# Check the expected frequencies condition
if np.any(expected < 5):
    print("Some expected frequencies are less than 5. Using Fisher's Exact Test instead of Chi-Square Test.")
    # Fisher's Exact Test is only applicable to 2x2 tables
    if contingency_table.shape == (2, 2):
        odds_ratio, fisher_p_value = stats.fisher_exact(contingency_table)
        print(f"Fisher's Exact Test p-value: {fisher_p_value}")
        print(f"Odds Ratio: {odds_ratio}")
        p_value = fisher_p_value  # Use this p-value for interpretation
    else:
        print("Fisher's Exact Test is only applicable to 2x2 tables. Chi-Square Test may not be valid.")
else:
    print(f"Chi-Square Statistic: {chi2_stat}")
    print(f"p-value: {p_value}")
    print(f"Degrees of Freedom: {dof}")
    print(f"Expected Frequencies:\n{expected}")

# Interpret the p-value
if p_value < 0.05:
    print("We reject the null hypothesis: There is a significant association between the two categorical variables.")
else:
    print("We fail to reject the null hypothesis: There is no significant association between the two categorical variables.")

# Prepare data for bar plots
# Convert contingency table to long-form DataFrame for plotting
df_long = contingency_table.reset_index().melt(id_vars='VOICE', var_name='comparison_result', value_name='Count')

# Plot bar plots
plt.figure(figsize=(14, 7))

# Bar plot for counts of gibberish_transcript within each VOICE level
plt.subplot(1, 2, 1)
sns.barplot(data=df_long, x='VOICE', y='Count', hue='comparison_result', palette='viridis')
plt.title('Result of the Transcripts Quality Comparison within each VOICE level')
plt.xlabel('VOICE')
plt.ylabel('Count')
plt.legend(title='Outcome of comparison: 1 = won, 0 = lost')

plt.tight_layout()
plt.show()
