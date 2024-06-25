from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")  # Replace "API_KEY" with the actual name of the environment variable
client = OpenAI(api_key=api_key)

def get_openai_response(model_name, inputString):
    response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": inputString}
    ],
    n = 2,
    temperature = 1,
    top_p = 1
    )
    return response