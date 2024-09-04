import os
import pandas as pd
import google.generativeai as genai
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure the Gemini API with the API key
genai.configure(api_key="YOUR_GEMINI_API")

# Define the generation configuration for the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start the chat session with the initial prompt
def start_chat_session():
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are an AI tasked with categorizing survey answers. Your task is to determine if each answer is 'gibberish' (nonsensical, random characters, or out of context) or 'not gibberish' (meaningful and relevant with respect to the question's topic).",
                    "Please always respond in the following format for each response: 'Response [index]: Category: gibberish' or 'Response [index]: Category: not gibberish'.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, I'm ready to start categorizing text responses. I understand the categories 'gibberish' and 'not gibberish' and will respond in the format you requested. Please provide me with the text you want me to categorize!",
                ],
            },
        ]
    )
    return chat_session

def classify_batch(responses, start_idx, chat_session):
    user_input = "Please categorize the following responses:\n"
    for i, response in enumerate(responses, start=1):
        user_input += f"Response {start_idx + i - 1}: \"{response}\"\n"

    attempt = 0
    max_attempts = 5
    delay = 5  # initial delay in seconds

    while attempt < max_attempts:
        try:
            model_response = chat_session.send_message(user_input)
            response_text = model_response.text.strip()

            # Log the response for debugging
            logging.info(f"Model Response: {response_text}")

            classifications = {}
            for line in response_text.split('\n'):
                if "Category:" in line:
                    try:
                        index_part = line.split("Response ")[1].split(":")[0].strip()
                        classification = line.split("Category:")[1].strip()
                        index = int(index_part)  # Convert the index to an integer
                        classifications[index] = classification
                    except (IndexError, ValueError) as e:
                        logging.warning(f"Failed to parse line: {line}. Error: {e}")
            return classifications
        except Exception as e:
            logging.error(f"Error during API request: {e}")
            if "429" in str(e):  # Rate limit error
                logging.info(f"Rate limit hit, retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e
        attempt += 1

    return {}

# Function to classify each cell in a DataFrame
def classify_dataframe(df):
    chat_session = start_chat_session()

    for column in df.columns:
        category_column = column + "_Category"
        df[category_column] = None

        for start_idx in range(2, len(df), 5):  # Start from row 2 and go in steps of 5
            batch_responses = df[column][start_idx:start_idx + 5].dropna().tolist()
            if batch_responses:
                classifications = classify_batch(batch_responses, start_idx, chat_session)
                for idx, classification in classifications.items():
                    df.at[idx, category_column] = classification

    return df

# Example usage
if __name__ == "__main__":
    # Load your DataFrame from a CSV file
    file_path = r"user_file_path\open-text_responses_dataset_[methodology].csv"
    df = pd.read_csv(file_path)

    # Process the DataFrame to categorize each response
    categorized_df = classify_dataframe(df)

    # Save the DataFrame with the categories to a new CSV file
    output_file_path = r"user_file_path\open-text_responses_dataset_[methodology]_labeled.csv"
    categorized_df.to_csv(output_file_path, index=False)

    # Print the DataFrame with the categorization results (optional)
    print(categorized_df)

# labels the rows as gibberish if they contain at least one cell with the value "gibberish"

def label_rows(df):
    # Create a new column for the row labels
    df['Gibberish interview?'] = None

    # Iterate over each row in the DataFrame
    for idx, row in df.iterrows():
        # Check if any cell in the row contains the value "gibberish"
        if 'gibberish' in row.values:
            df.at[idx, 'Gibberish interview?'] = 'gibberish'
        else:
            df.at[idx, 'Gibberish interview?'] = 'not gibberish'
    
    return df

if __name__ == "__main__":
    # Load your DataFrame from a CSV file
    file_path = r"user_file_path\open-text_responses_dataset_[methodology]_labeled.csv"
    df = pd.read_csv(file_path)

    # Label the rows based on the presence of "gibberish"
    labeled_df = label_rows(df)

    # Save the DataFrame with the row labels to a new CSV file
    output_file_path = r"user_file_path\gibberish_labeled_transcripts_[methodology].csv"
    labeled_df.to_csv(output_file_path, index=False)

    # Print the DataFrame with the row labels (optional)
    print(labeled_df)
