# AI Q&A Generator with Multiple AI Backends

Simple, efficient Python script to generate AI-powered answers for large datasets of questions with roleplay capabilities. Supports multiple AI backends:

- **Claude Login** with cookie-based authentication (no API key needed)
- **Claude Code SDK** with full agentic capabilities (API key + CLI required)
- **Qwen AI** (Alibaba) with Google Custom Search integration
- **LLM-only mode** for internal knowledge access

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment variables in `.env`:**
   
   **For Claude Login (No API key needed):**
   ```bash
   CLAUDE_COOKIE=your_claude_session_cookie_here
   ```
   *See [CLAUDE_LOGIN_GUIDE.md](CLAUDE_LOGIN_GUIDE.md) for detailed instructions*
   
   **For Claude Code SDK (API key + CLI required):**
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   *Also requires: `npm install -g @anthropic-ai/claude-code`*
   
   **For Qwen AI with Google Search:**
   ```bash
   QWEN_AI_KEY=your_qwen_api_key_here
   QWEN_AI_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
   QWEN_AI_MODEL=qwen-plus
   GOOGLE_SEARCH_KEY=your_google_search_key
   GOOGLE_SEARCH_CX=your_google_search_cx
   ```

3. **Test your setup (optional):**
   ```bash
   # Test Claude Login
   python test_claude_login.py
   
   # Test Claude Code SDK
   python test_claude_code.py
   ```
   
   **Prerequisites for Claude Code SDK:**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

4. **Run the script:**
   
   **Claude Login (No API key needed):**
   ```bash
   python main_claude_login.py --dataset your_questions.csv --character einstein
   ```
   
   **Claude Code SDK (API key + CLI required):**
   ```bash
   python main_claude_code.py --dataset your_questions.csv --character einstein
   ```
   
   **Qwen AI with Google Search:**
   ```bash
   python main.py --dataset your_questions.csv --character einstein
   ```
   
   **LLM-only mode:**
   ```bash
   python main_llm_only.py --dataset your_questions.csv --character einstein
   ```

## 📋 Features

- **Multiple AI Backends**: 
  - Claude Login with cookie-based authentication (no API key needed)
  - Claude Code SDK with full agentic capabilities (API key + CLI required)
  - Qwen AI with Google Custom Search integration
  - LLM-only mode for internal knowledge access
- **AI Roleplay**: Answer as Einstein, Newton, Darwin, Tesla, Curie, Mandela, or Academic Scholar
- **Large Dataset Support**: Efficiently processes thousands of questions
- **Progress Saving**: Automatic progress saving every 50 questions
- **Multiple Formats**: Supports CSV, JSON, and TXT input files
- **Resume Capability**: Continue from where you left off
- **Agentic Capabilities**: Web search, code execution, file reading (Claude Code SDK)

## 🎭 Available Characters

- `mandela` - Nelson Mandela (Leadership & Human Rights)
- `einstein` - Albert Einstein (Physics & Philosophy)
- `newton` - Isaac Newton (Mathematics & Physics)  
- `darwin` - Charles Darwin (Biology & Evolution)
- `tesla` - Nikola Tesla (Technology & Innovation)
- `curie` - Marie Curie (Chemistry & Physics)
- `default` - Academic Scholar (General expertise)

## 📊 Usage Examples

```bash
# Claude Code SDK (Recommended)
python main_claude_code.py --dataset questions.csv --character einstein

# Qwen AI with Google Search
python main.py --dataset questions.csv --character einstein

# LLM-only mode
python main_llm_only.py --dataset questions.csv --character einstein

# Process only first 100 questions
python main_claude_code.py --dataset questions.csv --max-questions 100

# Start from question 500
python main_claude_code.py --dataset questions.csv --start-from 500

# List available characters
python main_claude_code.py --list-characters
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
   python main_claude_code.py --dataset large.csv --max-questions 1000
   
   # Continue from 1000
   python main_claude_code.py --dataset large.csv --start-from 1000 --max-questions 1000
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
- **Claude Code SDK**: Anthropic API key (recommended)
- **Qwen AI**: Qwen AI API key (Alibaba) + Google Custom Search API

## 📄 Files

- `main_claude_code.py` - Claude Code SDK version (recommended)
- `main.py` - Qwen AI with Google Search version
- `main_llm_only.py` - LLM-only version
- `test_claude_code.py` - Test script for Claude Code SDK
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `README.md` - This file 