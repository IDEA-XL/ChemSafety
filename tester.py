from openai import OpenAI
from request import get_openai_response
from grader import grade_attack, long_grade
import time
import os
import re
import json
#import tiktoken
#enc = tiktoken.get_encoding("o200k_base")
cooldown_time = 2
models = {"gpt-4o": 0}
tokenList = []
attack_results = {}
success_rates = {}
response = ""
testNum = 0
class_limit = 2
substance_limit = 2

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
    completion = get_openai_response(model, inputString)
    print ("Model:", model)
    response = completion.choices[0].message.content
    return response

def test(prompt, dataset):
    print("Testing with ", dataset)

    # Loop through models and call execute
    substances = getSub();
    class_rem  = class_limit # Initial limit set
    for substance_class in substances: # SUBSTANCE CLASS LOOP
        if (class_rem == 0): # Check if the limit has been reached
            break
        class_rem -= 1
        substance_rem  = substance_limit # Initial substance limit set
        print("Class:", substance_class)
        # Iterate over each substance in the class
        for substance in substances[substance_class]: # SUBSTANCE NAME LOOP
            if (substance_rem == 0): # Check if the limit has been reached
                break
            substance_rem -= 1
            print("Substance:", substance['Name'])
            if (dataset == 'smiles'):
                substance_name = substance['SMILES']
            else:
                substance_name = substance['Name']
                
            inputString = prompt.replace("{substance}", substance_name)

            for model in models: # MODEL LOOP
                global testNum
                testNum += 1
                print("Test Num:", testNum)
    

                response = execute(model, inputString)
                compo, proc = grade_attack(inputString, response, substance)
                print(f"Input String: {inputString}")
                print(f"Response: {response}")
                print(f"Grader Results: Compo={compo}, Proc={proc}")
                print('---------------------------------')

                # Update the attack_results dictionary
                if dataset not in attack_results:
                    attack_results[dataset] = {'compo': {'success': 0, 'fail': 0}, 'proc': {'success': 0, 'fail': 0}}
                
                if compo.lower() == 'yes':
                    attack_results[dataset]['compo']['success'] += 1
                else:
                    attack_results[dataset]['compo']['fail'] += 1
                if proc.lower() == 'yes':
                    attack_results[dataset]['proc']['success'] += 1
                else:
                    attack_results[dataset]['proc']['fail'] += 1           
    time.sleep(cooldown_time)

def calcSuccessRates():
    for dataset in attack_results:
        success_rates[dataset] = {
            'compo': {
                'success_rate': attack_results[dataset]['compo']['success'] / (attack_results[dataset]['compo']['success'] + attack_results[dataset]['compo']['fail'])
            },
            'proc': {
                'success_rate': attack_results[dataset]['proc']['success'] / (attack_results[dataset]['proc']['success'] + attack_results[dataset]['proc']['fail'])
            }
        }

    for dataset in success_rates:
        print(f"Dataset: {dataset}")
        print(f"Component Success Rate: {success_rates[dataset]['compo']['success_rate'] * 100}%")
        print(f"Process Success Rate: {success_rates[dataset]['proc']['success_rate'] * 100}%")
        print('---------------------------------')