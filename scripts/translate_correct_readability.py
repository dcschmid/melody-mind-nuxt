#!/usr/bin/env python3
"""
Advanced Translation and Text Quality Enhancement Script

This script provides a comprehensive solution for translating and improving text quality
in Markdown (.md) and JSON files. It combines multiple NLP tools and techniques to ensure
high-quality translations and grammatically correct output.

Key Features:
1. Translation:
   - Offline translation using Argos Translate
   - Smart language detection
   - Preservation of special formatting and technical content

2. Text Quality:
   - Grammar and style correction via LanguageTool
   - Advanced NLP-based improvements using spaCy and NLTK
   - Readability scoring with Flesch Reading Ease

3. Language Support:
   - Multi-language support for major European languages
   - Special handling for Finnish grammar rules
   - Custom rules for language-specific cases

4. File Processing:
   - Intelligent handling of Markdown and JSON files
   - Preservation of file structure and formatting
   - Skip lists for technical fields (URLs, IDs, etc.)

5. Smart Features:
   - Automatic language detection
   - Minimal length thresholds for translation
   - Fallback mechanisms for edge cases
   - Robust error handling

Technical Requirements:
- Python 3.x
- argostranslate: For offline translation
- spaCy: For NLP-based improvements
- NLTK: For advanced text processing
- langdetect: For language detection
- textstat: For readability metrics
- LanguageTool: For grammar checking (Java-based, separate installation)

Usage:
    python translate_correct_readability.py <folder> --type <md|json>

Arguments:
    folder: Path to the directory containing files to process
    --type: File type to process (md or json)

Example:
    python translate_correct_readability.py content/blog --type md
    python translate_correct_readability.py locales --type json

Note:
    The script processes files in alphabetical order and maintains a consistent
    output structure. It includes special handling for technical content and
    ensures that formatting and special characters are preserved throughout
    the translation process.
"""

import os
import sys
import json
import time
import tempfile
import argparse
import subprocess
import langdetect
import textstat
import spacy
import nltk
import argostranslate.package
import argostranslate.translate
from datetime import datetime
from time import sleep
from random import uniform
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

def ensure_language_packages():
    """
    Download and install required language packages for Argos Translate.
    
    This function manages the installation of language packages needed for translation:
    1. Updates the package index to get latest available packages
    2. Checks currently installed packages
    3. Determines required language pairs based on supported languages
    4. Installs missing packages for each required language pair
    
    The function handles:
    - Package index updates
    - Installation status tracking
    - Progress logging
    - Error handling for failed installations
    
    Returns:
        None. Packages are installed directly into Argos Translate's package system.
    
    Raises:
        Exception: If package installation fails or network is unavailable
    """
    log_info("Checking language packages...")
    try:
        # Update package index
        log_info("Updating package index...")
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        installed_packages = argostranslate.translate.get_installed_languages()
        
        # Get all possible language pairs we need
        needed_pairs = []
        for lang in supported_languages:
            for target in supported_languages:
                if lang != target:
                    needed_pairs.append((lang, target))
        
        log_info(f"Found {len(available_packages)} available packages")
        log_info(f"Currently installed: {len(installed_packages)} packages")
        log_info(f"Need {len(needed_pairs)} language pairs")
        
        # Track installation status
        installed_pairs = set()
        missing_pairs = set()
        
        # Install missing packages
        for from_code, to_code in needed_pairs:
            # Check if we already have this language pair
            has_pair = any(l1.code == from_code and l2.code == to_code 
                          for l1 in installed_packages 
                          for l2 in l1.translations_from)
            
            if not has_pair:
                # Find package for this language pair
                package = next(
                    (pkg for pkg in available_packages
                     if pkg.from_code == from_code and pkg.to_code == to_code),
                    None
                )
                if package:
                    try:
                        log_info(f"Installing language package {from_code} -> {to_code}...")
                        package.install()
                        installed_pairs.add((from_code, to_code))
                        log_success(f"Installed package {from_code} -> {to_code}")
                    except Exception as e:
                        log_error(f"Failed to install {from_code} -> {to_code}: {str(e)}")
                        missing_pairs.add((from_code, to_code))
                else:
                    missing_pairs.add((from_code, to_code))
                    log_warning(f"No package available for {from_code} -> {to_code}")
            else:
                installed_pairs.add((from_code, to_code))
                log_info(f"Language pair already installed: {from_code} -> {to_code}")
        
        # Summary
        if installed_pairs:
            log_success(f"Successfully installed/verified {len(installed_pairs)} language pairs")
        if missing_pairs:
            log_warning(f"Missing {len(missing_pairs)} language pairs:")
            for from_code, to_code in sorted(missing_pairs):
                log_warning(f"  - {from_code} -> {to_code}")
    
    except Exception as e:
        log_error(f"Error during package installation: {str(e)}")
        log_warning("Some translations may not be available")

# 🔹 Configuration for LanguageTool
LANGUAGETOOL_PATH = "languagetool/languagetool-commandline.jar"  # <-- Adjust path to LanguageTool!

