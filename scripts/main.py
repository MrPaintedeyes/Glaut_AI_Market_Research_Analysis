from assess_themes_by_voice import assess_themes_by_voice
from assess_themes_by_followup import assess_themes_by_followup
from assess_rating_by_voice import assess_rating_by_voice
from assess_rating_by_followup import assess_rating_by_followup
from descriptive_statistics_glaut import descriptive_statistics_glaut
from descriptive_statistics_typeform import descriptive_statistics_typeform
def main():
    data_path = r"user_file_path\synthetic_dataset.csv"

    print("Performing descriptive statistics...")
    descriptive_statistics_glaut(data_path)
    descriptive_statistics_typeform(data_path)
    
    print("Assessing themes by voice...")
    assess_themes_by_voice(data_path)
    
    print("Assessing themes by followup...")
    assess_themes_by_followup(data_path)
    
    print("Assessing rating by voice...")
    assess_rating_by_voice(data_path)
    
    print("Assessing rating by followup...")
    assess_rating_by_followup(data_path)

if __name__ == "__main__":
    main()
