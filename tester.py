from openai import OpenAI
from request import get_openai_response, check_answer
from grader import grade_attack
import time
import os
import re
api_key = "sk-proj-k2OOmRix0W9DOuZWFqo3T3BlbkFJYWCZIJGx2PLiXAmp1nBq"

client = OpenAI(api_key=api_key)

cooldown_time = 2
models = {"gpt-4o": 0}
tokenList = []
response = ""

def sanitize(input_string):
    # Characters considered problematic on Windows and other common filesystems
    pattern = r"[<>:\"/\\|?*]"  
    return re.sub(pattern, '_', input_string)


num_models = len(models)

def execute(model, inputString):
    completion = get_openai_response(model, inputString)
    print ("Model:", model)
    response = completion.choices[0].message.content
    return response

def test(q_a, dataset_name):
    print("Testing with ", dataset_name)
    print(q_a)
    inputString = q_a[0];

    # Loop through models and call execute
    for model in models:
        response = execute(model, inputString)
        compo, proc = grade_attack(inputString, response)
        print(f"Input String: {inputString}")
        print(f"Response: {response}")
        print(f"Grader Results: {compo}, {proc}")
    time.sleep(cooldown_time)
        