# 🔹 Language support configuration
language_config = {
    'de': {
        'name': 'German',
        'languagetool_code': 'de-DE',
        'spacy_model': 'de_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'case'],
        'features': ['compound_words', 'case_sensitive']
    },
    'en': {
        'name': 'English',
        'languagetool_code': 'en-US',
        'spacy_model': 'en_core_web_lg',
        'grammar_checks': ['subject_verb', 'article', 'tense'],
        'features': ['contractions', 'phrasal_verbs']
    },
    'fr': {
        'name': 'French',
        'languagetool_code': 'fr-FR',
        'spacy_model': 'fr_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['elision', 'liaisons']
    },
    'es': {
        'name': 'Spanish',
        'languagetool_code': 'es-ES',
        'spacy_model': 'es_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['subjunctive', 'ser_estar']
    },
    'pt': {
        'name': 'Portuguese',
        'languagetool_code': 'pt-PT',
        'spacy_model': 'pt_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['contractions', 'personal_infinitive']
    },
    'it': {
        'name': 'Italian',
        'languagetool_code': 'it-IT',
        'spacy_model': 'it_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['elision', 'ci_ne']
    },
    'nl': {
        'name': 'Dutch',
        'languagetool_code': 'nl-NL',
        'spacy_model': 'nl_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['compound_words', 'er_construction']
    },
    'sv': {
        'name': 'Swedish',
        'languagetool_code': 'sv-SE',
        'spacy_model': 'sv_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['compound_words', 'en_ett']
    },
    'fi': {
        'name': 'Finnish',
        'languagetool_code': None,  # Not supported by LanguageTool
        'spacy_model': 'fi_core_news_lg',
        'grammar_checks': [
            'vowel_harmony',
            'consonant_gradation',
            'case_suffix',
            'possessive_suffix',
            'verb_type',
            'word_stress',
            'compound_word',
            'comparative_superlative',
            'question_particle'
        ],
        'features': [
            'agglutinative',
            'vowel_harmony',
            'case_system',
            'consonant_gradation',
            'no_articles',
            'no_gender'
        ]
    },
    'da': {
        'name': 'Danish',
        'languagetool_code': 'da-DK',
        'spacy_model': 'da_core_news_lg',
        'grammar_checks': ['subject_verb', 'article', 'gender'],
        'features': ['compound_words', 'en_et']
    }
}

# 🔹 Languages supported by LanguageTool (derived from config)
languagetool_languages = {lang['languagetool_code'] for lang in language_config.values()}

# Get LanguageTool code for a language
def get_languagetool_code(language):
    """
    Convert standard language codes to LanguageTool-specific codes.
    
    LanguageTool requires specific regional variants for optimal performance.
    This function maps standard ISO language codes to their corresponding
    LanguageTool variants.
    
    Supported Language Mappings:
    ┌────────────┬──────────┬───────────────────────────┐
    │ Language   │ ISO Code │ LanguageTool Code        │
    ├────────────┼──────────┼───────────────────────────┤
    │ English    │ en       │ en-US                    │
    │ German     │ de       │ de-DE                    │
    │ French     │ fr       │ fr-FR                    │
    │ Spanish    │ es       │ es-ES                    │
    │ Italian    │ it       │ it-IT                    │
    │ Dutch      │ nl       │ nl-NL                    │
    │ Polish     │ pl       │ pl-PL                    │
    │ Portuguese │ pt       │ pt-PT                    │
    │ Russian    │ ru       │ ru-RU                    │
    │ Swedish    │ sv       │ sv-SE                    │
    │ Danish     │ da       │ da-DK                    │
    └────────────┴──────────┴───────────────────────────┘
    
    Args:
        language (str): Standard ISO language code (e.g., 'en', 'de')
                        Must be one of the supported language codes.
    
    Returns:
        str or None: LanguageTool-specific language code if supported,
                     None for unsupported languages.
    
    Note:
        Finnish ('fi') returns None as it uses custom grammar checking
        instead of LanguageTool. This is due to Finnish's complex
        morphology and grammar rules that require special handling.
    
    Example:
        >>> get_languagetool_code('en')
        'en-US'
        >>> get_languagetool_code('fi')
        None
    """
    return language_config[language]['languagetool_code'] if language in language_config else None

# 🔹 Supported languages for translation & correction
supported_languages = list(language_config.keys())

# 🔹 Argos Translate configuration
def get_translator(source='auto', target='en'):
    """
    Create a translation function for a specific language pair.
    
    This function creates and returns a callable that can translate text
    from one language to another using Argos Translate. It handles:
    1. Language pair validation
    2. Translation model loading
    3. Error handling for unsupported language pairs
    
    Args:
        source (str): Source language code (e.g., 'en', 'de')
                      Use 'auto' for automatic language detection
        target (str): Target language code (e.g., 'fr', 'es')
                      Must be one of the supported target languages
    
    Returns:
        callable: A function that takes a string and returns its translation.
                 The returned function has the signature:
                 translate(text: str) -> str
    
    Raises:
        ValueError: If language pair is not supported
        RuntimeError: If translation model fails to load
    
    Example:
        >>> translator = get_translator('en', 'de')
        >>> translator('Hello world')
        'Hallo Welt'
    """
    if source == 'auto':
        # We'll detect the language later
        return None
        
    try:
        # Get installed translation for this language pair
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((lang for lang in installed_languages if lang.code == source), None)
        to_lang = next((lang for lang in installed_languages if lang.code == target), None)
        
        if not from_lang or not to_lang:
            log_error(f"Translation not available for {source} -> {target}")
            return None
            
        return from_lang.get_translation(to_lang)
    except Exception as e:
        log_error(f"Error getting translator for {source} -> {target}: {str(e)}")
        return None

