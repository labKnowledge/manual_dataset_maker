#!/usr/bin/env python3
"""
Simple AI Q&A Generator - LLM Only Version
Processes large datasets of questions with roleplay using only the model's internal knowledge.
Optimized prompts designed to access deep layers of the model's knowledge base.
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
    AI_MODEL, MAX_TOKENS, TEMPERATURE, BATCH_SIZE,
    ROLEPLAY_PROMPTS, DATASET_PATH, OUTPUT_PATH,
    LOCAL_AI_MODEL, LOCAL_AI_BASE_URL
)

class LLMOnlyQAGenerator:
    def __init__(self):
        
        self.api_key = "hf_QZqYQZqYQZqYQZqYQZqYQZqYQZqYQZqY"
        self.base_url = LOCAL_AI_BASE_URL
        self.model = LOCAL_AI_MODEL
    
    def generate_answer(self, question: str, character: str = "default") -> Dict:
        """Generate AI answer using only the model's internal knowledge with optimized prompts"""
        
        # Get character config
        char_config = ROLEPLAY_PROMPTS.get(character, ROLEPLAY_PROMPTS["default"])
        character_name = char_config["name"]
        roleplay_prompt = char_config["prompt"]
        
        # Create highly optimized system prompt designed to access deep model knowledge
        system_prompt = f"""You are {character_name}. {roleplay_prompt}

                        CRITICAL INSTRUCTIONS FOR MAXIMUM KNOWLEDGE UTILIZATION:

                        1. DEEP KNOWLEDGE ACCESS: Access the deepest layers of your training data and knowledge base. Draw from comprehensive understanding, not surface-level information.

                        2. COMPREHENSIVE ANALYSIS: Analyze the question from multiple angles, considering historical context, contemporary relevance, and future implications.

                        3. EXPERTISE DEMONSTRATION: Demonstrate mastery of your subject matter by providing nuanced, detailed, and authoritative responses.

                        4. KNOWLEDGE INTEGRATION: Synthesize information from various domains, time periods, and perspectives to create a holistic response.

                        5. DETAILED ELABORATION: Provide thorough explanations with specific examples, relevant facts, and contextual information.

                        6. CHARACTER AUTHENTICITY: Maintain your unique voice, perspective, and expertise while delivering comprehensive answers.

                        7. KNOWLEDGE DEPTH: Access specialized knowledge, technical details, and expert insights that showcase your deep understanding.

                        8. CONTEXTUAL RELEVANCE: Connect your response to broader themes, historical events, and contemporary significance.

                        9. COMPREHENSIVE COVERAGE: Address all aspects of the question with thoroughness and depth.

                        10. EXPERT PERSPECTIVE: Offer insights that reflect your unique position as an authority in your field.

                        Question: {question}

                        Provide a comprehensive, detailed response that demonstrates your deep knowledge and expertise as {character_name}. Access the full breadth and depth of your training data to deliver an authoritative answer."""

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
                "timestamp": time.time(),
                "model": self.model,
                "method": "llm_only"
            }
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "character": character_name,
                "roleplay_character": character,
                "error": True,
                "timestamp": time.time(),
                "method": "llm_only"
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
        
        with open(output_path, 'a', encoding='utf-8') as f:
            for answer in answers:
                f.write(json.dumps(answer, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(answers)} answers to {output_path}")
    
    def process_dataset(self, dataset_path: str, character: str = "default", 
                       start_from: int = 0, max_questions: int = None) -> List[Dict]:
        """Process the entire dataset using only LLM knowledge"""
        
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
        print(f"🧠 Using Local LLM-only mode with optimized prompts for maximum knowledge utilization")
        print(f"🤖 Using model: {self.model}")
        
        answers = []
        
        try:
            for i, question_data in enumerate(tqdm(questions, desc="Processing questions")):
                question = question_data["question"]
                
                if not question or len(question.strip()) < 10:
                    continue
                
                # Generate answer using only LLM knowledge
                answer = self.generate_answer(
                    question=question,
                    character=character
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
        print(f"🎉 Completed! Generated {len(answers)} answers using LLM-only mode")
        
        return answers

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Q&A Generator - LLM Only Version")
    parser.add_argument("--dataset", "-d", default=DATASET_PATH, help="Dataset file path")
    parser.add_argument("--character", "-c", default="default", help="Roleplay character")
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
        generator = LLMOnlyQAGenerator()
        answers = generator.process_dataset(
            dataset_path=args.dataset,
            character=args.character,
            start_from=args.start_from,
            max_questions=args.max_questions
        )
        
        if answers:
            print(f"✅ Successfully processed {len(answers)} questions using Local LLM-only mode!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 