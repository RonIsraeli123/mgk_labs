import openai

from src.config.config import OPENAI_KEY

openai.api_key = OPENAI_KEY


# Process client message using OpenAI's model
def process_with_openai(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=50
    )
    return response.choices[0].text.strip()