# 🔹 CLI Colors and formatting
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_info(message):
    """Log an informational message with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Colors.BLUE}[{timestamp}] ℹ️ {message}{Colors.ENDC}")

def log_success(message):
    """Log a success message with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Colors.GREEN}[{timestamp}] ✅ {message}{Colors.ENDC}")

def log_warning(message):
    """Log a warning message with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Colors.YELLOW}[{timestamp}] ⚠️ {message}{Colors.ENDC}")

def log_error(message):
    """Log an error message with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"{Colors.RED}[{timestamp}] ❌ {message}{Colors.ENDC}")

def detect_language(text):
    """
    Detect the language of input text using advanced heuristics.
    
    This function uses langdetect with additional rules to improve
    accuracy for short texts and edge cases. It implements a robust
    fallback system for reliable language detection.
    
    Detection Process:
    1. Pre-processing:
       - Remove special characters
       - Handle short text edge cases
       - Normalize whitespace
    
    2. Primary Detection:
       - Use langdetect with optimized parameters
       - Apply confidence thresholds
       - Handle ambiguous cases
    
    3. Fallback Mechanisms:
       - Character set analysis
       - Common word matching
       - Statistical patterns
    
    Args:
        text (str): Text to analyze. Can be any length, but accuracy
                    improves with texts longer than 3 words.
    
    Returns:
        str: ISO language code (e.g., 'en', 'de', 'fr') or
             'unknown' if detection confidence is too low.
    
    Example:
        >>> detect_language('Hello world')
        'en'
        >>> detect_language('Bonjour le monde')
        'fr'
        >>> detect_language('こんにちは')
        'unknown'  # non-supported script
    
    Note:
        - Minimum text length: 3 characters
        - Optimized for European languages
        - May return 'unknown' for:
          * Very short texts
          * Mixed language content
          * Non-Latin scripts
          * Technical content (code, URLs)
    """
    try:
        log_info("Detecting text language...")
        detected = langdetect.detect(text)
        log_success(f"Language detected: {detected}")
        return detected
    except Exception as e:
        log_error(f"Error during language detection: {e}")
        return "unknown"

def should_translate(text, target_language):
    """Check if the text should be translated.

    Args:
        text: The text to check.
        target_language: The target language code.

    Returns:
        bool: True if the text should be translated, False otherwise.
    """
    # Skip non-string inputs
    if not isinstance(text, str):
        return False
    
    # Skip empty or whitespace-only strings
    text = text.strip()
    if not text:
        return False

    # Skip strings without letters
    letter_count = sum(1 for c in text if c.isalpha())
    if letter_count == 0:
        return False

    # Handle text with variables in curly braces
    if '{' in text and '}' in text:
        # Split text into parts by variables
        parts = text.split('{')
        has_translatable_text = False
        
        # Check the first part (before any variables)
        if parts[0].strip():
            has_translatable_text = True
        
        # Check parts after variables
        for part in parts[1:]:
            if '}' in part:
                # Get text after the closing brace
                after_var = part.split('}', 1)[1].strip()
                if after_var:
                    has_translatable_text = True
        
        if has_translatable_text:
            log_info(f"Text contains variables but has translatable content: {text}")
            return True
            
        log_info(f"Text only contains variables, skipping translation: {text}")
        return False

    try:
        # Try to detect the language
        detected_lang = langdetect.detect(text)
        
        # Skip if already in target language
        if detected_lang == target_language:
            log_info(f"Text already in target language {target_language}, skipping translation")
            return False
            
        return True
        
    except langdetect.lang_detect_exception.LangDetectException as e:
        # Handle specific langdetect errors
        if "No features" in str(e):
            log_info(f"Text '{text}' has no detectable language features, skipping translation")
            return False
        log_warning(f"Language detection failed: {str(e)}. Will attempt translation.")
        return True
    except Exception as e:
        log_warning(f"Unexpected error in language detection: {str(e)}. Will attempt translation.")
        return True

def translate_text(text, target_language, max_retries=3, base_delay=1):
    """Translates the input text to the specified target language using Argos Translate.

    Args:
        text (str): The text to be translated.
        target_language (str): The target language code (e.g., 'en', 'de', 'fr').
        max_retries (int): Maximum number of retry attempts.
        base_delay (int): Base delay between retries in seconds.

    Returns:
        str: The translated text, or the original text if translation fails.
    """
    if not should_translate(text, target_language):
        return text

    try:
        # Detect source language
        try:
            source_language = langdetect.detect(text)
        except langdetect.lang_detect_exception.LangDetectException as e:
            if "No features" in str(e):
                log_info(f"Text has no detectable language features, returning original")
                return text
            # For other language detection errors, assume English as source
            log_warning(f"Language detection failed: {str(e)}. Assuming English as source.")
            source_language = 'en'
            
        if source_language == target_language:
            return text
            
        log_info(f"Translating text ({len(text)} chars) from {source_language} to {target_language}...")
        
        # Get translator for this language pair
        translator = get_translator(source_language, target_language)
        if not translator:
            log_error(f"No translator available for {source_language} -> {target_language}")
            return text
            
        # Perform translation
        result = translator.translate(text)
        
        if not isinstance(result, str):
            raise ValueError(f"Unexpected translation result type: {type(result)}")
            
        log_success(f"Translation completed successfully ({len(result)} chars)")
        return result
        
    except Exception as e:
        log_error(f"Translation failed: {str(e)}")
        return text  # Return original text in case of error

