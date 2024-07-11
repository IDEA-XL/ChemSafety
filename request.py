from openai import OpenAI
from dotenv import load_dotenv
import os
import httpx
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_openai_response(model_name, inputString):
    try:
        response = client.chat.completions.create(
        model=model_name,
        messages=[ # No system prompt provided, default is used
            {"role": "user", "content": inputString}
        ],
        n = 2,
        temperature = 1,
        top_p = 1
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

claude_api_key = os.getenv("CLAUDE_API_KEY")
model_name = "claude-3-5-sonnet-20240620" # for reference
clientgpt = OpenAI(
    base_url="https://api.xty.app/v1", 
    api_key=claude_api_key,
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

def get_claude_response(model_name, inputString):
  completion = clientgpt.chat.completions.create(
    model=model_name,
    messages=[ # No system prompt provided, default is used
      {"role": "user", "content": inputString}
    ]
  )
  
  return completion

llama_api_key=os.getenv("LLAMA_API_KEY")
clientLlama = OpenAI(
    base_url = 'http://192.168.81.67:11434/v1',
    api_key = llama_api_key, # required, but unused
)
def get_llama_response(model_name, inputString):
    response = clientLlama.chat.completions.create(
        model = model_name,
        messages=[
            {"role": "user", "content": inputString}
        ]
    )
    return response

ds_api_key=os.getenv("DS_API_KEY")
client = OpenAI(api_key=ds_api_key, base_url="https://api.deepseek.com")

def get_deepseek_response(inputString):
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        #{"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": inputString}
    ],
    stream=False
    )
    return response.choices[0].message.content
