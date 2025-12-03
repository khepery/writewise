"""
Example usage of WriteWise grammar checker.
"""

from writewise.core.grammar_checker import GrammarChecker


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===\n")
    
    # Initialize checker
    checker = GrammarChecker()
    
    # Example text with errors
    text = "She dont like apples. The weather are nice today."
    
    print(f"Original text: {text}\n")
    
    # Analyze text
    result = checker.analyze(text)
    
    # Print results
    print(f"Quality Score: {result.score:.1f}/100")
    print(f"Grammar Issues Found: {len(result.grammar_issues)}")
    print(f"Style Suggestions: {len(result.style_suggestions)}")
    print(f"\nWord Count: {result.word_count}")
    print(f"Reading Time: {result.readability.reading_time_minutes:.1f} minutes")
    
    # Show grammar issues
    if result.grammar_issues:
        print("\n--- Grammar Issues ---")
        for i, issue in enumerate(result.grammar_issues, 1):
            print(f"\n{i}. {issue.message}")
            print(f"   Suggestions: {', '.join(issue.suggestions[:3])}")
    
    # Auto-correct
    corrected = checker.correct_text(text)
    print(f"\n--- Auto-corrected Text ---")
    print(corrected)
    
    checker.close()


def example_style_analysis():
    """Style analysis example."""
    print("\n\n=== Style Analysis Example ===\n")
    
    checker = GrammarChecker()
    
    # Text with style issues
    text = """
    At this point in time, the report was written by the committee. 
    Due to the fact that the budget is limited, we need to make a decision 
    in order to proceed with the project.
    """
    
    print(f"Original text: {text}\n")
    
    result = checker.analyze(text)
    
    # Show style suggestions
    print("--- Style Suggestions ---")
    for i, sug in enumerate(result.style_suggestions, 1):
        print(f"\n{i}. {sug.message}")
        print(f"   Category: {sug.category}")
        print(f"   Original: '{sug.original}' → Suggestion: '{sug.suggestion}'")
    
    checker.close()


def example_readability_analysis():
    """Readability analysis example."""
    print("\n\n=== Readability Analysis Example ===\n")
    
    checker = GrammarChecker()
    
    # Two texts with different readability
    simple_text = "The cat sat on the mat. The dog ran in the park."
    complex_text = """
    The multifaceted implications of contemporary socioeconomic paradigms 
    necessitate comprehensive analytical frameworks that can adequately 
    address the intricate interdependencies inherent in modern institutional 
    structures.
    """
    
    print("--- Simple Text ---")
    result1 = checker.analyze(simple_text)
    print(f"Flesch Reading Ease: {result1.readability.flesch_reading_ease:.1f}")
    print(f"Grade Level: {result1.readability.flesch_kincaid_grade:.1f}")
    
    print("\n--- Complex Text ---")
    result2 = checker.analyze(complex_text)
    print(f"Flesch Reading Ease: {result2.readability.flesch_reading_ease:.1f}")
    print(f"Grade Level: {result2.readability.flesch_kincaid_grade:.1f}")
    print(f"Difficult Words: {result2.readability.difficult_words}")
    
    checker.close()


if __name__ == "__main__":
    example_basic_usage()
    example_style_analysis()
    example_readability_analysis()