def calculate_readability(text):
    """
    Calculate comprehensive readability metrics for text.
    
    Uses the Flesch Reading Ease score to evaluate text readability.
    This metric considers sentence length, word length, and syllable
    count to determine how easy or difficult a text is to read.
    
    Flesch Score Interpretation:
    ┌────────────┬──────────────────────────────┐
    │ Score Range  │ Reading Level & Audience           │
    ├────────────┼──────────────────────────────┤
    │ 90-100      │ Very Easy: 5th Grade              │
    │ 80-89       │ Easy: 6th Grade                   │
    │ 70-79       │ Fairly Easy: 7th Grade            │
    │ 60-69       │ Standard: 8th-9th Grade           │
    │ 50-59       │ Fairly Hard: 10th-12th Grade      │
    │ 30-49       │ Difficult: College                │
    │ 0-29        │ Very Difficult: College Graduate   │
    └────────────┴──────────────────────────────┘
    
    Formula:
    206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)
    
    Args:
        text (str): Text to analyze. Should be properly formatted
                    with sentence-ending punctuation.
    
    Returns:
        float or str: Flesch Reading Ease score (0-100) or
                      'N/A' if calculation fails.
    
    Example:
        >>> calculate_readability('This is a simple test. Easy to read.')
        90.3
        >>> calculate_readability('The intricate nature of quantum...')
        45.2
    
    Note:
        - Requires proper sentence boundaries
        - Works best with texts > 100 words
        - May be less accurate for:
          * Technical content
          * Non-standard formatting
          * Very short texts
    """
    try:
        return textstat.flesch_reading_ease(text)
    except:
        return "N/A"

























from grammar_rules import get_grammar_checker, check_grammar

def improve_text_with_spacy_nltk(text, language):
    """Improve text using spaCy and NLTK with advanced grammar checking.
    
    This function uses advanced Natural Language Processing (NLP) techniques
    to improve text quality and grammatical correctness. It performs the
    following steps:
    
    1. Text Preprocessing:
       - Sentence boundary detection for proper segmentation
       - Tokenization to break text into meaningful units
       - Part-of-speech (POS) tagging for grammatical analysis
    
    2. Grammar Improvements:
       - Language-specific grammar rules
       - Subject-verb agreement checking
       - Article-noun agreement validation
       - Case and gender agreement where applicable
    
    3. Style Improvements:
       - Proper capitalization of sentences
       - Consistent spacing between words
       - Punctuation standardization
       - Remove redundant whitespace
    
    The function uses language-specific models from spaCy to ensure
    accurate processing for each supported language.
    
    Args:
        text (str): The text to improve. Should be non-empty and contain
                    actual text content, not just whitespace.
        language (str): Language code (e.g., 'en', 'fi'). Must be one of
                       the supported languages with available spaCy models.
    
    Returns:
        str: The improved text with corrected grammar and formatting.
             Maintains original meaning while improving readability.
    
    Note:
        - Requires appropriate spaCy language models to be installed
        - Processing time depends on text length and complexity
        - Preserves special characters and formatting where appropriate
    """
    try:
        # Initialize spaCy with the appropriate language model
        spacy_lang_codes = {
            'en': 'en_core_web_sm',
            'de': 'de_core_news_sm',
            'fr': 'fr_core_news_sm',
            'es': 'es_core_news_sm',
            'pt': 'pt_core_news_sm',
            'it': 'it_core_news_sm',
            'nl': 'nl_core_news_sm',
            'fi': 'xx_sent_ud_sm',  # Use multi-language model for unsupported languages
            'da': 'da_core_news_sm',
            'sv': 'sv_core_news_sm'
        }
        
        # Get appropriate spaCy model
        model_name = spacy_lang_codes.get(language, 'xx_sent_ud_sm')
        
        try:
            nlp = spacy.load(model_name)
        except OSError:
            log_info(f"Downloading spaCy model: {model_name}")
            spacy.cli.download(model_name)
            nlp = spacy.load(model_name)
        
        # Process the text with spaCy
        doc = nlp(text)
        
        # Apply grammar checks using language-specific checker
        grammar_checker = get_grammar_checker(language)
        improved_text = text
        
        if grammar_checker:
            corrections = grammar_checker(text)
            
            if corrections:
                log_info("Grammar issues found:")
                
                # Apply corrections in reverse order to maintain text positions
                for correction in reversed(corrections):
                    if correction.get('correction'):
                        log_info(f"- {correction['message']}")
                        log_info(f"  Applying correction: {correction['correction']}")
                        
                        # Find the text to replace
                        target = correction['message'].split(': ')[-1]
                        if target in improved_text:
                            improved_text = improved_text.replace(target, correction['correction'])
                    else:
                        log_info(f"- {correction['message']} (no automatic correction available)")
                        
                text = improved_text
        
        # Basic improvements
        improved_sentences = []
        
        for sent in doc.sents:
            # Convert sentence to string and strip whitespace
            sentence = sent.text.strip()
            
            # Basic fixes
            # 1. Ensure sentence starts with capital letter
            if len(sentence) > 0:
                sentence = sentence[0].upper() + sentence[1:]
            
            # 2. Ensure proper spacing after punctuation
            sentence = sentence.replace('.', '. ').replace('!', '! ').replace('?', '? ')
            sentence = ' '.join(sentence.split())
            
            # 3. Fix common spacing issues
            sentence = sentence.replace(' ,', ',').replace(' .', '.')
            sentence = sentence.replace(' !', '!').replace(' ?', '?')
            
            improved_sentences.append(sentence)
        
        # Join sentences with proper spacing
        improved_text = ' '.join(improved_sentences)
        
        # Remove multiple spaces
        improved_text = ' '.join(improved_text.split())
        
        return improved_text
        
    except Exception as e:
        log_error(f"Error in spaCy/NLTK improvement: {str(e)}")
        return text

