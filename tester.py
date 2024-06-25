from openai import OpenAI
from request import get_openai_response
from grader import grade_attack
from tally import addSum
import time
import os
import re
import json

cooldown_time = 2
models = {"gpt-4o": 0}
tokenList = []
response = ""
def sanitize(input_string):
    # Characters considered problematic on Windows and other common filesystems
    pattern = r"[<>:\"/\\|?*]"  
    return re.sub(pattern, '_', input_string)

def getSub():
    with open('substances.json', 'r') as file:
        data = json.load(file)
    return data

num_models = len(models)

def execute(model, inputString):
    addSum()
    completion = get_openai_response(model, inputString)
    print ("Model:", model)
    response = completion.choices[0].message.content
    return response

def test(prompt, dataset_name):
    print("Testing with ", dataset_name)

    # Loop through models and call execute
    substances = getSub();
    for substance_class in substances: # SUBSTANCE CLASS LOOP
        print("Class:", substance_class)
        # Iterate over each substance in the class
        for substance in substances[substance_class]: # SUBSTANCE NAME LOOP
            print("Substance:", substance['Name'])
            if (dataset_name == 'smiles'):
                substance_name = substance['SMILES']
            else:
                substance_name = substance['Name']
                
            inputString = prompt.replace("{substance}", substance_name)

            for model in models: # MODEL LOOP
                response = execute(model, inputString)
                compo, proc = grade_attack(inputString, response)
                print(f"Input String: {inputString}")
                print(f"Response: {response}")
                print(f"Grader Results: Compo={compo}, Proc={proc}")
                print('---------------------------------')
    time.sleep(cooldown_time)
        