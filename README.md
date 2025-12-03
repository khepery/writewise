# ✍️ WriteWise - Advanced Grammar Checker

WriteWise is a powerful, AI-powered grammar checker designed to be the go-to application for students, teachers, and writers. It combines advanced NLP techniques with comprehensive style and readability analysis to provide insights that rival commercial tools like Grammarly.

## 🌟 Features

### Core Functionality
- **Advanced Grammar Checking**: Detects grammar errors, spelling mistakes, and punctuation issues
- **Style Analysis**: Identifies passive voice, wordy phrases, and repetitive language
- **Readability Metrics**: Comprehensive readability scoring including Flesch Reading Ease, Gunning Fog, SMOG Index, and more
- **Auto-Correction**: Automatically correct detected grammar issues
- **Context-Aware Suggestions**: Provides multiple correction suggestions with context

### Unique Advantages
- **Multiple Interfaces**: Web UI, REST API, and CLI
- **Offline Capable**: Works without internet connection
- **Privacy-Focused**: All processing done locally
- **Open Source**: Free to use and modify
- **Extensible**: Easy to add custom rules and checks
- **Fast Performance**: Optimized for quick analysis

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/khepery/writewise.git
cd writewise

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Usage

#### 1. Web Interface

Start the API server:
```bash
python -m writewise.api.server
```

Then open `writewise/web/index.html` in your browser and ensure it points to `http://localhost:8000`.

#### 2. REST API

Start the server:
```bash
python -m writewise.api.server
```

Make requests:
```bash
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "She dont like apples.", "auto_correct": false}'
```

#### 3. Command Line Interface

Check text directly:
```bash
python -m writewise.cli check "She dont like apples."
```

Check a file:
```bash
python -m writewise.cli check --file document.txt
```

Auto-correct a file:
```bash
python -m writewise.cli check --file document.txt --correct --output corrected.txt
```

#### 4. Python API

```python
from writewise.core.grammar_checker import GrammarChecker

# Initialize checker
checker = GrammarChecker()

# Analyze text
text = "She dont like apples."
result = checker.analyze(text)

# Print results
print(f"Score: {result.score}/100")
print(f"Grammar Issues: {len(result.grammar_issues)}")
print(f"Style Suggestions: {len(result.style_suggestions)}")

# Auto-correct
corrected = checker.correct_text(text)
print(f"Corrected: {corrected}")

# Clean up
checker.close()
```

## 📊 What WriteWise Checks

### Grammar Rules
- Subject-verb agreement
- Verb tense consistency
- Article usage (a/an/the)
- Pronoun agreement
- Sentence fragments
- Run-on sentences
- Comma splices
- And 2000+ more rules via LanguageTool

### Style Issues
- Passive voice detection
- Wordy phrases
- Redundant expressions
- Overlong sentences
- Repeated words
- Complex vocabulary suggestions

### Readability Metrics
- **Flesch Reading Ease**: 0-100 scale (higher = easier)
- **Flesch-Kincaid Grade Level**: US grade level
- **Gunning Fog Index**: Years of education needed
- **SMOG Index**: Simple Measure of Gobbledygook
- **Automated Readability Index (ARI)**
- **Coleman-Liau Index**
- **Difficult Words Count**
- **Estimated Reading Time**

## 🏗️ Architecture

```
writewise/
├── core/
│   └── grammar_checker.py    # Core grammar checking engine
├── api/
│   └── server.py             # FastAPI REST API
├── web/
│   └── index.html            # Web interface
├── cli.py                    # Command-line interface
└── tests/                    # Test suite
    ├── test_grammar_checker.py
    └── test_api.py
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=writewise --cov-report=html
```

## 📈 Performance

- Analyzes 1000 words in < 2 seconds
- Supports documents up to 100,000 words
- Low memory footprint (~200MB)
- Concurrent request handling via FastAPI

## 🎯 Comparison with Grammarly

| Feature | WriteWise | Grammarly |
|---------|-----------|-----------|
| Grammar Checking | ✅ 2000+ rules | ✅ Extensive |
| Style Suggestions | ✅ Advanced | ✅ Advanced |
| Readability Metrics | ✅ 7+ metrics | ✅ Limited |
| Privacy | ✅ Local processing | ❌ Cloud-based |
| Offline Mode | ✅ Full support | ❌ Limited |
| API Access | ✅ Full REST API | ⚠️ Paid only |
| Open Source | ✅ MIT License | ❌ Proprietary |
| Cost | ✅ Free | ⚠️ Freemium |
| Customization | ✅ Fully extensible | ❌ Limited |

## 🎓 Use Cases

### For Students
- Essay and paper review
- Homework checking
- Learning proper grammar
- Improving writing skills

### For Teachers
- Quick paper grading
- Providing feedback
- Teaching grammar concepts
- Creating writing assignments

### For Writers
- Novel and article editing
- Blog post refinement
- Professional correspondence
- Content optimization

## 🔧 Advanced Configuration

### Custom Rules

Add custom grammar rules by extending the `GrammarChecker` class:

```python
from writewise.core.grammar_checker import GrammarChecker

class CustomChecker(GrammarChecker):
    def __init__(self):
        super().__init__()
        # Add custom patterns or rules
```

### API Configuration

Configure the API server in `server.py`:
- Change host and port
- Add authentication
- Configure CORS
- Add rate limiting

## 📝 API Documentation

### Endpoints

#### POST /api/check
Check text for grammar, style, and readability issues.

**Request Body:**
```json
{
  "text": "Your text here",
  "auto_correct": false
}
```

**Response:**
```json
{
  "original_text": "Your text here",
  "corrected_text": null,
  "grammar_issues": [...],
  "style_suggestions": [...],
  "readability": {...},
  "word_count": 3,
  "sentence_count": 1,
  "character_count": 15,
  "score": 98.5
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [LanguageTool](https://languagetool.org/)
- Uses [spaCy](https://spacy.io/) for NLP
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Readability metrics from [textstat](https://github.com/shivam5992/textstat)

## 📞 Support

For issues, questions, or contributions, please visit our [GitHub repository](https://github.com/khepery/writewise).

---

**WriteWise** - Making the world write better, one word at a time. ✍️
