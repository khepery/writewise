"""
Core grammar checking engine for WriteWise.
Provides comprehensive grammar, style, and readability analysis.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import language_tool_python
import textstat
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)


@dataclass
class GrammarIssue:
    """Represents a grammar issue found in text."""
    message: str
    rule_id: str
    category: str
    offset: int
    length: int
    context: str
    suggestions: List[str]
    severity: str


@dataclass
class StyleSuggestion:
    """Represents a style improvement suggestion."""
    message: str
    category: str
    offset: int
    length: int
    original: str
    suggestion: str


@dataclass
class ReadabilityMetrics:
    """Readability metrics for text analysis."""
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    smog_index: float
    automated_readability_index: float
    coleman_liau_index: float
    difficult_words: int
    reading_time_minutes: float


@dataclass
class AnalysisResult:
    """Complete analysis result for a text."""
    original_text: str
    grammar_issues: List[GrammarIssue]
    style_suggestions: List[StyleSuggestion]
    readability: ReadabilityMetrics
    word_count: int
    sentence_count: int
    character_count: int
    score: float  # Overall quality score 0-100


class GrammarChecker:
    """
    Advanced grammar checking engine using multiple NLP techniques.
    Provides grammar checking, style analysis, and readability metrics.
    """
    
    def __init__(self):
        """Initialize the grammar checker with language tools."""
        self.tool = language_tool_python.LanguageTool('en-US')
        self.passive_voice_patterns = [
            r'\b(am|is|are|was|were|be|been|being)\s+\w+ed\b',
            r'\b(am|is|are|was|were|be|been|being)\s+\w+en\b'
        ]
        
    def analyze(self, text: str) -> AnalysisResult:
        """
        Perform comprehensive analysis of the input text.
        
        Args:
            text: The text to analyze
            
        Returns:
            AnalysisResult containing all detected issues and metrics
        """
        # Grammar checking
        grammar_issues = self._check_grammar(text)
        
        # Style analysis
        style_suggestions = self._analyze_style(text)
        
        # Readability metrics
        readability = self._calculate_readability(text)
        
        # Basic statistics
        word_count = len(text.split())
        sentences = nltk.sent_tokenize(text)
        sentence_count = len(sentences)
        character_count = len(text)
        
        # Calculate overall score
        score = self._calculate_score(grammar_issues, style_suggestions, readability)
        
        return AnalysisResult(
            original_text=text,
            grammar_issues=grammar_issues,
            style_suggestions=style_suggestions,
            readability=readability,
            word_count=word_count,
            sentence_count=sentence_count,
            character_count=character_count,
            score=score
        )
    
    def _check_grammar(self, text: str) -> List[GrammarIssue]:
        """Check text for grammar issues using LanguageTool."""
        matches = self.tool.check(text)
        issues = []
        
        for match in matches:
            # Extract context
            start = max(0, match.offset - 20)
            end = min(len(text), match.offset + match.errorLength + 20)
            context = text[start:end]
            
            # Determine severity
            severity = "error" if match.category in ["GRAMMAR", "TYPOS"] else "warning"
            
            issue = GrammarIssue(
                message=match.message,
                rule_id=match.ruleId,
                category=match.category,
                offset=match.offset,
                length=match.errorLength,
                context=context,
                suggestions=match.replacements[:3],  # Top 3 suggestions
                severity=severity
            )
            issues.append(issue)
        
        return issues
    
    def _analyze_style(self, text: str) -> List[StyleSuggestion]:
        """Analyze text for style improvements."""
        suggestions = []
        
        # Check for passive voice
        suggestions.extend(self._check_passive_voice(text))
        
        # Check for wordy phrases
        suggestions.extend(self._check_wordy_phrases(text))
        
        # Check for sentence length
        suggestions.extend(self._check_sentence_length(text))
        
        # Check for repeated words
        suggestions.extend(self._check_repeated_words(text))
        
        return suggestions
    
    def _check_passive_voice(self, text: str) -> List[StyleSuggestion]:
        """Detect passive voice constructions."""
        suggestions = []
        
        for pattern in self.passive_voice_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                suggestion = StyleSuggestion(
                    message="Consider using active voice for more direct writing",
                    category="passive_voice",
                    offset=match.start(),
                    length=match.end() - match.start(),
                    original=match.group(),
                    suggestion="Consider rewriting in active voice"
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _check_wordy_phrases(self, text: str) -> List[StyleSuggestion]:
        """Check for wordy phrases that can be simplified."""
        wordy_phrases = {
            r'\bat this point in time\b': 'now',
            r'\bdue to the fact that\b': 'because',
            r'\bin order to\b': 'to',
            r'\bfor the purpose of\b': 'to',
            r'\bin the event that\b': 'if',
            r'\bwith regard to\b': 'about',
            r'\bin spite of the fact that\b': 'although',
            r'\ba number of\b': 'many',
            r'\bprior to\b': 'before',
        }
        
        suggestions = []
        for pattern, replacement in wordy_phrases.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                suggestion = StyleSuggestion(
                    message=f"Consider simplifying to '{replacement}'",
                    category="wordiness",
                    offset=match.start(),
                    length=match.end() - match.start(),
                    original=match.group(),
                    suggestion=replacement
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _check_sentence_length(self, text: str) -> List[StyleSuggestion]:
        """Check for overly long sentences."""
        suggestions = []
        sentences = nltk.sent_tokenize(text)
        
        offset = 0
        for sentence in sentences:
            word_count = len(sentence.split())
            if word_count > 30:
                suggestion = StyleSuggestion(
                    message=f"This sentence has {word_count} words. Consider breaking it into shorter sentences for better readability.",
                    category="sentence_length",
                    offset=text.find(sentence, offset),
                    length=len(sentence),
                    original=sentence[:50] + "..." if len(sentence) > 50 else sentence,
                    suggestion="Break into shorter sentences"
                )
                suggestions.append(suggestion)
            offset += len(sentence)
        
        return suggestions
    
    def _check_repeated_words(self, text: str) -> List[StyleSuggestion]:
        """Check for unintentionally repeated words."""
        suggestions = []
        pattern = r'\b(\w+)\s+\1\b'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Skip intentional repetitions like "very very"
            word = match.group(1).lower()
            if word not in ['very', 'far', 'long', 'many']:
                suggestion = StyleSuggestion(
                    message=f"Possible unintentional word repetition: '{match.group()}'",
                    category="repetition",
                    offset=match.start(),
                    length=match.end() - match.start(),
                    original=match.group(),
                    suggestion=match.group(1)
                )
                suggestions.append(suggestion)
        
        return suggestions
    
    def _calculate_readability(self, text: str) -> ReadabilityMetrics:
        """Calculate various readability metrics."""
        return ReadabilityMetrics(
            flesch_reading_ease=textstat.flesch_reading_ease(text),
            flesch_kincaid_grade=textstat.flesch_kincaid_grade(text),
            gunning_fog=textstat.gunning_fog(text),
            smog_index=textstat.smog_index(text),
            automated_readability_index=textstat.automated_readability_index(text),
            coleman_liau_index=textstat.coleman_liau_index(text),
            difficult_words=textstat.difficult_words(text),
            reading_time_minutes=textstat.reading_time(text, ms_per_char=14.69)
        )
    
    def _calculate_score(
        self,
        grammar_issues: List[GrammarIssue],
        style_suggestions: List[StyleSuggestion],
        readability: ReadabilityMetrics
    ) -> float:
        """Calculate overall quality score (0-100)."""
        score = 100.0
        
        # Deduct points for grammar issues
        for issue in grammar_issues:
            if issue.severity == "error":
                score -= 2.0
            else:
                score -= 0.5
        
        # Deduct points for style issues
        score -= len(style_suggestions) * 0.3
        
        # Adjust based on readability (optimal Flesch Reading Ease is 60-70)
        if readability.flesch_reading_ease < 30:
            score -= 5
        elif readability.flesch_reading_ease > 90:
            score -= 2
        
        return max(0.0, min(100.0, score))
    
    def correct_text(self, text: str) -> str:
        """
        Automatically correct grammar issues in text.
        
        Args:
            text: The text to correct
            
        Returns:
            Corrected text
        """
        matches = self.tool.check(text)
        return language_tool_python.utils.correct(text, matches)
    
    def close(self):
        """Close the language tool connection."""
        self.tool.close()
