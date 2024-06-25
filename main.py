from tester import test
import json
import os

def retrieve_q_a_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    q_a_pairs = []
    for item in data:
        question = item.get('question', 'No question found')
        correct_answer = item.get('correct_answer', 'No correct answer found')
        q_a_pairs.append((question, correct_answer))
    
    return q_a_pairs

#interactive()
def test_with(file_path):
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    q_a_pairs = retrieve_q_a_pairs(file_path)
    for q_a_pair in q_a_pairs:
        test(q_a_pair, dataset_name)

# Specify the directory
directory = 'datasets'

# Iterate over all files in the specified directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):  # Check if it's a file
        test_with(file_path)
        # Add your file processing code here