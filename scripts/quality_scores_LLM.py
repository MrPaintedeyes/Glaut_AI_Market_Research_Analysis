import os
import pandas as pd
import google.generativeai as genai
import time
import re
import logging

# Configure the Gemini API with the API key directly
genai.configure(api_key="YOUR_GEMINI_API")

# Define the generation configuration for the model
generation_config = {
    "temperature": 1,
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
                    """You are an AI tasked with evaluating survey responses based on two key metrics: adequacy of the response with respect to the question's context and depth/richness of the response. Each response should be scored on a scale from 1 to 10.

# Scoring Criteria:
1. Adequacy to Context:
Does the response directly address the question?
Does the response stay relevant and on-topic?

2. Depth/Richness:
Does the response provide detailed, thoughtful insights?
Does it show a deep understanding or exploration of the topic?

# Scoring Scale:

0 (Very Bad response: completely no sense, random letters, out of context, or inconclusive)
Example:
Question: "What are your thoughts on remote work?"
Response: "ansdkjnbwidnwid" OR "I don't know" OR "nothing" OR "anything" OR something completely out of context
Adequacy: The response is completely nonsensical and meaningless.
Depth: No depth or elaboration is provided.

1-2 (Bad Response):
Example:
Question: "What are your thoughts on remote work?"
Response: "It's fine."
Adequacy: The response is minimally relevant but fails to address the question meaningfully.
Depth: No depth or elaboration is provided.

3-4 (Medium-Low Quality Response):
Example:
Question: "What are your thoughts on remote work?"
Response: "I think remote work is good because you can work from home."
Adequacy: The response is relevant but only partially addresses the question.
Depth: The response provides a simple reason but lacks depth or specific details.

5-6 (Medium Quality Response):
Example:
Question: "What are your thoughts on remote work?"
Response: "Remote work is beneficial because it offers flexibility and saves commuting time."
Adequacy: The response adequately addresses the question.
Depth: Some reasoning is provided, but it lacks further exploration or examples.

7-8 (Medium-High Quality Response):
Example:
Question: "What are your thoughts on remote work?"
Response: "Remote work is beneficial for productivity as it allows for flexible hours and eliminates commuting. However, it can also lead to a sense of isolation if not managed well."
Adequacy: The response directly addresses the question with relevant points.
Depth: The response includes multiple aspects and acknowledges potential downsides, showing a more nuanced understanding.

9-10 (Very Good Response):
Example:
Question: "What are your thoughts on remote work?"
Response: "Remote work has significantly improved my work-life balance and productivity. The flexibility allows for a better personal schedule, and the lack of commute reduces daily stress. However, it’s essential to maintain clear communication channels to avoid isolation and ensure team cohesion. A hybrid model might be the best solution, combining the benefits of both remote and in-office work."
Adequacy: The response fully addresses the question with multiple relevant points.
Depth: The response is rich with detailed insights, acknowledging both benefits and challenges, and even suggesting a balanced approach.

# Response Format:
Score: <numeric_score>
Explanation: <brief explanation for the score>

# Example:
Question: "What are your thoughts on remote work?"
Response: "I believe remote work offers flexibility but can reduce team collaboration."

# Example Evaluation Output:
Score: 7
Explanation: The response addresses both benefits and drawbacks of remote work, showing a reasonable level of depth and understanding.

# Task:
Given these guidelines, evaluate the following survey responses accordingly.
"""
                ],
            },
            {
                "role": "model",
                "parts": [
                    "I understand. Please provide the survey responses you want me to evaluate. I will score each response based on the criteria you provided, giving a score from 1 to 10 and explaining my reasoning. \n\nI will also identify responses that are off-topic or irrelevant and assign them a score of 0. \n",
                ],
            },
        ]
    )
    return chat_session

# Function to score each response in the DataFrame

# Function to extract the numeric score and explanation from the model's response
def extract_score_from_response(response_text):
    try:
        score_match = re.search(r"Score:\s*(\d+)", response_text)

        if score_match:
            score = int(score_match.group(1))
        else:
            score = None

        return score
    except Exception as e:
        print(f"Error extracting score: {e}")
        return None

def score_responses_in_dataframe(df, question_column):
    chat_session = start_chat_session()
    score_column = question_column + "_Score"
    df[score_column] = None

    for idx, response in df[question_column].items():
        if pd.notna(response):
            user_input = f"Question: \"{question_column}\"\nResponse: \"{response}\"\nProvide your evaluation."

            attempt = 0
            max_attempts = 10
            delay = 3  # seconds

            while attempt < max_attempts:
                try:
                    model_response = chat_session.send_message(user_input)
                    response_text = model_response.text.strip()

                    # Log the response for debugging
                    logging.info(f"Index {idx} Response: {response_text}")

                    score = extract_score_from_response(response_text)

                    if score is not None:
                        df.at[idx, score_column] = score
                        break  # Exit loop on successful extraction
                    else:
                        print(f"Could not extract score for index {idx}. Retrying...")
                except Exception as e:
                    print(f"Error for index {idx}: {e}")
                    if "429" in str(e):
                        print(f"Rate limit hit, retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= 2
                        # Exponential backoff
                    else:
                        break  # Exit loop on other exceptions
                attempt += 1

            time.sleep(3)  # Base delay between requests to not

    return df, score_column  # Return the DataFrame and column names

# Example usage
if __name__ == "__main__":
    # Load your DataFrame from a CSV file
    file_path = r"C:\Users\l440\Downloads\evaluated_Glaut8.csv"
    df = pd.read_csv(file_path)

    # Specify the column name containing the questions
    question_column = "Perchè hai assegnato questo voto alle aziende che producono caffè?"

    # Process the DataFrame to score each response
    evaluated_df, score_column = score_responses_in_dataframe(df, question_column)

    # Save the DataFrame with the scores to a new CSV file
    output_file_path = r"C:\Users\l440\Downloads\evaluated_Glaut9.csv"  # Replace with the desired output file path
    evaluated_df.to_csv(output_file_path, index=False)

    # Print the DataFrame with the evaluation results (optional)
    print(evaluated_df[[question_column, score_column]])
