import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path
file_path = r"user_file_path\synthetic_dataset.csv"

# Load the dataset
df = pd.read_csv(file_path)

# Split the data based on the Voice variable
group_0 = df[df['FOLLOWUP'] == 0]['Average_Quality_Score']
group_1 = df[df['FOLLOWUP'] == 1]['Average_Quality_Score']

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
if normal_0 and normal_1:
    if equal_var:
        # Perform t-test for independent samples (equal variances assumed)
        t_test = stats.ttest_ind(group_0.dropna(), group_1.dropna(), equal_var=True)
        print(f"Independent t-test: t-statistic={t_test.statistic}, p-value={t_test.pvalue}")
        positive_t_test = t_test.pvalue < 0.05
    else:
        # Perform Welch's t-test (unequal variances assumed)
        t_test = stats.ttest_ind(group_0.dropna(), group_1.dropna(), equal_var=False)
        print(f"Welch's t-test: t-statistic={t_test.statistic}, p-value={t_test.pvalue}")
        positive_t_test = t_test.pvalue < 0.05
else:
    # Perform Mann-Whitney U test for non-normal distributions
    mannwhitney_test = stats.mannwhitneyu(group_0.dropna(), group_1.dropna())
    print(f"Mann-Whitney U test: U-statistic={mannwhitney_test.statistic}, p-value={mannwhitney_test.pvalue}")
    positive_mannwhitney_test = mannwhitney_test.pvalue < 0.05

# Determine alternative hypothesis acceptance
if 't_test' in locals():
    positive_t_test = t_test.pvalue < 0.05
if 'mannwhitney_test' in locals():
    positive_mannwhitney_test = mannwhitney_test.pvalue < 0.05

# Plot the data
plt.figure(figsize=(10, 6))
sns.boxplot(x='FOLLOWUP', y='RATING', data=df)
plt.title('Boxplot of # themes / respondents by Voice')
plt.show()

# Variance Equality Check and Comments
if levene_test.pvalue < 0.05:
    print("Variances are not equal.")
else:
    print("Variances are equal.")

# Additional Comments
if not (normal_0 and normal_1):
    print("One or both groups are not normally distributed.")
else:
    print("Both groups are normally distributed.")

if positive_t_test is True:
  print("The difference in means for the variable "Average_Quality_Score" considering the two levels of the variable FOLLOWUP is statistically significant")
else:
  print("There is not a statistically significant difference between the means of the variable "Average_Quality_Score" considering the two levels of the variable FOLLOWUP")
