import openai

from src.config.openai_config import OPENAI_KEY

client = openai.OpenAI(api_key=OPENAI_KEY)


# Process client message using OpenAI's model
def process_with_openai(message):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=message,
        max_tokens=50
    )
    return response.choices[0].text.strip()
