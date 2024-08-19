from assess_themes_by_voice import assess_themes_by_voice
from assess_themes_by_followup import assess_themes_by_followup
from assess_rating_by_voice import assess_rating_by_voice
from assess_rating_by_followup import assess_rating_by_followup

def main():
    data_path = r"C:user_file_path\synthetic_dataset.csv"
    
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
