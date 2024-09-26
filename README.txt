# Glaut_AI_Market_Research_Analysis

This repository contains modules and scripts used for the analysis of data collected in a market research project utilizing Glaut's AI-native market research software and a globally known survey builder.
The project compares the performance of an AI conversational agent with traditional static surveys in extracting qualitative insights at scale.
This repository contains scripts to assess and visualize whether the means of specific variables are different when conditioned by categorical variables. Plus, we present the script used to automatically annotate (and classify) data with categorical levels through an instructed LLM. It is also included a synthetic dataset that resembles the original data distributions. 

## Main Contents
- Descriptive Statistics: modules for performing descriptive statistics on our dataset and ensure samples comparability and equivalence.
- Statistical Analysis and Visualization: modules for performing statistical hypothesis testing and data visualization.
- Transcripts Quality Comparison and Transcripts Classification as Gibberish through LLM: modules for performing quality comparison and text classification analysis of surveys and     
  interviews transcripts
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
│ └── README.txt
│ ├── transcripts_quality_comparison_LLM.py
│ ├── transcripts_gibberish_categorization_LLM.py
│ ├── descriptive_statistics_glaut.py
│ ├── descriptive_statistics_typeform.py
│ ├── exploratory_analysis_and_visualization.py
│ ├── statistical_tests_and_results_interpretation.py
├── docs/
│ └── research_paper_link
├── requirements.txt
├── LICENSE.txt
└── README.txt
