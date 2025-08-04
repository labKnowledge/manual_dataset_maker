#!/usr/bin/env python3
"""
Script to clean the All_Answers.jsonl file and extract only question and answer pairs.
"""

import json
import os

def clean_data(input_file, output_file):
    """
    Clean the data by extracting only question and answer pairs.
    
    Args:
        input_file (str): Path to the input JSONL file
        output_file (str): Path to the output JSONL file
    """
    cleaned_data = []
    
    print(f"Reading data from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # Parse each JSON line
                data = json.loads(line.strip())
                
                # Extract only question and answer
                if 'question' in data and 'answer' in data:
                    cleaned_item = {
                        "question": data['question'],
                        "answer": data['answer']
                    }
                    cleaned_data.append(cleaned_item)
                else:
                    print(f"Warning: Line {line_num} missing question or answer field")
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    print(f"Processed {len(cleaned_data)} valid question-answer pairs")
    
    # Write cleaned data to output file
    print(f"Writing cleaned data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in cleaned_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"Successfully created {output_file} with {len(cleaned_data)} entries")
    
    # Also create a JSON array version if needed
    json_array_file = output_file.replace('.jsonl', '.json')
    print(f"Creating JSON array version: {json_array_file}")
    with open(json_array_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully created {json_array_file}")

def main():
    input_file = "output/All_Answers.jsonl"
    output_file = "nelson_mandela_QA.jsonl"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found!")
        return
    
    # Clean the data
    clean_data(input_file, output_file)
    
    # Show some statistics
    print("\n" + "="*50)
    print("CLEANING COMPLETE")
    print("="*50)
    
    # Count lines in original and cleaned files
    with open(input_file, 'r') as f:
        original_lines = sum(1 for _ in f)
    
    with open(output_file, 'r') as f:
        cleaned_lines = sum(1 for _ in f)
    
    print(f"Original file: {original_lines} lines")
    print(f"Cleaned file: {cleaned_lines} lines")
    print(f"Files created:")
    print(f"  - {output_file} (JSONL format)")
    print(f"  - {output_file.replace('.jsonl', '.json')} (JSON array format)")

if __name__ == "__main__":
    main() 