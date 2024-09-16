import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Load your dataset
file_path = r"C:\Users\l440\Downloads\Merged data without responses.csv"
df = pd.read_csv(file_path)

# Clean the column names by removing special characters and spaces
df.columns = df.columns.str.replace("'", '', regex=False).str.replace(' ', '_')

# Define variables
independent_var = 'Completion_Mode'  # Independent variable column name
continuous_vars = ['User_Experience_Rating', 'Total_Themes_per_Respondent', 'Total_Words_per_Respondent']  # Continuous dependent variables
dependent_var_categorical_1 = 'Transcripts_Comparison_Result'  # Categorical dependent variable 1
dependent_var_categorical_2 = 'Transcript_Classification_Result'  # Categorical dependent variable 2

# Define color palette for histograms/boxplots
colors = {'User_Experience_Rating': 'yellow', 'Total_Themes_per_Respondent': 'red', 'Total_Words_per_Respondent': 'green'}

# Manual font size settings
title_fontsize = 30
label_fontsize = 20
legend_fontsize = 20
tick_fontsize = 20

# Step 1: Explore continuous dependent variables' distribution (not grouped) through histograms with normality curves
for variable in continuous_vars:
    plt.figure(figsize=(12, 10))  # Adjust the figure size
    
    # Plot histogram with KDE (Kernel Density Estimation) and same color as boxplot
    sns.histplot(df[variable], color=colors[variable], kde=False, stat="density", linewidth=0)
    
    # Plot normal distribution curve for comparison
    mean = df[variable].mean()
    std = df[variable].std()
    x = np.linspace(df[variable].min(), df[variable].max(), 100)
    plt.plot(x, stats.norm.pdf(x, mean, std), label='Normal curve', color='black', linestyle='--')
    
    # Set title, labels, and legend with increased font size
    plt.title(f'Distribution of {variable}', fontsize=title_fontsize)
    plt.xlabel(variable, fontsize=label_fontsize)
    plt.ylabel('Density', fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.legend(fontsize=legend_fontsize)
    plt.show()

# Step 2: Explore influence of independent variable on continuous dependent variables with separate boxplots
for variable in continuous_vars:
    plt.figure(figsize=(14, 10))  # Adjust the figure size
    sns.boxplot(x=independent_var, y=variable, data=df, palette=[colors[variable]])
    
    # Set title, labels, and legend with increased font size
    plt.title(f'{variable} by {independent_var}', fontsize=title_fontsize)
    plt.xlabel(independent_var, fontsize=label_fontsize)
    plt.ylabel(variable, fontsize=label_fontsize)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.show()

# Step 3: Q-Q plots for each dependent variable grouped
for variable in continuous_vars:
    plt.figure(figsize=(10, 6))
    for group in df[independent_var].unique():
        group_data = df[df[independent_var] == group][variable]
        stats.probplot(group_data, dist="norm", plot=plt)
        plt.title(f'Q-Q Plot for {variable} - {group}', fontsize=title_fontsize)
        plt.xticks(fontsize=tick_fontsize)
        plt.yticks(fontsize=tick_fontsize)
    plt.show()

# Step 4: Explore absolute counts for categorical dependent variables grouped by the independent variable

# Filter the dataset to show only the level "better" of the categorical dependent variable 1
df_better = df[df[dependent_var_categorical_1] == 'better']

plt.figure(figsize=(12, 8))
sns.countplot(x=dependent_var_categorical_1, hue=independent_var, data=df_better, palette=['#FF9999', '#66B2FF'])

# Set title and ylabel, but remove xlabel
plt.title(f'Better Transcripts Counts Grouped by {independent_var}', fontsize=title_fontsize)
plt.xlabel('')  # Remove the x-axis label
plt.ylabel('Count', fontsize=label_fontsize)

# Increase the size of the x-axis levels (Glaut, Typeform)
plt.xticks(fontsize=tick_fontsize + 4)  # Increase text size for the x-axis levels
plt.yticks(fontsize=tick_fontsize)

plt.legend(title=independent_var, fontsize=legend_fontsize)
plt.show()

plt.figure(figsize=(12, 10))
sns.countplot(x=dependent_var_categorical_2, hue=independent_var, data=df, palette=['#FF9999', '#66B2FF'])

# Set title and ylabel, but remove xlabel
plt.title(f'Transcripts Classification Results Grouped by {independent_var}', fontsize=title_fontsize)
plt.xlabel('')  # Remove the x-axis label
plt.ylabel('Count', fontsize=label_fontsize)

# Increase the size of the x-axis levels (Glaut, Typeform)
plt.xticks(fontsize=tick_fontsize + 4)  # Increase text size for the x-axis levels
plt.yticks(fontsize=tick_fontsize)

plt.legend(title=independent_var, fontsize=legend_fontsize)
plt.show()

# Step 5: Contingency tables for categorical variables
contingency_table_1 = pd.crosstab(df[dependent_var_categorical_1], df[independent_var])
contingency_table_2 = pd.crosstab(df[dependent_var_categorical_2], df[independent_var])
print("\nContingency Tables:")
print(contingency_table_1, contingency_table_2)
