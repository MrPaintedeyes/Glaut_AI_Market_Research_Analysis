import pandas as pd
from scipy.stats import chi2_contingency, shapiro, levene, ttest_ind, mannwhitneyu
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
file_path = user_file_path
df = pd.read_csv(file_path)

# List of continuous dependent variables (these are the variables you're testing with Mann-Whitney U or t-test)
continuous_vars = ['User_Experience_Rating', 'Total_Themes_per_Respondent', 'Total_Words_per_Respondent']

# Define the categorical independent and dependent variables
independent_var = 'Completion Mode'
dependent_var_categorical_1 = "Transcripts_Comparison_Result" 
dependent_var_categorical_2 = 'Transcript_Classification_Result'

# Bonferroni correction
alpha = 0.05
number_of_comparisons = 5  # Total number of comparisons (3 continuous + 1 categorical)
corrected_p_value = alpha / number_of_comparisons

print(f'Corrected p-value threshold based on Bonferroni correction: {corrected_p_value:.17f}\n')

# Store p-values for interpretation (parametric and non-parametric tests)
p_values_parametric = []
p_values_nonparametric = []
chi2_p_value = None

# Step 1: Loop through each continuous dependent variable
for variable in continuous_vars:
    group_glaut = df[df['Completion Mode'] == 'Glaut'][variable]
    group_typeform = df[df['Completion Mode'] == 'Typeform'][variable]

    # Step 2: Check normality using the Shapiro-Wilk test
    shapiro_glaut = shapiro(group_glaut)[1]  # Get the p-value
    shapiro_typeform = shapiro(group_typeform)[1]  # Get the p-value

    # Step 3: Check equal variances using Levene's test
    levene_test = levene(group_glaut, group_typeform)[1]  # Get the p-value

    # Step 4: Decide whether to use parametric (t-test) or non-parametric (Mann-Whitney U) based on normality and equal variance
    print(f"\n--- Results for {variable} ---")
    print(f"Shapiro-Wilk test p-values: Glaut={shapiro_glaut:.10f}, Typeform={shapiro_typeform:.10f}")
    print(f"Levene's test p-value for equal variances: p={levene_test:.17f}")

    if shapiro_glaut >= 0.05 and shapiro_typeform >= 0.05 and levene_test >= 0.05:
        # Parametric: Both normality and equal variances are met, use t-test
        print("Both normality and equal variances met. Proceeding with t-test.")
        stat, p_value = ttest_ind(group_glaut, group_typeform, equal_var=True)
        p_values_parametric.append(p_value)
        print(f't-test for {variable}: t={stat:.4f}, p={p_value:.17f}')
    else:
        # Non-parametric: Either normality or equal variances not met, use Mann-Whitney U test
        print("Normality or equal variances not met. Proceeding with Mann-Whitney U test.")
        stat, p_value = mannwhitneyu(group_glaut, group_typeform)
        p_values_nonparametric.append(p_value)
        print(f'Mann-Whitney U test for {variable}: U={stat:.4f}, p={p_value:.17f}')

# Step 5: Chi-Square tests for categorical dependent variables
print(f"\n--- Chi-Square Test for Categorical Variable ---")
contingency_table_1 = pd.crosstab(df[dependent_var_categorical_1], df[independent_var])
contingency_table_2 = pd.crosstab(df[dependent_var_categorical_2], df[independent_var])


# Perform Chi-Square test for the first categorical dependent variable
chi2_1, p_1, dof_1, expected_1 = chi2_contingency(contingency_table_1)
print(f'Chi-Square Test Results for {dependent_var_1}:\nChi2 Stat: {chi2_1:.17f}\nP-value: {p_1:.17f}\nDegrees of Freedom: {dof_1}')
print('\nExpected Frequencies for Transcript Classification Result:')
print(pd.DataFrame(expected_1, index=contingency_table_1.index, columns=contingency_table_1.columns))

# Perform Chi-Square test for the second categorical dependent variable
chi2_2, p_2, dof_2, expected_2 = chi2_contingency(contingency_table_2)
print(f'Chi-Square Test Results for {dependent_var_1}:\nChi2 Stat: {chi2_2:.17f}\nP-value: {p_2:.17f}\nDegrees of Freedom: {dof_2}')
print('\nExpected Frequencies for Transcript Classification Result:')
print(pd.DataFrame(expected_2, index=contingency_table_2.index, columns=contingency_table_2.columns))


# Step 6: Display all p-values and compare them to the corrected p-value threshold
print("\n--- Final Results and Interpretation ---")
# Continuous variables - Parametric (t-test) and Non-parametric (Mann-Whitney U)
for i, variable in enumerate(continuous_vars):
    if i < len(p_values_parametric):  # Parametric tests
        p_value = p_values_parametric[i]
        if p_value <= corrected_p_value:
            print(f'The result for {variable} (t-test) is statistically significant with a p-value of {p_value:.17f}.')
        else:
            print(f'The result for {variable} (t-test) is not statistically significant with a p-value of {p_value:.17f}.')
    else:  # Non-parametric tests
        p_value = p_values_nonparametric[i - len(p_values_parametric)]
        if p_value <= corrected_p_value:
            print(f'The result for {variable} (Mann-Whitney U) is statistically significant with a p-value of {p_value:.17f}.')
        else:
            print(f'The result for {variable} (Mann-Whitney U) is not statistically significant with a p-value of {p_value:.17f}.')

# Interpretation for 'Transcripts' Comparison Result'
print("\n--- Interpretation for Transcripts' Comparison Result ---")
if p_1 < corrected_p_value:
    print(f'The p-value is {p_1:.17f}, which is less than the significance level of {corrected_p_value}.')
    print(f'Conclusion: There is a statistically significant association between the independent variable ({independent_var}) and the dependent variable ({dependent_var_categorical_1}).')
else:
    print(f'The p-value is {p_1:.17f}, which is greater than or equal to the significance level of {corrected_p_value}.')
    print(f'Conclusion: There is no statistically significant association between the independent variable ({independent_var}) and the dependent variable ({dependent_var_categorical_1}).')
    
# Interpretation for 'Transcript Classification Result'
print("\n--- Interpretation for Transcripts Classification Result ---")
if p_2 < corrected_p_value:
    print(f'The p-value is {p_2:.17f}, which is less than the significance level of {corrected_p_value}.')
    print(f'Conclusion: There is a statistically significant association between the independent variable ({independent_var}) and the dependent variable ({dependent_var_categorical_2}).')
else:
    print(f'The p-value is {p_2:.17f}, which is greater than or equal to the significance level of {corrected_p_value}.')
    print(f'Conclusion: There is no statistically significant association between the independent variable ({independent_var}) and the dependent variable ({dependent_var_categorical_2}).')
