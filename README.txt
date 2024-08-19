# Glaut_AI_Market_Research_Analysis

This repository contains modules and scripts used for the analysis of data collected in a market research project utilizing Glaut's AI-native market research software. 
The project compares the performance of an AI conversational agent with traditional static surveys in extracting qualitative insights at scale.
This repository contains scripts to assess and visualize whether the means of specific variables are different when conditioned by categorical variables. 
The analyses include boxplot visualizations for better understanding.

## Main Contents
- Descriptive Statistics: modules for performing descriptive statistics on our dataset and ensure samples comparability and equivalence.
- Statistical Analysis and Visualization: modules for performing statistical hypothesis testing and data visualization.
- Dataset: please note that the actual datasets used in this research are not included in the repository due to privacy and confidentiality agreements. 
  However, synthetic data are provided for demonstration purposes. Download data on your local machine and change the file_path variable accordingly.
- Docs: redirect link to the research paper where we show our findings.

## Contributions
Contributions are welcome. Please submit a pull request or open an issue for any changes or suggestions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Repository Structure
Glaut_AI_Market_Research_Analysis/
├── data/
│ └── README.txt
│ ├── synthetic_dataset.csv
├── scripts/
│ ├── descriptive_statistics_glaut.py
│ ├── descriptive_statistics_typeform.py
│ ├── assess_means_themes_by_voice.py
│ ├── assess_means_themes_by_followup.py
│ ├── assess_means_words_by_voice.py
│ ├── assess_means_rating_by_voice.py
│ ├── assess_means_rating_by_followup.py
│ ├── generate_synthetic_dataset.py
│ ├── main.py
├── docs/
│ └── research_paper_link
├── requirements.txt
├── LICENSE.txt
└── README.txt
