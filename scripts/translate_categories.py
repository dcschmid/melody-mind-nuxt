#!/usr/bin/env python3
"""
Category Translation Script for MelodyMind

This script handles the translation of music category descriptions across multiple languages
using OpenAI's GPT-4 model. It maintains consistent terminology and style while preserving
the musical context and cultural nuances in each target language.

Features:
- Supports multiple target languages (German, Spanish, French, Italian, etc.)
- Preserves specialized music terminology
- Maintains language-specific formatting and style guidelines
- Handles incremental updates to avoid re-translating existing content
- Provides detailed progress tracking and error handling

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key for accessing the translation service

Usage:
    python translate_categories.py [--update] [--input INPUT_FILE]

Options:
    --update            Only translate new or modified categories
    --input INPUT_FILE  Path to English categories file
                        (default: app/json/en_categories.json)
"""

import json
import os
from openai import OpenAI
from pathlib import Path
import time
import argparse
from typing import Dict, List, Any, Optional, Union

def load_json_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file to load
        
    Returns:
        Parsed JSON content as a list of dictionaries
        
    Raises:
        JSONDecodeError: If the file contains invalid JSON
        FileNotFoundError: If the file doesn't exist
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: List[Dict[str, Any]], file_path: Union[str, Path]) -> None:
    """Save data to a JSON file with proper formatting.
    
    Args:
        data: List of dictionaries to save
        file_path: Path where to save the JSON file
        
    Notes:
        - Uses UTF-8 encoding to preserve special characters
        - Formats JSON with indentation for readability
        - Preserves non-ASCII characters in output
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def should_translate_headline(headline: str) -> bool:
    """Determine if a headline should be translated based on content.
    
    Currently configured to translate all headlines, with proper handling
    of special terms managed through language-specific translation instructions.
    
    Args:
        headline: The headline text to evaluate
        
    Returns:
        True for all headlines, as we handle special cases in the translation prompt
    """
    # Always return True to translate all categories
    # We'll ensure proper translations through the translation prompt
    return True

def get_language_specific_instructions(target_language: str) -> str:
    """Get language-specific translation instructions"""
    instructions = {
        "English": (
            "For nationality/language categories, use adjectival forms (e.g., 'Argentine music' not 'Argentinian', 'Colombian' not 'Columbian'). "
            "Ensure proper capitalization of nationality terms. "
            "Use natural English expressions and musical terminology."
        ),
        "German": (
            "Übersetze den Text von Englisch ins Deutsche unter Beachtung dieser Richtlinien:\n"
            "1. Verwende natürliche und idiomatische deutsche Formulierungen.\n"
            "2. Bei Musikgenres und -stilen:\n"
            "   - Etablierte Genrenamen bleiben auf Englisch (z.B. 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Beschreibende Begriffe werden sinnvoll übersetzt (z.B. 'Alternative' → 'Alternative', 'Electronic' → 'Elektronisch')\n"
            "   - Bei zusammengesetzten Begriffen: Genreteil bleibt Englisch, Beschreibung wird übersetzt (z.B. 'Modern Rock' → 'Moderner Rock')\n"
            "3. Bei kulturellen und regionalen Begriffen:\n"
            "   - Verwende etablierte deutsche Bezeichnungen (z.B. 'French Music' → 'Französische Musik')\n"
            "   - Eigennamen bleiben unverändert\n"
            "4. Bei Stimmungen und beschreibenden Kategorien:\n"
            "   - Übersetze in natürliche deutsche Entsprechungen (z.B. 'Happy' → 'Fröhlich', 'Relaxed' → 'Entspannt')\n"
            "5. Bei Jahrzehnten und Zeiträumen:\n"
            "   - Verwende das deutsche Standardformat (z.B. '1980s' → '1980er')"
        ),
        "French": (
            "Traduisez le texte de l'anglais vers le français en suivant ces directives:\n"
            "1. Utilisez des expressions naturelles et idiomatiques en français.\n"
            "2. Pour les genres et styles musicaux:\n"
            "   - Conservez les noms de genres établis en anglais (ex: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Traduisez les termes descriptifs de manière appropriée (ex: 'Alternative' → 'Alternatif', 'Electronic' → 'Électronique')\n"
            "   - Pour les termes composés: gardez le genre en anglais, traduisez le descriptif (ex: 'Modern Rock' → 'Rock Moderne')\n"
            "3. Pour les termes culturels et régionaux:\n"
            "   - Utilisez les termes français établis (ex: 'French Music' → 'Musique Française')\n"
            "   - Conservez les noms propres inchangés\n"
            "4. Pour les ambiances et catégories descriptives:\n"
            "   - Traduisez avec des équivalents naturels en français (ex: 'Happy' → 'Joyeux', 'Relaxed' → 'Détendu')\n"
            "5. Pour les décennies et périodes:\n"
            "   - Utilisez le format français standard (ex: '1980s' → 'Années 80')"
        ),
        "Spanish": (
            "Traduce el texto del inglés al español siguiendo estas pautas:\n"
            "1. Utiliza expresiones naturales e idiomáticas en español.\n"
            "2. Para géneros y estilos musicales:\n"
            "   - Mantén los nombres de géneros establecidos en inglés (ej: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Traduce los términos descriptivos de manera apropiada (ej: 'Alternative' → 'Alternativo', 'Electronic' → 'Electrónico')\n"
            "   - Para términos compuestos: mantén el género en inglés, traduce el descriptivo (ej: 'Modern Rock' → 'Rock Moderno')\n"
            "3. Para términos culturales y regionales:\n"
            "   - Utiliza los términos españoles establecidos (ej: 'French Music' → 'Música Francesa')\n"
            "   - Mantén los nombres propios sin cambios\n"
            "4. Para estados de ánimo y categorías descriptivas:\n"
            "   - Traduce con equivalentes naturales en español (ej: 'Happy' → 'Alegre', 'Relaxed' → 'Relajado')\n"
            "5. Para décadas y períodos:\n"
            "   - Utiliza el formato estándar español (ej: '1980s' → 'Años 80')"
        ),
        "Italian": (
            "Traduci il testo dall'inglese all'italiano seguendo queste linee guida:\n"
            "1. Utilizza espressioni naturali e idiomatiche in italiano.\n"
            "2. Per generi e stili musicali:\n"
            "   - Mantieni i nomi dei generi stabiliti in inglese (es: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Traduci i termini descrittivi in modo appropriato (es: 'Alternative' → 'Alternativo', 'Electronic' → 'Elettronico')\n"
            "   - Per termini composti: mantieni il genere in inglese, traduci il descrittivo (es: 'Modern Rock' → 'Rock Moderno')\n"
            "3. Per termini culturali e regionali:\n"
            "   - Utilizza i termini italiani stabiliti (es: 'French Music' → 'Musica Francese')\n"
            "   - Mantieni i nomi propri invariati\n"
            "4. Per stati d'animo e categorie descrittive:\n"
            "   - Traduci con equivalenti naturali in italiano (es: 'Happy' → 'Felice', 'Relaxed' → 'Rilassato')\n"
            "5. Per decenni e periodi:\n"
            "   - Utilizza il formato standard italiano (es: '1980s' → 'Anni '80')"
        ),
        "Portuguese": (
            "Traduza o texto do inglês para o português seguindo estas diretrizes:\n"
            "1. Utilize expressões naturais e idiomáticas em português.\n"
            "2. Para gêneros e estilos musicais:\n"
            "   - Mantenha os nomes de gêneros estabelecidos em inglês (ex: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Traduza os termos descritivos de forma apropriada (ex: 'Alternative' → 'Alternativo', 'Electronic' → 'Eletrônico')\n"
            "   - Para termos compostos: mantenha o gênero em inglês, traduza o descritivo (ex: 'Modern Rock' → 'Rock Moderno')\n"
            "3. Para termos culturais e regionais:\n"
            "   - Utilize os termos portugueses estabelecidos (ex: 'French Music' → 'Música Francesa')\n"
            "   - Mantenha os nomes próprios inalterados\n"
            "4. Para estados de ânimo e categorias descritivas:\n"
            "   - Traduza com equivalentes naturais em português (ex: 'Happy' → 'Feliz', 'Relaxed' → 'Relaxado')\n"
            "5. Para décadas e períodos:\n"
            "   - Utilize o formato padrão português (ex: '1980s' → 'Anos 80')"
        ),
        "Chinese": (
            "请按以下准则将文本从英语翻译成中文：\n"
            "1. 使用自然、地道的中文表达。\n"
            "2. 对于音乐流派和风格：\n"
            "   - 保留已经确立的英文流派名称（如：'Heavy Metal'、'Rock'、'Jazz'、'Blues'）\n"
            "   - 将描述性术语适当翻译（如：'Alternative' → '另类'，'Electronic' → '电子'）\n"
            "   - 对于组合术语：保留英文流派名，翻译描述词（如：'Modern Rock' → '现代Rock'）\n"
            "3. 对于文化和地区相关术语：\n"
            "   - 使用中文习用表达（如：'French Music' → '法国音乐'）\n"
            "   - 保持专有名词不变\n"
            "4. 对于心情和描述性类别：\n"
            "   - 使用自然的中文对应词（如：'Happy' → '欢乐'，'Relaxed' → '轻松'）\n"
            "5. 对于年代和时期：\n"
            "   - 使用中文标准格式（如：'1980s' → '80年代'）"
        ),

        "Arabic": (
            "يرجى ترجمة النص من الإنجليزية إلى العربية وفقاً للإرشادات التالية:\n"
            "1. استخدم تعبيرات عربية طبيعية واصطلاحية.\n"
            "2. للأنواع والأساليب الموسيقية:\n"
            "   - احتفظ بأسماء الأنواع المعتمدة بالإنجليزية (مثل: 'Heavy Metal'، 'Rock'، 'Jazz'، 'Blues')\n"
            "   - ترجم المصطلحات الوصفية بشكل مناسب (مثل: 'Alternative' → 'بديل'، 'Electronic' → 'إلكتروني')\n"
            "   - للمصطلحات المركبة: احتفظ باسم النوع بالإنجليزية، وترجم الوصف (مثل: 'Modern Rock' → 'Rock الحديث')\n"
            "3. للمصطلحات الثقافية والإقليمية:\n"
            "   - استخدم التعبيرات العربية المعتمدة (مثل: 'French Music' → 'الموسيقى الفرنسية')\n"
            "   - احتفظ بالأسماء الخاصة دون تغيير\n"
            "4. للمزاج والفئات الوصفية:\n"
            "   - استخدم مقابلات عربية طبيعية (مثل: 'Happy' → 'سعيد'، 'Relaxed' → 'مسترخي')\n"
            "5. للعقود والفترات الزمنية:\n"
            "   - استخدم الصيغة العربية القياسية (مثل: '1980s' → 'ثمانينيات القرن العشرين')"
        ),
        "Russian": (
            "Пожалуйста, переведите текст с английского на русский, следуя этим указаниям:\n"
            "1. Используйте естественные и идиоматические русские выражения.\n"
            "2. Для музыкальных жанров и стилей:\n"
            "   - Сохраняйте устоявшиеся названия жанров на английском (например: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - Переводите описательные термины подходящим образом (например: 'Alternative' → 'Альтернативный', 'Electronic' → 'Электронный')\n"
            "   - Для составных терминов: сохраняйте название жанра на английском, переводите описание (например: 'Modern Rock' → 'Современный Rock')\n"
            "3. Для культурных и региональных терминов:\n"
            "   - Используйте устоявшиеся русские выражения (например: 'French Music' → 'Французская музыка')\n"
            "   - Сохраняйте имена собственные без изменений\n"
            "4. Для настроений и описательных категорий:\n"
            "   - Используйте естественные русские эквиваленты (например: 'Happy' → 'Радостный', 'Relaxed' → 'Расслабленный')\n"
            "5. Для десятилетий и периодов:\n"
            "   - Используйте стандартный русский формат (например: '1980s' → '1980-е')"
        )
    }
    return instructions.get(target_language, "")

def translate_text(client: OpenAI, text: str, target_language: str) -> Optional[str]:
    """Translate text using OpenAI's GPT-4 model with language-specific guidelines.
    
    Uses a specialized system prompt that includes:
    1. Language-specific translation instructions
    2. Musical terminology handling guidelines
    3. Cultural context preservation rules
    
    Args:
        client: Initialized OpenAI client
        text: Source text to translate (in English)
        target_language: Target language name (e.g., 'German', 'Spanish')
        
    Returns:
        Translated text if successful, None if translation fails
        
    Raises:
        Any exceptions from the OpenAI API are caught and logged
    """
    try:
        language_instructions = get_language_specific_instructions(target_language)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are a professional translator specializing in {target_language}. "
                        f"Translate the following text to {target_language}, ensuring:"
                        f"\n1. Natural flow and readability in {target_language}"
                        f"\n2. Proper use of language-specific idioms and expressions"
                        f"\n3. Correct grammar and syntax specific to {target_language}"
                        f"\n4. Cultural appropriateness and context awareness"
                        f"\n\nLanguage-specific guidelines:\n{language_instructions}"
                        f"\n\nOnly respond with the translation, nothing else."
                    )
                },
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

def get_category_key(category: Dict[str, Any]) -> str:
    """Generate a unique key for a category based on its URL.
    
    Uses the categoryUrl as a unique identifier since it remains constant
    across all language versions of the same category.
    
    Args:
        category: Dictionary containing category data
        
    Returns:
        Category URL as string, or empty string if URL not found
    """
    return category.get('categoryUrl', '')

def load_existing_translations(output_dir: Path, lang_code: str) -> Dict[str, Dict[str, Any]]:
    """Load existing translations from a language-specific JSON file.
    
    Attempts to load and parse existing translations, creating a lookup
    dictionary keyed by category URL for efficient access.
    
    Args:
        output_dir: Directory containing translation files
        lang_code: Language code (e.g., 'de', 'es')
        
    Returns:
        Dictionary mapping category URLs to their translated content,
        or empty dict if file doesn't exist or can't be loaded
        
    Notes:
        - Handles missing files gracefully
        - Reports but doesn't raise file access/parsing errors
    """
    translation_file = output_dir / f"{lang_code}_categories.json"
    if translation_file.exists():
        try:
            categories = load_json_file(translation_file)
            return {get_category_key(cat): cat for cat in categories}
        except Exception as e:
            print(f"Warning: Could not load existing translations for {lang_code}: {e}")
    return {}

def get_missing_categories(source_categories: List[Dict[str, Any]], 
                        existing_translations: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find categories that exist in source but not in target language.
    
    Compares source categories against existing translations to identify
    categories that need to be translated for the first time.
    
    Args:
        source_categories: List of categories from source language
        existing_translations: Dict of existing translations keyed by URL
        
    Returns:
        List of categories that need translation
        
    Notes:
        Uses category URLs as unique identifiers for comparison
    """
    missing = []
    for category in source_categories:
        category_key = get_category_key(category)
        if category_key not in existing_translations:
            missing.append(category)
    return missing

