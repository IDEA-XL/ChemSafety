from openai import OpenAI
from request import get_openai_response, check_answer
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import re
api_key = "sk-proj-k2OOmRix0W9DOuZWFqo3T3BlbkFJYWCZIJGx2PLiXAmp1nBq"
 
client = OpenAI(api_key=api_key)
altNum = 3
colWidth = 15
ogPrec = 3
cooldown_time = 2
models = {"gpt-3.5-turbo": 0, "gpt-4-turbo": 1, "gpt-4": 2, "gpt-4o": 3}
logprob_data = []
tokenList = []
response = ""
normsumProb = 0

def sanitize(input_string):
    # Characters considered problematic on Windows and other common filesystems
    pattern = r"[<>:\"/\\|?*]"  
    return re.sub(pattern, '_', input_string)


num_models = len(models)

def execute(model, inputString):
    global logprob_data, normsumProb
    sumProb = 0
    tokens = []
    completion = get_openai_response(model, inputString)
    print ("Model:", model)
 
    response = completion.choices[0].message.content
    print(response)

    # Calculate and Scale Probabilities
    
    tokenList.append(tokens)
    return response

def test(q_a_pair, dataset_name):
    print("Testing with ", dataset_name)
    print(q_a_pair)
    inputString = q_a_pair[0];
    plt.close()
    tokenList.clear()
    fig, axes = plt.subplots(rows, cols, figsize=(12, 6), sharex=False, sharey=True)
    fig.tight_layout()
    fig.suptitle(f"Scaled Probability Graphs for Responses (Input: {inputString})")

    # Loop through models and call execute
    for model in models:

        execute(model, inputString)
        model_index = models[model]
        #print("1st test: ", tokenList[model_index], " with model ", model_index)


    #plt.show()
    plt.pause(0.001)  # Brief, non-blocking display

    time.sleep(cooldown_time)
        