#!/usr/bin/env python3
"""
Command-line interface for WriteWise grammar checker.
"""

import argparse
import sys
from pathlib import Path

from writewise.core.grammar_checker import GrammarChecker


def print_separator():
    """Print a visual separator."""
    print("=" * 80)


def format_score_color(score):
    """Return colored score based on value."""
    if score >= 90:
        return f"\033[92m{score:.1f}\033[0m"  # Green
    elif score >= 75:
        return f"\033[93m{score:.1f}\033[0m"  # Yellow
    else:
        return f"\033[91m{score:.1f}\033[0m"  # Red


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WriteWise - Advanced Grammar Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  writewise check "Your text here"
  writewise check --file document.txt
  writewise check --file document.txt --correct
  writewise check --file document.txt --output corrected.txt
        """
    )
    
    parser.add_argument(
        "command",
        choices=["check", "correct"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to check (or use --file)"
    )
    
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="File to check"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file for corrected text"
    )
    
    parser.add_argument(
        "--correct",
        action="store_true",
        help="Auto-correct grammar issues"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Get text to analyze
    if args.file:
        if not args.file.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        text = args.file.read_text(encoding='utf-8')
    elif args.text:
        text = args.text
    else:
        print("Error: Please provide text or use --file option", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Initialize checker
    print("Initializing WriteWise Grammar Checker...")
    checker = GrammarChecker()
    
    try:
        if args.command == "correct":
            # Just correct the text
            print("Correcting text...")
            corrected = checker.correct_text(text)
            
            if args.output:
                args.output.write_text(corrected, encoding='utf-8')
                print(f"✓ Corrected text saved to: {args.output}")
            else:
                print_separator()
                print("CORRECTED TEXT:")
                print_separator()
                print(corrected)
        
        else:  # check command
            print("Analyzing text...")
            result = checker.analyze(text)
            
            # Print summary
            print_separator()
            print("ANALYSIS SUMMARY")
            print_separator()
            print(f"Quality Score: {format_score_color(result.score)}/100")
            print(f"Word Count: {result.word_count}")
            print(f"Sentence Count: {result.sentence_count}")
            print(f"Character Count: {result.character_count}")
            print(f"Grammar Issues: {len(result.grammar_issues)}")
            print(f"Style Suggestions: {len(result.style_suggestions)}")
            
            # Print grammar issues
            if result.grammar_issues:
                print_separator()
                print("GRAMMAR ISSUES")
                print_separator()
                for i, issue in enumerate(result.grammar_issues, 1):
                    severity_marker = "❌" if issue.severity == "error" else "⚠️"
                    print(f"\n{severity_marker} Issue {i}: {issue.message}")
                    print(f"   Category: {issue.category}")
                    print(f"   Context: ...{issue.context}...")
                    if issue.suggestions:
                        print(f"   Suggestions: {', '.join(issue.suggestions[:3])}")
                    if args.verbose:
                        print(f"   Rule ID: {issue.rule_id}")
                        print(f"   Position: {issue.offset} (length {issue.length})")
            
            # Print style suggestions
            if result.style_suggestions:
                print_separator()
                print("STYLE SUGGESTIONS")
                print_separator()
                for i, sug in enumerate(result.style_suggestions, 1):
                    print(f"\n💡 Suggestion {i}: {sug.message}")
                    print(f"   Category: {sug.category}")
                    print(f"   Original: {sug.original}")
                    print(f"   Suggestion: {sug.suggestion}")
                    if args.verbose:
                        print(f"   Position: {sug.offset} (length {sug.length})")
            
            # Print readability metrics
            print_separator()
            print("READABILITY METRICS")
            print_separator()
            print(f"Flesch Reading Ease: {result.readability.flesch_reading_ease:.1f}")
            print(f"Flesch-Kincaid Grade: {result.readability.flesch_kincaid_grade:.1f}")
            print(f"Gunning Fog Index: {result.readability.gunning_fog:.1f}")
            print(f"SMOG Index: {result.readability.smog_index:.1f}")
            print(f"Difficult Words: {result.readability.difficult_words}")
            print(f"Reading Time: {result.readability.reading_time_minutes:.1f} minutes")
            
            # Auto-correct if requested
            if args.correct:
                print_separator()
                print("AUTO-CORRECTED TEXT")
                print_separator()
                corrected = checker.correct_text(text)
                
                if args.output:
                    args.output.write_text(corrected, encoding='utf-8')
                    print(f"✓ Corrected text saved to: {args.output}")
                else:
                    print(corrected)
            
            # Final message
            print_separator()
            if len(result.grammar_issues) == 0 and len(result.style_suggestions) == 0:
                print("✅ Excellent! No issues found.")
            else:
                print(f"Found {len(result.grammar_issues)} grammar issues and {len(result.style_suggestions)} style suggestions.")
    
    finally:
        checker.close()


if __name__ == "__main__":
    main()