def save_progress(categories: List[Dict[str, Any]], output_file: Path, lang_code: str) -> None:
    """Save current translation progress to a JSON file.
    
    Saves the current state of translations to allow for recovery
    in case of interruption and to track progress.
    
    Args:
        categories: List of category dictionaries to save
        output_file: Path where to save the progress file
        lang_code: Language code for progress reporting
        
    Notes:
        - Creates parent directories if they don't exist
        - Reports but doesn't raise save errors
        - Uses UTF-8 encoding for proper character handling
    """
    try:
        save_json_file(categories, output_file)
        print(f"Progress saved for {lang_code}")
    except Exception as e:
        print(f"Warning: Could not save progress for {lang_code}: {e}")

def translate_categories(input_file: str, target_languages: Dict[str, str], update_mode: bool = False) -> None:
    """Main function to translate categories into multiple target languages.
    
    Processes each category in the source file, translating content into
    specified target languages while preserving special formatting and
    maintaining consistency in musical terminology.
    
    Args:
        input_file: Path to source language (English) categories file
        target_languages: Dict mapping language codes to language names
        update_mode: If True, only translate new or modified categories
        
    Notes:
        - Uses OpenAI API for translations
        - Implements rate limiting to avoid API throttling
        - Saves progress after each category translation
        - Preserves existing translations in update mode
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
    """
    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    client = OpenAI(api_key=api_key)
    
    # Load the English categories
    categories = load_json_file(input_file)
    if not categories:
        print(f"Error: Could not load source categories from {input_file}")
        return
    
    # Create output directory if it doesn't exist
    output_dir = Path(input_file).parent
    
    # Process each target language
    for lang_code, lang_name in target_languages.items():
        if lang_code == 'en':
            continue  # Skip English as it's our source language
            
        print(f"\nProcessing {lang_name} ({lang_code})...")
        
        # Define output file path
        output_file = output_dir / f"{lang_code}_categories.json"
        
        # If file doesn't exist, copy English file first
        if not output_file.exists():
            print(f"Creating initial {lang_code}_categories.json from English source...")
            save_json_file(categories, output_file)
        
        # Load current state of translations
        current_translations = load_json_file(output_file)
        
        # Find categories that need translation (still in English)
        needs_translation = []
        for cat in current_translations:
            # Check if the category is still in English by comparing with source
            for src_cat in categories:
                if cat['categoryUrl'] == src_cat['categoryUrl']:
                    if cat['headline'] == src_cat['headline'] or \
       cat['introSubline'] == src_cat['introSubline'] or \
       cat['text'] == src_cat['text']:
                        needs_translation.append(cat)
                    break
        
        if not needs_translation:
            print(f"All categories are already translated for {lang_name}")
            continue

        print(f"Found {len(needs_translation)} categories that need translation")

        # Translate each category that needs translation
        for idx, category in enumerate(needs_translation, 1):
            print(f"\nTranslating category {idx}/{len(needs_translation)}: {category['headline']}")

            try:
                # Find index of this category in current_translations
                current_idx = next(i for i, cat in enumerate(current_translations) 
                                  if cat['categoryUrl'] == category['categoryUrl'])
                
                # Create working copy
                working_category = category.copy()
                
                # Translate fields
                if should_translate_headline(category['headline']):
                    print("Translating headline...")
                    translated_headline = translate_text(client, category['headline'], lang_name)
                    if translated_headline:
                        working_category['headline'] = translated_headline

                print("Translating introSubline...")
                translated_subline = translate_text(client, category['introSubline'], lang_name)
                if translated_subline:
                    working_category['introSubline'] = translated_subline

                print("Translating main text...")
                translated_text = translate_text(client, category['text'], lang_name)
                if translated_text:
                    working_category['text'] = translated_text

                # Update in current_translations
                current_translations[current_idx] = working_category
                
                # Save progress after each successful category translation
                save_json_file(current_translations, output_file)
                print(f"Saved progress for {working_category['headline']}")

            except Exception as e:
                print(f"Error translating category {category['headline']}: {e}")
                continue

            # Sleep to avoid rate limiting
            time.sleep(1)

        print(f"\nCompleted translations for {lang_name}")

def main() -> None:
    """Entry point for the category translation script.
    
    Parses command line arguments and initiates the translation process
    for all configured target languages. Handles the overall execution
    flow and error reporting.
    
    Command Line Arguments:
        --update: Run in update mode (only translate new/modified categories)
        --input: Path to source English categories file
        
    Environment Variables Required:
        OPENAI_API_KEY: API key for OpenAI services
        
    Exit Codes:
        0: Successful completion
        1: Error during execution
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Translate category files to multiple languages')
    parser.add_argument('--update', action='store_true', 
                      help='Update mode: only translate new or modified categories')
    parser.add_argument('--input', default='app/json/en_categories.json',
                      help='Path to the English categories file (default: app/json/en_categories.json)')
    args = parser.parse_args()
    
    # Dictionary of language codes to full names
    target_languages = {
        "de": "German",
        "es": "Spanish",
        "fr": "French",
        "it": "Italian",
        "pt": "Portuguese"
    }
    
    try:
        translate_categories(args.input, target_languages, args.update)
        print("\nTranslation completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
