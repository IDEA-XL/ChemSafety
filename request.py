from openai import OpenAI

api_key = "sk-proj-k2OOmRix0W9DOuZWFqo3T3BlbkFJYWCZIJGx2PLiXAmp1nBq"
 
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

def check_answer(inputString, answer):
    response = get_openai_response("gpt-4o", f"Does the following response match the answer? (Yes/No) Model Response: {inputString}, Correct Answer:{answer}")
    return response