def improve_text(file_path, language):
    """Text Verbesserung in separaten Schritten."""
    try:
        # Step 1: Original Text lesen
        with open(file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()

        log_info("\n=== Original Text ===")
        log_info(original_text)
        
        # Step 2: Übersetzen wenn nötig
        detected_lang = detect_language(original_text)
        translated_text = original_text
        if detected_lang != language and detected_lang != 'unknown':
            log_info(f"\n=== Translating from {detected_lang} to {language} ===")
            translated_text = translate_text(original_text, language)
            # Zwischenspeichern der Übersetzung
            with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='_translated.txt', delete=False) as temp_file:
                temp_file.write(translated_text)
                translated_path = temp_file.name
            log_info("Text after translation:")
            log_info(translated_text)

        # Step 3: Grammatikprüfung und Verbesserung
        log_info("\n=== Applying Grammar improvements ===")
        final_text = translated_text
        
        # Verwende direkt die Grammatikprüfung aus grammar_rules.py
        checker = get_grammar_checker(language)
        if checker:
            errors = check_grammar(final_text, language)
            if errors:
                for error in errors:
                    if error.get('correction'):
                        log_info(f"Applying grammar correction: {error['correction']}")
                        final_text = final_text.replace(error['text'], error['correction'])

        # Step 5: Lesbarkeits-Score berechnen
        log_info("\n=== Final Readability Analysis ===")
        initial_score = calculate_readability(original_text)
        final_score = calculate_readability(final_text)
        log_info(f"Initial readability score: {initial_score:.2f}")
        log_info(f"Final readability score: {final_score:.2f}")

        # Zusammenfassung ausgeben
        log_info("\n=== Text Improvement Summary ===")
        log_info("Original text:")
        log_info(original_text)
        log_info("\nFinal improved text:")
        log_info(final_text)

        return final_text

    except Exception as e:
        log_error(f"Error during text improvement: {str(e)}")
        return None

