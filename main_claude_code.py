#!/usr/bin/env python3
"""
Simple AI Q&A Generator - Claude Code SDK Version
Processes large datasets of questions with roleplay using Claude Code SDK.
Uses the official Claude Code SDK for agentic capabilities.
"""

import pandas as pd
import json
import time
import os
import anyio
import asyncio
from tqdm import tqdm
from typing import List, Dict
from pathlib import Path
from claude_code_sdk import query, ClaudeCodeOptions, Message
from config import (
    ANTHROPIC_API_KEY, AI_MODEL, MAX_TOKENS, TEMPERATURE, BATCH_SIZE,
    ROLEPLAY_PROMPTS, DATASET_PATH, OUTPUT_PATH
)

class ClaudeCodeQAGenerator:
    def __init__(self):
        self.model = AI_MODEL
    
    async def generate_answer(self, question: str, character: str = "default") -> Dict:
        """Generate AI answer using Claude Code SDK"""
        
        # Get character config
        char_config = ROLEPLAY_PROMPTS.get(character, ROLEPLAY_PROMPTS["default"])
        character_name = char_config["name"]
        roleplay_prompt = char_config["prompt"]
        
        # Create system prompt for Claude Code
        system_prompt = f"""You are {character_name}. {roleplay_prompt}

You have access to Claude Code's full agentic capabilities including:
- Web search for current information
- Code execution for calculations
- File reading for reference materials
- Tool use for enhanced reasoning

Use these capabilities as needed to provide the most comprehensive and accurate answer possible.

When answering:
1. Think step by step about what information would be most helpful
2. Use web search if you need current or specific information
3. Use code execution for any calculations or data analysis
4. Maintain your character's voice and expertise
5. Provide detailed, well-reasoned responses

Please provide a comprehensive answer as {character_name}, using your capabilities as needed."""

        # Configure Claude Code options
        options = ClaudeCodeOptions(
            max_turns=3,  # Allow multiple turns for complex reasoning
            system_prompt=system_prompt,
            cwd=Path("."),  # Set working directory
            allowed_tools=["Read", "Write", "Bash"],  # Allow code execution
            permission_mode="acceptEdits"  # Allow Claude to make edits and use tools
        )

        # Generate response using Claude Code SDK
        try:
            messages: list[Message] = []
            result_text = ""
            session_id = None
            
            # Use Claude Code SDK to process the question
            async for message in query(
                prompt=f"Answer as {character_name}. conversational style. clear and concise. Use web search if needed. output is json: ```question: {question}```",
                options=options
            ):
                messages.append(message)
                
                # Extract session ID from system message
                if hasattr(message, 'type') and message.type == "system" and hasattr(message, 'subtype') and message.subtype == "init":
                    session_id = message.session_id
                
                # Extract the final result using the proven method from test file
                if type(message).__name__ == "ResultMessage":
                    result = getattr(message, "result", None)
                    if result:
                        # Extract JSON from the result using regex
                        import re
                        match = re.search(r"```json\s*(\{.*?\})\s*```", result, re.DOTALL)
                        if match:
                            json_text = match.group(1)
                            try:
                                # Parse the JSON and extract just the answer
                                json_data = json.loads(json_text)
                                result_text = json_data.get("answer", json_text)
                            except json.JSONDecodeError:
                                result_text = json_text
                        else:
                            # If no JSON block found, use the full result
                            result_text = result
                        break
            
            # Print progress
            if result_text:
                print(f"✅ Generated answer for: {question[:50]}...")
            else:
                print(f"⚠️ No answer extracted for: {question[:50]}...")
            
            return {
                "question": question,
                "answer": result_text,
                "character": character_name,
                "roleplay_character": character,
                "timestamp": time.time(),
                "model": "claude-code",
                "method": "claude_code_sdk",
                "num_turns": len([m for m in messages if hasattr(m, 'type') and m.type in ["user", "assistant"]]),
                "session_id": session_id,
                "total_cost_usd": getattr(messages[-1], 'total_cost_usd', None) if messages else None,
                "duration_ms": getattr(messages[-1], 'duration_ms', None) if messages else None
            }
            
        except Exception as e:
            print(f"❌ Error processing question: {str(e)}")
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "character": character_name,
                "roleplay_character": character,
                "error": True,
                "timestamp": time.time(),
                "method": "claude_code_sdk"
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
    
    async def process_dataset_async(self, dataset_path: str, character: str = "default", 
                                   start_from: int = 0, max_questions: int = None) -> List[Dict]:
        """Process the entire dataset using Claude Code SDK"""
        
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
        print(f"🧠 Using Claude Code SDK with agentic capabilities")
        print(f"🤖 Using model: {self.model}")
        
        answers = []
        
        try:
            for i, question_data in enumerate(tqdm(questions, desc="Processing questions")):
                question = question_data["question"]
                
                if not question or len(question.strip()) < 10:
                    continue
                
                # Generate answer using Claude Code SDK
                answer = await self.generate_answer(
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
                await anyio.sleep(2)  # Rate limiting for Claude Code
        
        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")
            if answers:
                self.save_answers(answers, f"{OUTPUT_PATH}.interrupted")
            return answers
        
        # Save final results
        self.save_answers(answers, OUTPUT_PATH)
        print(f"🎉 Completed! Generated {len(answers)} answers using Claude Code SDK")
        
        return answers
    
    def process_dataset(self, dataset_path: str, character: str = "default", 
                       start_from: int = 0, max_questions: int = None) -> List[Dict]:
        """Synchronous wrapper for async processing"""
        return asyncio.run(self.process_dataset_async(
            dataset_path=dataset_path,
            character=character,
            start_from=start_from,
            max_questions=max_questions
        ))

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Q&A Generator - Claude Code SDK Version")
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
        generator = ClaudeCodeQAGenerator()
        answers = generator.process_dataset(
            dataset_path=args.dataset,
            character=args.character,
            start_from=args.start_from,
            max_questions=args.max_questions
        )
        
        if answers:
            print(f"✅ Successfully processed {len(answers)} questions using Claude Code SDK!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 