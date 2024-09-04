import os
import pandas as pd
import google.generativeai as genai
import time
import logging

# Load the DataFrame 1
file_path_1 = r"user_file_path\Glaut_transcripts.csv"
df = pd.read_csv(file_path_1)

def count_words_excluding_interviewer(transcript):
    """Counts words in a transcript, excluding 'Interviewer:' lines."""
    words = []
    counting = False
    for line in transcript.splitlines():
        if line.strip().startswith(("Interviewee:", "interviewee:")):
            counting = True
        elif line.strip().startswith(("Interviewer:", "interviewer:")):
            counting = False
        if counting:
            words.extend(line.strip().split())
    return len(words)

# Apply the word count function to calculate word counts for each transcript
df['word_count'] = df['Glaut transcripts'].apply(count_words_excluding_interviewer)

# Sort by word count while preserving the original order index
df['original_index'] = df.index
df = df.sort_values(by='word_count', ascending=True).reset_index(drop=True)

# Assign unique ranks
df['rank'] = range(1, len(df) + 1)

# Sort back to the original order
df = df.sort_values(by='original_index').drop(columns=['original_index'])

# Save the DataFrame with the ranks
output_file_path = r"C:\Users\l440\Downloads\Glaut_transcripts_ranked.csv"
df.to_csv(output_file_path, index=False)

# Print to check the result
print(df[['Glaut transcripts', 'word_count', 'rank']])

# Load the DataFrame 2
file_path_2 = r"user_file_path\Typeform_transcripts.csv"
df = pd.read_csv(file_path_2)

def count_words_excluding_interviewer(transcript):
    """Counts words in a transcript, excluding 'Interviewer:' lines."""
    words = []
    counting = False
    for line in transcript.splitlines():
        if line.strip().startswith(("Interviewee:", "interviewee:")):
            counting = True
        elif line.strip().startswith(("Interviewer:", "interviewer:")):
            counting = False
        if counting:
            words.extend(line.strip().split())
    return len(words)

# Apply the word count function to calculate word counts for each transcript
df['word_count'] = df['Typeform transcripts'].apply(count_words_excluding_interviewer)

# Sort by word count while preserving the original order index
df['original_index'] = df.index
df = df.sort_values(by='word_count', ascending=True).reset_index(drop=True)

# Assign unique ranks
df['rank'] = range(1, len(df) + 1)

# Sort back to the original order
df = df.sort_values(by='original_index').drop(columns=['original_index'])

# Save the DataFrame with the ranks
output_file_path = r"user_file_path\Typeform_transcripts_ranked.csv"
df.to_csv(output_file_path, index=False)

# Print to check the result
print(df[['Typeform transcripts', 'word_count', 'rank']])

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure the Gemini API with the API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# Function to start a chat session with the initial prompt
def start_chat_session():
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    """You are an AI tasked with evaluating survey transcripts based on two key metrics: adequacy of the response with respect to the question's context and depth/richness of the response. 

    # Selection criteria:
    1. Adequacy to Context:
    Which response addresses better the questions?
    Which response stays more relevant and on-topic?

    2. Depth/Richness:
    Which response provides more detailed and thoughtful insights?
    Which response shows a deeper understanding or exploration of the topic?

    # Task:
    Compare the following two responses to the question: '{column}' and select the better one based on the criteria mentioned above.

    # Responses:
    Response 1: '{response1}'
    Response 2: '{response2}'

    # Expected Output Format:
    Please respond with the better response source only in the following format:
    "Selected: Response 1" or "Selected: Response 2"
"""
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Please provide me with the question, response 1, and response 2 so I can evaluate them and select the better response based on the scoring criteria. \n",
                ],
            },
        ]
    )
    return chat_session

