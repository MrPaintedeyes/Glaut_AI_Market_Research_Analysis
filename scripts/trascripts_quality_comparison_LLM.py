import os
import pandas as pd
import google.generativeai as genai
import logging
import time
import random  # Import random for swapping

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure the Gemini API with the API key
genai.configure(api_key="YOUR_API_KEY")

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
def start_chat_session(transcript1, transcript2):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"""You are an AI tasked with evaluating survey transcripts based on two three metrics: adequacy of the response with respect to the questions' context and depth of the responses, and the engagement level of the respondent.

# Selection criteria:
1. Adequacy to Context:
Which transcript addresses better the questions?

2. Depth/Richness:
Which transcript shows a deeper understanding or exploration of the topic?

3. Engagement level:
Which transcript contains the most engaged respondent? Look for enthusiasm, detailed examples, or elaborations.

# Task:
Compare the following two transcripts and select the better one based on the criteria mentioned above. 

# Responses:
Transcript 1: '{transcript1}'
Transcript 2: '{transcript2}'

# Expected Output Format:
Please respond with the better response source only in the following format:
"Selected: Transcript 1" or "Selected: Transcript 2"
"""
                ],
            },  
            {
                "role": "model",
                "parts": [
                    "Please provide me with the Transcript 1 and Transcript 2 so I can evaluate them and select the better transcript based on your evaluation criteria. \n",
                ],
            },
        ]
    )
    return chat_session

def compare_transcripts(transcript1, transcript2):
    
    should_swap = random.choice([True, False])
    if should_swap:
        transcript1, transcript2 = transcript2, transcript1
    
    prompt = f"""You are an AI tasked with evaluating survey transcripts based on two key metrics: adequacy of the response with respect to the questions' context and depth/richness of the responses, and the engagement level of the respondent.


# Selection criteria:
1. Adequacy to Context:
Which transcript addresses better the questions, providing answers that are meaningful with respect to the question context?
Which transcript contains less non-sensical answers? (Consider non-sensical answers embedding random characters or out-of-context meanings)
When you consider there is not a better transcript for this criteria, specify that the transcripts draw.

2. Depth:
Which transcript shows a deeper understanding or exploration of the topic?
Which transcript yelds more singular and distinct piece of informations?
When you consider there is not a better transcript for this criteria, specify that the transcripts draw.

3. Cheaters:
Which transcript contains less serial answers? Consider cheating serial answers the set of responses containing the same wording or fundamental meaning for multiple times in a row (for example, cheater transcripts contains multiple sequential answers in the form: "Non saprei", "Niente", "Nessuno")
Do not penalize transcripts just because they contain one isolated answer in the form: "Nessuno", "Niente", "Non saprei", because it's legitimate to consider that respondent might not have a specific answer for the question. Penalize this behaviour only when it is serial.
Which transcript contains does not contain serial cheating answers in the above cited form?
When you consider there is not a better transcript for this criteria, specify that the transcripts draw.

# Task:
Compare the following two transcripts and select the better one based on the criteria mentioned above.
When you consider there is not an overall better transcript with respect to the mentioned criteria, specify that the transcripts draw.

# Responses:
Transcript 1: '{transcript1}'
Transcript 2: '{transcript2}'

# Expected Output Format:
Please respond giving explanation of your choice and transmitting the winner transcript only in the following format:
"Selected: Transcript 1" if Transcript 1 was better or "Selected: Transcript 2" if Transcript 2 was better.
If the transcripts draw, trasmit the output in the following format: "Selected: Draw".
"""
    
    chat_session = start_chat_session(transcript1, transcript2)
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
            if "Selected: Transcript 1" in response_text:
                return "0" if should_swap else "1"
            elif "Selected: Transcript 2" in response_text:
                return "1" if should_swap else "0"
            elif "Selected: Draw":
                return "draw"
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

# Load dataframes from CSV
file_path_glaut = Glaut_transcripts_dataframe_file_path
file_path_typeform = Typeform_transcripts_dataframe_file_path

df_glaut = pd.read_csv(file_path_glaut)
df_typeform = pd.read_csv(file_path_typeform)

# Ensure both dataframes have the same structure: "Transcripts", "word_count", "rank"
if not all(col in df_glaut.columns for col in ["Transcripts", "word_count", "rank"]) or \
   not all(col in df_typeform.columns for col in ["Transcripts", "word_count", "rank"]):
    raise ValueError("Both dataframes must contain the columns: 'Transcripts', 'word_count', and 'rank'.")

# Initialize a new column in the Glaut dataframe to store the comparison results
df_glaut['Comparison_Result'] = None

# Iterate over the ranks and compare transcripts
for rank in df_glaut['rank'].unique():
    # Get the corresponding transcripts for the current rank from both dataframes
    transcript1 = df_glaut[df_glaut['rank'] == rank]['Transcripts'].values[0]
    transcript2 = df_typeform[df_typeform['rank'] == rank]['Transcripts'].values[0]

    # Compare the transcripts using the Gemini LLM
    result = compare_transcripts(transcript1, transcript2)

    # Update the comparison result in the Glaut dataframe for the matching rank
    df_glaut.loc[df_glaut['rank'] == rank, 'Comparison_Result'] = result

# Save the updated Glaut dataframe with the comparison results to a CSV
output_file_path = user_output_file_path
df_glaut.to_csv(output_file_path, index=False)

print("Comparison complete. Results saved to:", output_file_path)