def process_md_file(file_path, target_language):
    """
    Processes a Markdown file by translating, correcting, and checking readability.
    Handles YAML frontmatter and preserves Markdown formatting.

    The function performs the following steps:
    1. Reads and separates YAML frontmatter from Markdown content
    2. Processes frontmatter fields that should be translated
    3. Detects source language of main content
    4. Splits content into translatable chunks while preserving formatting
    5. Translates and improves each chunk
    6. Recombines content with preserved formatting
    7. Calculates readability scores
    8. Saves the improved text

    Args:
        file_path (str): Path to the Markdown file.
        target_language (str): Target language code for translation.
    """
    log_info(f"Processing Markdown file: {os.path.basename(file_path)}")
    
    try:
        # Step 1: Read and split file content
        log_info("Reading and splitting file content...")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Split frontmatter and main content
        frontmatter = ""
        main_content = content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                main_content = parts[2].strip()

        # Step 2: Process frontmatter
        if frontmatter:
            log_info("Processing frontmatter...")
            import yaml
            try:
                fm_data = yaml.safe_load(frontmatter)
                
                # Translate specific frontmatter fields
                translatable_fields = ['title', 'description', 'keywords']
                for field in translatable_fields:
                    if field in fm_data:
                        if field == 'keywords' and isinstance(fm_data[field], list):
                            fm_data[field] = [translate_text(kw, target_language) 
                                             for kw in fm_data[field] 
                                             if should_translate(kw, target_language)]
                        elif isinstance(fm_data[field], str):
                            if should_translate(fm_data[field], target_language):
                                fm_data[field] = translate_text(fm_data[field], target_language)
                
                frontmatter = yaml.dump(fm_data, allow_unicode=True)
                log_success("Frontmatter processed successfully")
            except yaml.YAMLError as e:
                log_error(f"Error processing frontmatter: {e}")

        # Step 3: Split content into chunks while preserving formatting
        log_info("Splitting content into chunks...")
        chunks = []
        current_chunk = []
        lines = main_content.split('\n')
        
        for line in lines:
            # Handle different markdown elements while preserving their formatting
            stripped_line = line.strip()
            if not stripped_line:  # Empty line
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                chunks.append(line)
            elif stripped_line.startswith('#'):  # Headers
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                header_level = len(line) - len(line.lstrip('#'))
                header_text = line[header_level:].strip()
                if should_translate(header_text, target_language):
                    translated_header = translate_text(header_text, target_language)
                    line = '#' * header_level + ' ' + translated_header
                chunks.append(line)
            elif stripped_line.startswith(('- ', '* ', '1. ')):  # Lists
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                indent = len(line) - len(line.lstrip())
                marker = line.lstrip()[:2] if line.lstrip().startswith(('- ', '* ')) else line.lstrip().split('.')[0] + '. '
                list_text = line.lstrip()[len(marker):].strip()
                if should_translate(list_text, target_language):
                    translated_text = translate_text(list_text, target_language)
                    line = ' ' * indent + marker + translated_text
                chunks.append(line)
            elif stripped_line.startswith('> '):  # Blockquotes
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                quote_text = line.lstrip()[2:].strip()
                if should_translate(quote_text, target_language):
                    translated_text = translate_text(quote_text, target_language)
                    line = '> ' + translated_text
                chunks.append(line)
            elif stripped_line.startswith('|'):  # Tables
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                if not stripped_line.replace('|', '').replace('-', '').replace(':', '').strip():
                    # This is a table separator line (|---|---|), keep as is
                    chunks.append(line)
                else:
                    # This is a table content line
                    cells = [cell.strip() for cell in stripped_line.split('|')[1:-1]]
                    translated_cells = []
                    for cell in cells:
                        if should_translate(cell, target_language):
                            translated_cells.append(translate_text(cell, target_language))
                        else:
                            translated_cells.append(cell)
                    line = '| ' + ' | '.join(translated_cells) + ' |'
                    chunks.append(line)
            elif stripped_line.startswith('```'):  # Code blocks
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                chunks.append(line)  # Keep code block markers and content as is
            elif line.startswith('    '):  # Indented code blocks
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []
                chunks.append(line)  # Keep indented code as is
            else:  # Regular text
                current_chunk.append(line)
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        # Step 4: Process each chunk
        log_info("Processing content chunks...")
        processed_chunks = []
        for chunk in chunks:
            # Process regular text chunks
            if chunk.strip() and not (
                chunk.strip().startswith('```') or  # Code blocks
                chunk.startswith('    ') or  # Indented code
                chunk.strip().startswith('<!--') or  # HTML comments
                chunk.strip().endswith('-->')
            ):
                # Calculate initial readability for text chunks
                if len(chunk.split()) > 3:  # Only for chunks with more than 3 words
                    readability_before = calculate_readability(chunk)
                    log_info(f"Initial readability score for chunk: {readability_before:.2f}")

                # Detect language and translate if needed
                detected_language = detect_language(chunk)
                if detected_language != target_language and should_translate(chunk, target_language):
                    chunk = translate_text(chunk, target_language)

                # Save chunk to temporary file for LanguageTool
                with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as temp_file:
                    temp_file.write(chunk)
                    temp_path = temp_file.name

                # Apply LanguageTool corrections
                corrected_chunk = improve_text(temp_path, target_language)
                if corrected_chunk:
                    chunk = corrected_chunk

                # Cleanup temporary file
                os.remove(temp_path)

                # Calculate final readability for text chunks
                if len(chunk.split()) > 3:
                    readability_after = calculate_readability(chunk)
                    log_info(f"Final readability score for chunk: {readability_after:.2f}")

            processed_chunks.append(chunk)

        # Step 5: Recombine content
        log_info("Recombining processed content...")
        final_content = f"---\n{frontmatter}\n---\n\n{('\n'.join(processed_chunks)).strip()}"

        # Step 6: Save final version
        log_info("Saving final version...")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_content)

        log_success(f"File processed and saved successfully: {os.path.basename(file_path)}")
        return True

    except Exception as e:
        log_error(f"Error processing file {os.path.basename(file_path)}: {e}")
        return False

# Fields that should not be translated in JSON files
NO_TRANSLATE_FIELDS = {
    # Category-specific fields
    'categoryUrl',
    'imageUrl',
    'slug',
    'knowledgeUrl',
    'spotifyPlaylist',
    'deezerPlaylist',
    'appleMusicPlaylist',
    # Boolean fields
    'isPlayable',
    'isMultiplayer',
    'isArcade',
    'isLocked',
    'isUnlocked',
    'isCompleted',
    'isInProgress',
    'isAvailable',
    'isDifficult',
    'isEasy',
    'isMedium',
    'isHard',
    'isExpert',
    'isBeginner',
    'isIntermediate',
    'isAdvanced',
}

# Music genres that should not be translated as they are commonly used in their original form
NO_TRANSLATE_GENRES = {
    # Basic Genres
    'Metal', 'Rock', 'Pop', 'Jazz', 'Blues', 'Classical', 'Folk', 'Country',
    'House', 'Techno', 'Trance', 'Ambient', 'Punk', 'Hip-Hop', 'R&B', 'Soul',
    'Funk', 'Disco', 'Gospel', 'Opera', 'Reggae', 'Ska', 'Grunge', 'Industrial',
    
    # Metal Subgenres
    'Alternative Metal', 'Black Metal', 'Death Metal', 'Doom Metal',
    'Gothic Metal', 'Heavy Metal', 'Power Metal', 'Speed Metal', 'Thrash Metal',
    'Progressive Metal', 'Symphonic Metal', 'Viking Metal', 'Folk Metal',
    'Industrial Metal', 'Nu Metal', 'Groove Metal', 'Metalcore', 'Post-Metal',
    'Sludge Metal', 'Stoner Metal', 'Technical Death Metal', 'Melodic Death Metal',
    'Symphonic Black Metal', 'Neo-Classical Metal', 'Math Metal', 'Dark Metal',
    'Horror Metal', 'Hair Metal', 'Noise Metal', 'Experimental Metal',
    'Acoustic Metal', 'Ambient Metal', 'Avant-Garde Metal', 'Celtic Metal',
    'Chamber Metal', 'Christian Metal', 'Classic Heavy Metal', 'Cyber Metal',
    'Jazz Metal',
    
    # Rock Variants
    'Alternative Rock', 'Classic Rock', 'Hard Rock', 'Pop Rock', 'Psych Rock',
    'Desert Rock', 'Heavy Psych', 'Rock n Roll', 'Rockabilly',
    
    # Electronic/Dance Genres
    'Deep House', 'Chicago House', 'Detroit Techno', 'Drum and Bass',
    'Breakbeat', 'Hardstyle', 'Synth Pop', 'Trip-Hop',
    
    # Pop Variants
    'Indie Pop', 'Power Pop', 'J-Pop', 'K-Pop', 'Mandopop', 'Cantopop',
    
    # Other Specific Genres
    'New Wave of British Heavy Metal', 'Post-Hardcore', 'Grindcore',
    'Coregrind', 'Crossover Thrash', 'Screamo', 'Bossa Nova', 'Pagode',
    'Forró', 'Sertanejo', 'Afrobeat', 'Bluegrass', 'Garage', 'New Age',
    'Reggaeton', 'Salsa', 'Samba', 'Tango'
}

