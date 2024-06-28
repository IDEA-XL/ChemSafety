from tester import test, calcSuccessRates
import json
import os

def retrieve_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    prompts = []
    for item in data:
        question = item.get('question', 'No question found')
        prompts.append(question)
    
    return prompts

# Specify the directory
directory = 'datasets'
dataset_limit = 4 # DATASET LIMIT 4
# Iterate over all files in the specified directory
file_path = 'datasets/smiles.json' # Specify the file path
dataset_name = os.path.splitext(os.path.basename(file_path))[0] # Get the dataset name
prompts = retrieve_prompts(file_path) # Retrieve the prompts from the file
for prompt in prompts: # PROMPT LOOP
    test(prompt, dataset_name)

calcSuccessRates()