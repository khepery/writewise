"""
Tests for the WriteWise grammar checker.
"""

import pytest
from writewise.core.grammar_checker import GrammarChecker


@pytest.fixture
def checker():
    """Create a grammar checker instance for testing."""
    checker = GrammarChecker()
    yield checker
    checker.close()


def test_grammar_checker_initialization(checker):
    """Test that the grammar checker initializes correctly."""
    assert checker is not None
    assert checker.tool is not None


def test_simple_correct_text(checker):
    """Test analysis of grammatically correct text."""
    text = "This is a simple sentence. It has no errors."
    result = checker.analyze(text)
    
    assert result.original_text == text
    assert result.word_count > 0
    assert result.sentence_count == 2
    assert result.score >= 0
    assert result.score <= 100


def test_grammar_error_detection(checker):
    """Test detection of basic grammar errors."""
    text = "She don't like apples."
    result = checker.analyze(text)
    
    # Should detect subject-verb agreement error
    assert len(result.grammar_issues) > 0


def test_passive_voice_detection(checker):
    """Test detection of passive voice."""
    text = "The ball was thrown by the boy."
    result = checker.analyze(text)
    
    # Should detect passive voice in style suggestions
    passive_suggestions = [s for s in result.style_suggestions if s.category == "passive_voice"]
    assert len(passive_suggestions) > 0


def test_wordy_phrases_detection(checker):
    """Test detection of wordy phrases."""
    text = "At this point in time, we need to make a decision."
    result = checker.analyze(text)
    
    # Should detect "at this point in time" as wordy
    wordy_suggestions = [s for s in result.style_suggestions if s.category == "wordiness"]
    assert len(wordy_suggestions) > 0


def test_long_sentence_detection(checker):
    """Test detection of overly long sentences."""
    text = "This is a very long sentence that goes on and on and on with many clauses and phrases that could easily be broken up into multiple shorter sentences to improve readability and make the text easier to understand for the average reader."
    result = checker.analyze(text)
    
    # Should detect long sentence
    length_suggestions = [s for s in result.style_suggestions if s.category == "sentence_length"]
    assert len(length_suggestions) > 0


def test_repeated_words_detection(checker):
    """Test detection of repeated words."""
    text = "The the cat sat on the mat."
    result = checker.analyze(text)
    
    # Should detect repeated "the"
    repetition_suggestions = [s for s in result.style_suggestions if s.category == "repetition"]
    assert len(repetition_suggestions) > 0


def test_readability_metrics(checker):
    """Test that readability metrics are calculated."""
    text = "The cat sat on the mat. The dog ran in the park."
    result = checker.analyze(text)
    
    assert result.readability.flesch_reading_ease > 0
    assert result.readability.flesch_kincaid_grade >= 0
    assert result.readability.reading_time_minutes >= 0


def test_auto_correction(checker):
    """Test automatic text correction."""
    text = "She don't like apples."
    corrected = checker.correct_text(text)
    
    # The corrected text should be different
    assert corrected != text
    # Should suggest "doesn't"
    assert "doesn't" in corrected.lower() or "does not" in corrected.lower()


def test_empty_text(checker):
    """Test handling of empty text."""
    text = ""
    result = checker.analyze(text)
    
    assert result.word_count == 0
    assert result.sentence_count == 0


def test_score_calculation(checker):
    """Test that score is calculated correctly."""
    # Perfect text
    good_text = "This is a well-written sentence."
    good_result = checker.analyze(good_text)
    
    # Text with errors
    bad_text = "She don't like apples. He don't like oranges either."
    bad_result = checker.analyze(bad_text)
    
    # Good text should have higher score
    assert good_result.score > bad_result.score


def test_multiple_sentences(checker):
    """Test analysis of multiple sentences."""
    text = "First sentence. Second sentence. Third sentence."
    result = checker.analyze(text)
    
    assert result.sentence_count == 3
    assert result.word_count == 6


def test_complex_text(checker):
    """Test analysis of more complex text."""
    text = """
    The importance of proper grammar cannot be overstated. Clear communication 
    is essential in both academic and professional settings. Students, teachers, 
    and writers all benefit from tools that help improve their writing quality.
    """
    result = checker.analyze(text)
    
    assert result.word_count > 0
    assert result.sentence_count > 0
    assert result.score >= 0
    assert result.score <= 100
    assert result.readability.flesch_reading_ease > 0
