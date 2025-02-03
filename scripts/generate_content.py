#!/usr/bin/env python3
"""
Content Generation Script for MelodyMind

This script generates comprehensive, multilingual content for music categories
using the Arli AI API. It creates structured markdown files with SEO-optimized
metadata and detailed content sections for each music category.

Features:
- Multilingual content generation
- SEO metadata optimization
- Structured content sections
- Progress tracking and error handling
- Language-specific content adaptation

The script uses a template-based approach for consistent content structure
while adapting to language-specific requirements and cultural contexts.

Author: Daniel Schmid
Date: February 2025
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Dict, List, Tuple, Optional

# Configuration
ARLI_API_KEY = os.getenv("ARLI_API_KEY")  # API key for Arli AI
BASE_DIR = Path(__file__).parent.parent  # Project root directory
CONTENT_DIR = BASE_DIR / "content" / "knowledge"  # Directory for generated content
JSON_DIR = BASE_DIR / "app" / "json"  # Directory for JSON data

def get_available_languages() -> List[str]:
    """Get list of supported languages for content generation.
    
    Returns:
        List[str]: ISO 639-1 language codes for supported languages
    """
    return ["ar", "de", "en", "es", "fr", "it", "ja", "ko", "pt", "ru", "zh"]

def read_categories() -> List[str]:
    """Read and parse music categories from the categories file.
    
    Reads categories from category_headlines.txt, ignoring empty lines.
    Each category should be on a new line.
    
    Returns:
        List[str]: List of music category names
    """
    with open(BASE_DIR / "scripts" / "category_headlines.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Read AI help text templates
def read_templates() -> Dict[str, str]:
    """Read and parse AI help text templates for content generation.
    
    Reads templates from 'Helptexte für AI.md' and splits them into
    separate templates for decades and genres.
    
    Returns:
        Dict[str, str]: Dictionary containing templates for 'decades' and 'genres'
    """
    with open(BASE_DIR / "Helptexte für AI.md", "r", encoding="utf-8") as f:
        content = f.read()
        # Split into decades and genres templates
        decades_template, genres_template = content.split("# Für einzelne Genres")
        return {
            "decades": decades_template.strip(),
            "genres": "# Für einzelne Genres" + genres_template.strip()
        }

def is_decade(category: str) -> bool:
    """Check if a category name represents a decade.
    
    A decade category ends with 's' and has digits before it (e.g., '1950s').
    
    Args:
        category: The category name to check
        
    Returns:
        bool: True if the category represents a decade, False otherwise
    """
    return category.endswith("s") and category[:-1].isdigit()

def get_category_type(category: str) -> str:
    """Determine the category type from the sorted headlines file.
    
    Reads the category_headlines_sorted.txt file and determines the category type
    based on the section headers. The file is organized with # section headers
    followed by categories belonging to that section.
    
    Args:
        category: The category name to look up
        
    Returns:
        str: The category type (section title) or 'Genres' if not found
    """
    with open(BASE_DIR / "scripts" / "category_headlines_sorted.txt", "r", encoding="utf-8") as f:
        content = f.read()
        sections = content.split("#")
        for section in sections:
            if section.strip():
                title = section.split('\n')[0].strip()
                if category in section:
                    return title
    return "Genres"  # default to genres if not found

def get_translated_sections(language: str = "en") -> Dict[str, Dict[str, str]]:
    """Get section headers translated into the specified language.
    
    Provides a mapping of standard section headers to their translations
    in various languages. This ensures consistent content structure across
    all languages while maintaining natural language flow.
    
    Args:
        language: ISO 639-1 language code (default: "en")
        
    Returns:
        Dict[str, Dict[str, str]]: Nested dictionary mapping section names
        to their translations in different languages
    """
    sections = {
        "en": {
            "Introduction": "Introduction",
            "Historical Background": "Historical Background",
            "Musical Characteristics": "Musical Characteristics",
            "Subgenres and Variations": "Subgenres and Variations",
            "Key Figures and Important Works": "Key Figures and Important Works",
            "Technical Aspects": "Technical Aspects",
            "Cultural Significance": "Cultural Significance",
            "Performance and Live Culture": "Performance and Live Culture",
            "Development and Evolution": "Development and Evolution",
            "Legacy and Influence": "Legacy and Influence"
        },
        "ar": {
            "Introduction": "مقدمة",
            "Historical Background": "تاريخ النشأة",
            "Musical Characteristics": "الخصائص الموسيقية",
            "Subgenres and Variations": "الأنواع الفرعية والاختلافات",
            "Key Figures and Important Works": "الشخصيات الرئيسية والأعمال الهامة",
            "Technical Aspects": "الجوانب التقنية",
            "Cultural Significance": "الأهمية الثقافية",
            "Performance and Live Culture": "الأداء وثقافة العروض الحية",
            "Development and Evolution": "التطور والتقدم",
            "Legacy and Influence": "التراث والتأثير"
        },
        "de": {
            "Introduction": "Einleitung",
            "Historical Background": "Entstehungsgeschichte",
            "Musical Characteristics": "Musikalische Charakteristika",
            "Subgenres and Variations": "Subgenres und Variationen",
            "Key Figures and Important Works": "Schlüsselfiguren und wichtige Werke",
            "Technical Aspects": "Technische Aspekte",
            "Cultural Significance": "Kulturelle Bedeutung",
            "Performance and Live Culture": "Performance und Live-Kultur",
            "Development and Evolution": "Entwicklung und Evolution",
            "Legacy and Influence": "Vermächtnis und Einfluss"
        },

        "es": {
            "Introduction": "Introducción",
            "Historical Background": "Historia y Orígenes",
            "Musical Characteristics": "Características Musicales",
            "Subgenres and Variations": "Subgéneros y Variaciones",
            "Key Figures and Important Works": "Figuras Clave y Obras Importantes",
            "Technical Aspects": "Aspectos Técnicos",
            "Cultural Significance": "Significado Cultural",
            "Performance and Live Culture": "Cultura de Actuación en Vivo",
            "Development and Evolution": "Desarrollo y Evolución",
            "Legacy and Influence": "Legado e Influencia"
        },
        "fr": {
            "Introduction": "Introduction",
            "Historical Background": "Histoire et Origines",
            "Musical Characteristics": "Caractéristiques Musicales",
            "Subgenres and Variations": "Sous-genres et Variations",
            "Key Figures and Important Works": "Figures Clés et Œuvres Importantes",
            "Technical Aspects": "Aspects Techniques",
            "Cultural Significance": "Signification Culturelle",
            "Performance and Live Culture": "Culture de Performance Live",
            "Development and Evolution": "Développement et Évolution",
            "Legacy and Influence": "Héritage et Influence"
        },
        "it": {
            "Introduction": "Introduzione",
            "Historical Background": "Storia e Origini",
            "Musical Characteristics": "Caratteristiche Musicali",
            "Subgenres and Variations": "Sottogeneri e Variazioni",
            "Key Figures and Important Works": "Figure Chiave e Opere Importanti",
            "Technical Aspects": "Aspetti Tecnici",
            "Cultural Significance": "Significato Culturale",
            "Performance and Live Culture": "Cultura delle Performance dal Vivo",
            "Development and Evolution": "Sviluppo ed Evoluzione",
            "Legacy and Influence": "Eredità e Influenza"
        },
        "ja": {
            "Introduction": "はじめに",
            "Historical Background": "歴史的背景",
            "Musical Characteristics": "音楽的特徴",
            "Subgenres and Variations": "サブジャンルとバリエーション",
            "Key Figures and Important Works": "重要人物と主要作品",
            "Technical Aspects": "技術的側面",
            "Cultural Significance": "文化的意義",
            "Performance and Live Culture": "パフォーマンスとライブ文化",
            "Development and Evolution": "発展と進化",
            "Legacy and Influence": "遺産と影響"
        },
        "ko": {
            "Introduction": "소개",
            "Historical Background": "역사적 배경",
            "Musical Characteristics": "음악적 특징",
            "Subgenres and Variations": "하위 장르와 변주",
            "Key Figures and Important Works": "주요 인물과 중요 작품",
            "Technical Aspects": "기술적 측면",
            "Cultural Significance": "문화적 의의",
            "Performance and Live Culture": "공연과 라이브 문화",
            "Development and Evolution": "발전과 진화",
            "Legacy and Influence": "유산과 영향"
        },
        "pt": {
            "Introduction": "Introdução",
            "Historical Background": "História e Origens",
            "Musical Characteristics": "Características Musicais",
            "Subgenres and Variations": "Subgêneros e Variações",
            "Key Figures and Important Works": "Figuras-Chave e Obras Importantes",
            "Technical Aspects": "Aspectos Técnicos",
            "Cultural Significance": "Significado Cultural",
            "Performance and Live Culture": "Cultura de Performance ao Vivo",
            "Development and Evolution": "Desenvolvimento e Evolução",
            "Legacy and Influence": "Legado e Influência"
        },
        "ru": {
            "Introduction": "Введение",
            "Historical Background": "История и происхождение",
            "Musical Characteristics": "Музыкальные характеристики",
            "Subgenres and Variations": "Поджанры и вариации",
            "Key Figures and Important Works": "Ключевые фигуры и важные произведения",
            "Technical Aspects": "Технические аспекты",
            "Cultural Significance": "Культурное значение",
            "Performance and Live Culture": "Культура живых выступлений",
            "Development and Evolution": "Развитие и эволюция",
            "Legacy and Influence": "Наследие и влияние"
        },
        "zh": {
            "Introduction": "引言",
            "Historical Background": "历史背景",
            "Musical Characteristics": "音乐特点",
            "Subgenres and Variations": "子类型与变体",
            "Key Figures and Important Works": "重要人物与作品",
            "Technical Aspects": "技术方面",
            "Cultural Significance": "文化意义",
            "Performance and Live Culture": "现场表演文化",
            "Development and Evolution": "发展与演变",
            "Legacy and Influence": "遗产与影响"
        }
    }
    return sections.get(language, sections["en"])  # Default to English if language not found

def get_section_limits(category, language="en"):
    # Sprachspezifische Anpassungsfaktoren für die Textlänge
    language_factors = {
        "ar": 0.9,  # Arabisch tendiert zu kürzeren Texten
        "de": 1.1,  # Deutsch tendiert zu längeren Texten
        "en": 1.0,  # Englisch als Basis
        "es": 1.05,  # Spanisch etwas länger als Englisch
        "fr": 1.05,  # Französisch etwas länger als Englisch
        "it": 1.05,  # Italienisch etwas länger als Englisch
        "ja": 0.7,  # Japanisch kann Inhalte kürzer ausdrücken
        "ko": 0.8,  # Koreanisch tendiert zu kürzeren Texten
        "pt": 1.05,  # Portugiesisch etwas länger als Englisch
        "ru": 0.9,  # Russisch kann kompakter sein
        "zh": 0.7   # Chinesisch kann Inhalte kürzer ausdrücken
    }
    
    # Standardfaktor falls Sprache nicht definiert
    factor = language_factors.get(language, 1.0)
    
    category_type = get_category_type(category)
    base_limits = {}
    
    if category.endswith('s') and category[:-1].isdigit():  # Decades
        base_limits = {
            "Introduction": (2500, 3000),
            "Political and Social Background": (4000, 4500),
            "Musical Developments": (1000, 1500),
            "Musical Diversity and Subgenres": (4500, 5000),
            "Rhythm and Style": (2500, 3000),
            "Key Artists and Albums": (4500, 5000),
            "Technical and Economic Aspects": (800, 1000),
            "Technological Innovations": (3000, 3500),
            "Musical Innovation and New Markets": (3000, 3500),
            "Cultural Dimensions": (800, 1000),
            "Festivals and Live Culture": (2500, 3000),
            "Lyrics and Themes": (3000, 3500),
            "Subcultures and Fashion": (2500, 3000),
            "Legacy and Outlook": (800, 1000),
            "Cultural Significance": (2500, 3000),
            "Lasting Influences": (2500, 3000),
            "Conclusion": (2000, 2500)
        }
    elif "Countries" in category_type:  # Countries and Regional Genres
        base_limits = {
            "Introduction": (2500, 3000),
            "Historical and Cultural Context": (4000, 4500),
            "Traditional Music": (4500, 5000),
            "Modern Music Development": (4500, 5000),
            "Notable Artists and Bands": (4500, 5000),
            "Music Industry and Infrastructure": (3000, 3500),
            "Live Music and Events": (3000, 3500),
            "Media and Promotion": (3000, 3500),
            "Education and Support": (3000, 3500),
            "International Connections": (3000, 3500),
            "Current Trends and Future": (2500, 3000)
        }
    elif "Emotional" in category_type:  # Emotional Genres
        base_limits = {
            "Introduction": (2500, 3000),
            "Music Psychology": (4500, 5000),
            "Musical Characteristics": (4500, 5000),
            "Cross-Genre Examples": (4500, 5000),
            "Cultural Perspectives": (3500, 4000),
            "Therapeutic Applications": (3500, 4000),
            "Notable Works and Artists": (4000, 4500),
            "Use in Media": (3000, 4500),
            "Modern Interpretations": (3000, 3500),
            "Practical Significance": (2500, 3000)
        }
    elif "Seasonal" in category_type:  # Seasonal Genres
        base_limits = {
            "Introduction": (2500, 3000),
            "Cultural Tradition": (4500, 5000),
            "Musical Characteristics": (4500, 5000),
            "Classical Compositions": (4000, 5000),
            "Popular Music": (4500, 5000),
            "Festive Events": (3500, 4000),
            "Media Presence": (3500, 4000),
            "International Perspectives": (2500, 3000)
        }
    else:  # Standard Genres
        base_limits = {
            "Introduction": (2500, 3000),
            "Historical Background": (3500, 4000),
            "Musical Characteristics": (5000, 5500),
            "Subgenres and Variations": (3000, 3500),
            "Key Figures and Important Works": (5500, 6000),
            "Technical Aspects": (3500, 4000),
            "Cultural Significance": (4500, 5000),
            "Performance and Live Culture": (3500, 4000),
            "Development and Evolution": (3000, 3500),
            "Legacy and Influence": (2000, 2500)
        }
    
    # Anwenden des Sprachfaktors auf alle Limits
    adjusted_limits = {}
    for section, (min_chars, max_chars) in base_limits.items():
        adjusted_limits[section] = (
            int(min_chars * factor),
            int(max_chars * factor)
        )
    
    return adjusted_limits

def get_language_prompts(language):
    prompts = {
        "ar": {
            "style": "العربية",
            "characteristics": "لغة فصحى معاصرة، أسلوب أدبي راقي، تعبيرات اصطلاحية مناسبة",
            "prompt": """
            قم بإنشاء محتوى للقسم '{section_name}' من فئة الموسيقى '{category}'.
            
            متطلبات مهمة:
            1. اكتب بالعربية الفصحى المعاصرة الراقية
            2. استخدم تعبيرات اصطلاحية وجمل متقنة
            3. يجب أن يكون المحتوى بين {char_min} و {char_max} حرف
            4. ركز فقط على الموسيقى العالمية
            5. استخدم جملاً كاملة وهيكل فقرات واضح
            6. يجب أن يكون النص سلساً وجذاباً
            7. تجنب القوائم - استخدم فقرات متدفقة
            8. استخدم انتقالات مناسبة بين الأفكار
            9. أدرج السياق الثقافي عند الحاجة
            10. حافظ على نبرة وأسلوب متناسقين
            
            مهم: عدد الأحرف الدقيق أمر حاسم - يجب أن يكون بين {char_min} و {char_max} حرف.
            """
        },
        "de": {
            "style": "deutschen",
            "characteristics": "längere, verschachtelte Sätze mit Nebensätzen, präzise Fachbegriffe, formellere Ausdrucksweise",
            "prompt": """
            Erstelle Inhalte für den Abschnitt '{section_name}' der Musikkategorie '{category}'.
            
            WICHTIGE ANFORDERUNGEN:
            1. Schreibe in einem flüssigen, natürlichen deutschen Stil
            2. Verwende verschachtelte Sätze und präzise Fachbegriffe
            3. Der Text MUSS zwischen {char_min} und {char_max} Zeichen lang sein
            4. Konzentriere dich NUR auf internationale Musik
            5. Nutze vollständige Sätze und eine klare Absatzstruktur
            6. Der Text soll natürlich fließen und fesselnd sein
            7. Vermeide Aufzählungen - nutze stattdessen fließende Absätze
            8. Verwende passende Überleitungen zwischen den Ideen
            9. Beziehe kulturellen Kontext mit ein
            10. Behalte durchgehend einen einheitlichen Ton und Stil bei
            
            Wichtig: Die genaue Zeichenzahl ist entscheidend - sie muss zwischen {char_min} und {char_max} Zeichen liegen.
            """
        },
        "en": {
            "style": "English",
            "characteristics": "clear and concise sentences, active voice, engaging tone",
            "prompt": """
            Create content for the section '{section_name}' of the music category '{category}'.
            
            IMPORTANT REQUIREMENTS:
            1. Write in clear, engaging English
            2. Use active voice and concise sentences
            3. Content MUST be between {char_min} and {char_max} characters
            4. Focus ONLY on international music
            5. Use complete sentences and proper paragraph structure
            6. Make the text flow naturally and be engaging
            7. Avoid lists - use flowing paragraphs instead
            8. Use appropriate transitions between ideas
            9. Include cultural context when relevant
            10. Maintain consistent tone and style throughout
            
            Important: The exact character count is crucial - must be between {char_min} and {char_max} characters.
            """
        },
        "es": {
            "style": "español",
            "characteristics": "expresivo y fluido, uso del subjuntivo, frases descriptivas",
            "prompt": """
            Crea contenido para la sección '{section_name}' de la categoría musical '{category}'.
            
            REQUISITOS IMPORTANTES:
            1. Escribe en español fluido y expresivo
            2. Utiliza el subjuntivo y frases descriptivas
            3. El contenido DEBE tener entre {char_min} y {char_max} caracteres
            4. Céntrate SOLO en música internacional
            5. Usa oraciones completas y estructura de párrafos adecuada
            6. El texto debe fluir naturalmente y ser cautivador
            7. Evita las listas - usa párrafos fluidos
            8. Utiliza transiciones apropiadas entre ideas
            9. Incluye contexto cultural cuando sea relevante
            10. Mantén un tono y estilo consistentes
            
            Importante: El conteo exacto de caracteres es crucial - debe estar entre {char_min} y {char_max} caracteres.
            """
        },
        "fr": {
            "style": "français",
            "characteristics": "phrases élégantes, vocabulaire précis, style soutenu",
            "prompt": """
            Créez du contenu pour la section '{section_name}' de la catégorie musicale '{category}'.
            
            EXIGENCES IMPORTANTES:
            1. Écrivez en français élégant et soutenu
            2. Utilisez un vocabulaire précis et des phrases élégantes
            3. Le contenu DOIT contenir entre {char_min} et {char_max} caractères
            4. Concentrez-vous UNIQUEMENT sur la musique internationale
            5. Utilisez des phrases complètes et une structure de paragraphes claire
            6. Le texte doit être fluide et captivant
            7. Évitez les listes - utilisez des paragraphes fluides
            8. Utilisez des transitions appropriées entre les idées
            9. Incluez le contexte culturel lorsque c'est pertinent
            10. Maintenez un ton et un style cohérents
            
            Important: Le nombre exact de caractères est crucial - il doit être entre {char_min} et {char_max} caractères.
            """
        },
        "ja": {
            "style": "日本語",
            "characteristics": "丁寧な表現、適切な敬語、自然な文章の流れ",
            "prompt": """
            音楽カテゴリー '{category}' の '{section_name}' セクションのコンテンツを作成してください。
            
            重要な要件：
            1. 丁寧で自然な日本語で書く
            2. 適切な敬語と専門用語を使用
            3. コンテンツは必ず {char_min} から {char_max} 文字の間にする
            4. 国際音楽のみに焦点を当てる
            5. 完全な文章と明確な段落構造を使用
            6. 文章は自然に流れ、魅力的であること
            7. 箇条書きを避け、流れるような段落を使用
            8. アイデア間の適切な移行を使用
            9. 関連する場合は文化的な文脈を含める
            10. 一貫した調子とスタイルを維持する
            
            重要：正確な文字数が重要です - {char_min} から {char_max} 文字の間でなければなりません。
            """
        },
        "ko": {
            "style": "한국어",
            "characteristics": "정중한 표현, 적절한 존댓말, 자연스러운 문장 흐름",
            "prompt": """
            음악 카테고리 '{category}'의 '{section_name}' 섹션에 대한 콘텐츠를 작성하세요.
            
            중요 요구사항:
            1. 정중하고 자연스러운 한국어로 작성
            2. 적절한 존댓말과 전문 용어 사용
            3. 콘텐츠는 반드시 {char_min}자에서 {char_max}자 사이여야 함
            4. 국제 음악에만 초점을 맞출 것
            5. 완전한 문장과 명확한 단락 구조 사용
            6. 글이 자연스럽게 흐르고 매력적이어야 함
            7. 나열식을 피하고 유려한 단락 사용
            8. 아이디어 간의 적절한 전환 사용
            9. 관련된 경우 문화적 맥락 포함
            10. 일관된 어조와 스타일 유지
            
            중요: 정확한 글자 수가 중요합니다 - {char_min}자에서 {char_max}자 사이여야 합니다.
            """
        },
        "pt": {
            "style": "português",
            "characteristics": "linguagem fluida, uso apropriado do subjuntivo, expressões idiomáticas",
            "prompt": """
            Crie conteúdo para a seção '{section_name}' da categoria musical '{category}'.
            
            REQUISITOS IMPORTANTES:
            1. Escreva em português fluido e expressivo
            2. Use o subjuntivo e expressões idiomáticas apropriadas
            3. O conteúdo DEVE ter entre {char_min} e {char_max} caracteres
            4. Foque APENAS em música internacional
            5. Use frases completas e estrutura clara de parágrafos
            6. O texto deve fluir naturalmente e ser cativante
            7. Evite listas - use parágrafos fluidos
            8. Use transições apropriadas entre as ideias
            9. Inclua contexto cultural quando relevante
            10. Mantenha um tom e estilo consistentes
            
            Importante: A contagem exata de caracteres é crucial - deve estar entre {char_min} e {char_max} caracteres.
            """
        },
        "ru": {
            "style": "русский",
            "characteristics": "богатый словарный запас, сложные предложения, литературный стиль",
            "prompt": """
            Создайте контент для раздела '{section_name}' музыкальной категории '{category}'.
            
            ВАЖНЫЕ ТРЕБОВАНИЯ:
            1. Пишите на грамотном русском языке
            2. Используйте богатый словарный запас и сложные предложения
            3. Контент ДОЛЖЕН содержать от {char_min} до {char_max} символов
            4. Сосредоточьтесь ТОЛЬКО на международной музыке
            5. Используйте полные предложения и четкую структуру абзацев
            6. Текст должен быть плавным и увлекательным
            7. Избегайте списков - используйте плавные абзацы
            8. Используйте подходящие переходы между идеями
            9. Включайте культурный контекст, где это уместно
            10. Поддерживайте последовательный тон и стиль
            
            Важно: Точное количество символов критично - должно быть между {char_min} и {char_max} символов.
            """
        },
        "ar": {
            "style": "العربية",
            "characteristics": "لغة فصحى معاصرة، أسلوب أدبي راقي، تعبيرات اصطلاحية مناسبة",
            "prompt": """
            قم بإنشاء محتوى للقسم '{section_name}' من فئة الموسيقى '{category}'.
            
            متطلبات مهمة:
            1. اكتب بالعربية الفصحى المعاصرة الراقية
            2. استخدم تعبيرات اصطلاحية وجمل متقنة
            3. يجب أن يكون المحتوى بين {char_min} و {char_max} حرف
            4. ركز فقط على الموسيقى العالمية
            5. استخدم جملاً كاملة وهيكل فقرات واضح
            6. يجب أن يكون النص سلساً وجذاباً
            7. تجنب القوائم - استخدم فقرات متدفقة
            8. استخدم انتقالات مناسبة بين الأفكار
            9. أدرج السياق الثقافي عند الحاجة
            10. حافظ على نبرة وأسلوب متناسقين
            
            مهم: عدد الأحرف الدقيق أمر حاسم - يجب أن يكون بين {char_min} و {char_max} حرف.
            """
        },
        "it": {
            "style": "italiano",
            "characteristics": "stile elegante, frasi articolate, ricchezza lessicale",
            "prompt": """
            Crea contenuti per la sezione '{section_name}' della categoria musicale '{category}'.
            
            REQUISITI IMPORTANTI:
            1. Scrivi in italiano elegante e fluido
            2. Usa un linguaggio ricco e frasi ben articolate
            3. Il contenuto DEVE essere tra {char_min} e {char_max} caratteri
            4. Concentrati SOLO sulla musica internazionale
            5. Usa frasi complete e una struttura chiara dei paragrafi
            6. Il testo deve scorrere naturalmente ed essere coinvolgente
            7. Evita gli elenchi - usa paragrafi scorrevoli
            8. Usa transizioni appropriate tra le idee
            9. Includi il contesto culturale quando pertinente
            10. Mantieni un tono e uno stile coerenti
            
            Importante: Il conteggio esatto dei caratteri è cruciale - deve essere tra {char_min} e {char_max} caratteri.
            """
        },
        "zh": {
            "style": "中文",
            "characteristics": "优雅的书面语，恰当的成语运用，流畅的表达方式",
            "prompt": """
            为音乐类别 '{category}' 的 '{section_name}' 部分创建内容。
            
            重要要求：
            1. 使用优雅的书面中文写作
            2. 恰当使用成语和专业术语
            3. 内容必须在 {char_min} 到 {char_max} 字符之间
            4. 仅关注国际音乐
            5. 使用完整句子和清晰的段落结构
            6. 文本应该流畅且引人入胜
            7. 避免列表 - 使用流畅的段落
            8. 使用适当的过渡连接想法
            9. 在相关时包含文化背景
            10. 保持一致的语气和风格
            
            重要：字符数的准确性至关重要 - 必须在 {char_min} 到 {char_max} 字符之间。
            """
        }
    }
    return prompts.get(language, prompts["en"])  # Default to English if language not found

def get_language_style_guide(language: str) -> Dict[str, str]:
    """Get language-specific style guide for content generation.
    
    Extracts style and characteristics information from language prompts
    to ensure content maintains appropriate language style and tone.
    
    Args:
        language: ISO 639-1 language code
        
    Returns:
        Dict[str, str]: Dictionary containing 'style' and 'characteristics'
        for the specified language
    """
    prompts = get_language_prompts(language)
    return {
        "style": prompts["style"],
        "characteristics": prompts["characteristics"]
    }

def generate_section(category: str, language: str, section_name: str, 
                   char_min: int, char_max: int) -> str:
    """Generate content for a specific section of a music category.
    
    Uses the Arli AI API to generate language-specific content that adheres
    to style guidelines and length requirements. Includes retry logic for
    handling API errors and content length mismatches.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        section_name: Name of the section to generate
        char_min: Minimum character count for the content
        char_max: Maximum character count for the content
        
    Returns:
        str: Generated content for the section
        
    Raises:
        ValueError: If ARLI_API_KEY is not set or content generation fails
        Exception: For API errors or other issues
    """
    if not ARLI_API_KEY:
        raise ValueError("ARLI_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {ARLI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    style_guide = get_language_style_guide(language)
    language_prompts = get_language_prompts(language)
    
    # Format the user prompt
    user_prompt = language_prompts["prompt"].format(
        section_name=section_name,
        category=category,
        char_min=char_min,
        char_max=char_max
    )
    
    # Try up to 3 times to get content with correct length
    for attempt in range(3):
        try:
            data = {
                "model": "Mistral-Nemo-12B-Instruct-2407",
                "messages": [
                    {"role": "system", "content": f"You are an expert music historian and writer. Write in {language}. {style_guide}"},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "repetition_penalty": 1.1,
                "top_p": 0.9,
                "top_k": 40,
                "max_tokens": 2500,
                "stream": False
            }
            
            response = requests.post(
                "https://api.arliai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"API call failed: {response.text}")
            
            content = response.json()["choices"][0]["message"]["content"].strip()
            
            # Verify character count
            char_count = len(content)
            if char_min <= char_count <= char_max:
                return content
            
            # If length is wrong, adjust the prompt for next attempt
            if char_count < char_min:
                user_prompt += f"\n\nThe previous response was too short ({char_count} chars). Please make it longer, aiming for {char_min}-{char_max} characters."
            else:
                user_prompt += f"\n\nThe previous response was too long ({char_count} chars). Please make it shorter, aiming for {char_min}-{char_max} characters."
                
        except Exception as e:
            if attempt == 2:  # Last attempt
                raise e
            print(f"  Attempt {attempt + 1} failed: {str(e)}")
            continue
    
    raise ValueError(f"Failed to generate content with correct length after 3 attempts")

def generate_content(category: str, language: str) -> str:
    """Generate or update content for a music category in a specific language.
    
    This function manages the content generation process, including:
    1. Loading and parsing existing content to avoid regenerating sections
    2. Generating new sections as needed
    3. Saving content incrementally to preserve progress
    
    The function is designed to be resilient, continuing even if some
    sections fail to generate. It also preserves existing content,
    only generating missing sections.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        str: Status message indicating completion
    """
    section_limits = get_section_limits(category)
    
    # Check for existing content
    existing_content = load_existing_content(category, language)
    if existing_content:
        print(f"  Found existing content for {category} in {language}")
        # Parse existing sections to avoid regenerating them
        existing_sections = {}
        current_section = None
        current_content = []
        
        for line in existing_content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    existing_sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            existing_sections[current_section] = '\n'.join(current_content)
    else:
        existing_sections = {}
        # Create new file with frontmatter
        save_content(category, language, '', 'w')
    
    # Generate or skip each section
    for section_name, (char_min, char_max) in section_limits.items():
        if section_name in existing_sections:
            print(f"  Skipping existing section: {section_name}")
            continue
            
        print(f"  Generating section: {section_name}...")
        try:
            section_content = generate_section(category, language, section_name, char_min, char_max)
            content = f"\n## {section_name}\n\n{section_content}\n"
            
            # Append the new section to the file
            save_content(category, language, content, 'a')
            print(f"  ✓ Saved section: {section_name}")
            
        except Exception as e:
            print(f"  ✗ Error generating section {section_name}: {str(e)}")
            # Continue with next section on error
            continue
    
    return "Content generation completed"

def get_output_path(category: str, language: str) -> Path:
    """Get the output file path for a category in a specific language.
    
    Creates the necessary directory structure if it doesn't exist and
    returns the path where the markdown file should be saved.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        Path: Path object pointing to the output markdown file
    """
    output_dir = CONTENT_DIR / language
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{category.lower().replace(' ', '-')}.md"

def generate_seo_metadata(category: str, language: str) -> Tuple[str, str, List[str]]:
    """Generate SEO metadata for a music category using AI.
    
    Uses the Arli AI API to generate SEO-optimized title, description,
    and keywords for a music category page. Includes fallback values
    in case of API errors.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        Tuple[str, str, List[str]]: Title, description, and keywords
        
    Raises:
        ValueError: If ARLI_API_KEY is not set
    """
    if not ARLI_API_KEY:
        raise ValueError("ARLI_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {ARLI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Generate SEO metadata for a music category page about {category} in {language}. The content should be in {language}.
    
    Please provide:
    1. An engaging, keyword-rich title (max 60 characters)
    2. A compelling meta description (150-160 characters) that includes the main keywords and encourages clicks
    3. A list of 5-7 relevant keywords/phrases for the category
    
    Format the response exactly like this:
    Title: [title]
    Description: [description]
    Keywords: [keyword1, keyword2, keyword3, ...]
    """
    
    data = {
        "model": "Mistral-Nemo-12B-Instruct-2407",
        "messages": [
            {"role": "system", "content": "You are an SEO expert specializing in music content."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "repetition_penalty": 1.1,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False
    }
    
    try:
        response = requests.post(
            "https://api.arliai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API call failed: {response.text}")
        
        content = response.json()["choices"][0]["message"]["content"].strip()
        
        # Parse the response
        lines = content.split('\n')
        title = ''
        description = ''
        keywords = []
        
        for line in lines:
            if line.startswith('Title:'):
                title = line.replace('Title:', '').strip()
            elif line.startswith('Description:'):
                description = line.replace('Description:', '').strip()
            elif line.startswith('Keywords:'):
                keywords_str = line.replace('Keywords:', '').strip()
                keywords = [k.strip() for k in keywords_str.split(',')]
        
        return title, description, keywords
        
    except Exception as e:
        print(f"  Error generating SEO metadata: {str(e)}")
        return category, f"{category} music category description", [category, "music"]

def create_frontmatter(category: str, language: str) -> str:
    """Create YAML frontmatter for a music category markdown file.
    
    Generates SEO-optimized metadata and formats it as YAML frontmatter.
    The frontmatter includes:
    - Title and description
    - Category image path
    - Creation and update timestamps
    - SEO keywords
    - Author and locale information
    - Music streaming service playlist placeholders
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        str: Formatted YAML frontmatter string
    """
    # Generate SEO metadata
    print(f"  Generating SEO metadata for {category}...")
    title, description, keywords = generate_seo_metadata(category, language)
    
    return f"""---
title: {title}
description: {description}
image: /category/{category.lower().replace(' ', '-')}.jpg
createdAt: {datetime.now().strftime('%Y-%m-%d')}
updatedAt: {datetime.now().strftime('%Y-%m-%d')}
keywords:
{chr(10).join([f'  - {keyword}' for keyword in keywords])}
author: MelodyMind
locale: {language}
category:
  spotifyPlaylist: 
  deezerPlaylist: 
  appleMusicPlaylist: 
isPlayable: false
---

"""

def save_content(category: str, language: str, content: str, mode: str = 'w') -> None:
    """Save or append content to a category's markdown file.
    
    For new files (mode='w'), automatically adds YAML frontmatter before
    the content. For existing files (mode='a'), appends content as is.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        content: Content to write or append
        mode: File mode, 'w' for write or 'a' for append (default: 'w')
    """
    output_path = get_output_path(category, language)
    
    # For new files, add frontmatter
    if mode == 'w':
        content = create_frontmatter(category, language) + content
    
    # Save or append to the file
    with open(output_path, mode, encoding="utf-8") as f:
        f.write(content)

def load_existing_content(category: str, language: str) -> Optional[str]:
    """Load existing content for a category in a specific language.
    
    Checks if content already exists for the category and language
    combination and loads it if found.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        Optional[str]: File contents if file exists, None otherwise
    """
    output_path = get_output_path(category, language)
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

from datetime import datetime
from typing import Dict, List
import time

def print_header(text: str, width: int = 80) -> None:
    """Print a centered header with decorative borders.
    
    Creates a visually distinct section header using '=' characters
    as borders and centers the text within the specified width.
    
    Args:
        text: Header text to display
        width: Total width of the header (default: 80)
    """
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width)

def print_section(text: str, width: int = 80) -> None:
    """Print a section divider with text.
    
    Creates a visual section break using '-' characters as borders
    and displays the text with consistent spacing.
    
    Args:
        text: Section text to display
        width: Total width of the section divider (default: 80)
    """
    print("\n" + "-" * width)
    print(text)
    print("-" * width)

def print_progress(current: int, total: int, prefix: str = "", width: int = 30) -> None:
    """Display a progress bar showing completion status.
    
    Creates a visual progress indicator with percentage and fraction,
    updating in place using carriage return. The progress bar uses
    block characters to show completion and dashes for remaining progress.
    
    Args:
        current: Current progress value
        total: Total value for 100% completion
        prefix: Text to display before the progress bar (default: "")
        width: Width of the progress bar in characters (default: 30)
    """
    percentage = int((current / total) * 100)
    filled = int(width * current / total)
    bar = "█" * filled + "-" * (width - filled)
    print(f"\r{prefix} |{bar}| {percentage}% ({current}/{total})", end="")
    if current == total:
        print()

def main() -> None:
    """Main execution function for the content generation script.
    
    This function orchestrates the entire content generation process:
    1. Initializes and displays script header
    2. Gets list of supported languages
    3. Reads and parses categories from the sorted headlines file
    4. Processes each category type and its subcategories
    5. Generates content for each category in all supported languages
    6. Tracks and displays progress throughout the process
    
    The function uses a structured approach to handle categories by type
    (e.g., decades, genres) and maintains progress indicators for the user.
    It also measures and reports total execution time.
    """
    start_time = time.time()
    print_header("MelodyMind Content Generator")
    
    # Get available languages
    languages = get_available_languages()
    print_section(f"Languages: {len(languages)}")
    for lang in languages:
        print(f"✓ {lang}")
    
    # Read categories from sorted file
    with open(BASE_DIR / "scripts" / "category_headlines_sorted.txt", "r", encoding="utf-8") as f:
        content = f.readlines()
    
    # Parse categories by type
    categories_by_type: Dict[str, List[str]] = {}
    current_type = ""
    for line in content:
        line = line.strip()
        if line.startswith('#'):
            current_type = line[1:].strip()
            categories_by_type[current_type] = []
        elif line:
            categories_by_type[current_type].append(line)
    
    total_categories = sum(len(cats) for cats in categories_by_type.values())
    processed_categories = 0
    
    print_section(f"Categories: {total_categories}")
    for category_type, categories in categories_by_type.items():
        print(f"\n{category_type}: {len(categories)}")
        for cat in categories:
            print(f"• {cat}")
    
    # Create content directory structure
    print_section("Creating Directory Structure")
    for language in languages:
        path = CONTENT_DIR / language
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ {path}")
    
    # Process categories
    print_section("Generating Content")
    skipped = 0
    errors = 0
    generated = 0
    
    for category_type, categories in categories_by_type.items():
        print(f"\n📂 {category_type}")
        for category in categories:
            processed_categories += 1
            print(f"\n🎵 {category}")
            
            for language in languages:
                output_path = get_output_path(category, language)
                if output_path.exists():
                    print(f"  ⏭️  Skipping {language}, file exists")
                    skipped += 1
                    continue
                
                try:
                    result = generate_content(category, language)
                    print(f"  ✓ {language}: {result}")
                    generated += 1
                except Exception as e:
                    print(f"  ❌ {language}: {str(e)}")
                    errors += 1
            
            print_progress(processed_categories, total_categories, "Overall Progress")
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print_header("Generation Complete")
    print(f"Duration: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"Total Categories: {total_categories}")
    print(f"Files Generated: {generated}")
    print(f"Files Skipped: {skipped}")
    print(f"Errors: {errors}")
    print("=" * 80)

if __name__ == "__main__":
    main()
