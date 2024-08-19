import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path
file_path = r"user_file_path\synthetic_dataset.csv"

# Load the dataset
df = pd.read_csv(file_path)

# Convert 'VOICE' to string if it's not already
df['VOICE'] = df['VOICE'].astype(str)

# Split the data based on the Voice variable
group_0 = df[df['VOICE'] == '0']['# words / respondent']
group_1 = df[df['VOICE'] == '1']['# words / respondent']

# Check the number of data points in each group
print(f"Number of data points in group 0: {len(group_0)}")
print(f"Number of data points in group 1: {len(group_1)}")

# Ensure that each group has at least 3 data points
if len(group_0) < 3 or len(group_1) < 3:
    raise ValueError("Each group must have at least 3 data points for the statistical tests.")

# Check for normality using Shapiro-Wilk test
shapiro_0 = stats.shapiro(group_0.dropna())
shapiro_1 = stats.shapiro(group_1.dropna())

print(f"Shapiro-Wilk test for group 0: W={shapiro_0.statistic}, p-value={shapiro_0.pvalue}")
print(f"Shapiro-Wilk test for group 1: W={shapiro_1.statistic}, p-value={shapiro_1.pvalue}")

# Determine normality
normal_0 = shapiro_0.pvalue > 0.05
normal_1 = shapiro_1.pvalue > 0.05

# Check for equality of variances using Levene's test
levene_test = stats.levene(group_0.dropna(), group_1.dropna())
print(f"Levene's test for equality of variances: W={levene_test.statistic}, p-value={levene_test.pvalue}")

# Determine variance equality
equal_var = levene_test.pvalue > 0.05

# Perform the appropriate test based on normality and variance results
t_test = None
mannwhitney_test = None

if normal_0 and normal_1:
    if equal_var:
        # Perform t-test for independent samples (equal variances assumed)
        t_test = stats.ttest_ind(group_0.dropna(), group_1.dropna(), equal_var=True)
        print(f"Independent t-test: t-statistic={t_test.statistic}, p-value={t_test.pvalue}")
    else:
        # Perform Welch's t-test (unequal variances assumed)
        t_test = stats.ttest_ind(group_0.dropna(), group_1.dropna(), equal_var=False)
        print(f"Welch's t-test: t-statistic={t_test.statistic}, p-value={t_test.pvalue}")
else:
    # Perform Mann-Whitney U test for non-normal distributions
    mannwhitney_test = stats.mannwhitneyu(group_0.dropna(), group_1.dropna())
    print(f"Mann-Whitney U test: U-statistic={mannwhitney_test.statistic}, p-value={mannwhitney_test.pvalue}")

# Determine alternative hypothesis acceptance
if t_test:
    if t_test.pvalue < 0.05:
        print("We accept the alternative hypothesis")
    else: 
        print("We reject the alternative hypothesis and support the null hypothesis")

if mannwhitney_test:
    if mannwhitney_test.pvalue < 0.05:
        print("We accept the alternative hypothesis")
    else:
        print("We reject the alternative hypothesis and support the null hypothesis")

# Plot the data with different colors for the two groups
plt.figure(figsize=(10, 6))

# Define colors for the groups based on the actual unique values in the VOICE column
unique_voices = df['VOICE'].unique()  # Ensure VOICE is treated as string
palette = {voice: color for voice, color in zip(unique_voices, ['skyblue', 'salmon'])}

sns.boxplot(x='VOICE', y='# words / respondent', data=df, palette=palette)
plt.title('Number of Words per Survey Conditioned by the Use of Voice')
plt.show()

# Variance Equality Check and Comments
if levene_test.pvalue < 0.05:
    print("Variances are not equal.")
else:
    print("Variances are equal.")

# Additional Comments
if not (normal_0 and normal_1):
    print("One or both groups are not normally distributed.")
