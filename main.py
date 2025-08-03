#!/usr/bin/env python3
"""
Simple AI Q&A Generator with Google Custom Search
Processes large datasets of questions with roleplay and search integration.
"""

import requests
import pandas as pd
import json
import time
import os
from tqdm import tqdm
from typing import List, Dict
from config import (
    QWEN_AI_KEY, QWEN_AI_BASE_URL, QWEN_AI_MODEL,
    GOOGLE_CSE_API_KEY, GOOGLE_CSE_ID,
    AI_MODEL, MAX_TOKENS, TEMPERATURE, BATCH_SIZE,
    ROLEPLAY_PROMPTS, DATASET_PATH, OUTPUT_PATH
)

class SimpleQAGenerator:
    def __init__(self):
        if not QWEN_AI_KEY:
            raise ValueError("QWEN_AI_KEY required. Set QWEN_AI_KEY in .env file")
        
        self.api_key = QWEN_AI_KEY
        self.base_url = QWEN_AI_BASE_URL
        self.model = QWEN_AI_MODEL
    
    def google_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using Google Custom Search API"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_CSE_API_KEY,
                'cx': GOOGLE_CSE_ID,
                'q': query,
                'num': min(max_results, 10)  # Google CSE max is 10
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'items' in data:
                for item in data['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'snippet': item.get('snippet', ''),
                        'url': item.get('link', ''),
                        'source': 'google_cse'
                    })
            
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def generate_answer(self, question: str, character: str = "default", include_search: bool = True) -> Dict:
        """Generate AI answer with optional search integration using Qwen AI"""
        
        # Get character config
        char_config = ROLEPLAY_PROMPTS.get(character, ROLEPLAY_PROMPTS["default"])
        character_name = char_config["name"]
        roleplay_prompt = char_config["prompt"]
        
        # Search for context
        search_context = ""
        search_results = []
        
        if include_search:
            search_results = self.google_search(question, max_results=5)
            
            if search_results:
                search_context = "\n\nRelevant research findings:\n"
                for i, result in enumerate(search_results[:3], 1):
                    search_context += f"{i}. {result['title']}\n"
                    search_context += f"   {result['snippet'][:200]}...\n\n"
        
        # Create system prompt
        system_prompt = f"""You are {character_name}. {roleplay_prompt}

Your task is to answer the following question while maintaining your character's voice and expertise.
Use the provided research context to enhance your response with factual accuracy.

{search_context}

Question: {question}

Provide your response as {character_name}:"""

        # Generate response using Qwen AI
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt}
                ],
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            answer = data['choices'][0]['message']['content'].strip()
            
            return {
                "question": question,
                "answer": answer,
                "character": character_name,
                "roleplay_character": character,
                "search_results": search_results,
                "timestamp": time.time(),
                "model": self.model
            }
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "character": character_name,
                "roleplay_character": character,
                "error": True,
                "timestamp": time.time()
            }
    
    def load_dataset(self, file_path: str) -> List[Dict]:
        """Load dataset from various formats"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext == 'csv':
            df = pd.read_csv(file_path)
            # Find question column
            question_col = None
            for col in ['question', 'Question', 'text', 'Text', 'content', 'Content']:
                if col in df.columns:
                    question_col = col
                    break
            
            if not question_col:
                raise ValueError("No question column found in CSV")
            
            questions = []
            for idx, row in df.iterrows():
                questions.append({
                    "id": idx,
                    "question": str(row[question_col]).strip()
                })
            
            return questions
        
        elif file_ext == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return [{"id": i, "question": str(item.get("question", item))} for i, item in enumerate(data)]
            else:
                return [{"id": k, "question": str(v)} for k, v in data.items()]
        
        elif file_ext == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            return [{"id": i, "question": line.strip()} for i, line in enumerate(lines) if line.strip()]
        
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def save_answers(self, answers: List[Dict], output_path: str):
        """Save answers to JSONL file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for answer in answers:
                f.write(json.dumps(answer, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(answers)} answers to {output_path}")
    
    def process_dataset(self, dataset_path: str, character: str = "default", 
                       start_from: int = 0, max_questions: int = None,
                       include_search: bool = True) -> List[Dict]:
        """Process the entire dataset"""
        
        print(f"🚀 Loading dataset: {dataset_path}")
        questions = self.load_dataset(dataset_path)
        
        # Apply limits
        if start_from > 0:
            questions = questions[start_from:]
            print(f"⏭️ Starting from question {start_from}")
        
        if max_questions:
            questions = questions[:max_questions]
            print(f"📏 Processing maximum {max_questions} questions")
        
        print(f"📊 Processing {len(questions)} questions as {ROLEPLAY_PROMPTS[character]['name']}")
        print(f"🔍 Search enabled: {include_search}")
        print(f"🤖 Using model: {self.model}")
        
        answers = []
        
        try:
            for i, question_data in enumerate(tqdm(questions, desc="Processing questions")):
                question = question_data["question"]
                
                if not question or len(question.strip()) < 10:
                    continue
                
                # Generate answer
                answer = self.generate_answer(
                    question=question,
                    character=character,
                    include_search=include_search
                )
                
                # Add question ID
                answer["question_id"] = question_data.get("id", i)
                
                answers.append(answer)
                
                # Save progress every 50 questions
                if (i + 1) % 50 == 0:
                    temp_path = f"{OUTPUT_PATH}.temp"
                    self.save_answers(answers, temp_path)
                    print(f"💾 Progress saved: {i + 1}/{len(questions)} questions")
                
                # Rate limiting
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")
            if answers:
                self.save_answers(answers, f"{OUTPUT_PATH}.interrupted")
            return answers
        
        # Save final results
        self.save_answers(answers, OUTPUT_PATH)
        print(f"🎉 Completed! Generated {len(answers)} answers")
        
        return answers

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Q&A Generator with Google Search")
    parser.add_argument("--dataset", "-d", default=DATASET_PATH, help="Dataset file path")
    parser.add_argument("--character", "-c", default="default", help="Roleplay character")
    parser.add_argument("--no-search", action="store_true", help="Disable search")
    parser.add_argument("--start-from", type=int, default=0, help="Start from question number")
    parser.add_argument("--max-questions", type=int, help="Maximum questions to process")
    parser.add_argument("--list-characters", action="store_true", help="List available characters")
    
    args = parser.parse_args()
    
    # List characters
    if args.list_characters:
        print("🎭 Available characters:")
        for key, config in ROLEPLAY_PROMPTS.items():
            print(f"   {key}: {config['name']}")
        return
    
    # Validate character
    if args.character not in ROLEPLAY_PROMPTS:
        print(f"❌ Invalid character: {args.character}")
        print(f"Available: {', '.join(ROLEPLAY_PROMPTS.keys())}")
        return
    
    # Process dataset
    try:
        generator = SimpleQAGenerator()
        answers = generator.process_dataset(
            dataset_path=args.dataset,
            character=args.character,
            start_from=args.start_from,
            max_questions=args.max_questions,
            include_search=not args.no_search
        )
        
        if answers:
            print(f"✅ Successfully processed {len(answers)} questions!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 