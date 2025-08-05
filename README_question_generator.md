# AI Question Generator - LLM Only Version

A powerful tool for generating rich, comprehensive question datasets on any topic using local LLM capabilities. This script creates high-quality questions similar to the Nelson Mandela dataset, with a target of 5000+ questions per topic.

## Features

- **Multiple Question Types**: Comprehensive, Expert, and Personal reflection questions
- **High-Quality Generation**: Optimized prompts for maximum knowledge utilization
- **Duplicate Removal**: Automatic filtering of duplicate questions
- **Batch Processing**: Efficient generation in configurable batches
- **Progress Saving**: Automatic progress saving with resume capability
- **Flexible Output**: JSONL format for easy processing

## Installation

1. Ensure you have the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables in `.env`:
```bash
LOCAL_AI_MODEL=hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL
LOCAL_AI_BASE_URL=http://localhost:11434/v1
```

## Usage

### Basic Usage

Generate a comprehensive dataset (5000 questions by default):
```bash
python question_generator.py --topic "Artificial Intelligence"
```

### Advanced Usage

Generate specific number of questions:
```bash
python question_generator.py --topic "Climate Change" --count 10000
```

Generate multiple question types simultaneously:
```bash
# All three types (comprehensive, expert, personal)
python question_generator.py --topic "Julius Nyerere" --types comprehensive expert personal --count 1000

# Expert and personal questions only
python question_generator.py --topic "Leadership" --types expert personal --count 500

# Single type (legacy support)
python question_generator.py --topic "Quantum Physics" --types expert --count 1000
```

Specify custom output file:
```bash
python question_generator.py --topic "Machine Learning" --output "output/ml_questions.jsonl"
```

### Command Line Options

- `--topic, -t`: Topic to generate questions about (required)
- `--count, -c`: Target number of questions (default: 5000)
- `--types`: Question generation types (can specify multiple): comprehensive, expert, personal (default: comprehensive)
- `--output, -o`: Output file path
- `--batch-size`: Questions per batch (default: 50)

## Question Types

### 1. Comprehensive Questions
- Mix of factual, analytical, reflective, and comparative questions
- Covers multiple angles and perspectives
- Suitable for general audiences
- Balanced complexity levels

### 2. Expert Questions
- Advanced, nuanced questions requiring deep knowledge
- Focus on specialized aspects and controversies
- Interdisciplinary connections
- Critical thinking emphasis

### 3. Personal Reflection Questions
- Deeply personal and introspective
- Connect topic to personal experiences and values
- Encourage self-reflection and growth
- Emotional and meaningful engagement

## Multi-Type Generation

The question generator now supports generating questions from multiple types simultaneously, creating rich, diverse datasets:

### Benefits of Multi-Type Generation:
- **Comprehensive Coverage**: Questions from different angles and perspectives
- **Depth and Breadth**: Combines shallow and deep questions for complete coverage
- **Biographical Richness**: Perfect for roleplaying scenarios with historical figures
- **Educational Value**: Questions suitable for different learning levels
- **Research Applications**: Diverse question types for various research needs

### Example Use Cases:
- **Biographical Datasets**: Questions about historical figures from multiple perspectives
- **Educational Content**: Questions for different student levels and learning styles
- **Research Surveys**: Comprehensive question sets for academic research
- **Roleplaying Scenarios**: Questions that simulate real conversations with experts

## Output Format

Each question is saved as a JSON object with the following structure:

```json
{
  "question": "What are the fundamental principles of quantum mechanics?",
  "category": "physics",
  "complexity": "advanced",
  "focus_area": "quantum mechanics",
  "topic": "Physics",
  "generation_type": "expert",
  "batch": 0,
  "timestamp": 1703123456.789
}
```

## Example Topics

Here are some example topics that work well with the question generator:

### Science & Technology
- Artificial Intelligence
- Quantum Physics
- Climate Change
- Biotechnology
- Space Exploration
- Renewable Energy

### History & Politics
- World War II
- Civil Rights Movement
- Ancient Civilizations
- Democracy
- International Relations
- Economic Systems