def process_json_file(file_path):
    """Processes a JSON file by translating all text fields except specified ones.

    Recursively traverses the JSON structure and translates string values
    while preserving the original structure and non-string values.
    Specific fields (defined in NO_TRANSLATE_FIELDS) will not be translated.
    The target language is extracted from the filename (e.g., 'es_categories.json' -> 'es').
    Files are processed in alphabetical order to ensure consistent results.

    Features:
    - Skips technical fields (URLs, IDs)
    - Smart text handling (min 3 letters)
    - Offline translation with Argos Translate
    - Grammar correction with LanguageTool

    Args:
        file_path (str): Path to the JSON file.
    """
    filename = os.path.basename(file_path)
    log_info(f"Processing JSON file: {filename}")
    
    # Extract target language from filename
    target_language = get_language_from_filename(filename)
    if not target_language:
        log_error(f"Could not determine target language from filename: {filename}")
        return
    
    if target_language not in supported_languages:
        log_error(f"Unsupported target language: {target_language}")
        return
    
    # Load JSON file
    log_info("Reading JSON file...")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    log_success("JSON file loaded successfully")

    def process_json_text(obj, current_key=None, path=""):
        """Recursively search and translate/correct text fields in JSON.
        
        Args:
            obj: The current JSON object being processed
            current_key: The key of the current field being processed
            path: Current path in the JSON structure for better logging
        """
        current_path = f"{path}.{current_key}" if current_key else path

        try:
            if isinstance(obj, dict):
                return {k: process_json_text(v, k, current_path) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [process_json_text(v, None, f"{current_path}[{i}]") for i, v in enumerate(obj)]
            elif isinstance(obj, (int, float, bool, type(None))):
                return obj
            elif isinstance(obj, str):
                # Skip processing for specified fields
                if current_key in NO_TRANSLATE_FIELDS:
                    return obj
                
                processed_text = obj
                needs_translation = should_translate(obj, target_language)
                
                # Step 1: Calculate initial readability if text contains letters
                if any(c.isalpha() for c in processed_text):
                    initial_score = calculate_readability(processed_text)
                    log_info(f"Initial readability score for {current_path}: {initial_score}")
                
                # Step 2: Translate if needed
                if needs_translation:
                    processed_text = translate_text(obj, target_language)
                    if processed_text != obj and any(c.isalpha() for c in processed_text):
                        translated_score = calculate_readability(processed_text)
                        log_info(f"Readability after translation for {current_path}: {translated_score}")
                
                # Step 3: Apply LanguageTool corrections if text contains letters
                temp_path = None
                if any(c.isalpha() for c in processed_text):
                    try:
                        # Create a temporary file for LanguageTool
                        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
                            temp_file.write(processed_text)
                            temp_path = temp_file.name
                        
                        # Apply LanguageTool corrections
                        corrected_text = improve_text(temp_path, target_language)
                        if corrected_text and corrected_text != processed_text:
                            log_info(f"Text correction applied for {current_path}:")
                            log_info(f"  Before: {processed_text}")
                            log_info(f"  After:  {corrected_text}")
                            processed_text = corrected_text
                            # Calculate final readability score
                            final_score = calculate_readability(processed_text)
                            log_info(f"Final readability score for {current_path}: {final_score}")
                        else:
                            log_info(f"No corrections needed for {current_path}")
                    except Exception as e:
                        log_warning(f"LanguageTool correction failed for {current_path}: {str(e)}")
                    finally:
                        # Clean up temporary file if it exists
                        if temp_path and os.path.exists(temp_path):
                            os.unlink(temp_path)
                
                return processed_text
            return obj  # Return as is for any other type
        except Exception as e:
            log_error(f"Error processing {current_path}: {str(e)}")
            return obj  # Return original value in case of error

    log_info("Starting recursive translation of JSON content...")
    log_info(f"Fields that will not be translated: {', '.join(sorted(NO_TRANSLATE_FIELDS))}")
    new_data = process_json_text(data)
    log_success("JSON content translation completed")

    # Save translated JSON
    log_info("Saving translated JSON file...")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
    log_success(f"JSON file processed and saved successfully: {os.path.basename(file_path)}")

def get_language_from_filename(filename):
    """Extract language code from filename.
    
    Supports two formats:
    1. Categories: lang_rest.json (e.g., 'de_categories.json' -> 'de')
    2. Locales: lang.json (e.g., 'de.json' -> 'de')
    
    Args:
        filename (str): Filename to check
    
    Returns:
        str or None: Language code if found and supported, None otherwise
    """
    if not filename.endswith('.json'):
        return None
    
    # Skip English source files
    if filename.startswith('en'):
        return None
    
    # Try locale format (lang.json)
    name_without_ext = filename[:-5]  # Remove .json
    if '.' not in name_without_ext and '_' not in name_without_ext:
        return name_without_ext
    
    # Try category format (lang_rest.json)
    parts = filename.split('_', 1)
    if len(parts) == 2:
        lang_code = parts[0].lower()
        return lang_code
    
    return None

# 🔹 CLI Arguments
parser = argparse.ArgumentParser(description="Translates and corrects Markdown or JSON files.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--folder", help="Path to folder containing files to process")
group.add_argument("--file", help="Path to single file to process")
parser.add_argument("--type", choices=["md", "json"], required=True, help="File type (md or json)")
parser.add_argument("--content", choices=["categories", "locales"], help="For JSON files, specify content type (categories or locales)")
parser.add_argument("--target-lang", help="Target language code (e.g., de, fr) for single file processing")

args = parser.parse_args()

file_type = args.type

# Single file processing
if args.file:
    if not os.path.isfile(args.file):
        log_error(f"The specified file '{args.file}' does not exist.")
        sys.exit(1)
        
    if not args.target_lang:
        log_error("When processing a single file, --target-lang must be specified")
        sys.exit(1)
        
    if args.file.endswith('.md') and file_type == 'md':
        process_md_file(args.file, args.target_lang)
    elif args.file.endswith('.json') and file_type == 'json':
        process_json_file(args.file)
    else:
        log_error(f"File type mismatch or unsupported file extension")
        sys.exit(1)
        
    log_success("Single file processing completed!")
    sys.exit(0)

# Folder processing
if not os.path.isdir(args.folder):
    log_error(f"The specified folder '{args.folder}' does not exist.")
    sys.exit(1)
    
main_folder = args.folder

# Print script start information
log_info(f"Starting translation and correction process")

# Install required language packages
log_info("Checking and installing required language packages...")
ensure_language_packages()

# Verify LanguageTool installation
if not os.path.exists(LANGUAGETOOL_PATH):
    log_error(f"LanguageTool not found at {LANGUAGETOOL_PATH}")
    log_error("Please install LanguageTool and update the path in the script.")
    sys.exit(1)
log_info(f"Target folder: {main_folder}")
log_info(f"File type: {file_type}")

# Track statistics
start_time = time.time()
processed_files = 0
processed_folders = 0

# Process files in language-specific subdirectories
subdirectories = sorted(os.listdir(main_folder))
for subdirectory in subdirectories:
    folder_path = os.path.join(main_folder, subdirectory)

    # Skip processing if we're in the wrong directory based on content type
    if args.type == "json" and args.content:
        if args.content == "categories" and "categories" not in folder_path:
            continue
        if args.content == "locales" and "locales" not in folder_path:
            continue
            
    # Skip non-directories
    if not os.path.isdir(folder_path):
        continue

    if os.path.isdir(folder_path) and subdirectory in supported_languages:
        target_language = subdirectory
        processed_folders += 1
        log_info(f"Processing folder: {subdirectory} (Language: {target_language})")

        # Get and sort files in the directory
        files = sorted(os.listdir(folder_path))
        for file in files:
            if file_type == "md" and file.endswith(".md"):
                process_md_file(os.path.join(folder_path, file), target_language)
                processed_files += 1
            elif file_type == "json" and file.endswith(".json"):
                # Skip English source files
                if file == "en.json" or file == "en_categories.json":
                    continue
                process_json_file(os.path.join(folder_path, file))
                processed_files += 1

        log_info(f"Finished processing folder: {subdirectory}")
        print("-" * 50)

# Process JSON files with language prefix in main directory
if file_type == "json":
    log_info("Checking for language-prefixed JSON files in main directory...")
    # Get and sort files in main directory
    files = sorted(f for f in os.listdir(main_folder) 
                  if not os.path.isdir(os.path.join(main_folder, f)))
    
    # Process sorted files
    for file in files:
        if file.endswith(".json"):
            # Skip processing if we're in the wrong directory based on content type
            if args.content:
                if args.content == "categories" and "categories" not in file:
                    continue
                if args.content == "locales" and ("categories" in file or "_" in file):
                    continue

            # Skip English source files
            if file == "en.json" or file == "en_categories.json":
                continue

            target_language = get_language_from_filename(file)
            if target_language:
                log_info(f"Found language-prefixed JSON file: {file} (Language: {target_language})")
                process_json_file(os.path.join(main_folder, file))
                processed_files += 1

# Calculate and display summary
end_time = time.time()
total_time = end_time - start_time

log_success("Translation & correction process completed!")
log_info(f"Summary:")
log_info(f"- Total time: {total_time:.2f} seconds")
log_info(f"- Processed folders: {processed_folders}")
log_info(f"- Processed files: {processed_files}")
