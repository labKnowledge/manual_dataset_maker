# AI Q&A Generator with Google Search

Simple, efficient Python script to generate AI-powered answers for large datasets of questions with roleplay capabilities and Google Custom Search integration. Uses Qwen AI (Alibaba) for responses.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment variables in `.env`:**
   ```bash
   QWEN_AI_KEY=your_qwen_api_key_here
   QWEN_AI_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
   QWEN_AI_MODEL=qwen-plus
   GOOGLE_SEARCH_KEY=your_google_search_key
   GOOGLE_SEARCH_CX=your_google_search_cx
   ```

3. **Run the script:**
   ```bash
   python main.py --dataset your_questions.csv --character einstein
   ```

## 📋 Features

- **Qwen AI Integration**: Uses Alibaba's Qwen AI model for responses
- **Google Custom Search Integration**: Uses Google Custom Search API for research
- **AI Roleplay**: Answer as Einstein, Newton, Darwin, Tesla, Curie, or Academic Scholar
- **Large Dataset Support**: Efficiently processes thousands of questions
- **Progress Saving**: Automatic progress saving every 50 questions
- **Multiple Formats**: Supports CSV, JSON, and TXT input files
- **Resume Capability**: Continue from where you left off

## 🎭 Available Characters

- `einstein` - Albert Einstein (Physics & Philosophy)
- `newton` - Isaac Newton (Mathematics & Physics)  
- `darwin` - Charles Darwin (Biology & Evolution)
- `tesla` - Nikola Tesla (Technology & Innovation)
- `curie` - Marie Curie (Chemistry & Physics)
- `default` - Academic Scholar (General expertise)

## 📊 Usage Examples

```bash
# Basic usage
python main.py --dataset questions.csv --character einstein

# Process only first 100 questions
python main.py --dataset questions.csv --max-questions 100

# Start from question 500
python main.py --dataset questions.csv --start-from 500

# Disable search (faster, less factual)
python main.py --dataset questions.csv --no-search

# List available characters
python main.py --list-characters
```

## 📁 Dataset Format

**CSV Format:**
```csv
question,id
"What is quantum mechanics?",1
"How does evolution work?",2
```

**JSON Format:**
```json
[
  {"question": "What is quantum mechanics?"},
  {"question": "How does evolution work?"}
]
```

**TXT Format:**
```
What is quantum mechanics?
How does evolution work?
```

## 📤 Output

Results are saved to `output/answers.jsonl` with:
- Question and AI-generated answer
- Character used for roleplay
- Search results used for context
- Timestamp and metadata

## 🔧 Configuration

Edit `config.py` to modify:
- AI model settings
- Processing batch size
- Roleplay character prompts
- File paths

## 💡 Tips for Large Datasets (4000+ questions)

1. **Process in chunks:**
   ```bash
   # First 1000 questions
   python main.py --dataset large.csv --max-questions 1000
   
   # Continue from 1000
   python main.py --dataset large.csv --start-from 1000 --max-questions 1000
   ```

2. **Monitor progress:**
   - Progress is saved every 50 questions to `.temp` file
   - Check console output for real-time progress

3. **Handle interruptions:**
   - Use Ctrl+C to stop safely
   - Results are saved to `.interrupted` file
   - Resume with `--start-from` parameter

## 🛠️ Requirements

- Python 3.8+
- Qwen AI API key (Alibaba)
- Google Custom Search API

## 📄 Files

- `main.py` - Main script
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `README.md` - This file 