from datasets import Dataset
import json

data = []

with open("nelson_mandela_QA.json", "r") as f:
    data = json.load(f)

# Clean the data - flatten nested answers
cleaned_data = []
for item in data:
    question = item.get('question', '')
    answer = item.get('answer', '')
    
    # If answer is a dict, convert it to a string
    if isinstance(answer, dict):
        answer = json.dumps(answer, indent=2)
    
    # Ensure both are strings
    if isinstance(question, str) and isinstance(answer, str):
        cleaned_data.append({
            'question': question,
            'answer': answer
        })

print(f"Original data: {len(data)} items")
print(f"Cleaned data: {len(cleaned_data)} items")

dataset = Dataset.from_list(cleaned_data)

dataset.push_to_hub("takenolab/nelson_mandela_qa")