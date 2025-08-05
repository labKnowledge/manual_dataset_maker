#!/usr/bin/env python3
"""
AI Question Generator - LLM Only Version
Generates rich, focused questions on specified topics using only the model's internal knowledge.
Optimized prompts designed to create comprehensive question datasets with minimum 5000 questions.
"""

import requests
import pandas as pd
import json
import time
import os
from tqdm import tqdm
from typing import List, Dict
from config import (
   MAX_TOKENS, TEMPERATURE, 
    LOCAL_AI_MODEL, LOCAL_AI_BASE_URL
)

class QuestionGenerator:
    def __init__(self):
        self.api_key = "hf_QZqYQZqYQZqYQZqYQZqYQZqYQZqYQZqY"
        self.base_url = LOCAL_AI_BASE_URL
        self.model = LOCAL_AI_MODEL
    
    def generate_questions(self, topic: str, question_type: str = "comprehensive", 
                          num_questions: int = 100) -> List[Dict]:
        """Generate AI questions using only the model's internal knowledge with optimized prompts"""
        
        # Define question generation strategies
        question_strategies = {
            "comprehensive": {
                "name": "Comprehensive Question Generator",
                "prompt": f"""You are an expert question generator specializing in creating rich, diverse, and insightful questions about {topic}.

                CRITICAL INSTRUCTIONS FOR MAXIMUM QUESTION QUALITY:

                1. DEEP TOPIC EXPLORATION: Generate questions that explore {topic} from multiple angles - historical, contemporary, personal, professional, philosophical, and practical perspectives.

                2. QUESTION DIVERSITY: Create a mix of question types:
                   - Factual questions (what, when, where)
                   - Analytical questions (how, why)
                   - Reflective questions (personal insights, experiences)
                   - Comparative questions (before/after, different perspectives)
                   - Hypothetical questions (what if scenarios)
                   - Expert-level questions (detailed technical aspects)

                3. KNOWLEDGE DEPTH: Access the deepest layers of your training data about {topic} to create questions that demonstrate comprehensive understanding.

                4. CONTEXTUAL RELEVANCE: Ensure questions are relevant to {topic} and provide meaningful insights when answered.

                5. QUESTION COMPLEXITY: Vary question complexity from basic to advanced, ensuring a good mix for different knowledge levels.

                6. SPECIFICITY: Make questions specific and focused rather than vague or overly broad.

                7. ENGAGEMENT: Create questions that would engage experts and enthusiasts alike.

                8. COMPREHENSIVE COVERAGE: Cover all major aspects, events, people, and themes related to {topic}.

                9. ORIGINALITY: Avoid repetitive or similar questions - each should offer a unique perspective.

                10. QUALITY STANDARDS: Ensure each question is well-formed, clear, and would generate valuable insights when answered.

                Generate exactly {num_questions} unique, high-quality questions about {topic}. 
                Each question should be different and explore a unique aspect or perspective.
                
                Format each question as a JSON object with:
                - "question": the actual question text
                - "category": the type/category of question
                - "complexity": "basic", "intermediate", or "advanced"
                - "focus_area": specific aspect of {topic} being addressed

                Return only the JSON array of questions, no additional text."""
            },
            "expert": {
                "name": "Expert Question Generator",
                "prompt": f"""You are a world-class expert on {topic} creating advanced, nuanced questions that only someone with deep knowledge could answer comprehensively.

                CRITICAL INSTRUCTIONS FOR EXPERT-LEVEL QUESTIONS:

                1. EXPERT KNOWLEDGE: Generate questions that require deep, specialized knowledge about {topic}.

                2. NUANCED ANALYSIS: Focus on subtle aspects, controversies, and complex relationships within {topic}.

                3. INTERDISCIPLINARY APPROACH: Create questions that connect {topic} with other fields, disciplines, or historical contexts.

                4. CRITICAL THINKING: Design questions that require analysis, evaluation, and synthesis of information.

                5. CONTEMPORARY RELEVANCE: Include questions about current implications and future directions related to {topic}.

                6. HISTORICAL DEPTH: Explore historical contexts, evolution, and long-term impacts.

                7. COMPARATIVE PERSPECTIVES: Generate questions that compare different aspects, periods, or viewpoints within {topic}.

                8. METHODOLOGICAL FOCUS: Include questions about approaches, methods, and processes related to {topic}.

                9. ETHICAL DIMENSIONS: Address moral, ethical, and philosophical aspects of {topic}.

                10. PRACTICAL APPLICATIONS: Create questions about real-world applications and implications.

                Generate exactly {num_questions} expert-level questions about {topic}.
                Each question should demonstrate deep understanding and require sophisticated analysis to answer.

                Format each question as a JSON object with:
                - "question": the expert-level question
                - "category": specialized category
                - "complexity": "advanced"
                - "focus_area": specific expert aspect being addressed

                Return only the JSON array of questions, no additional text."""
            },
            "personal": {
                "name": "Personal Reflection Question Generator",
                "prompt": f"""You are creating deeply personal and reflective questions about {topic} that encourage introspection and personal connection.

                CRITICAL INSTRUCTIONS FOR PERSONAL QUESTIONS:

                1. EMOTIONAL CONNECTION: Generate questions that connect {topic} to personal experiences, emotions, and values.

                2. SELF-REFLECTION: Create questions that encourage deep introspection about one's relationship to {topic}.

                3. LIFE EXPERIENCES: Design questions that relate {topic} to personal life events, decisions, and growth.

                4. VALUES AND BELIEFS: Explore how {topic} relates to personal values, beliefs, and worldviews.

                5. FUTURE IMPLICATIONS: Ask about personal hopes, fears, and aspirations related to {topic}.

                6. RELATIONSHIP IMPACT: Consider how {topic} affects relationships with others and society.

                7. PERSONAL GROWTH: Create questions about learning, development, and transformation through {topic}.

                8. MEANING AND PURPOSE: Explore questions about finding meaning and purpose through {topic}.

                9. CHALLENGES AND STRUGGLES: Address personal challenges and difficulties related to {topic}.

                10. INSPIRATION AND MOTIVATION: Generate questions that inspire and motivate deeper engagement with {topic}.

                Generate exactly {num_questions} personal, reflective questions about {topic}.
                Each question should encourage deep personal connection and introspection.

                Format each question as a JSON object with:
                - "question": the personal reflection question
                - "category": "personal_reflection"
                - "complexity": "introspective"
                - "focus_area": personal aspect being explored

                Return only the JSON array of questions, no additional text."""
            }
        }
        
        # Get strategy config
        strategy_config = question_strategies.get(question_type, question_strategies["comprehensive"])
        strategy_name = strategy_config["name"]
        system_prompt = strategy_config["prompt"]
        
        # Generate questions using Local AI
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
                "max_tokens": MAX_TOKENS * 2,  # More tokens for question generation
                "temperature": TEMPERATURE + 0.1  # Slightly higher creativity
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120  # Longer timeout for question generation
            )
            response.raise_for_status()
            
            data = response.json()
            content = data['choices'][0]['message']['content'].strip()
            
            # Parse JSON response
            try:
                questions = json.loads(content)
                if isinstance(questions, list):
                    return questions
                else:
                    raise ValueError("Response is not a list")
            except json.JSONDecodeError:
                # Fallback: try to extract questions from text
                questions = self._extract_questions_from_text(content, topic, num_questions)
                return questions
            
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            # Fallback: generate basic questions
            return self._generate_fallback_questions(topic, num_questions)
    
    def _extract_questions_from_text(self, text: str, topic: str, num_questions: int) -> List[Dict]:
        """Extract questions from text response if JSON parsing fails"""
        questions = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('?' in line or line.startswith('"question"')):
                # Try to extract question from various formats
                if '"question"' in line:
                    try:
                        # Extract from JSON-like format
                        start = line.find('"question"') + 11
                        end = line.find('"', start)
                        if end == -1:
                            end = line.find(',', start)
                        if end == -1:
                            end = len(line)
                        question_text = line[start:end].strip('"')
                    except:
                        continue
                else:
                    question_text = line.strip('"')
                
                if question_text and len(question_text) > 10:
                    questions.append({
                        "question": question_text,
                        "category": "extracted",
                        "complexity": "intermediate",
                        "focus_area": topic
                    })
                
                if len(questions) >= num_questions:
                    break
        
        return questions
    
    def _generate_fallback_questions(self, topic: str, num_questions: int) -> List[Dict]:
        """Generate basic questions as fallback"""
        questions = []
        question_templates = [
            f"What are the key principles of {topic}?",
            f"How did {topic} evolve over time?",
            f"What impact has {topic} had on society?",
            f"What are the main challenges in {topic}?",
            f"How does {topic} relate to current events?",
            f"What are the different perspectives on {topic}?",
            f"How has {topic} influenced other fields?",
            f"What are the future implications of {topic}?",
            f"What role does {topic} play in education?",
            f"How can {topic} be applied in practice?"
        ]
        
        for i in range(num_questions):
            template = question_templates[i % len(question_templates)]
            questions.append({
                "question": template,
                "category": "fallback",
                "complexity": "basic",
                "focus_area": topic
            })
        
        return questions
    
    def save_questions(self, questions: List[Dict], output_path: str):
        """Save questions to JSONL file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'a', encoding='utf-8') as f:
            for question in questions:
                f.write(json.dumps(question, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(questions)} questions to {output_path}")
    
    def generate_multi_type_dataset(self, topic: str, question_types: List[str], 
                                   target_count: int = 5000, output_path: str = None) -> List[Dict]:
        """Generate a comprehensive dataset using multiple question types simultaneously"""
        
        if output_path is None:
            output_path = f"output/{topic.replace(' ', '_').lower()}_questions.jsonl"
        
        print(f"🚀 Starting multi-type question generation for: {topic}")
        print(f"📊 Target: {target_count} questions")
        print(f"🎭 Question types: {', '.join(question_types)}")
        print(f"🧠 Using Local LLM with optimized question generation prompts")
        print(f"🤖 Using model: {self.model}")
        
        all_questions = []
        questions_per_type = target_count // len(question_types)
        
        try:
            for question_type in question_types:
                print(f"\n📝 Generating {questions_per_type} {question_type} questions...")
                
                # Generate in batches to avoid token limits
                batch_size = 50
                num_batches = (questions_per_type + batch_size - 1) // batch_size
                
                for batch in tqdm(range(num_batches), desc=f"Generating {question_type} questions"):
                    batch_size_actual = min(batch_size, questions_per_type - batch * batch_size)
                    
                    if batch_size_actual <= 0:
                        break
                    
                    questions = self.generate_questions(
                        topic=topic,
                        question_type=question_type,
                        num_questions=batch_size_actual
                    )
                    
                    # Add metadata
                    for question in questions:
                        question["topic"] = topic
                        question["generation_type"] = question_type
                        question["batch"] = batch
                        question["timestamp"] = time.time()
                    
                    all_questions.extend(questions)
                    
                    # Save progress every batch
                    temp_path = f"{output_path}.temp"
                    self.save_questions(all_questions, temp_path)
                    
                    # Rate limiting
                    time.sleep(2)
                
                print(f"✅ Generated {len([q for q in all_questions if q['generation_type'] == question_type])} {question_type} questions")
            
            # Remove duplicates
            unique_questions = []
            seen_questions = set()
            
            for question in all_questions:
                question_text = question["question"].lower().strip()
                if question_text not in seen_questions:
                    seen_questions.add(question_text)
                    unique_questions.append(question)
            
            print(f"🔄 Removed {len(all_questions) - len(unique_questions)} duplicate questions")
            
            # Save final results
            self.save_questions(unique_questions, output_path)
            print(f"🎉 Completed! Generated {len(unique_questions)} unique questions about {topic}")
            print(f"📁 Saved to: {output_path}")
            
            return unique_questions
        
        except KeyboardInterrupt:
            print("\n⚠️ Process interrupted by user")
            if all_questions:
                self.save_questions(all_questions, f"{output_path}.interrupted")
            return all_questions

    def generate_comprehensive_dataset(self, topic: str, target_count: int = 5000, 
                                     output_path: str = None) -> List[Dict]:
        """Generate a comprehensive dataset of questions on the specified topic"""
        return self.generate_multi_type_dataset(
            topic=topic,
            question_types=["comprehensive", "expert", "personal"],
            target_count=target_count,
            output_path=output_path
        )

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Question Generator - LLM Only Version")
    parser.add_argument("--topic", "-t", required=True, help="Topic to generate questions about")
    parser.add_argument("--count", "-c", type=int, default=5000, help="Target number of questions")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--types", nargs="+", 
                       choices=["comprehensive", "expert", "personal"],
                       default=["comprehensive"], 
                       help="Question generation types (can specify multiple)")
    parser.add_argument("--batch-size", type=int, default=50, help="Questions per batch")
    
    args = parser.parse_args()
    
    # Process question generation
    try:
        generator = QuestionGenerator()
        
        if len(args.types) == 1 and args.types[0] != "comprehensive":
            # Generate single type
            questions = generator.generate_questions(
                topic=args.topic,
                question_type=args.types[0],
                num_questions=args.count
            )
            
            output_path = args.output or f"output/{args.topic.replace(' ', '_').lower()}_{args.types[0]}_questions.jsonl"
            generator.save_questions(questions, output_path)
            
        else:
            # Generate multi-type dataset
            questions = generator.generate_multi_type_dataset(
                topic=args.topic,
                question_types=args.types,
                target_count=args.count,
                output_path=args.output
            )
        
        # if questions:
        #     print(f"✅ Successfully generated {len(questions)} questions about {args.topic}!")
            
        #     # Show distribution by type
        #     type_counts = {}
        #     for q in questions:
        #         q_type = q.get('generation_type', 'unknown')
        #         type_counts[q_type] = type_counts.get(q_type, 0) + 1
            
        #     print(f"\n📊 Question distribution by type:")
        #     for q_type, count in type_counts.items():
        #         print(f"   {q_type}: {count} questions")
            
        #     # Print sample questions
        #     print(f"\n📋 Sample questions:")
        #     for i, q in enumerate(questions[:5]):
        #         print(f"{i+1}. {q['question']}")
        #         print(f"   Type: {q.get('generation_type', 'N/A')}, Category: {q.get('category', 'N/A')}")
        #         print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Example usage:")
        print(f"   python question_generator.py --topic 'Julius Nyerere' --types comprehensive expert personal --count 1000")
        print(f"   python question_generator.py --topic 'Leadership' --types expert personal --count 500")

if __name__ == "__main__":
    main() 