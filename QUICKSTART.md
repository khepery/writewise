# WriteWise Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/khepery/writewise.git
cd writewise

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Basic Usage

### 1. Python API (Recommended for Integration)

```python
from writewise.core.grammar_checker import GrammarChecker

# Initialize the checker
checker = GrammarChecker(use_language_tool=False)

# Analyze text
text = "She dont like apples."
result = checker.analyze(text)

# View results
print(f"Score: {result.score}/100")
print(f"Issues: {len(result.grammar_issues)}")

for issue in result.grammar_issues:
    print(f"- {issue.message}")
    print(f"  Suggestions: {', '.join(issue.suggestions)}")

# Auto-correct
corrected = checker.correct_text(text)
print(f"Corrected: {corrected}")

# Clean up
checker.close()
```

### 2. REST API (Recommended for Web/Mobile Apps)

Start the server:
```bash
python -m writewise.api.server
```

The API will be available at `http://localhost:8000`

Make requests:
```bash
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{
    "text": "She dont like apples.",
    "auto_correct": false
  }'
```

API Documentation: Visit `http://localhost:8000/docs` for interactive API docs.

### 3. Command Line Interface (Recommended for Quick Checks)

Check text directly:
```bash
python -m writewise.cli check "She dont like apples."
```

Check a file:
```bash
python -m writewise.cli check --file document.txt
```

Auto-correct and save:
```bash
python -m writewise.cli check --file document.txt --correct --output corrected.txt
```

### 4. Web Interface (Recommended for End Users)

1. Start the API server:
   ```bash
   python -m writewise.api.server
   ```

2. Open `writewise/web/index.html` in your browser

3. Enter text and click "Check Grammar"

## Example Output

### Grammar Issues
```
❌ Subject-verb agreement error
   "She dont" → Suggestion: "She doesn't"
```

### Style Suggestions
```
💡 Wordy phrase detected
   "at this point in time" → Suggestion: "now"
   
💡 Passive voice detected
   "was written by" → Suggestion: Use active voice
```

### Readability Metrics
```
Flesch Reading Ease: 89.5 (Easy to read)
Grade Level: 1.9 (Primary school)
Reading Time: 0.6 minutes
```

## Features Comparison

| Feature | WriteWise | Grammarly |
|---------|-----------|-----------|
| Grammar Checking | ✅ | ✅ |
| Style Analysis | ✅ | ✅ |
| Readability Metrics | ✅ (7+ metrics) | ⚠️ Limited |
| Privacy | ✅ Local processing | ❌ Cloud-based |
| Offline Mode | ✅ | ❌ |
| API Access | ✅ Free | ⚠️ Paid |
| Open Source | ✅ | ❌ |
| Cost | ✅ Free | ⚠️ Freemium |

## Target Users

### Students
- Essay and paper review
- Homework checking
- Learning proper grammar

### Teachers
- Quick paper grading
- Providing feedback
- Teaching grammar concepts

### Writers
- Novel and article editing
- Blog post refinement
- Professional correspondence

## Advanced Features

### Custom Checks
You can extend the checker with custom rules:

```python
class CustomChecker(GrammarChecker):
    def _basic_grammar_checks(self, text):
        issues = super()._basic_grammar_checks(text)
        # Add your custom checks here
        return issues
```

### Batch Processing
Process multiple files:

```python
import glob

checker = GrammarChecker(use_language_tool=False)

for file_path in glob.glob("*.txt"):
    with open(file_path) as f:
        text = f.read()
    result = checker.analyze(text)
    print(f"{file_path}: Score {result.score}/100")

checker.close()
```

## Troubleshooting

### Issue: LanguageTool download fails
**Solution:** The system works in offline mode with basic checks. For full LanguageTool support, ensure internet access or use `use_language_tool=False`.

### Issue: NLTK data not found
**Solution:** The required NLTK data downloads automatically. If it fails, run:
```python
import nltk
nltk.download('punkt_tab')
```

### Issue: Import errors
**Solution:** Ensure you installed the package:
```bash
pip install -e .
```

## Next Steps

1. Read the full documentation in `README.md`
2. Run the examples in `examples/usage_examples.py`
3. Check out the sample documents in `examples/sample_documents.md`
4. Explore the test suite in `tests/` for more usage patterns

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review the test suite for examples

---

**WriteWise** - Making the world write better! ✍️
