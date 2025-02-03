import json
import os
from openai import OpenAI
from pathlib import Path
import time
import argparse
from typing import Dict, List, Any

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def should_translate_headline(headline: str) -> bool:
    """Determine if a headline should be translated based on content"""
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
        "Japanese": (
            "以下のガイドラインに従って英語から日本語に翻訳してください：\n"
            "1. 自然で慣用的な日本語表現を使用してください。\n"
            "2. 音楽のジャンルとスタイルについて：\n"
            "   - 確立されたジャンル名は英語のまま保持（例：'Heavy Metal'、'Rock'、'Jazz'、'Blues'）\n"
            "   - 説明的な用語は適切に翻訳（例：'Alternative' → 'オルタナティブ'、'Electronic' → 'エレクトロニック'）\n"
            "   - 複合用語の場合：ジャンル名は英語のまま、説明部分を翻訳（例：'Modern Rock' → 'モダンRock'）\n"
            "3. 文化や地域に関する用語：\n"
            "   - 日本語で確立された表現を使用（例：'French Music' → 'フランス音楽'）\n"
            "   - 固有名詞は変更しない\n"
            "4. ムードや説明的なカテゴリー：\n"
            "   - 自然な日本語の対応語を使用（例：'Happy' → 'ハッピー'、'Relaxed' → 'リラックス'）\n"
            "5. 年代や時代について：\n"
            "   - 日本語の標準的な形式を使用（例：'1980s' → '1980年代'）"
        ),
        "Korean": (
            "다음 지침에 따라 영어에서 한국어로 번역해 주세요:\n"
            "1. 자연스럽고 관용적인 한국어 표현을 사용하세요.\n"
            "2. 음악 장르와 스타일에 대해:\n"
            "   - 확립된 장르명은 영어 그대로 유지(예: 'Heavy Metal', 'Rock', 'Jazz', 'Blues')\n"
            "   - 설명적인 용어는 적절히 번역(예: 'Alternative' → '대안', 'Electronic' → '전자')\n"
            "   - 복합 용어의 경우: 장르명은 영어 그대로, 설명부를 번역(예: 'Modern Rock' → '모던 Rock')\n"
            "3. 문화와 지역 관련 용어:\n"
            "   - 한국어로 확립된 표현 사용(예: 'French Music' → '프랑스 음악')\n"
            "   - 고유명사는 변경하지 않음\n"
            "4. 분위기와 설명적 카테고리:\n"
            "   - 자연스러운 한국어 대응어 사용(예: 'Happy' → '행복한', 'Relaxed' → '편안한')\n"
            "5. 연대와 시대 표현:\n"
            "   - 한국어 표준 형식 사용(예: '1980s' → '1980년대')"
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

def translate_text(client, text, target_language):
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
    """Generate a unique key for a category based on its URL"""
    return category.get('categoryUrl', '')

def load_existing_translations(output_dir: Path, lang_code: str) -> Dict[str, Dict[str, Any]]:
    """Load existing translations if they exist"""
    translation_file = output_dir / f"{lang_code}_categories.json"
    if translation_file.exists():
        try:
            categories = load_json_file(translation_file)
            return {get_category_key(cat): cat for cat in categories}
        except Exception as e:
            print(f"Warning: Could not load existing translations for {lang_code}: {e}")
    return {}

def get_missing_categories(source_categories: List[Dict[str, Any]], existing_translations: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find categories that exist in source but not in target language"""
    missing = []
    for category in source_categories:
        category_key = get_category_key(category)
        if category_key not in existing_translations:
            missing.append(category)
    return missing

def save_progress(categories: List[Dict[str, Any]], output_file: Path, lang_code: str) -> None:
    """Save current progress to a file"""
    try:
        save_json_file(categories, output_file)
        print(f"Progress saved for {lang_code}")
    except Exception as e:
        print(f"Warning: Could not save progress for {lang_code}: {e}")

def translate_categories(input_file: str, target_languages: Dict[str, str], update_mode: bool = False):
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

def main():
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
        "pt": "Portuguese",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "ru": "Russian"
    }
    
    try:
        translate_categories(args.input, target_languages, args.update)
        print("\nTranslation completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
