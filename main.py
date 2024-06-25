from tester import test
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

def test_with(file_path):
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    prompts = retrieve_prompts(file_path)
    for prompt in prompts:
        test(prompt, dataset_name)

# Specify the directory
directory = 'datasets'

# Iterate over all files in the specified directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):  # Check if it's a file
        test_with(file_path)