### Philosophy & Ethics
- Moral Philosophy
- Existentialism
- Ethics in Technology
- Human Rights
- Justice
- Free Will

### Business & Leadership
- Entrepreneurship
- Leadership Styles
- Innovation
- Corporate Social Responsibility
- Strategic Management
- Team Building

## Performance Tips

1. **Batch Size**: Use smaller batch sizes (20-50) for more stable generation
2. **Rate Limiting**: The script includes built-in delays to prevent API overload
3. **Progress Saving**: Checkpoints are saved every batch for resume capability
4. **Duplicate Removal**: Automatic filtering ensures unique questions
5. **Error Handling**: Graceful fallback for failed generations

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure your local LLM server is running
2. **Token Limits**: Reduce batch size if encountering token limit errors
3. **Memory Issues**: Process smaller batches for large datasets
4. **Duplicate Questions**: Normal behavior - the script automatically removes duplicates

### Resume Generation

If the process is interrupted, you can resume by:
1. Checking the `.temp` or `.interrupted` files
2. Adjusting the count to account for already generated questions
3. Using a different output file to avoid conflicts

## Quality Assurance

The question generator includes several quality measures:

- **Diversity Check**: Ensures questions cover different aspects of the topic
- **Complexity Balance**: Mix of basic, intermediate, and advanced questions
- **Uniqueness Filter**: Automatic removal of duplicate questions
- **Format Validation**: Ensures proper JSON structure
- **Content Quality**: Optimized prompts for high-quality generation

## Integration

The generated questions can be used with:

- `main_local_llm_only.py`: Generate answers to the questions
- `main_claude_code.py`: Use with Claude for enhanced answers
- Custom analysis scripts: Process and analyze the question datasets

## Example Output

### Multi-Type Generation Example:
```bash
$ python question_generator.py --topic "Julius Nyerere" --types comprehensive expert personal --count 100

🚀 Starting multi-type question generation for: Julius Nyerere
📊 Target: 100 questions
🎭 Question types: comprehensive, expert, personal
🧠 Using Local LLM with optimized question generation prompts
🤖 Using model: hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL

📝 Generating 33 comprehensive questions...
✅ Generated 33 comprehensive questions

📝 Generating 33 expert questions...
✅ Generated 33 expert questions

📝 Generating 34 personal questions...
✅ Generated 34 personal questions

🔄 Removed 5 duplicate questions
🎉 Completed! Generated 95 unique questions about Julius Nyerere
📁 Saved to: output/julius_nyerere_questions.jsonl

✅ Successfully generated 95 questions about Julius Nyerere!

📊 Question distribution by type:
   comprehensive: 33 questions
   expert: 33 questions
   personal: 29 questions

📋 Sample questions:
1. What were the key principles of Ujamaa socialism that Nyerere implemented in Tanzania?
   Type: comprehensive, Category: political_philosophy

2. How did Nyerere's educational background influence his approach to nation-building?
   Type: expert, Category: biographical_analysis

3. What personal sacrifices did Nyerere make for the independence movement?
   Type: personal, Category: personal_reflection
```

### Single Type Example:
```bash
$ python question_generator.py --topic "Leadership" --types expert --count 50

🚀 Starting question generation for: Leadership
📊 Target: 50 questions
🧠 Using Local LLM with optimized question generation prompts
🤖 Using model: hf.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:UD-Q4_K_XL

📝 Generating 50 expert questions...
✅ Generated 50 expert questions

✅ Successfully generated 50 questions about Leadership!

📊 Question distribution by type:
   expert: 50 questions

📋 Sample questions:
1. How do cultural differences impact leadership effectiveness in global organizations?
   Type: expert, Category: cross_cultural
```

## Contributing

To improve the question generator:

1. Add new question types in the `question_strategies` dictionary
2. Enhance prompt engineering for better question quality
3. Add new output formats or processing options
4. Improve error handling and recovery mechanisms

## License

This project follows the same license as the main manual_dataset_maker project. 