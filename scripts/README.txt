# Scripts Overview
This folder contains Python scripts for data analysis and generation tasks. Each script is designed to perform specific operations on the dataset. 
Below is a description of each script and its purpose.

## Scripts
- descriptive_statistics_glaut.py
Calculates and outputs descriptive statistics (median, average, IQR, max, min, etc.) for selected variables in the dataset, specifically for rows where the methodology column has the value "Glaut". Variables include RATING, COMPL_TIME_SEC, # words / respondent, # themes / respondent, and # total followups / respondent.

- descriptive_statistics_typeform.py
Similar to descriptive_statistics_glaut.py, this script calculates and outputs descriptive statistics for the same set of variables but for rows where the methodology column has the value "Typeform".

- assess_means_themes_by_voice.py
Assesses and compares the mean number of themes per respondent based on different voice types. This script helps to analyze how the number of themes varies with different voice categories.

- assess_means_words_by_voice.py
Analyzes the average number of words per respondent across different voice types. This script is useful for understanding how the number of words varies with voice types.

- assess_means_rating_by_voice.py
Evaluates and compares the average ratings provided by respondents across different voice types. This script helps in analyzing how ratings vary with different voice categories.

- assess_means_rating_by_followup.py
Assesses the average ratings based on the number of follow-ups. This script examines how ratings are influenced by the number of follow-ups received.

- generate_synthetic_dataset.py
Generates a synthetic dataset that preserves the frequency distributions of the original dataset. This script can be used for testing or simulating data scenarios.

- quality_score_LLM.py
Performs quality scores evaluation of surveys answers through the iteration of an adequately-prompted LLM over the dataframe responses.

- main.py
Serves as the main entry point for running the various analyses. This script might include functionality to call other scripts or to execute a series of predefined tasks.

## Usage
To run any of these scripts, you need to have Python installed along with the required libraries. Make sure to have your dataset available and adjust any file paths or configurations as necessary.
Install Dependencies: Ensure you have the required packages installed. You can use the requirements.txt file for this purpose.
pip install -r requirements.txt

## Contributions
If you wish to contribute to this project, please fork the repository, make your changes, and submit a pull request. Ensure that any new features or fixes are accompanied by appropriate tests and documentation.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