# Function to compare responses and determine the better source with exponential backoff
def compare_responses(response1, response2, column):
    prompt = f"""
    You are an AI tasked with evaluating survey transcripts based on two key metrics: adequacy and meaningfulness with respect to the questions' context and depth/richness of the responses.

    # Selection criteria:
    1. Adequacy to Context:
    Which response addresses better the questions?
    Which response stays more relevant and on-topic?

    2. Depth/Richness:
    Which response provides more detailed and thoughtful insights?
    Which response shows a deeper understanding or exploration of the topic?

    # Task:
    Compare the following two responses to the question: '{column}' and select the better one based on the criteria mentioned above.

    # Responses:
    Response 1: '{response1}'
    Response 2: '{response2}'

    # Expected Output Format:
    Please respond with the better response source only in the following format:
    "Selected: Response 1" or "Selected: Response 2"
    """

    chat_session = start_chat_session()
    user_input = prompt

    attempt = 0
    max_attempts = 10
    delay = 3  # initial delay in seconds

    while attempt < max_attempts:
        try:
            model_response = chat_session.send_message(user_input)
            response_text = model_response.text.strip()

            logging.info(f"Model Response: {response_text}")

            # Extract the selected source from the model's response
            if "Selected: Response 1" in response_text:
                return "1"
            elif "Selected: Response 2" in response_text:
                return "0"
            else:
                logging.warning(f"Unclear model response: {response_text}")
                return "Unclear"
        except Exception as e:
            if "429" in str(e):  # Rate limit error
                logging.warning(f"Rate limit hit, retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                logging.error(f"Error during LLM call: {e}")
                return "Error"
            attempt += 1

    logging.error("Maximum retry attempts reached.")
    return "Error"

# Function to compare responses in the two datasets based on the 'rank' column
def compare_responses_by_rank(df1, df2):
    # Ensure that both DataFrames have a 'rank' column
    assert 'rank' in df1.columns and 'rank' in df2.columns, "Both DataFrames must have a 'rank' column for comparison"
    
    # Store the original index
    df1['original_index'] = df1.index
    df2['original_index'] = df2.index
    
    # Sort the DataFrames by 'rank' to align corresponding rows
    df1_sorted = df1.sort_values(by='rank').reset_index(drop=True)
    df2_sorted = df2.sort_values(by='rank').reset_index(drop=True)

    # Check columns in DataFrames
    response_columns = [col for col in df1_sorted.columns if col not in ['rank', 'comparison_result', 'original_index']]
    
    # Create a new column in df1 to store the comparison results
    df1_sorted['comparison_result'] = None

    for idx in df1_sorted.index:
        for column in response_columns:
            response1 = df1_sorted.at[idx, column]
            response2 = df2_sorted.at[idx, column]

            better_source = compare_responses(response1, response2, column)
            df1_sorted.at[idx, 'comparison_result'] = better_source

            # Sleep to avoid rate limiting
            time.sleep(3)

    # Restore the original index order
    df1_sorted = df1_sorted.sort_values(by='original_index').drop(columns=['original_index'])

    return df1_sorted

# Function to count occurrences of '1' and '0' in the 'comparison_result' column
def count_comparison_results(file_path):
    df = pd.read_csv(file_path)
    if 'comparison_result' not in df.columns:
        raise KeyError("The DataFrame does not contain a 'comparison_result' column.")
    
    result_counts = df['comparison_result'].value_counts()
    return result_counts

# Main script execution
if __name__ == "__main__":
    # Load the two datasets
    file_path1 = r"user_file_path\Glaut_transcripts.csv"
    file_path2 = r"user_file_path\Typeform_transcripts.csv"

    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)

    # Print columns to check their names
    print("Columns in df1:", df1.columns)
    print("Columns in df2:", df2.columns)

    # Perform the pairwise comparison based on the 'rank' column
    comparison_results_df = compare_responses_by_rank(df1, df2)

    # Save the comparison results back to the first DataFrame (Glaut_transcripts.csv)
    output_file_path = r"user_file_path\comparison_results.csv"
    comparison_results_df.to_csv(output_file_path, index=False)

    # Output the result DataFrame
    print(comparison_results_df)

    # Count and print occurrences of '1' and '0' in the comparison results
    result_counts = count_comparison_results(output_file_path)
    print("Comparison result counts:")
    print(result_counts)
