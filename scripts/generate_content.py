#!/usr/bin/env python3
"""
Content Generation Script for MelodyMind
=======================================

This script generates comprehensive, multilingual content for music categories
using the OpenAI API. It creates structured markdown files with SEO-optimized
metadata and detailed content sections for each music category.

Features:
- Multilingual content generation (10 languages supported)
- SEO metadata optimization with AI-powered suggestions
- Structured content sections with consistent formatting
- Real-time progress tracking and error handling
- Language-specific content adaptation and cultural awareness
- Template-based generation for consistency
- Automatic frontmatter generation with metadata

Dependencies:
- Python 3.8+
- External packages:
  - openai: For API communication with OpenAI
  - pathlib: For cross-platform path handling
  - typing: For type hints
- Requirements:
  - OpenAI API key must be set as environment variable
  - Compatible model access (e.g., o3-mini)

File Structure:
- Input Files:
  - category_headlines.txt: List of music categories
  - category_headlines_sorted.txt: Categorized music genres
  - Helptexte für AI.md: AI prompt templates

- Output Structure:
  content/
  └── knowledge/
      ├── en/
      │   ├── rock-music.md
      │   └── ...
      ├── de/
      │   ├── rock-musik.md
      │   └── ...
      └── ...

Workflow:
1. Initialization
   - Load configuration and templates
   - Set up logging and progress tracking

2. Category Processing
   - Read and parse category files
   - Determine category types (decade/genre)
   - Sort into processing queue

3. Content Generation
   - Generate SEO metadata
   - Create frontmatter
   - Generate section content
   - Apply language-specific formatting

4. Output Management
   - Create directory structure
   - Save markdown files
   - Update existing content

Error Handling:
- Retries for API failures
- Graceful degradation for missing templates
- Detailed error logging
- Progress preservation on failure

Author: Daniel Schmid
Date: February 2025
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Configuration
BASE_DIR = Path(__file__).parent.parent  # Project root directory
CONTENT_DIR = BASE_DIR / "content" / "knowledge"  # Directory for generated content
JSON_DIR = BASE_DIR / "app" / "json"  # Directory for JSON data

# OpenAI configuration - customize as needed
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "o3-mini")  # Default model to use

# Initialize OpenAI client
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    )

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_available_languages() -> List[str]:
    """Get list of supported languages for content generation.

    Returns:
        List[str]: ISO 639-1 language codes for supported languages
    """
    return ["da", "de", "en", "es", "fi", "fr", "it", "nl", "pt", "sv"]


def read_categories() -> List[str]:
    """Read and parse music categories from the categories file.

    Reads categories from category_headlines.txt, ignoring empty lines.
    Each category should be on a new line.

    Returns:
        List[str]: List of music category names
    """
    with open(
        BASE_DIR / "scripts" / "category_headlines.txt", "r", encoding="utf-8"
    ) as f:
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
            "genres": "# Für einzelne Genres" + genres_template.strip(),
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
    with open(
        BASE_DIR / "scripts" / "category_headlines_sorted.txt", "r", encoding="utf-8"
    ) as f:
        content = f.read()
        sections = content.split("#")
        for section in sections:
            if section.strip():
                title = section.split("\n")[0].strip()
                if category in section:
                    return title
    return "Genres"  # default to genres if not found


def get_translated_sections(language: str = "en") -> Dict[str, str]:
    """Get section headers translated into the specified language.

    Provides a mapping of standard section headers to their translations
    in various languages. This ensures consistent content structure across
    all languages while maintaining natural language flow.

    Args:
        language: ISO 639-1 language code (default: "en")

    Returns:
        Dict[str, str]: Dictionary mapping English section names to their translations
        in the specified language

    Raises:
        ValueError: If translations for the specified language are not available
    """
    if language not in get_available_languages():
        raise ValueError(f"Language {language} is not supported")

    translations = {
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
            "Legacy and Influence": "Legacy and Influence",
        },
        "da": {
            "Introduction": "Introduktion",
            "Historical Background": "Historisk Baggrund",
            "Musical Characteristics": "Musikalske Karakteristika",
            "Subgenres and Variations": "Undergenrer og Variationer",
            "Key Figures and Important Works": "Nøglefigurer og Vigtige Værker",
            "Technical Aspects": "Tekniske Aspekter",
            "Cultural Significance": "Kulturel Betydning",
            "Performance and Live Culture": "Performance og Live-Kultur",
            "Development and Evolution": "Udvikling og Evolution",
            "Legacy and Influence": "Arv og Indflydelse",
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
            "Legacy and Influence": "Vermächtnis und Einfluss",
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
            "Legacy and Influence": "Legado e Influencia",
        },
        "fi": {
            "Introduction": "Johdanto",
            "Historical Background": "Historiallinen Tausta",
            "Musical Characteristics": "Musiikilliset Ominaisuudet",
            "Subgenres and Variations": "Alagenret ja Variaatiot",
            "Key Figures and Important Works": "Keskeiset Hahmot ja Tärkeät Teokset",
            "Technical Aspects": "Tekniset Näkökohdat",
            "Cultural Significance": "Kulttuurinen Merkitys",
            "Performance and Live Culture": "Esitys- ja Live-Kulttuuri",
            "Development and Evolution": "Kehitys ja Evoluutio",
            "Legacy and Influence": "Perintö ja Vaikutus",
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
            "Legacy and Influence": "Héritage et Influence",
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
            "Legacy and Influence": "Eredità e Influenza",
        },
        "nl": {
            "Introduction": "Inleiding",
            "Historical Background": "Historische Achtergrond",
            "Musical Characteristics": "Muzikale Kenmerken",
            "Subgenres and Variations": "Subgenres en Variaties",
            "Key Figures and Important Works": "Belangrijke Figuren en Werken",
            "Technical Aspects": "Technische Aspecten",
            "Cultural Significance": "Culturele Betekenis",
            "Performance and Live Culture": "Performance en Live Cultuur",
            "Development and Evolution": "Ontwikkeling en Evolutie",
            "Legacy and Influence": "Erfenis en Invloed",
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
            "Legacy and Influence": "Legado e Influência",
        },
        "sv": {
            "Introduction": "Introduktion",
            "Historical Background": "Historisk Bakgrund",
            "Musical Characteristics": "Musikaliska Egenskaper",
            "Subgenres and Variations": "Undergenrer och Variationer",
            "Key Figures and Important Works": "Nyckelfigurer och Viktiga Verk",
            "Technical Aspects": "Tekniska Aspekter",
            "Cultural Significance": "Kulturell Betydelse",
            "Performance and Live Culture": "Framförande och Live-Kultur",
            "Development and Evolution": "Utveckling och Evolution",
            "Legacy and Influence": "Arv och Inflytande",
        },
    }
    if language not in translations:
        raise ValueError(f"Translations not available for language: {language}")

    return translations[language]


def get_section_limits(category, language="en"):
    # Language-specific adjustment factors for text length
    language_factors = {
        "da": 1.05,  # Danish slightly longer than English
        "de": 1.1,  # German tends to be longer
        "en": 1.0,  # English as base
        "es": 1.05,  # Spanish slightly longer than English
        "fi": 1.1,  # Finnish tends to be longer
        "fr": 1.05,  # French slightly longer than English
        "it": 1.05,  # Italian slightly longer than English
        "nl": 1.05,  # Dutch slightly longer than English
        "pt": 1.05,  # Portuguese slightly longer than English
        "sv": 1.05,  # Swedish slightly longer than English
    }

    # Default factor if language not defined
    factor = language_factors.get(language, 1.0)

    # Apply language factor to base calculations
    # The factor will be applied to the category-specific limits below

    category_type = get_category_type(category)
    base_limits = {}

    if category.endswith("s") and category[:-1].isdigit():  # Decades
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Political and Social Background": "Political and Social Background",
                "Musical Developments": "Musical Developments",
                "Musical Diversity and Subgenres": "Musical Diversity and Subgenres",
                "Key Artists and Albums": "Key Artists and Albums",
                "Technical and Economic Aspects": "Technical and Economic Aspects",
                "Musical Innovation and Markets": "Musical Innovation and Markets",
                "Cultural Impact": "Cultural Impact",
                "Festivals and Live Culture": "Festivals and Live Culture",
                "Lyrics and Themes": "Lyrics and Themes",
                "Legacy and Influences": "Legacy and Influences",
                "Conclusion": "Conclusion",
            },
            "de": {
                "Introduction": "Einleitung",
                "Political and Social Background": "Politischer und sozialer Hintergrund",
                "Musical Developments": "Musikalische Entwicklungen",
                "Musical Diversity and Subgenres": "Musikalische Vielfalt und Subgenres",
                "Key Artists and Albums": "Wichtige Künstler und Alben",
                "Technical and Economic Aspects": "Technische und wirtschaftliche Aspekte",
                "Musical Innovation and Markets": "Musikalische Innovation und Märkte",
                "Cultural Impact": "Kulturelle Auswirkungen",
                "Festivals and Live Culture": "Festivals und Live-Kultur",
                "Lyrics and Themes": "Liedtexte und Themen",
                "Legacy and Influences": "Vermächtnis und Einflüsse",
                "Conclusion": "Fazit",
            },
            "es": {
                "Introduction": "Introducción",
                "Political and Social Background": "Contexto político y social",
                "Musical Developments": "Desarrollos musicales",
                "Musical Diversity and Subgenres": "Diversidad musical y subgéneros",
                "Key Artists and Albums": "Artistas y álbumes principales",
                "Technical and Economic Aspects": "Aspectos técnicos y económicos",
                "Musical Innovation and Markets": "Innovación musical y mercados",
                "Cultural Impact": "Impacto cultural",
                "Festivals and Live Culture": "Festivales y cultura en vivo",
                "Lyrics and Themes": "Letras y temas",
                "Legacy and Influences": "Legado e influencias",
                "Conclusion": "Conclusión",
            },
            "fr": {
                "Introduction": "Introduction",
                "Political and Social Background": "Contexte politique et social",
                "Musical Developments": "Développements musicaux",
                "Musical Diversity and Subgenres": "Diversité musicale et sous-genres",
                "Key Artists and Albums": "Artistes et albums majeurs",
                "Technical and Economic Aspects": "Aspects techniques et économiques",
                "Musical Innovation and Markets": "Innovation musicale et marchés",
                "Cultural Impact": "Impact culturel",
                "Festivals and Live Culture": "Festivals et culture live",
                "Lyrics and Themes": "Paroles et thèmes",
                "Legacy and Influences": "Héritage et influences",
                "Conclusion": "Conclusion",
            },
            "it": {
                "Introduction": "Introduzione",
                "Political and Social Background": "Contesto politico e sociale",
                "Musical Developments": "Sviluppi musicali",
                "Musical Diversity and Subgenres": "Diversità musicale e sottogeneri",
                "Key Artists and Albums": "Artisti e album principali",
                "Technical and Economic Aspects": "Aspetti tecnici ed economici",
                "Musical Innovation and Markets": "Innovazione musicale e mercati",
                "Cultural Impact": "Impatto culturale",
                "Festivals and Live Culture": "Festival e cultura dal vivo",
                "Lyrics and Themes": "Testi e temi",
                "Legacy and Influences": "Eredità e influenze",
                "Conclusion": "Conclusione",
            },
            "pt": {
                "Introduction": "Introdução",
                "Political and Social Background": "Contexto político e social",
                "Musical Developments": "Desenvolvimentos musicais",
                "Musical Diversity and Subgenres": "Diversidade musical e subgêneros",
                "Key Artists and Albums": "Artistas e álbuns principais",
                "Technical and Economic Aspects": "Aspectos técnicos e econômicos",
                "Musical Innovation and Markets": "Inovação musical e mercados",
                "Cultural Impact": "Impacto cultural",
                "Festivals and Live Culture": "Festivais e cultura ao vivo",
                "Lyrics and Themes": "Letras e temas",
                "Legacy and Influences": "Legado e influências",
                "Conclusion": "Conclusão",
            },
            "da": {
                "Introduction": "Introduktion",
                "Political and Social Background": "Politisk og social baggrund",
                "Musical Developments": "Musikalsk udvikling",
                "Musical Diversity and Subgenres": "Musikalsk mangfoldighed og undergenrer",
                "Key Artists and Albums": "Nøglekunstnere og albums",
                "Technical and Economic Aspects": "Tekniske og økonomiske aspekter",
                "Musical Innovation and Markets": "Musikalsk innovation og markeder",
                "Cultural Impact": "Kulturel påvirkning",
                "Festivals and Live Culture": "Festivaler og livekultur",
                "Lyrics and Themes": "Tekster og temaer",
                "Legacy and Influences": "Arv og påvirkninger",
                "Conclusion": "Konklusion",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Political and Social Background": "Politieke en sociale achtergrond",
                "Musical Developments": "Muzikale ontwikkelingen",
                "Musical Diversity and Subgenres": "Muzikale diversiteit en subgenres",
                "Key Artists and Albums": "Belangrijke artiesten en albums",
                "Technical and Economic Aspects": "Technische en economische aspecten",
                "Musical Innovation and Markets": "Muzikale innovatie en markten",
                "Cultural Impact": "Culturele impact",
                "Festivals and Live Culture": "Festivals en livecultuur",
                "Lyrics and Themes": "Teksten en thema's",
                "Legacy and Influences": "Erfenis en invloeden",
                "Conclusion": "Conclusie",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Political and Social Background": "Politisk och social bakgrund",
                "Musical Developments": "Musikalisk utveckling",
                "Musical Diversity and Subgenres": "Musikalisk mångfald och undergenrer",
                "Key Artists and Albums": "Viktiga artister och album",
                "Technical and Economic Aspects": "Tekniska och ekonomiska aspekter",
                "Musical Innovation and Markets": "Musikalisk innovation och marknader",
                "Cultural Impact": "Kulturell påverkan",
                "Festivals and Live Culture": "Festivaler och livekultur",
                "Lyrics and Themes": "Texter och teman",
                "Legacy and Influences": "Arv och influenser",
                "Conclusion": "Slutsats",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Political and Social Background": "Poliittinen ja sosiaalinen tausta",
                "Musical Developments": "Musiikillinen kehitys",
                "Musical Diversity and Subgenres": "Musiikillinen monimuotoisuus ja alagenret",
                "Key Artists and Albums": "Tärkeät artistit ja albumit",
                "Technical and Economic Aspects": "Tekniset ja taloudelliset näkökohdat",
                "Musical Innovation and Markets": "Musiikillinen innovaatio ja markkinat",
                "Cultural Impact": "Kulttuurinen vaikutus",
                "Festivals and Live Culture": "Festivaalit ja livekulttuuri",
                "Lyrics and Themes": "Sanoitukset ja teemat",
                "Legacy and Influences": "Perintö ja vaikutteet",
                "Conclusion": "Yhteenveto",
            },
        }

        # Get the section titles for the current language
        section_titles = sections.get(language, sections["en"])

        # Define the base limits for each section
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Political and Social Background"]: 2000,
            section_titles["Musical Developments"]: 2000,
            section_titles["Musical Diversity and Subgenres"]: 2000,
            section_titles["Key Artists and Albums"]: 2500,
            section_titles["Technical and Economic Aspects"]: 1500,
            section_titles["Musical Innovation and Markets"]: 2000,
            section_titles["Cultural Impact"]: 2000,
            section_titles["Festivals and Live Culture"]: 1500,
            section_titles["Lyrics and Themes"]: 1500,
            section_titles["Legacy and Influences"]: 2000,
            section_titles["Conclusion"]: 1000,
        }
    elif "Female-Focused" in category_type:  # Female-Focused Categories
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Historical Development": "Historical Development",
                "Musical Characteristics": "Musical Characteristics",
                "Vocal Styles and Techniques": "Vocal Styles and Techniques",
                "Notable Artists": "Notable Artists",
                "Iconic Albums and Songs": "Iconic Albums and Songs",
                "Cultural Impact": "Cultural Impact",
                "Evolution and Trends": "Evolution and Trends",
                "Global Influence": "Global Influence",
                "Media Representation": "Media Representation",
                "Legacy and Future": "Legacy and Future",
            },
            "de": {
                "Introduction": "Einleitung",
                "Historical Development": "Historische Entwicklung",
                "Musical Characteristics": "Musikalische Merkmale",
                "Vocal Styles and Techniques": "Gesangsstile und -techniken",
                "Notable Artists": "Bedeutende Künstlerinnen",
                "Iconic Albums and Songs": "Ikonische Alben und Lieder",
                "Cultural Impact": "Kultureller Einfluss",
                "Evolution and Trends": "Entwicklung und Trends",
                "Global Influence": "Globaler Einfluss",
                "Media Representation": "Mediale Darstellung",
                "Legacy and Future": "Vermächtnis und Zukunft",
            },
            "es": {
                "Introduction": "Introducción",
                "Historical Development": "Desarrollo histórico",
                "Musical Characteristics": "Características musicales",
                "Vocal Styles and Techniques": "Estilos y técnicas vocales",
                "Notable Artists": "Artistas destacadas",
                "Iconic Albums and Songs": "Álbumes y canciones icónicos",
                "Cultural Impact": "Impacto cultural",
                "Evolution and Trends": "Evolución y tendencias",
                "Global Influence": "Influencia global",
                "Media Representation": "Representación en los medios",
                "Legacy and Future": "Legado y futuro",
            },
            "fr": {
                "Introduction": "Introduction",
                "Historical Development": "Développement historique",
                "Musical Characteristics": "Caractéristiques musicales",
                "Vocal Styles and Techniques": "Styles et techniques vocaux",
                "Notable Artists": "Artistes remarquables",
                "Iconic Albums and Songs": "Albums et chansons emblématiques",
                "Cultural Impact": "Impact culturel",
                "Evolution and Trends": "Évolution et tendances",
                "Global Influence": "Influence mondiale",
                "Media Representation": "Représentation médiatique",
                "Legacy and Future": "Héritage et avenir",
            },
            "it": {
                "Introduction": "Introduzione",
                "Historical Development": "Sviluppo storico",
                "Musical Characteristics": "Caratteristiche musicali",
                "Vocal Styles and Techniques": "Stili e tecniche vocali",
                "Notable Artists": "Artiste di rilievo",
                "Iconic Albums and Songs": "Album e canzoni iconici",
                "Cultural Impact": "Impatto culturale",
                "Evolution and Trends": "Evoluzione e tendenze",
                "Global Influence": "Influenza globale",
                "Media Representation": "Rappresentazione nei media",
                "Legacy and Future": "Eredità e futuro",
            },
            "pt": {
                "Introduction": "Introdução",
                "Historical Development": "Desenvolvimento histórico",
                "Musical Characteristics": "Características musicais",
                "Vocal Styles and Techniques": "Estilos e técnicas vocais",
                "Notable Artists": "Artistas notáveis",
                "Iconic Albums and Songs": "Álbuns e canções icônicos",
                "Cultural Impact": "Impacto cultural",
                "Evolution and Trends": "Evolução e tendências",
                "Global Influence": "Influência global",
                "Media Representation": "Representação na mídia",
                "Legacy and Future": "Legado e futuro",
            },
            "da": {
                "Introduction": "Introduktion",
                "Historical Development": "Historisk udvikling",
                "Musical Characteristics": "Musikalske karakteristika",
                "Vocal Styles and Techniques": "Vokale stilarter og teknikker",
                "Notable Artists": "Bemærkelsesværdige kunstnere",
                "Iconic Albums and Songs": "Ikoniske album og sange",
                "Cultural Impact": "Kulturel indflydelse",
                "Evolution and Trends": "Udvikling og tendenser",
                "Global Influence": "Global indflydelse",
                "Media Representation": "Medierepræsentation",
                "Legacy and Future": "Arv og fremtid",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Historical Development": "Historische ontwikkeling",
                "Musical Characteristics": "Muzikale kenmerken",
                "Vocal Styles and Techniques": "Vocale stijlen en technieken",
                "Notable Artists": "Opmerkelijke artiesten",
                "Iconic Albums and Songs": "Iconische albums en liedjes",
                "Cultural Impact": "Culturele impact",
                "Evolution and Trends": "Evolutie en trends",
                "Global Influence": "Wereldwijde invloed",
                "Media Representation": "Mediarepresentatie",
                "Legacy and Future": "Erfenis en toekomst",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Historical Development": "Historisk utveckling",
                "Musical Characteristics": "Musikaliska egenskaper",
                "Vocal Styles and Techniques": "Vokala stilar och tekniker",
                "Notable Artists": "Anmärkningsvärda artister",
                "Iconic Albums and Songs": "Ikoniska album och låtar",
                "Cultural Impact": "Kulturell påverkan",
                "Evolution and Trends": "Evolution och trender",
                "Global Influence": "Globalt inflytande",
                "Media Representation": "Medierepresentation",
                "Legacy and Future": "Arv och framtid",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Historical Development": "Historiallinen kehitys",
                "Musical Characteristics": "Musiikilliset ominaisuudet",
                "Vocal Styles and Techniques": "Laulutyylit ja -tekniikat",
                "Notable Artists": "Merkittävät artistit",
                "Iconic Albums and Songs": "Ikoniset albumit ja kappaleet",
                "Cultural Impact": "Kulttuurinen vaikutus",
                "Evolution and Trends": "Kehitys ja trendit",
                "Global Influence": "Maailmanlaajuinen vaikutus",
                "Media Representation": "Mediarepresentaatio",
                "Legacy and Future": "Perintö ja tulevaisuus",
            },
        }

        section_titles = sections.get(language, sections["en"])
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Historical Development"]: 2000,
            section_titles["Musical Characteristics"]: 2000,
            section_titles["Vocal Styles and Techniques"]: 2000,
            section_titles["Notable Artists"]: 2500,
            section_titles["Iconic Albums and Songs"]: 2000,
            section_titles["Cultural Impact"]: 2000,
            section_titles["Evolution and Trends"]: 1500,
            section_titles["Global Influence"]: 1500,
            section_titles["Media Representation"]: 1500,
            section_titles["Legacy and Future"]: 1500,
        }
    elif "Instruments" in category_type:  # Musical Instruments
        sections = {
            "en": {
                "Introduction": "Introduction",
                "History and Development": "History and Development",
                "Construction and Design": "Construction and Design",
                "Playing Technique": "Playing Technique",
                "Notable Players": "Notable Players",
                "Musical Genres": "Musical Genres",
                "Cultural Significance": "Cultural Significance",
                "Modern Applications": "Modern Applications",
                "Learning and Education": "Learning and Education",
                "Variations and Related Instruments": "Variations and Related Instruments",
                "Conclusion": "Conclusion",
            },
            "de": {
                "Introduction": "Einleitung",
                "History and Development": "Geschichte und Entwicklung",
                "Construction and Design": "Konstruktion und Design",
                "Playing Technique": "Spieltechnik",
                "Notable Players": "Bekannte Interpreten",
                "Musical Genres": "Musikalische Genres",
                "Cultural Significance": "Kulturelle Bedeutung",
                "Modern Applications": "Moderne Anwendungen",
                "Learning and Education": "Lernen und Unterricht",
                "Variations and Related Instruments": "Variationen und verwandte Instrumente",
                "Conclusion": "Fazit",
            },
            "es": {
                "Introduction": "Introducción",
                "History and Development": "Historia y desarrollo",
                "Construction and Design": "Construcción y diseño",
                "Playing Technique": "Técnica de ejecución",
                "Notable Players": "Intérpretes destacados",
                "Musical Genres": "Géneros musicales",
                "Cultural Significance": "Importancia cultural",
                "Modern Applications": "Aplicaciones modernas",
                "Learning and Education": "Aprendizaje y enseñanza",
                "Variations and Related Instruments": "Variaciones e instrumentos relacionados",
                "Conclusion": "Conclusión",
            },
            "fr": {
                "Introduction": "Introduction",
                "History and Development": "Histoire et développement",
                "Construction and Design": "Construction et conception",
                "Playing Technique": "Technique de jeu",
                "Notable Players": "Interprètes notables",
                "Musical Genres": "Genres musicaux",
                "Cultural Significance": "Importance culturelle",
                "Modern Applications": "Applications modernes",
                "Learning and Education": "Apprentissage et enseignement",
                "Variations and Related Instruments": "Variations et instruments apparentés",
                "Conclusion": "Conclusion",
            },
            "it": {
                "Introduction": "Introduzione",
                "History and Development": "Storia e sviluppo",
                "Construction and Design": "Costruzione e design",
                "Playing Technique": "Tecnica di esecuzione",
                "Notable Players": "Interpreti di rilievo",
                "Musical Genres": "Generi musicali",
                "Cultural Significance": "Importanza culturale",
                "Modern Applications": "Applicazioni moderne",
                "Learning and Education": "Apprendimento e insegnamento",
                "Variations and Related Instruments": "Variazioni e strumenti correlati",
                "Conclusion": "Conclusione",
            },
            "pt": {
                "Introduction": "Introdução",
                "History and Development": "História e desenvolvimento",
                "Construction and Design": "Construção e design",
                "Playing Technique": "Técnica de execução",
                "Notable Players": "Instrumentistas notáveis",
                "Musical Genres": "Gêneros musicais",
                "Cultural Significance": "Significado cultural",
                "Modern Applications": "Aplicações modernas",
                "Learning and Education": "Aprendizagem e educação",
                "Variations and Related Instruments": "Variações e instrumentos relacionados",
                "Conclusion": "Conclusão",
            },
            "da": {
                "Introduction": "Introduktion",
                "History and Development": "Historie og udvikling",
                "Construction and Design": "Konstruktion og design",
                "Playing Technique": "Spilleteknik",
                "Notable Players": "Kendte udøvere",
                "Musical Genres": "Musikalske genrer",
                "Cultural Significance": "Kulturel betydning",
                "Modern Applications": "Moderne anvendelser",
                "Learning and Education": "Læring og undervisning",
                "Variations and Related Instruments": "Variationer og beslægtede instrumenter",
                "Conclusion": "Konklusion",
            },
            "nl": {
                "Introduction": "Inleiding",
                "History and Development": "Geschiedenis en ontwikkeling",
                "Construction and Design": "Constructie en ontwerp",
                "Playing Technique": "Speeltechniek",
                "Notable Players": "Bekende uitvoerenden",
                "Musical Genres": "Muziekgenres",
                "Cultural Significance": "Culturele betekenis",
                "Modern Applications": "Moderne toepassingen",
                "Learning and Education": "Leren en onderwijs",
                "Variations and Related Instruments": "Variaties en verwante instrumenten",
                "Conclusion": "Conclusie",
            },
            "sv": {
                "Introduction": "Introduktion",
                "History and Development": "Historia och utveckling",
                "Construction and Design": "Konstruktion och design",
                "Playing Technique": "Spelteknik",
                "Notable Players": "Kända utövare",
                "Musical Genres": "Musikgenrer",
                "Cultural Significance": "Kulturell betydelse",
                "Modern Applications": "Moderna tillämpningar",
                "Learning and Education": "Lärande och undervisning",
                "Variations and Related Instruments": "Variationer och relaterade instrument",
                "Conclusion": "Slutsats",
            },
            "fi": {
                "Introduction": "Johdanto",
                "History and Development": "Historia ja kehitys",
                "Construction and Design": "Rakenne ja suunnittelu",
                "Playing Technique": "Soittotekniikka",
                "Notable Players": "Tunnetut soittajat",
                "Musical Genres": "Musiikkigenret",
                "Cultural Significance": "Kulttuurinen merkitys",
                "Modern Applications": "Modernit sovellukset",
                "Learning and Education": "Oppiminen ja opetus",
                "Variations and Related Instruments": "Variaatiot ja lähisoittimet",
                "Conclusion": "Yhteenveto",
            },
        }

        # Get the section titles for the current language
        section_titles = sections.get(language, sections["en"])

        # Define character limits for each section
        return {
            section_titles["Introduction"]: 1500,
            section_titles["History and Development"]: 2000,
            section_titles["Construction and Design"]: 2000,
            section_titles["Playing Technique"]: 2000,
            section_titles["Notable Players"]: 2000,
            section_titles["Musical Genres"]: 1500,
            section_titles["Cultural Significance"]: 1500,
            section_titles["Modern Applications"]: 1500,
            section_titles["Learning and Education"]: 1500,
            section_titles["Variations and Related Instruments"]: 1500,
            section_titles["Conclusion"]: 1000,
        }

    elif "Countries" in category_type:  # Countries and Regional Genres
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Historical and Cultural Context": "Historical and Cultural Context",
                "Traditional Music": "Traditional Music",
                "Modern Music Development": "Modern Music Development",
                "Notable Artists and Bands": "Notable Artists and Bands",
                "Music Industry and Infrastructure": "Music Industry and Infrastructure",
                "Live Music and Events": "Live Music and Events",
                "Media and Promotion": "Media and Promotion",
                "Education and Support": "Education and Support",
                "International Connections": "International Connections",
                "Current Trends and Future": "Current Trends and Future",
            },
            "de": {
                "Introduction": "Einleitung",
                "Historical and Cultural Context": "Historischer und kultureller Kontext",
                "Traditional Music": "Traditionelle Musik",
                "Modern Music Development": "Moderne Musikentwicklung",
                "Notable Artists and Bands": "Bedeutende Künstler und Bands",
                "Music Industry and Infrastructure": "Musikindustrie und Infrastruktur",
                "Live Music and Events": "Live-Musik und Veranstaltungen",
                "Media and Promotion": "Medien und Promotion",
                "Education and Support": "Ausbildung und Förderung",
                "International Connections": "Internationale Verbindungen",
                "Current Trends and Future": "Aktuelle Trends und Zukunft",
            },
            "es": {
                "Introduction": "Introducción",
                "Historical and Cultural Context": "Contexto histórico y cultural",
                "Traditional Music": "Música tradicional",
                "Modern Music Development": "Desarrollo de la música moderna",
                "Notable Artists and Bands": "Artistas y bandas destacados",
                "Music Industry and Infrastructure": "Industria musical e infraestructura",
                "Live Music and Events": "Música en vivo y eventos",
                "Media and Promotion": "Medios y promoción",
                "Education and Support": "Educación y apoyo",
                "International Connections": "Conexiones internacionales",
                "Current Trends and Future": "Tendencias actuales y futuro",
            },
            "fr": {
                "Introduction": "Introduction",
                "Historical and Cultural Context": "Contexte historique et culturel",
                "Traditional Music": "Musique traditionnelle",
                "Modern Music Development": "Développement de la musique moderne",
                "Notable Artists and Bands": "Artistes et groupes notables",
                "Music Industry and Infrastructure": "Industrie musicale et infrastructure",
                "Live Music and Events": "Musique live et événements",
                "Media and Promotion": "Médias et promotion",
                "Education and Support": "Éducation et soutien",
                "International Connections": "Connexions internationales",
                "Current Trends and Future": "Tendances actuelles et avenir",
            },
            "it": {
                "Introduction": "Introduzione",
                "Historical and Cultural Context": "Contesto storico e culturale",
                "Traditional Music": "Musica tradizionale",
                "Modern Music Development": "Sviluppo della musica moderna",
                "Notable Artists and Bands": "Artisti e band di rilievo",
                "Music Industry and Infrastructure": "Industria musicale e infrastrutture",
                "Live Music and Events": "Musica dal vivo ed eventi",
                "Media and Promotion": "Media e promozione",
                "Education and Support": "Educazione e supporto",
                "International Connections": "Connessioni internazionali",
                "Current Trends and Future": "Tendenze attuali e futuro",
            },
            "pt": {
                "Introduction": "Introdução",
                "Historical and Cultural Context": "Contexto histórico e cultural",
                "Traditional Music": "Música tradicional",
                "Modern Music Development": "Desenvolvimento da música moderna",
                "Notable Artists and Bands": "Artistas e bandas notáveis",
                "Music Industry and Infrastructure": "Indústria musical e infraestrutura",
                "Live Music and Events": "Música ao vivo e eventos",
                "Media and Promotion": "Mídia e promoção",
                "Education and Support": "Educação e apoio",
                "International Connections": "Conexões internacionais",
                "Current Trends and Future": "Tendências atuais e futuro",
            },
            "da": {
                "Introduction": "Introduktion",
                "Historical and Cultural Context": "Historisk og kulturel kontekst",
                "Traditional Music": "Traditionel musik",
                "Modern Music Development": "Moderne musikudvikling",
                "Notable Artists and Bands": "Bemærkelsesværdige kunstnere og bands",
                "Music Industry and Infrastructure": "Musikindustri og infrastruktur",
                "Live Music and Events": "Livekoncerter og begivenheder",
                "Media and Promotion": "Medier og promovering",
                "Education and Support": "Uddannelse og støtte",
                "International Connections": "Internationale forbindelser",
                "Current Trends and Future": "Aktuelle tendenser og fremtid",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Historical and Cultural Context": "Historische en culturele context",
                "Traditional Music": "Traditionele muziek",
                "Modern Music Development": "Moderne muziekontwikkeling",
                "Notable Artists and Bands": "Opmerkelijke artiesten en bands",
                "Music Industry and Infrastructure": "Muziekindustrie en infrastructuur",
                "Live Music and Events": "Live muziek en evenementen",
                "Media and Promotion": "Media en promotie",
                "Education and Support": "Opleiding en ondersteuning",
                "International Connections": "Internationale verbindingen",
                "Current Trends and Future": "Huidige trends en toekomst",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Historical and Cultural Context": "Historisk och kulturell kontext",
                "Traditional Music": "Traditionell musik",
                "Modern Music Development": "Modern musikutveckling",
                "Notable Artists and Bands": "Framstående artister och band",
                "Music Industry and Infrastructure": "Musikindustri och infrastruktur",
                "Live Music and Events": "Livemusik och evenemang",
                "Media and Promotion": "Media och marknadsföring",
                "Education and Support": "Utbildning och stöd",
                "International Connections": "Internationella kontakter",
                "Current Trends and Future": "Aktuella trender och framtid",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Historical and Cultural Context": "Historiallinen ja kulttuurinen konteksti",
                "Traditional Music": "Perinteinen musiikki",
                "Modern Music Development": "Modernin musiikin kehitys",
                "Notable Artists and Bands": "Merkittävät artistit ja yhtyet",
                "Music Industry and Infrastructure": "Musiikkiteollisuus ja infrastruktuuri",
                "Live Music and Events": "Live-musiikki ja tapahtumat",
                "Media and Promotion": "Media ja markkinointi",
                "Education and Support": "Koulutus ja tuki",
                "International Connections": "Kansainväliset yhteydet",
                "Current Trends and Future": "Nykyiset trendit ja tulevaisuus",
            },
        }

        section_titles = sections.get(language, sections["en"])
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Historical and Cultural Context"]: 2000,
            section_titles["Traditional Music"]: 2000,
            section_titles["Modern Music Development"]: 2000,
            section_titles["Notable Artists and Bands"]: 2000,
            section_titles["Music Industry and Infrastructure"]: 1500,
            section_titles["Live Music and Events"]: 1500,
            section_titles["Media and Promotion"]: 1500,
            section_titles["Education and Support"]: 1500,
            section_titles["International Connections"]: 1500,
            section_titles["Current Trends and Future"]: 1500,
        }
    elif "Emotional" in category_type:  # Emotional Genres
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Music Psychology": "Music Psychology",
                "Musical Characteristics": "Musical Characteristics",
                "Cross-Genre Examples": "Cross-Genre Examples",
                "Cultural Perspectives": "Cultural Perspectives",
                "Therapeutic Applications": "Therapeutic Applications",
                "Notable Works and Artists": "Notable Works and Artists",
                "Use in Media": "Use in Media",
                "Modern Interpretations": "Modern Interpretations",
                "Practical Significance": "Practical Significance",
            },
            "de": {
                "Introduction": "Einleitung",
                "Music Psychology": "Musikpsychologie",
                "Musical Characteristics": "Musikalische Merkmale",
                "Cross-Genre Examples": "Genreübergreifende Beispiele",
                "Cultural Perspectives": "Kulturelle Perspektiven",
                "Therapeutic Applications": "Therapeutische Anwendungen",
                "Notable Works and Artists": "Bedeutende Werke und Künstler",
                "Use in Media": "Verwendung in Medien",
                "Modern Interpretations": "Moderne Interpretationen",
                "Practical Significance": "Praktische Bedeutung",
            },
            "es": {
                "Introduction": "Introducción",
                "Music Psychology": "Psicología musical",
                "Musical Characteristics": "Características musicales",
                "Cross-Genre Examples": "Ejemplos entre géneros",
                "Cultural Perspectives": "Perspectivas culturales",
                "Therapeutic Applications": "Aplicaciones terapéuticas",
                "Notable Works and Artists": "Obras y artistas destacados",
                "Use in Media": "Uso en medios",
                "Modern Interpretations": "Interpretaciones modernas",
                "Practical Significance": "Significado práctico",
            },
            "fr": {
                "Introduction": "Introduction",
                "Music Psychology": "Psychologie musicale",
                "Musical Characteristics": "Caractéristiques musicales",
                "Cross-Genre Examples": "Exemples inter-genres",
                "Cultural Perspectives": "Perspectives culturelles",
                "Therapeutic Applications": "Applications thérapeutiques",
                "Notable Works and Artists": "Œuvres et artistes notables",
                "Use in Media": "Utilisation dans les médias",
                "Modern Interpretations": "Interprétations modernes",
                "Practical Significance": "Signification pratique",
            },
            "it": {
                "Introduction": "Introduzione",
                "Music Psychology": "Psicologia musicale",
                "Musical Characteristics": "Caratteristiche musicali",
                "Cross-Genre Examples": "Esempi tra generi",
                "Cultural Perspectives": "Prospettive culturali",
                "Therapeutic Applications": "Applicazioni terapeutiche",
                "Notable Works and Artists": "Opere e artisti notevoli",
                "Use in Media": "Uso nei media",
                "Modern Interpretations": "Interpretazioni moderne",
                "Practical Significance": "Significato pratico",
            },
            "pt": {
                "Introduction": "Introdução",
                "Music Psychology": "Psicologia musical",
                "Musical Characteristics": "Características musicais",
                "Cross-Genre Examples": "Exemplos entre gêneros",
                "Cultural Perspectives": "Perspectivas culturais",
                "Therapeutic Applications": "Aplicações terapêuticas",
                "Notable Works and Artists": "Obras e artistas notáveis",
                "Use in Media": "Uso na mídia",
                "Modern Interpretations": "Interpretações modernas",
                "Practical Significance": "Significado prático",
            },
            "da": {
                "Introduction": "Introduktion",
                "Music Psychology": "Musikpsykologi",
                "Musical Characteristics": "Musikalske karakteristika",
                "Cross-Genre Examples": "Eksempler på tværs af genrer",
                "Cultural Perspectives": "Kulturelle perspektiver",
                "Therapeutic Applications": "Terapeutiske anvendelser",
                "Notable Works and Artists": "Bemærkelsesværdige værker og kunstnere",
                "Use in Media": "Brug i medier",
                "Modern Interpretations": "Moderne fortolkninger",
                "Practical Significance": "Praktisk betydning",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Music Psychology": "Muziekpsychologie",
                "Musical Characteristics": "Muzikale kenmerken",
                "Cross-Genre Examples": "Voorbeelden over genres heen",
                "Cultural Perspectives": "Culturele perspectieven",
                "Therapeutic Applications": "Therapeutische toepassingen",
                "Notable Works and Artists": "Opmerkelijke werken en artiesten",
                "Use in Media": "Gebruik in media",
                "Modern Interpretations": "Moderne interpretaties",
                "Practical Significance": "Praktische betekenis",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Music Psychology": "Musikpsykologi",
                "Musical Characteristics": "Musikaliska egenskaper",
                "Cross-Genre Examples": "Exempel över genregränser",
                "Cultural Perspectives": "Kulturella perspektiv",
                "Therapeutic Applications": "Terapeutiska tillämpningar",
                "Notable Works and Artists": "Framstående verk och artister",
                "Use in Media": "Användning i media",
                "Modern Interpretations": "Moderna tolkningar",
                "Practical Significance": "Praktisk betydelse",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Music Psychology": "Musiikkipsykologia",
                "Musical Characteristics": "Musiikilliset ominaisuudet",
                "Cross-Genre Examples": "Esimerkkejä eri genreistä",
                "Cultural Perspectives": "Kulttuuriset näkökulmat",
                "Therapeutic Applications": "Terapeuttiset sovellukset",
                "Notable Works and Artists": "Merkittävät teokset ja artistit",
                "Use in Media": "Käyttö mediassa",
                "Modern Interpretations": "Modernit tulkinnat",
                "Practical Significance": "Käytännön merkitys",
            },
        }

        section_titles = sections.get(language, sections["en"])
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Music Psychology"]: 2000,
            section_titles["Musical Characteristics"]: 2000,
            section_titles["Cross-Genre Examples"]: 2000,
            section_titles["Cultural Perspectives"]: 1500,
            section_titles["Therapeutic Applications"]: 1500,
            section_titles["Notable Works and Artists"]: 2000,
            section_titles["Use in Media"]: 1500,
            section_titles["Modern Interpretations"]: 1500,
            section_titles["Practical Significance"]: 1500,
        }
    elif "Seasonal" in category_type:  # Seasonal Genres
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Cultural Tradition": "Cultural Tradition",
                "Musical Characteristics": "Musical Characteristics",
                "Classical Compositions": "Classical Compositions",
                "Popular Music": "Popular Music",
                "Festive Events": "Festive Events",
                "Media Presence": "Media Presence",
                "International Perspectives": "International Perspectives",
            },
            "de": {
                "Introduction": "Einleitung",
                "Cultural Tradition": "Kulturelle Tradition",
                "Musical Characteristics": "Musikalische Merkmale",
                "Classical Compositions": "Klassische Kompositionen",
                "Popular Music": "Populäre Musik",
                "Festive Events": "Festliche Veranstaltungen",
                "Media Presence": "Medienpräsenz",
                "International Perspectives": "Internationale Perspektiven",
            },
            "es": {
                "Introduction": "Introducción",
                "Cultural Tradition": "Tradición cultural",
                "Musical Characteristics": "Características musicales",
                "Classical Compositions": "Composiciones clásicas",
                "Popular Music": "Música popular",
                "Festive Events": "Eventos festivos",
                "Media Presence": "Presencia en medios",
                "International Perspectives": "Perspectivas internacionales",
            },
            "fr": {
                "Introduction": "Introduction",
                "Cultural Tradition": "Tradition culturelle",
                "Musical Characteristics": "Caractéristiques musicales",
                "Classical Compositions": "Compositions classiques",
                "Popular Music": "Musique populaire",
                "Festive Events": "Événements festifs",
                "Media Presence": "Présence médiatique",
                "International Perspectives": "Perspectives internationales",
            },
            "it": {
                "Introduction": "Introduzione",
                "Cultural Tradition": "Tradizione culturale",
                "Musical Characteristics": "Caratteristiche musicali",
                "Classical Compositions": "Composizioni classiche",
                "Popular Music": "Musica popolare",
                "Festive Events": "Eventi festivi",
                "Media Presence": "Presenza nei media",
                "International Perspectives": "Prospettive internazionali",
            },
            "pt": {
                "Introduction": "Introdução",
                "Cultural Tradition": "Tradição cultural",
                "Musical Characteristics": "Características musicais",
                "Classical Compositions": "Composições clássicas",
                "Popular Music": "Música popular",
                "Festive Events": "Eventos festivos",
                "Media Presence": "Presença na mídia",
                "International Perspectives": "Perspectivas internacionais",
            },
            "da": {
                "Introduction": "Introduktion",
                "Cultural Tradition": "Kulturel tradition",
                "Musical Characteristics": "Musikalske karakteristika",
                "Classical Compositions": "Klassiske kompositioner",
                "Popular Music": "Populær musik",
                "Festive Events": "Festlige begivenheder",
                "Media Presence": "Tilstedeværelse i medierne",
                "International Perspectives": "Internationale perspektiver",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Cultural Tradition": "Culturele traditie",
                "Musical Characteristics": "Muzikale kenmerken",
                "Classical Compositions": "Klassieke composities",
                "Popular Music": "Populaire muziek",
                "Festive Events": "Feestelijke evenementen",
                "Media Presence": "Aanwezigheid in de media",
                "International Perspectives": "Internationale perspectieven",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Cultural Tradition": "Kulturell tradition",
                "Musical Characteristics": "Musikaliska egenskaper",
                "Classical Compositions": "Klassiska kompositioner",
                "Popular Music": "Populärmusik",
                "Festive Events": "Festliga evenemang",
                "Media Presence": "Medienärvaro",
                "International Perspectives": "Internationella perspektiv",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Cultural Tradition": "Kulttuuriperinne",
                "Musical Characteristics": "Musiikilliset ominaisuudet",
                "Classical Compositions": "Klassiset sävellykset",
                "Popular Music": "Populaarimusiikki",
                "Festive Events": "Juhlatapahtumat",
                "Media Presence": "Medianäkyvyys",
                "International Perspectives": "Kansainväliset näkökulmat",
            },
        }

        section_titles = sections.get(language, sections["en"])
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Cultural Tradition"]: 2000,
            section_titles["Musical Characteristics"]: 2000,
            section_titles["Classical Compositions"]: 2000,
            section_titles["Popular Music"]: 2000,
            section_titles["Festive Events"]: 1500,
            section_titles["Media Presence"]: 1500,
            section_titles["International Perspectives"]: 1500,
        }
    else:  # Standard Genres
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
                "Legacy and Influence": "Legacy and Influence",
            },
            "de": {
                "Introduction": "Einleitung",
                "Historical Background": "Historischer Hintergrund",
                "Musical Characteristics": "Musikalische Merkmale",
                "Subgenres and Variations": "Subgenres und Variationen",
                "Key Figures and Important Works": "Schlüsselfiguren und wichtige Werke",
                "Technical Aspects": "Technische Aspekte",
                "Cultural Significance": "Kulturelle Bedeutung",
                "Performance and Live Culture": "Aufführung und Live-Kultur",
                "Development and Evolution": "Entwicklung und Evolution",
                "Legacy and Influence": "Vermächtnis und Einfluss",
            },
            "es": {
                "Introduction": "Introducción",
                "Historical Background": "Contexto histórico",
                "Musical Characteristics": "Características musicales",
                "Subgenres and Variations": "Subgéneros y variaciones",
                "Key Figures and Important Works": "Figuras clave y obras importantes",
                "Technical Aspects": "Aspectos técnicos",
                "Cultural Significance": "Significado cultural",
                "Performance and Live Culture": "Interpretación y cultura en vivo",
                "Development and Evolution": "Desarrollo y evolución",
                "Legacy and Influence": "Legado e influencia",
            },
            "fr": {
                "Introduction": "Introduction",
                "Historical Background": "Contexte historique",
                "Musical Characteristics": "Caractéristiques musicales",
                "Subgenres and Variations": "Sous-genres et variations",
                "Key Figures and Important Works": "Figures clés et œuvres importantes",
                "Technical Aspects": "Aspects techniques",
                "Cultural Significance": "Signification culturelle",
                "Performance and Live Culture": "Performance et culture live",
                "Development and Evolution": "Développement et évolution",
                "Legacy and Influence": "Héritage et influence",
            },
            "it": {
                "Introduction": "Introduzione",
                "Historical Background": "Contesto storico",
                "Musical Characteristics": "Caratteristiche musicali",
                "Subgenres and Variations": "Sottogeneri e variazioni",
                "Key Figures and Important Works": "Figure chiave e opere importanti",
                "Technical Aspects": "Aspetti tecnici",
                "Cultural Significance": "Significato culturale",
                "Performance and Live Culture": "Performance e cultura dal vivo",
                "Development and Evolution": "Sviluppo ed evoluzione",
                "Legacy and Influence": "Eredità e influenza",
            },
            "pt": {
                "Introduction": "Introdução",
                "Historical Background": "Contexto histórico",
                "Musical Characteristics": "Características musicais",
                "Subgenres and Variations": "Subgêneros e variações",
                "Key Figures and Important Works": "Figuras-chave e obras importantes",
                "Technical Aspects": "Aspectos técnicos",
                "Cultural Significance": "Significância cultural",
                "Performance and Live Culture": "Performance e cultura ao vivo",
                "Development and Evolution": "Desenvolvimento e evolução",
                "Legacy and Influence": "Legado e influência",
            },
            "da": {
                "Introduction": "Introduktion",
                "Historical Background": "Historisk baggrund",
                "Musical Characteristics": "Musikalske karakteristika",
                "Subgenres and Variations": "Undergenrer og variationer",
                "Key Figures and Important Works": "Nøglepersoner og vigtige værker",
                "Technical Aspects": "Tekniske aspekter",
                "Cultural Significance": "Kulturel betydning",
                "Performance and Live Culture": "Optræden og livekultur",
                "Development and Evolution": "Udvikling og evolution",
                "Legacy and Influence": "Arv og indflydelse",
            },
            "nl": {
                "Introduction": "Inleiding",
                "Historical Background": "Historische achtergrond",
                "Musical Characteristics": "Muzikale kenmerken",
                "Subgenres and Variations": "Subgenres en variaties",
                "Key Figures and Important Works": "Belangrijke figuren en werken",
                "Technical Aspects": "Technische aspecten",
                "Cultural Significance": "Culturele betekenis",
                "Performance and Live Culture": "Uitvoering en livecultuur",
                "Development and Evolution": "Ontwikkeling en evolutie",
                "Legacy and Influence": "Erfenis en invloed",
            },
            "sv": {
                "Introduction": "Introduktion",
                "Historical Background": "Historisk bakgrund",
                "Musical Characteristics": "Musikaliska egenskaper",
                "Subgenres and Variations": "Undergenrer och variationer",
                "Key Figures and Important Works": "Nyckelfigurer och viktiga verk",
                "Technical Aspects": "Tekniska aspekter",
                "Cultural Significance": "Kulturell betydelse",
                "Performance and Live Culture": "Framträdande och livekultur",
                "Development and Evolution": "Utveckling och evolution",
                "Legacy and Influence": "Arv och påverkan",
            },
            "fi": {
                "Introduction": "Johdanto",
                "Historical Background": "Historiallinen tausta",
                "Musical Characteristics": "Musiikilliset ominaisuudet",
                "Subgenres and Variations": "Alagenret ja variaatiot",
                "Key Figures and Important Works": "Avainhahmot ja tärkeät teokset",
                "Technical Aspects": "Tekniset näkökohdat",
                "Cultural Significance": "Kulttuurinen merkitys",
                "Performance and Live Culture": "Esiintyminen ja livekulttuuri",
                "Development and Evolution": "Kehitys ja evoluutio",
                "Legacy and Influence": "Perintö ja vaikutus",
            },
        }

        section_titles = sections.get(language, sections["en"])
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Historical Background"]: 2000,
            section_titles["Musical Characteristics"]: 2000,
            section_titles["Subgenres and Variations"]: 1500,
            section_titles["Key Figures and Important Works"]: 2000,
            section_titles["Technical Aspects"]: 1500,
            section_titles["Cultural Significance"]: 2000,
            section_titles["Performance and Live Culture"]: 1500,
            section_titles["Development and Evolution"]: 1500,
            section_titles["Legacy and Influence"]: 1500,
        }

    # Anwenden des Sprachfaktors auf alle Limits
    adjusted_limits = {}
    for section, min_chars in base_limits.items():
        adjusted_limits[section] = int(min_chars * factor)

    return adjusted_limits


def get_language_prompts(language):
    prompts = {
        "de": {
            "style": "Klares, verständliches Deutsch",
            "characteristics": "präzise Fachterminologie, komplexe Satzstrukturen, formelle Ausdrucksweise, musikwissenschaftliche Genauigkeit",
            "prompt": """
            Erstelle Inhalte für den Abschnitt '{section_name}' der Musikkategorie '{category}'.
            
            SPRACHLICHE ANFORDERUNGEN:
            1. Verwende ausschließlich standardisiertes Hochdeutsch
            2. Nutze präzise musikwissenschaftliche Fachterminologie
            3. Vermeide Anglizismen und umgangssprachliche Ausdrücke
            4. Achte auf korrekte deutsche Grammatik und Rechtschreibung
            5. Verwende natürliche Satzkonstruktionen und Übergänge
            6. Stelle sicher, dass der Text flüssig lesbar ist
            7. Beachte die deutsche Kommasetzung und Zeichensetzung
            8. Nutze idiomatische deutsche Wendungen wo angemessen
            9. Berücksichtige den deutschen Sprachrhythmus
            10. Verwende dem Kontext angemessene Formulierungen
            
            ABSATZSTRUKTUR UND LESEFLUSS:
            1. Beginne einen neuen Absatz bei jedem Themenwechsel oder neuer Idee
            2. Halte Absätze auf 3-5 Sätze begrenzt für optimale Lesbarkeit
            3. Verwende kürzere Absätze für wichtige Aussagen oder Übergänge
            4. Schaffe visuelle Pausen im Text durch sinnvolle Absatzstruktur
            5. Stelle sicher, dass jeder Absatz eine klare Kernaussage enthält
            6. Vermeide zu lange, ungegliederte Textblöcke
            7. Nutze Absätze zur inhaltlichen Strukturierung und Argumentationsentwicklung
            
            ABSATZÜBERGÄNGE UND TEXTFLUSS:
            1. Schaffe nahtlose Übergänge zwischen allen Absätzen
            2. Verwende Überleitungswörter und -sätze (z.B. "Zudem", "Darüber hinaus", "Im Gegensatz dazu")
            3. Stelle inhaltliche Verbindungen zwischen aufeinanderfolgenden Absätzen her
            4. Sorge für thematische Kontinuität durch den gesamten Text
            5. Nutze Bezugnahmen auf vorherige Absätze, um Kohärenz zu schaffen
            6. Vermeide abrupte Themenwechsel ohne passende Überleitungen
            7. Entwickle Argumente und Ideen über mehrere Absätze hinweg fließend
            8. Baue eine logische Progression auf, die den Leser durch den Text führt
            
            INHALTLICHE ANFORDERUNGEN:
            1. Der Text MUSS mindestens {char_min} Zeichen lang sein
            2. Konzentriere dich ausschließlich auf internationale Musik
            3. Strukturiere den Text mit klaren, logischen Absätzen
            4. Verwende komplexe, aber verständliche Satzstrukturen
            5. Vermeide Aufzählungen zugunsten fließender Textpassagen
            6. Integriere kulturhistorische Kontexte wo relevant
            7. Nutze präzise musikalische Fachbegriffe
            8. Stelle musiktheoretische Zusammenhänge klar dar
            9. Verwende angemessene Überleitungen zwischen Absätzen
            10. Wahre durchgehend einen akademischen Schreibstil
            
            KRITISCH: Die Mindestzeichenzahl von {char_min} ist zwingend einzuhalten.
            """,
        },
        "en": {
            "style": "Clear and simple English",
            "characteristics": "precise musicological terminology, scholarly tone, complex sentence structures, formal academic style",
            "prompt": """
            Create content for the section '{section_name}' of the music category '{category}'.
            
            LINGUISTIC REQUIREMENTS:
            1. Use formal British English exclusively
            2. Employ precise musicological terminology
            3. Avoid colloquialisms and informal expressions
            4. Ensure proper English grammar and spelling
            5. Use natural sentence constructions and transitions
            6. Maintain smooth reading flow throughout
            7. Follow British English punctuation rules
            8. Use idiomatic expressions where appropriate
            9. Consider English language rhythm and cadence
            10. Apply context-appropriate phrasing
            
            PARAGRAPH STRUCTURE AND READABILITY:
            1. Begin a new paragraph with each topic change or new idea
            2. Keep paragraphs to 3-5 sentences for optimal readability
            3. Use shorter paragraphs for important statements or transitions
            4. Create visual breaks in the text through thoughtful paragraph structure
            5. Ensure each paragraph contains one clear main point
            6. Avoid long, undivided blocks of text
            7. Use paragraphs to structure content and develop arguments
            
            PARAGRAPH TRANSITIONS AND TEXT FLOW:
            1. Create seamless transitions between all paragraphs
            2. Use transitional words and phrases (e.g., "Moreover," "Furthermore," "In contrast")
            3. Establish content connections between consecutive paragraphs
            4. Maintain thematic continuity throughout the entire text
            5. Reference previous paragraphs to build coherence
            6. Avoid abrupt topic changes without appropriate transitions
            7. Develop arguments and ideas fluidly across multiple paragraphs
            8. Build a logical progression that guides the reader through the text
            
            CONTENT SPECIFICATIONS:
            1. Text length MUST be at least {char_min} characters
            2. Focus exclusively on international music
            3. Structure content with clear, logical paragraphs
            4. Employ complex yet comprehensible sentence structures
            5. Avoid bullet points in favor of flowing prose
            6. Integrate relevant cultural-historical contexts
            7. Utilize accurate musical terminology
            8. Articulate music-theoretical relationships clearly
            9. Implement appropriate inter-paragraph transitions
            10. Maintain consistent scholarly tone throughout
            
            CRITICAL: Character count MUST be at least {char_min}.
            """,
        },
        "fr": {
            "style": "Français clair et simple",
            "characteristics": "terminologie musicologique précise, style académique rigoureux, structures syntaxiques complexes",
            "prompt": """
            Élaborez un contenu académique pour la section '{section_name}' de la catégorie musicale '{category}'.
            
            EXIGENCES LINGUISTIQUES:
            1. Employez un français académique rigoureux
            2. Utilisez une terminologie musicologique précise
            3. Évitez les anglicismes et expressions familières
            4. Respectez la grammaire et l'orthographe françaises
            5. Utilisez des constructions de phrases naturelles
            6. Assurez une lecture fluide du texte
            7. Respectez la ponctuation française
            8. Employez des expressions idiomatiques appropriées
            9. Tenez compte du rythme de la langue française
            10. Adaptez le style au contexte culturel français
            
            STRUCTURE DES PARAGRAPHES ET LISIBILITÉ:
            1. Commencez un nouveau paragraphe à chaque changement de sujet ou nouvelle idée
            2. Limitez les paragraphes à 3-5 phrases pour une lisibilité optimale
            3. Utilisez des paragraphes plus courts pour des déclarations importantes ou des transitions
            4. Créez des pauses visuelles dans le texte grâce à une structure de paragraphe réfléchie
            5. Assurez-vous que chaque paragraphe contient un point principal clair
            6. Évitez les blocs de texte longs et non divisés
            7. Utilisez des paragraphes pour structurer le contenu et développer des arguments
            
            TRANSITIONS ENTRE PARAGRAPHES ET FLUX DU TEXTE:
            1. Créez des transitions fluides entre tous les paragraphes
            2. Utilisez des mots et des phrases de transition (par exemple, "De plus", "En outre", "En revanche")
            3. Établissez des connexions de contenu entre les paragraphes consécutifs
            4. Maintenez la continuité thématique tout au long du texte
            5. Faites référence aux paragraphes précédents pour renforcer la cohérence
            6. Évitez les changements de sujet abrupts sans transitions appropriées
            7. Développez des arguments et des idées de manière fluide sur plusieurs paragraphes
            8. Construisez une progression logique qui guide le lecteur à travers le texte
            
            EXIGENCES DE CONTENU:
            1. Respectez strictement le minimum de caractères : {char_min}
            2. Développez une analyse académique de la musique internationale
            3. Structurez le texte avec des paragraphes logiquement articulés
            4. Intégrez les aspects théoriques et le contexte historique
            5. Privilégiez l'argumentation à l'énumération
            6. Incorporez des références culturelles pertinentes
            7. Appliquez la terminologie musicale avec précision
            8. Maintenez un registre académique constant
            9. Utilisez des citations selon les normes académiques
            10. Préservez une approche analytique rigoureuse
            
            ESSENTIEL : Le nombre de caractères doit être au moins {char_min}.
            """,
        },
        "es": {
            "style": "Español claro y sencillo",
            "characteristics": "terminología musicológica precisa, estilo académico riguroso, estructuras sintácticas complejas",
            "prompt": """
            Elabore un contenido académico para la sección '{section_name}' de la categoría musical '{category}'.
            
            REQUISITOS LINGÜÍSTICOS:
            1. Emplee un español académico riguroso
            2. Utilice terminología musicológica precisa
            3. Evite anglicismos y expresiones coloquiales
            4. Cuide la gramática y ortografía españolas
            5. Use construcciones naturales de frases
            6. Garantice una lectura fluida
            7. Respete las normas de puntuación españolas
            8. Emplee expresiones idiomáticas adecuadas
            9. Considere el ritmo del español
            10. Adapte el estilo al contexto hispanohablante
            
            ESTRUCTURA DE PÁRRAFOS Y LEGIBILIDAD:
            1. Comience un nuevo párrafo con cada cambio de tema o nueva idea
            2. Mantenga los párrafos en 3-5 oraciones para una legibilidad óptima
            3. Use párrafos más cortos para declaraciones importantes o transiciones
            4. Cree pausas visuales en el texto a través de una estructura de párrafo reflexiva
            5. Asegúrese de que cada párrafo contenga un punto principal claro
            6. Evite bloques de texto largos y no divididos
            7. Use párrafos para estructurar el contenido y desarrollar argumentos
            
            TRANSICIONES ENTRE PÁRRAFOS Y FLUJO DEL TEXTO:
            1. Cree transiciones fluidas entre todos los párrafos
            2. Use palabras y frases de transición (por ejemplo, "Además", "Asimismo", "En contraste")
            3. Establezca conexiones de contenido entre párrafos consecutivos
            4. Mantenga la continuidad temática a lo largo de todo el texto
            5. Haga referencia a párrafos anteriores para construir coherencia
            6. Evite cambios abruptos de tema sin transiciones apropiadas
            7. Desarrolle argumentos e ideas de manera fluida a lo largo de varios párrafos
            8. Construya una progresión lógica que guíe al lector a través del texto
            
            REQUISITOS DE CONTENIDO:
            1. Respete estrictamente el mínimo de caracteres: {char_min}
            2. Desarrolle un análisis académico de la música internacional
            3. Estructure el texto con párrafos lógicamente articulados
            4. Integre aspectos teóricos y contexto histórico
            5. Privilegie la argumentación sobre la enumeración
            6. Incorpore referencias culturales pertinentes
            7. Aplique la terminología musical con precisión
            8. Mantenga un registro académico constante
            9. Utilice citas según las normas académicas
            10. Preserve un enfoque analítico riguroso
            
            ESENCIAL: El recuento de caracteres debe ser al menos {char_min}.
            """,
        },
        "it": {
            "style": "Italiano chiaro e semplice",
            "characteristics": "terminologia musicologica precisa, stile accademico rigoroso, strutture sintattiche complesse",
            "prompt": """
            Elabora un contenuto accademico per la sezione '{section_name}' della categoria musicale '{category}'.
            
            REQUISITI LINGUISTICI:
            1. Utilizza un italiano accademico rigoroso
            2. Impiega una terminologia musicologica precisa
            3. Evita anglicismi ed espressioni colloquiali
            4. Rispetta la grammatica e l'ortografia italiana
            5. Usa costruzioni di frasi naturali
            6. Assicura una lettura scorrevole
            7. Segui le regole di punteggiatura italiana
            8. Utilizza espressioni idiomatiche appropriate
            9. Considera il ritmo della lingua italiana
            10. Adatta lo stile al contesto culturale italiano
            
            STRUTTURA DEI PARAGRAFI E LEGGIBILITÀ:
            1. Inizia un nuovo paragrafo con ogni cambio di argomento o nuova idea
            2. Mantieni i paragrafi a 3-5 frasi per una leggibilità ottimale
            3. Usa paragrafi più brevi per dichiarazioni importanti o transizioni
            4. Crea pause visive nel testo attraverso una struttura di paragrafo ponderata
            5. Assicurati che ogni paragrafo contenga un punto principale chiaro
            6. Evita blocchi di testo lunghi e non divisi
            7. Usa i paragrafi per strutturare il contenuto e sviluppare argomenti
            
            TRANSIZIONI TRA PARAGRAFI E FLUSSO DEL TESTO:
            1. Crea transizioni fluide tra tutti i paragrafi
            2. Usa parole e frasi di transizione (ad esempio, "Inoltre", "In aggiunta", "In contrasto")
            3. Stabilisci connessioni di contenuto tra paragrafi consecutivi
            4. Mantieni la continuità tematica in tutto il testo
            5. Fai riferimento ai paragrafi precedenti per costruire coerenza
            6. Evita cambiamenti di argomento bruschi senza transizioni appropriate
            7. Sviluppa argomenti e idee in modo fluido su più paragrafi
            8. Costruisci una progressione logica che guidi il lettore attraverso il testo
            
            REQUISITI DI CONTENUTO:
            1. Rispetta rigorosamente il minimo di caratteri: {char_min}
            2. Sviluppa un'analisi accademica della musica internazionale
            3. Struttura il testo con paragrafi logicamente articolati
            4. Integra aspetti teorici e contesto storico
            5. Privilegia l'argomentazione rispetto all'enumerazione
            6. Incorpora riferimenti culturali pertinenti
            7. Applica la terminologia musicale con precisione
            8. Mantieni un registro accademico costante
            9. Utilizza citazioni secondo le norme accademiche
            10. Preserva un approccio analitico rigoroso
            
            ESSENZIALE: Il conteggio dei caratteri deve essere almeno {char_min}.
            """,
        },
        "pt": {
            "style": "Português claro e simples",
            "characteristics": "terminologia musicológica precisa, estilo académico rigoroso, estruturas sintáticas complexas, metodologia científica",
            "prompt": """
            Elabore um conteúdo acadêmico para a seção '{section_name}' da categoria musical '{category}'.
            
            REQUISITOS LINGUÍSTICOS:
            1. Empregue um português acadêmico rigoroso
            2. Utilize terminologia musicológica precisa
            3. Evite anglicismos e expressões coloquiais
            4. Respeite a gramática e ortografia portuguesa
            5. Use construções naturais de frases
            6. Garanta uma leitura fluida
            7. Siga as regras de pontuação portuguesas
            8. Empregue expressões idiomáticas adequadas
            9. Considere o ritmo da língua portuguesa
            10. Adapte o estilo ao contexto lusófono
            
            ESTRUTURA DE PARÁGRAFOS E LEGIBILIDADE:
            1. Comece um novo parágrafo com cada mudança de tópico ou nova ideia
            2. Mantenha os parágrafos em 3-5 frases para uma legibilidade ideal
            3. Use parágrafos mais curtos para declarações importantes ou transições
            4. Crie pausas visuais no texto através de uma estrutura de parágrafo ponderada
            5. Certifique-se de que cada parágrafo contenha um ponto principal claro
            6. Evite blocos de texto longos e não divididos
            7. Use parágrafos para estruturar o conteúdo e desenvolver argumentos
            
            TRANSIÇÕES ENTRE PARÁGRAFOS E FLUXO DO TEXTO:
            1. Crie transições fluidas entre todos os parágrafos
            2. Use palavras e frases de transição (por exemplo, "Além disso", "Ademais", "Em contraste")
            3. Estabeleça conexões de conteúdo entre parágrafos consecutivos
            4. Mantenha a continuidade temática ao longo de todo o texto
            5. Faça referência a parágrafos anteriores para construir coerência
            6. Evite mudanças abruptas de tópico sem transições apropriadas
            7. Desenvolva argumentos e ideias de forma fluida ao longo de vários parágrafos
            8. Construa uma progressão lógica que guie o leitor através do texto
            
            REQUISITOS DE CONTEÚDO:
            1. Respeite estritamente o mínimo de caracteres: {char_min}
            2. Desenvolva uma análise acadêmica da música internacional
            3. Estruture o texto com parágrafos logicamente articulados
            4. Integre aspectos teóricos e contexto histórico
            5. Privilegie a argumentação sobre a enumeração
            6. Incorpore referências culturais pertinentes
            7. Aplique a terminologia musical com precisão
            8. Mantenha um registro acadêmico constante
            9. Utilize citações segundo as normas acadêmicas
            10. Preserve uma abordagem analítica rigorosa
            
            ESSENCIAL: A contagem de caracteres deve ser pelo menos {char_min}.
            """,
        },
        "nl": {
            "style": "Helder en eenvoudig Nederlands",
            "characteristics": "nauwkeurige musicologische terminologie, wetenschappelijke toon, complexe zinsstructuren",
            "prompt": """
            Maak inhoud voor de sectie '{section_name}' van de muziekcategorie '{category}'.
            
            TAALKUNDIGE VEREISTEN:
            1. Gebruik uitsluitend academisch Nederlands
            2. Hanteer nauwkeurige musicologische terminologie
            3. Vermijd anglicismen en informele uitdrukkingen
            4. Let op correcte Nederlandse grammatica en spelling
            5. Gebruik natuurlijke zinsconstructies
            6. Zorg voor een vloeiende leesbaarheid
            7. Volg de Nederlandse interpunctieregels
            8. Gebruik passende idiomatische uitdrukkingen
            9. Houd rekening met het Nederlandse taalritme
            10. Pas de stijl aan de Nederlandse context aan
            
            STRUCTUUR VAN PARAGRAFEN EN LEESBAARHEID:
            1. Begin een nieuwe alinea bij elke onderwerpwijziging of nieuw idee
            2. Houd alinea's op 3-5 zinnen voor optimale leesbaarheid
            3. Gebruik kortere alinea's voor belangrijke uitspraken of overgangen
            4. Creëer visuele pauzes in de tekst door middel van doordachte alinea-indeling
            5. Zorg ervoor dat elke alinea één duidelijk hoofdidee bevat
            6. Vermijd lange, onverdeelde tekstblokken
            7. Gebruik alinea's om inhoud te structureren en argumenten te ontwikkelen
            
            OVERGANGEN TUSSEN PARAGRAFEN EN TEKSTSTROOM:
            1. Creëer naadloze overgangen tussen alle alinea's
            2. Gebruik overgangswoorden en -zinnen (bijv. "Bovendien", "Verder", "In tegenstelling tot")
            3. Leg inhoudelijke verbanden tussen opeenvolgende alinea's
            4. Behoud thematische continuïteit door de hele tekst
            5. Verwijs naar eerdere alinea's om samenhang te creëren
            6. Vermijd abrupte onderwerpwisselingen zonder passende overgangen
            7. Ontwikkel argumenten en ideeën vloeiend over meerdere alinea's
            8. Bouw een logische voortgang op die de lezer door de tekst leidt
            
            INHOUDELIJKE VEREISTEN:
            1. De tekst MOET minimaal {char_min} tekens bevatten
            2. Focus uitsluitend op internationale muziek
            3. Structureer de inhoud met duidelijke, logische alinea's
            4. Gebruik complexe maar begrijpelijke zinsstructuren
            5. Vermijd opsommingen ten gunste van vloeiende tekst
            6. Integreer relevante cultuurhistorische contexten
            7. Gebruik nauwkeurige muzikale terminologie
            8. Articuleer muziektheoretische verbanden helder
            9. Implementeer passende overgangen tussen alinea's
            10. Behoud een consistente wetenschappelijke toon
            
            KRITISCH: Het aantal tekens MOET minimaal {char_min} zijn.
            """,
        },
        "da": {
            "style": "Klar og enkel dansk",
            "characteristics": "præcis musikologisk terminologi, akademisk tone, komplekse sætningsstrukturer",
            "prompt": """
            Opret indhold til sektionen '{section_name}' i musikkategorien '{category}'.
            
            SPROGLIGE KRAV:
            1. Brug udelukkende akademisk dansk
            2. Anvend præcis musikologisk terminologi
            3. Undgå anglicismer og uformelle udtryk
            4. Overhold dansk grammatik og retskrivning
            5. Brug naturlige sætningskonstruktioner
            6. Sørg for en flydende læsbarhed
            7. Følg danske tegnsætningsregler
            8. Anvend passende idiomatiske udtryk
            9. Tag hensyn til det danske sprogflow
            10. Tilpas stilen til dansk sprogbrug
            
            STRUKTUR AF AFSNIT OG LÆSBARHED:
            1. Begynd et nyt afsnit ved hvert emneskift eller ny idé
            2. Hold afsnit på 3-5 sætninger for optimal læsbarhed
            3. Brug kortere afsnit til vigtige udsagn eller overgange
            4. Skab visuelle pauser i teksten gennem gennemtænkt afsnitsstruktur
            5. Sørg for, at hvert afsnit indeholder ét klart hovedpunkt
            6. Undgå lange, udelte tekstblokke
            7. Brug afsnit til at strukturere indhold og udvikle argumenter
            
            OVERGANGE MELLEM AFSNIT OG TEKSTSTRØM:
            1. Skab sømløse overgange mellem alle afsnit
            2. Brug overgangsord og -sætninger (f.eks. "Desuden", "Yderligere", "I modsætning til")
            3. Etabler indholdsmæssige forbindelser mellem på hinanden følgende afsnit
            4. Bevar tematisk kontinuitet gennem hele teksten
            5. Henvis til tidligere afsnit for at skabe sammenhæng
            6. Undgå pludselige emneskift uden passende overgange
            7. Udvikl argumenter og ideer flydende over flere afsnit
            8. Byg en logisk progression, der guider læseren gennem teksten
            
            INDHOLDSKRAV:
            1. Teksten SKAL være mindst {char_min} tegn
            2. Fokuser udelukkende på international musik
            3. Strukturer indholdet med klare, logiske afsnit
            4. Brug komplekse men forståelige sætningsstrukturer
            5. Undgå punktopstillinger til fordel for flydende tekst
            6. Integrer relevante kulturhistoriske kontekster
            7. Brug præcis musikalsk terminologi
            8. Artikuler musikkteoretiske sammenhænge klart
            9. Implementer passende overgange mellem afsnit
            10. Bevar en konsistent akademisk tone
            
            KRITISK: Antallet af tegn SKAL være mindst {char_min}.
            """,
        },
        "sv": {
            "style": "Tydlig och enkel svenska",
            "characteristics": "precis musikologisk terminologi, vetenskaplig ton, komplexa meningsstrukturer",
            "prompt": """
            Skapa innehåll för sektionen '{section_name}' i musikkategorin '{category}'.
            
            SPRÅKLIGA KRAV:
            1. Använd uteslutande akademisk svenska
            2. Använd precis musikologisk terminologi
            3. Undvik anglicismer och informella uttryck
            4. Följ svensk grammatik och rättstavning
            5. Använd naturliga meningskonstruktioner
            6. Säkerställ ett flytande läsflöde
            7. Följ svenska interpunktionsregler
            8. Använd lämpliga idiomatiska uttryck
            9. Beakta det svenska språkrytmen
            10. Anpassa stilen till svensk språkkontext
            
            STRUKTUR AV STYCKEN OCH LÄSBARHET:
            1. Börja ett nytt stycke vid varje ämnesbyte eller ny idé
            2. Håll stycken på 3-5 meningar för optimal läsbarhet
            3. Använd kortare stycken för viktiga uttalanden eller övergångar
            4. Skapa visuella pauser i texten genom genomtänkt styckesstruktur
            5. Se till att varje stycke innehåller en tydlig huvudpunkt
            6. Undvik långa, odelade textblock
            7. Använd stycken för att strukturera innehåll och utveckla argument
            
            ÖVERGÅNGAR MELLAN STYCKEN OCH TEXTFLÖDE:
            1. Skapa sömlösa övergångar mellan alla stycken
            2. Använd övergångsord och -fraser (t.ex. "Dessutom", "Vidare", "I kontrast")
            3. Etablera innehållsförbindelser mellan på varandra följande stycken
            4. Bevara tematisk kontinuitet genom hela texten
            5. Hänvisa till tidigare stycken för att bygga sammanhang
            6. Undvik plötsliga ämnesbyten utan lämpliga övergångar
            7. Utveckla argument och idéer flytande över flera stycken
            8. Bygg en logisk progression som vägleder läsaren genom texten
            
            INNEHÅLLSKRAV:
            1. Texten MÅSTE vara minst {char_min} tecken
            2. Fokusera uteslutande på internationell musik
            3. Strukturera innehållet med tydliga, logiska stycken
            4. Använd komplexa men förståeliga meningsstrukturer
            5. Undvik punktlistor till förmån för flytande text
            6. Integrera relevanta kulturhistoriska sammanhang
            7. Använd precis musikalisk terminologi
            8. Artikuler musikteoretiska samband tydligt
            9. Implementera lämpliga övergångar mellan stycken
            10. Behåll en konsekvent vetenskaplig ton
            
            KRITISKT: Antalet tecken MÅSTE vara minst {char_min}.
            """,
        },
        "fi": {
            "style": "Selkeä ja yksinkertainen suomi",
            "characteristics": "tarkka musikologinen terminologia, tieteellinen sävy, monimutkaiset lauserakenteet",
            "prompt": """
            Luo sisältöä musiikkikategorian '{category}' osioon '{section_name}'.
            
            KIELELLISET VAATIMUKSET:
            1. Käytä yksinomaan akateemista suomea
            2. Käytä tarkkaa musikologista terminologiaa
            3. Vältä anglismeja ja puhekielisiä ilmaisuja
            4. Noudata suomen kielioppia ja oikeinkirjoitusta
            5. Käytä luonnollisia lauserakenteita
            6. Varmista sujuva luettavuus
            7. Seuraa suomen välimerkkisääntöjä
            8. Käytä sopivia idiomeja
            9. Huomioi suomen kielen rytmi
            10. Mukauta tyyli suomalaiseen kielikontekstiin
            
            KAPPALEIDEN RAKENNE JA LUETTAVUUS:
            1. Aloita uusi kappale jokaisella aiheenvaihdolla tai uudella idealla
            2. Pidä kappaleet 3-5 lauseen pituisina optimaalisen luettavuuden takaamiseksi
            3. Käytä lyhyempiä kappaleita tärkeisiin lausuntoihin tai siirtymiin
            4. Luo visuaalisia taukoja tekstiin harkitun kappalerakenteen avulla
            5. Varmista, että jokainen kappale sisältää yhden selkeän pääkohdan
            6. Vältä pitkiä, jakamattomia tekstilohkoja
            7. Käytä kappaleita sisällön jäsentämiseen ja argumenttien kehittämiseen
            
            KAPPALEIDEN VÄLISET SIIRTYMÄT JA TEKSTIN VIRTAUS:
            1. Luo saumattomia siirtymiä kaikkien kappaleiden välillä
            2. Käytä siirtymäsanoja ja -lauseita (esim. "Lisäksi", "Edelleen", "Vastakohtana")
            3. Luo sisältöyhteyksiä peräkkäisten kappaleiden välille
            4. Säilytä temaattinen jatkuvuus koko tekstin ajan
            5. Viittaa aiempiin kappaleisiin rakentaaksesi johdonmukaisuutta
            6. Vältä äkillisiä aiheenvaihtoja ilman sopivia siirtymiä
            7. Kehitä argumentteja ja ideoita sujuvasti useiden kappaleiden ajan
            8. Rakenna looginen eteneminen, joka ohjaa lukijaa tekstin läpi
            
            SISÄLTÖVAATIMUKSET:
            1. Tekstin pituuden TÄYTYY olla vähintään {char_min} merkkiä
            2. Keskity yksinomaan kansainväliseen musiikkiin
            3. Jäsennä sisältö selkeillä, loogisilla kappaleilla
            4. Käytä monimutkaisia mutta ymmärrettäviä lauserakenteita
            5. Vältä luetteloita suosien sujuvaa proosaa
            6. Integroi relevantit kulttuurihistorialliset kontekstit
            7. Käytä tarkkaa musiikillista terminologiaa
            8. Artikuloi musiikkiteoreettiset suhteet selkeästi
            9. Toteuta asianmukaiset kappaleiden väliset siirtymät
            10. Ylläpidä johdonmukaista tieteellistä sävyä
            
            KRIITTINEN: Merkkimäärän TÄYTYY olla vähintään {char_min}.
            """,
        },
    }

    return prompts.get(language, prompts["en"])


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
    return {"style": prompts["style"], "characteristics": prompts["characteristics"]}


def get_language_quality_criteria(language: str) -> str:
    """Get language-specific quality criteria for content generation.

    Provides standardized quality guidelines for each supported language
    to ensure consistent, high-quality content across all articles.

    Args:
        language: ISO 639-1 language code

    Returns:
        str: Language-specific quality criteria
    """
    criteria = {
        "en": """
        QUALITY REQUIREMENTS:
        - Use contemporary language and consistent terminology throughout
        - Avoid repetition of words, phrases, and ideas
        - Create smooth transitions between sections and paragraphs
        - Vary sentence structure for engaging reading experience
        - Ensure impeccable spelling and grammar
        - Create fluid reading experience with natural cadence
        - Use appropriate paragraph breaks to enhance readability (typically every 3-5 sentences)
        - Start a new paragraph when introducing a new idea, concept, or perspective
        - Use shorter paragraphs for emphasizing key points or dramatic effect
        - Include sufficient white space to improve visual comfort and reduce cognitive load
        - Break up long explanations with logical paragraph divisions
        - Connect paragraphs with smooth transitions that maintain narrative flow
        - Use connective phrases between paragraphs (e.g., "Furthermore," "In addition," "However," "As a result")
        - Ensure each paragraph follows logically from the previous one
        - Maintain thematic continuity across paragraph boundaries
        - Create a sense of progression between paragraphs to guide the reader forward
        - Express information in flowing prose rather than bullet points or lists
        """,
        "de": """
        QUALITÄTSANFORDERUNGEN:
        - Verwenden Sie zeitgemäße Sprachbilder und konsistente Terminologie
        - Vermeiden Sie Wiederholungen von Wörtern, Phrasen und Ideen
        - Schaffen Sie flüssige Übergänge zwischen Abschnitten und Absätzen
        - Variieren Sie den Satzbau für ein ansprechendes Leseerlebnis
        - Gewährleisten Sie fehlerfreie Rechtschreibung und Grammatik
        - Erzeugen Sie ein flüssiges Leseerlebnis mit natürlichem Sprachrhythmus
        - Verwenden Sie angemessene Absatzumbrüche zur Verbesserung der Lesbarkeit (üblicherweise alle 3-5 Sätze)
        - Beginnen Sie einen neuen Absatz, wenn Sie eine neue Idee, ein neues Konzept oder eine neue Perspektive einführen
        - Nutzen Sie kürzere Absätze, um wichtige Punkte zu betonen oder dramatische Effekte zu erzielen
        - Sorgen Sie für ausreichend Weißraum, um den visuellen Komfort zu verbessern und die kognitive Belastung zu reduzieren
        - Unterteilen Sie lange Erklärungen mit logischen Absatztrennungen
        - Verbinden Sie Absätze mit fließenden Übergängen, die den narrativen Fluss aufrechterhalten
        - Verwenden Sie Überleitungsphrasen zwischen Absätzen (z.B. "Darüber hinaus", "Zusätzlich", "Allerdings", "Infolgedessen")
        - Stellen Sie sicher, dass jeder Absatz logisch aus dem vorherigen folgt
        - Bewahren Sie thematische Kontinuität über Absatzgrenzen hinweg
        - Erzeugen Sie ein Gefühl der Progression zwischen Absätzen, um den Leser vorwärts zu führen
        - Präsentieren Sie Informationen in fließendem Text statt in Aufzählungen oder Listen
        """,
        "es": """
        REQUISITOS DE CALIDAD:
        - Utilice lenguaje contemporáneo y terminología consistente
        - Evite la repetición de palabras, frases e ideas
        - Cree transiciones fluidas entre secciones y párrafos
        - Varíe la estructura de las frases para una experiencia de lectura atractiva
        - Asegure una ortografía y gramática impecables
        - Cree una experiencia de lectura fluida con cadencia natural
        - Utilice saltos de párrafo apropiados para mejorar la legibilidad (generalmente cada 3-5 oraciones)
        - Inicie un nuevo párrafo al introducir una nueva idea, concepto o perspectiva
        - Use párrafos más cortos para enfatizar puntos clave o efectos dramáticos
        - Incluya suficiente espacio en blanco para mejorar la comodidad visual y reducir la carga cognitiva
        - Divida las explicaciones largas con divisiones lógicas de párrafos
        - Mantenga la continuidad de los párrafos sin interrupciones innecesarias
        - Exprese la información en prosa fluida en lugar de puntos o listas
        """,
        "fr": """
        EXIGENCES DE QUALITÉ:
        - Utilisez un langage contemporain et une terminologie cohérente
        - Évitez la répétition de mots, de phrases et d'idées
        - Créez des transitions fluides entre les sections et les paragraphes
        - Variez la structure des phrases pour une expérience de lecture engageante
        - Assurez une orthographe et une grammaire impeccables
        - Créez une expérience de lecture fluide avec une cadence naturelle
        - Utilisez des sauts de paragraphe appropriés pour améliorer la lisibilité (généralement toutes les 3 à 5 phrases)
        - Commencez un nouveau paragraphe lorsque vous introduisez une nouvelle idée, un nouveau concept ou une nouvelle perspective
        - Utilisez des paragraphes plus courts pour mettre l'accent sur des points clés ou des effets dramatiques
        - Incluez suffisamment d'espace blanc pour améliorer le confort visuel et réduire la charge cognitive
        - Divisez les longues explications avec des divisions logiques de paragraphes
        - Maintenez la continuité des paragraphes sans interruptions inutiles
        - Exprimez l'information en prose fluide plutôt qu'en points ou en listes
        """,
        "it": """
        REQUISITI DI QUALITÀ:
        - Utilizzare un linguaggio contemporaneo e una terminologia coerente
        - Evitare la ripetizione di parole, frasi e idee
        - Creare transizioni fluide tra sezioni e paragrafi
        - Variare la struttura delle frasi per un'esperienza di lettura coinvolgente
        - Garantire un'ortografia e una grammatica impeccabili
        - Creare un'esperienza di lettura fluida con una cadenza naturale
        - Utilizzare interruzioni di paragrafo appropriate per migliorare la leggibilità (generalmente ogni 3-5 frasi)
        - Iniziare un nuovo paragrafo quando si introduce una nuova idea, concetto o prospettiva
        - Usare paragrafi più brevi per enfatizzare punti chiave o effetti drammatici
        - Includere sufficiente spazio bianco per migliorare il comfort visivo e ridurre il carico cognitivo
        - Dividere le spiegazioni lunghe con divisioni logiche dei paragrafi
        - Mantenere la continuità dei paragrafi senza interruzioni non necessarie
        - Esprimere le informazioni in prosa scorrevole anziché in punti o elenchi
        """,
        "pt": """
        REQUISITOS DE QUALIDADE:
        - Use linguagem contemporânea e terminologia consistente
        - Evite a repetição de palavras, frases e ideias
        - Crie transições suaves entre seções e parágrafos
        - Varie a estrutura das frases para uma experiência de leitura envolvente
        - Garanta ortografia e gramática impecáveis
        - Crie uma experiência de leitura fluida com cadência natural
        - Use quebras de parágrafo apropriadas para melhorar a legibilidade (geralmente a cada 3-5 frases)
        - Inicie um novo parágrafo ao introduzir uma nova ideia, conceito ou perspectiva
        - Use parágrafos mais curtos para enfatizar pontos-chave ou efeitos dramáticos
        - Inclua espaço em branco suficiente para melhorar o conforto visual e reduzir a carga cognitiva
        - Divida explicações longas com divisões lógicas de parágrafos
        - Mantenha a continuidade do parágrafo sem quebras desnecessárias
        - Expresse informações em prosa fluente em vez de pontos ou listas
        """,
        "nl": """
        KWALITEITSEISEN:
        - Gebruik hedendaags taalgebruik en consistente terminologie
        - Vermijd herhaling van woorden, zinnen en ideeën
        - Creëer vloeiende overgangen tussen secties en alinea's
        - Varieer de zinsstructuur voor een boeiende leeservaring
        - Zorg voor foutloze spelling en grammatica
        - Creëer een vloeiende leeservaring met een natuurlijk ritme
        - Gebruik gepaste alineaonderbrekingen om de leesbaarheid te verbeteren (doorgaans elke 3-5 zinnen)
        - Begin een nieuwe alinea wanneer u een nieuw idee, concept of perspectief introduceert
        - Gebruik kortere alinea's om belangrijke punten te benadrukken of dramatische effecten te creëren
        - Zorg voor voldoende witruimte om het visuele comfort te verbeteren en de cognitieve belasting te verminderen
        - Verdeel lange verklaringen met logische alinea-indelingen
        - Handhaaf de continuïteit van alinea's zonder onnodige onderbrekingen
        - Presenteer informatie in vloeiend proza in plaats van opsommingen of lijsten
        """,
        "da": """
        KVALITETSKRAV:
        - Brug tidssvarende sprog og konsistent terminologi
        - Undgå gentagelse af ord, sætninger og idéer
        - Skab flydende overgange mellem afsnit
        - Varier sætningsstrukturen for en engagerende læseoplevelse
        - Sikre fejlfri stavning og grammatik
        - Skab en flydende læseoplevelse med naturlig rytme
        - Brug passende afsnitsskift til at forbedre læsbarheden (typisk hver 3-5 sætninger)
        - Start et nyt afsnit, når du introducerer en ny idé, et nyt koncept eller perspektiv
        - Brug kortere afsnit til at fremhæve vigtige pointer eller dramatiske effekter
        - Inkluder tilstrækkelig med hvidt rum for at forbedre den visuelle komfort og reducere den kognitive belastning
        - Del lange forklaringer med logiske afsnitsinddeling
        - Oprethold kontinuiteten i afsnit uden unødvendige afbrydelser
        - Udtrykk information i flydende prosa i stedet for punkter eller lister
        """,
        "sv": """
        KVALITETSKRAV:
        - Använd modernt språkbruk och konsekvent terminologi
        - Undvik upprepning av ord, fraser och idéer
        - Skapa smidiga övergångar mellan avsnitt
        - Variera meningsstrukturen för en engagerande läsupplevelse
        - Säkerställ felfri stavning och grammatik
        - Skapa en flytande läsupplevelse med naturlig rytm
        - Använd lämpliga styckebrytningar för att förbättra läsbarheten (vanligtvis var 3-5 meningar)
        - Börja ett nytt stycke när du introducerar en ny idé, ett nytt koncept eller perspektiv
        - Använd kortare stycken för att betona viktiga punkter eller dramatiska effekter
        - Inkludera tillräckligt med vitt utrymme för att förbättra visuell komfort och minska kognitiv belastning
        - Dela upp långa förklaringar med logiska styckesindelningar
        - Upprätthåll styckets kontinuitet utan onödiga avbrott
        - Uttryck information i flytande prosa snarare än punkter eller listor
        """,
        "fi": """
        LAATUVAATIMUKSET:
        - Käytä ajanmukaista kieltä ja johdonmukaista terminologiaa
        - Vältä sanojen, lauseiden ja ajatusten toistoa
        - Luo sujuvat siirtymät osioiden ja kappaleiden välillä
        - Vaihtele lauserakennetta miellyttävän lukukokemuksen luomiseksi
        - Varmista virheetön oikeinkirjoitus ja kielioppi
        - Luo sujuva lukukokemus luonnollisella rytmillä
        - Käytä asianmukaisia kappalejakoja luettavuuden parantamiseksi (yleensä 3-5 lauseen välein)
        - Aloita uusi kappale, kun esittelet uuden idean, käsitteen tai näkökulman
        - Käytä lyhyempiä kappaleita tärkeiden kohtien korostamiseen tai dramaattisen vaikutuksen luomiseen
        - Sisällytä riittävästi tyhjää tilaa visuaalisen mukavuuden parantamiseksi ja kognitiivisen kuormituksen vähentämiseksi
        - Jaa pitkät selitykset loogisiin kappaleisiin
        - Ylläpidä kappaleiden jatkuvuutta ilman tarpeettomia katkoksia
        - Esitä tiedot sujuvana tekstinä luetteloiden sijaan
        """,
    }

    # Erweitern Sie alle Sprachkriterien mit spezifischen Absatzübergangsanweisungen
    for lang in ["es", "fr", "it", "pt", "nl", "da", "sv", "fi"]:
        if lang in criteria:
            # Füge spezifische Absatzübergangsrichtlinien für jede Sprache hinzu
            if lang == "es":
                criteria[
                    lang
                ] += """
        - Conecte los párrafos con transiciones fluidas que mantengan el flujo narrativo
        - Utilice frases conectivas entre párrafos (p.ej., "Además", "Por otra parte", "Sin embargo", "Como resultado")
        - Asegúrese de que cada párrafo siga lógicamente del anterior
        - Mantenga la continuidad temática a través de los límites entre párrafos
        - Cree una sensación de progresión entre párrafos para guiar al lector hacia adelante
        """
            elif lang == "fr":
                criteria[
                    lang
                ] += """
        - Connectez les paragraphes avec des transitions fluides qui maintiennent le flux narratif
        - Utilisez des phrases de liaison entre les paragraphes (p.ex., "En outre", "Par ailleurs", "Cependant", "Par conséquent")
        - Assurez-vous que chaque paragraphe découle logiquement du précédent
        - Maintenez une continuité thématique au-delà des limites des paragraphes
        - Créez un sentiment de progression entre les paragraphes pour guider le lecteur vers l'avant
        """
            elif lang == "it":
                criteria[
                    lang
                ] += """
        - Collega i paragrafi con transizioni fluide che mantengono il flusso narrativo
        - Utilizza frasi di collegamento tra i paragrafi (es. "Inoltre", "D'altra parte", "Tuttavia", "Di conseguenza")
        - Assicurati che ogni paragrafo segua logicamente dal precedente
        - Mantieni la continuità tematica attraverso i confini dei paragrafi
        - Crea un senso di progressione tra i paragrafi per guidare il lettore in avanti
        """
            elif lang == "pt":
                criteria[
                    lang
                ] += """
        - Conecte os parágrafos com transições fluidas que mantenham o fluxo narrativo
        - Use frases conectivas entre parágrafos (por exemplo, "Além disso", "Por outro lado", "No entanto", "Como resultado")
        - Certifique-se de que cada parágrafo siga logicamente do anterior
        - Mantenha a continuidade temática através dos limites dos parágrafos
        - Crie uma sensação de progressão entre parágrafos para guiar o leitor adiante
        """
            elif lang == "nl":
                criteria[
                    lang
                ] += """
        - Verbind alinea's met vloeiende overgangen die de verhalende stroom behouden
        - Gebruik verbindende zinnen tussen alinea's (bijv. "Bovendien", "Daarentegen", "Echter", "Als gevolg hiervan")
        - Zorg ervoor dat elke alinea logisch volgt uit de vorige
        - Behoud thematische continuïteit over alineagrenzen heen
        - Creëer een gevoel van progressie tussen alinea's om de lezer voorwaarts te leiden
        """
            elif lang == "da":
                criteria[
                    lang
                ] += """
        - Forbind afsnit med flydende overgange, der opretholder den fortællende strøm
        - Brug forbindende sætninger mellem afsnit (f.eks. "Desuden", "På den anden side", "Dog", "Som et resultat")
        - Sørg for, at hvert afsnit følger logisk fra det forrige
        - Oprethold tematisk kontinuitet på tværs af afsnitsgrænser
        - Skab en fornemmelse af progression mellem afsnit for at lede læseren fremad
        """
            elif lang == "sv":
                criteria[
                    lang
                ] += """
        - Koppla samman stycken med flytande övergångar som upprätthåller berättelsens flöde
        - Använd sammanbindande fraser mellan stycken (t.ex. "Dessutom", "Å andra sidan", "Emellertid", "Som ett resultat")
        - Se till att varje stycke följer logiskt från det föregående
        - Upprätthåll tematisk kontinuitet över styckegränser
        - Skapa en känsla av progression mellan stycken för att guida läsaren framåt
        """
            elif lang == "fi":
                criteria[
                    lang
                ] += """
        - Yhdistä kappaleet sujuvilla siirtymillä, jotka ylläpitävät kerronnan virtausta
        - Käytä yhdistäviä lauseita kappaleiden välillä (esim. "Lisäksi", "Toisaalta", "Kuitenkin", "Tämän seurauksena")
        - Varmista, että jokainen kappale seuraa loogisesti edellistä
        - Ylläpidä temaattista jatkuvuutta kappalerajan yli
        - Luo etenemisen tunne kappaleiden välillä ohjataksesi lukijaa eteenpäin
        """

    return criteria.get(language, criteria["en"])


def generate_complete_content(category: str, language: str) -> str:
    """Generate complete content for a music category in a specific language.

    Generates all sections of content in a single API call, ensuring that each
    section meets minimum length requirements and follows quality guidelines.

    Args:
        category: Music category name
        language: ISO 639-1 language code

    Returns:
        str: Complete formatted content for the category
    """
    logging.info(
        f"Starting complete content generation for category '{category}' in language '{language}'"
    )

    # Check if language is supported
    if language not in get_available_languages():
        logging.error(f"Language '{language}' is not supported")
        raise ValueError(f"Language '{language}' is not supported")

    # Get section limits and translations
    logging.info("Getting section limits and translations")
    section_limits = get_section_limits(category, language)
    translations = get_translated_sections(language)
    logging.info(f"Found {len(section_limits)} sections to generate")

    # Prepare section requirements
    section_requirements = []
    total_min_chars = 0

    for section_name, char_min in section_limits.items():
        translated_title = translations.get(section_name, section_name)
        section_requirements.append(
            {
                "title": translated_title,
                "original_title": section_name,
                "min_chars": char_min,
            }
        )
        total_min_chars += char_min

    # Prepare API request
    style_guide = get_language_style_guide(language)
    quality_criteria = get_language_quality_criteria(language)
    category_type = get_category_type(category)
    is_decade_category = is_decade(category)

    # Prepare section specifications
    section_specs = "\n\n".join(
        [
            f"Section: {section['title']}\nMinimum characters: {section['min_chars']}"
            for section in section_requirements
        ]
    )

    # Base historical accuracy guidelines
    historical_accuracy = """
    Important historical guidelines:
    - Ensure strict historical accuracy for the specific time period, genre, or region being discussed
    - Only mention artists, bands, and cultural phenomena that were active/present during the relevant time period
    - Pay careful attention to when specific music styles, technologies, and cultural movements emerged
    - Be precise with dates and chronological order of events
    - Consider the geographical and cultural context of musical developments
    - Verify the accuracy of technological developments and their impact on music
    - When discussing influences, ensure they are chronologically possible and historically accurate
    """

    # Add category-specific guidelines
    if is_decade_category:
        decade = category[:-1]
        historical_accuracy += f"""
        Decade-specific guidelines for the {decade}s:
        - Focus EXCLUSIVELY on artists, bands, and trends that were active/prominent during the {decade}s
        - DO NOT mention any developments or artists that emerged after the {decade}s
        - DO NOT discuss musical styles or technologies that weren't available in the {decade}s
        - When mentioning influences, only reference artists/styles from the {decade}s or earlier
        - Ensure all cultural and social references are specific to the {decade}s
        - For technological developments, only mention what was actually available in the {decade}s
        - When discussing international influences, verify they were possible in the {decade}s
        - Keep all fashion and cultural references authentic to the {decade}s period
        """
    elif "Countries" in category_type:
        historical_accuracy += f"""
        Country-specific guidelines for {category}:
        - Focus primarily on artists who are actually from {category}
        - When discussing international influences, verify the historical connections
        - Respect the cultural authenticity of {category}'s musical traditions
        - Consider the specific regional variations within {category}
        - Discuss musical developments in chronological order
        - Only mention cultural exchanges that were historically possible
        - Verify the accuracy of local music scene developments
        """
    elif "Genres" in category_type:
        historical_accuracy += f"""
        Genre-specific guidelines for {category}:
        - Only mention artists who genuinely contributed to or performed in {category}
        - Trace the genre's development chronologically
        - Verify the authenticity of genre characteristics
        - Discuss subgenres in their historical context
        - When mentioning technical aspects, ensure they match the genre's era
        - Consider regional variations in how the genre developed
        - Only include cross-genre influences that were historically possible
        """
    elif "Instruments" in category_type:
        historical_accuracy += f"""
        Instrument-specific guidelines for {category}:
        - Follow the chronological development of the instrument
        - Only mention technological improvements when they were actually invented
        - Discuss playing techniques in their historical context
        - Verify the accuracy of manufacturing methods for each period
        - Consider regional variations in instrument construction and playing styles
        - Only mention performers from periods when the instrument existed
        - Ensure all technical specifications match historical records
        """

    # Language-specific system prompts with enhanced instructions
    language_system_prompts = {
        "en": "You are an expert music historian writing in English. Focus on accuracy, clarity, and engaging narrative.",
        "de": "Sie sind ein Musikhistoriker, der auf Deutsch schreibt. Legen Sie Wert auf Präzision, Klarheit und fesselnde Erzählweise.",
        "es": "Eres un historiador musical que escribe en español. Enfócate en la precisión, claridad y narrativa cautivadora.",
        "fr": "Vous êtes un historien de la musique écrivant en français. Concentrez-vous sur la précision, la clarté et un récit engageant.",
        "it": "Sei uno storico della musica che scrive in italiano. Concentrati su precisione, chiarezza e narrativa coinvolgente.",
        "pt": "Você é um historiador musical escrevendo em português. Foque em precisão, clareza e narrativa envolvente.",
        "da": "Du er en musikhistoriker, der skriver på dansk. Fokusér på nøjagtighed, klarhed og engagerende fortælling.",
        "fi": "Olet musiikkihistorioitsija, joka kirjoittaa suomeksi. Keskity tarkkuuteen, selkeyteen ja mukaansatempaavaan kerrontaan.",
        "nl": "U bent een muziekhistoricus die in het Nederlands schrijft. Focus op nauwkeurigheid, duidelijkheid en een boeiend verhaal.",
        "sv": "Du är en musikhistoriker som skriver på svenska. Fokusera på noggrannhet, tydlighet och engagerande berättande.",
    }

    # Get language-specific system prompt, default to English if not found
    system_prompt = language_system_prompts.get(language, language_system_prompts["en"])

    # Language-specific user prompt
    language_name = {
        "en": "English",
        "de": "German (Deutsch)",
        "es": "Spanish (Español)",
        "fr": "French (Français)",
        "it": "Italian (Italiano)",
        "pt": "Portuguese (Português)",
        "da": "Danish (Dansk)",
        "fi": "Finnish (Suomi)",
        "nl": "Dutch (Nederlands)",
        "sv": "Swedish (Svenska)",
    }.get(language, "English")

    # Add explicit language instruction to system prompt
    enhanced_system_prompt = f"{system_prompt}\n\nIMPORTANT: You MUST write ONLY in {language_name}. Do not include any content in other languages. The entire response must be in {language_name} only."

    # Craft user prompt for complete content generation
    user_prompt = f"""
    Create complete content for a music article about the category '{category}' in {language_name}.
    
    CONTENT STRUCTURE:
    {section_specs}
    
    OVERALL REQUIREMENTS:
    1. Write a complete article with all sections
    2. Each section must meet or exceed its minimum character count
    3. Start each section with the exact section title as specified
    4. Maintain a cohesive narrative throughout the entire article
    5. Ensure strong connections between all sections
    6. Total article length should be at least {total_min_chars} characters
    
    PARAGRAPH STRUCTURE AND READABILITY:
    1. Use appropriate paragraph breaks to enhance readability (typically every 3-5 sentences)
    2. Start a new paragraph when introducing a new idea, concept, or perspective
    3. Use shorter paragraphs for emphasizing key points or dramatic effect
    4. Include sufficient white space to improve visual comfort and reduce cognitive load
    5. Break up long explanations with logical paragraph divisions
    6. Ensure each paragraph focuses on a single main point or idea
    7. Avoid excessively long paragraphs that create "walls of text"
    8. Use logical paragraph flow to guide the reader through your narrative
    
    PARAGRAPH TRANSITIONS AND CONTENT FLOW:
    1. Create seamless transitions between all paragraphs
    2. Use transitional words and phrases to connect ideas between paragraphs
    3. Ensure each paragraph flows naturally from the previous one
    4. Maintain thematic continuity across paragraph boundaries
    5. Build logical connections between consecutive paragraphs
    6. Use reference words to connect back to previous content
    7. Create a sense of progression that carries the reader forward
    8. Avoid jarring shifts in topic, tone, or perspective
    9. Develop ideas progressively across multiple paragraphs when needed
    10. Use a variety of transition techniques to keep the text engaging
    
    STYLE REQUIREMENTS:
    {style_guide['style']}
    {style_guide['characteristics']}
    
    {quality_criteria}
    
    HISTORICAL ACCURACY:
    {historical_accuracy}
    
    RESPONSE FORMAT:
    - Start each section with '## [Section Title]'
    - Don't include any additional formatting or numbering
    - Don't add any introduction or conclusion beyond the specified sections
    """

    # Prepare API request
    messages = [
        {
            "role": "system",
            "content": enhanced_system_prompt,
        },
        {"role": "user", "content": user_prompt},
    ]

    # Call API with exponential backoff for retries
    attempt = 0
    max_attempts = 5

    while attempt < max_attempts:
        attempt += 1

        try:
            if attempt > 1:
                wait_time = min(2 ** (attempt - 1), 30)
                print(f"Attempt {attempt}: Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

            # Log API call
            logging.info(
                f"Calling OpenAI API with model {OPENAI_MODEL} for complete content generation"
            )

            # Make the API call
            start_time = time.time()
            response = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
            )
            elapsed_time = time.time() - start_time

            logging.info(f"OpenAI API response received: time={elapsed_time:.2f}s")

            # Extract content
            content = response.choices[0].message.content.strip()

            # Validate language
            language_markers = {
                "fi": ["ä", "ö", "Ä", "Ö"],
                "sv": ["å", "ä", "ö", "Å", "Ä", "Ö"],
                "da": ["æ", "ø", "å", "Æ", "Ø", "Å"],
                "de": ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"],
                "es": ["ñ", "¿", "¡", "á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú"],
                "fr": [
                    "ç",
                    "à",
                    "â",
                    "ê",
                    "î",
                    "ô",
                    "û",
                    "ë",
                    "ï",
                    "ü",
                    "ÿ",
                    "é",
                    "è",
                    "ù",
                ],
                "it": ["à", "è", "é", "ì", "ò", "ù"],
                "nl": ["ij", "IJ", "é", "ë", "ï", "ö", "ü"],
                "pt": ["ã", "õ", "á", "à", "â", "é", "ê", "í", "ó", "ô", "ú", "ç"],
            }

            # Typische Wörter in jeder Sprache zum zusätzlichen Check
            common_words = {
                "en": ["the", "and", "this", "was", "with"],
                "de": ["der", "die", "das", "und", "ist", "von", "mit"],
                "es": ["el", "la", "los", "las", "es", "por", "que"],
                "fr": ["le", "la", "les", "et", "est", "pour", "avec"],
                "it": ["il", "lo", "la", "e", "è", "per", "con"],
                "pt": ["o", "a", "os", "as", "e", "para", "com"],
                "da": ["det", "den", "er", "og", "at", "på", "med"],
                "fi": ["on", "ja", "se", "että", "ovat", "kuin"],
                "nl": ["de", "het", "een", "is", "en", "van", "voor"],
                "sv": ["är", "och", "att", "det", "som", "med", "för"],
            }

            # Check language markers and common words
            markers = language_markers.get(language, [])
            words = common_words.get(language, [])
            content_lower = content.lower()

            has_markers = not markers or any(marker in content for marker in markers)
            has_words = not words or any(
                f" {word} " in f" {content_lower} " for word in words
            )

            if not has_markers or not has_words:
                logging.warning(f"Warning: Content may not be in {language_name}")
                if attempt < max_attempts:
                    # Add stronger language instructions
                    enhanced_system_prompt += f"""
                    
                    WARNING: The previous response was NOT in {language_name}!
                    It is ABSOLUTELY CRUCIAL that you write ONLY in {language_name}.
                    
                    CRITICAL: ALL content MUST be in {language_name}.
                    """
                    messages[0]["content"] = enhanced_system_prompt
                    continue

            # Validate section lengths
            sections = []
            current_section = None
            current_content = []

            # Parse content into sections
            for line in content.split("\n"):
                if line.startswith("## "):
                    # Save previous section if exists
                    if current_section is not None:
                        sections.append(
                            {
                                "title": current_section,
                                "content": "\n".join(current_content),
                            }
                        )
                        current_content = []

                    # Start new section
                    current_section = line[3:].strip()
                elif current_section is not None:
                    current_content.append(line)

            # Add the last section
            if current_section is not None and current_content:
                sections.append(
                    {"title": current_section, "content": "\n".join(current_content)}
                )

            # Validate section lengths
            all_sections_valid = True
            missing_sections = []
            short_sections = []

            # Check that all required sections are present and meet minimum length
            for req in section_requirements:
                found = False
                for section in sections:
                    if section["title"] == req["title"]:
                        found = True
                        if len(section["content"]) < req["min_chars"]:
                            short_sections.append(
                                {
                                    "title": req["title"],
                                    "current": len(section["content"]),
                                    "required": req["min_chars"],
                                }
                            )
                            all_sections_valid = False
                        break

                if not found:
                    missing_sections.append(req["title"])
                    all_sections_valid = False

            if not all_sections_valid:
                if attempt < max_attempts:
                    # Enhance prompt with specific guidance on missing/short sections
                    additional_guidance = "\n\nPrevious attempt was not satisfactory:"

                    if missing_sections:
                        additional_guidance += (
                            f"\n- Missing sections: {', '.join(missing_sections)}"
                        )

                    if short_sections:
                        additional_guidance += "\n- Sections too short:"
                        for section in short_sections:
                            additional_guidance += f"\n  * {section['title']}: {section['current']}/{section['required']} characters"

                    messages[1]["content"] = user_prompt + additional_guidance
                    continue

            # If we get here, content is valid
            logging.info(
                f"Successfully generated complete content for {category} in {language}"
            )

            # Format complete content
            formatted_content = ""
            for section in sections:
                formatted_content += (
                    f"\n## {section['title']}\n\n{section['content']}\n"
                )

            return formatted_content

        except Exception as e:
            logging.error(f"API Error on attempt {attempt}: {str(e)}")
            if attempt >= max_attempts:
                raise RuntimeError(
                    f"Failed to generate content after {max_attempts} attempts: {str(e)}"
                )


def generate_section(
    category: str, language: str, section_name: str, char_min: int
) -> str:
    """Generate content for a specific section of a music category.

    Uses the OpenAI API to generate language-specific content that adheres
    to style guidelines and meets minimum length requirements.

    Args:
        category: Music category name
        language: ISO 639-1 language code
        section_name: Name of the section to generate
        char_min: Minimum character count for the content

    Returns:
        str: Generated content for the section

    Raises:
        Exception: For API errors or other issues
    """
    # Generate content in one go
    return generate_section_chunk(
        category=category,
        language=language,
        section_name=section_name,
        char_min=char_min,
        chunk_number=1,
        total_chunks=1,
    )


def generate_section_chunk(
    category: str,
    language: str,
    section_name: str,
    char_min: int,
    chunk_number: int,
    total_chunks: int,
) -> str:
    """Generate a chunk of content for a section.

    Helper function that handles the actual API calls and retries for
    generating a single chunk of content. Will keep retrying until valid
    content is received. Uses OpenAI for generation.
    """
    style_guide = get_language_style_guide(language)
    language_prompts = get_language_prompts(language)

    # Add category-specific guidelines
    category_type = get_category_type(category)

    # Base historical accuracy guidelines
    historical_accuracy = """
    Important historical guidelines:
    - Ensure strict historical accuracy for the specific time period, genre, or region being discussed
    - Only mention artists, bands, and cultural phenomena that were active/present during the relevant time period
    - Pay careful attention to when specific music styles, technologies, and cultural movements emerged
    - Be precise with dates and chronological order of events
    - Consider the geographical and cultural context of musical developments
    - Verify the accuracy of technological developments and their impact on music
    - When discussing influences, ensure they are chronologically possible and historically accurate
    """

    # Add category-specific guidelines
    if category.endswith("s") and category[:-1].isdigit():  # Decades
        decade = category[:-1]
        historical_accuracy += f"""
        Decade-specific guidelines for the {decade}s:
        - Focus EXCLUSIVELY on artists, bands, and trends that were active/prominent during the {decade}s
        - DO NOT mention any developments or artists that emerged after the {decade}s
        - DO NOT discuss musical styles or technologies that weren't available in the {decade}s
        - When mentioning influences, only reference artists/styles from the {decade}s or earlier
        - Ensure all cultural and social references are specific to the {decade}s
        - For technological developments, only mention what was actually available in the {decade}s
        - When discussing international influences, verify they were possible in the {decade}s
        - Keep all fashion and cultural references authentic to the {decade}s period
        """
    elif "Countries" in category_type:
        historical_accuracy += f"""
        Country-specific guidelines for {category}:
        - Focus primarily on artists who are actually from {category}
        - When discussing international influences, verify the historical connections
        - Respect the cultural authenticity of {category}'s musical traditions
        - Consider the specific regional variations within {category}
        - Discuss musical developments in chronological order
        - Only mention cultural exchanges that were historically possible
        - Verify the accuracy of local music scene developments
        """
    elif "Genres" in category_type:
        historical_accuracy += f"""
        Genre-specific guidelines for {category}:
        - Only mention artists who genuinely contributed to or performed in {category}
        - Trace the genre's development chronologically
        - Verify the authenticity of genre characteristics
        - Discuss subgenres in their historical context
        - When mentioning technical aspects, ensure they match the genre's era
        - Consider regional variations in how the genre developed
        - Only include cross-genre influences that were historically possible
        """
    elif "Instruments" in category_type:
        historical_accuracy += f"""
        Instrument-specific guidelines for {category}:
        - Follow the chronological development of the instrument
        - Only mention technological improvements when they were actually invented
        - Discuss playing techniques in their historical context
        - Verify the accuracy of manufacturing methods for each period
        - Consider regional variations in instrument construction and playing styles
        - Only mention performers from periods when the instrument existed
        - Ensure all technical specifications match historical records
        """

    # Format the base prompt
    base_prompt = language_prompts["prompt"].format(
        section_name=section_name, category=category, char_min=char_min
    )

    # Add historical guidelines for all content
    base_prompt = historical_accuracy + "\n\n" + base_prompt

    # Add chunk-specific instructions if this is part of a multi-chunk section
    if total_chunks > 1:
        if chunk_number == 1:
            base_prompt += f"\n\nThis is part {chunk_number} of {total_chunks}. Start with a strong opening."
        elif chunk_number == total_chunks:
            base_prompt += f"\n\nThis is part {chunk_number} of {total_chunks}. Provide a good conclusion."
        else:
            base_prompt += f"\n\nThis is part {chunk_number} of {total_chunks}. Continue the narrative smoothly."

    # Try up to 5 times with different strategies
    attempt = 0
    # We'll track the best character count in case we need to return
    # a less-than-ideal result after max attempts
    best_char_count = 0

    while True:
        attempt += 1
        try:
            # Exponential backoff for retries, capped at 30 seconds
            if attempt > 1:
                wait_time = min(120 ** (attempt - 1), 30)
                print(f"Attempt {attempt}: Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

            # Language-specific system prompts with enhanced instructions
            language_system_prompts = {
                "en": "You are an expert music historian writing in English. Focus on accuracy, clarity, and engaging narrative.",
                "de": "Sie sind ein Musikhistoriker, der auf Deutsch schreibt. Legen Sie Wert auf Präzision, Klarheit und fesselnde Erzählweise.",
                "es": "Eres un historiador musical que escribe en español. Enfócate en la precisión, claridad y narrativa cautivadora.",
                "fr": "Vous êtes un historien de la musique écrivant en français. Concentrez-vous sur la précision, la clarté et un récit engageant.",
                "it": "Sei uno storico della musica che scrive in italiano. Concentrati su precisione, chiarezza e narrativa coinvolgente.",
                "pt": "Você é um historiador musical escrevendo em português. Foque em precisão, clareza e narrativa envolvente.",
                "da": "Du er en musikhistoriker, der skriver på dansk. Fokusér på nøjagtighed, klarhed og engagerende fortælling.",
                "fi": "Olet musiikkihistorioitsija, joka kirjoittaa suomeksi. Keskity tarkkuuteen, selkeyteen ja mukaansatempaavaan kerrontaan.",
                "nl": "U bent een muziekhistoricus die in het Nederlands schrijft. Focus op nauwkeurigheid, duidelijkheid en een boeiend verhaal.",
                "sv": "Du är en musikhistoriker som skriver på svenska. Fokusera på noggrannhet, tydlighet och engagerande berättande.",
            }

            # Get language-specific system prompt, default to English if not found
            system_prompt = language_system_prompts.get(
                language, language_system_prompts["en"]
            )

            # Get category type
            category_type = get_category_type(category)
            is_decade_category = is_decade(category)

            # Enhanced prompt with more specific guidance
            current_prompt = base_prompt

            # Add category-specific instructions
            if is_decade_category:
                current_prompt += f"\n\nThis is a DECADE category ({category}). Only include events, artists, and developments from this exact time period."
                current_prompt += f"\nDo not mention anything that happened before or after the {category}."
            else:
                current_prompt += (
                    f"\n\nThis is a {category_type} category ({category})."
                )

            if attempt > 0:
                current_prompt += (
                    "\n\nPrevious attempts were insufficient. Please ensure:"
                )
                current_prompt += "\n1. Comprehensive coverage of the topic"
                current_prompt += "\n2. Detailed examples and analysis"
                current_prompt += "\n3. Clear progression of ideas"
                current_prompt += f"\n4. Minimum length of {char_min} characters"

            # Add language-specific style guide
            current_prompt += f"\n\nStyle Guide:\n{style_guide['style']}\n{style_guide['characteristics']}"

            # Prepare messages for OpenAI with strong language instruction
            language_name = {
                "en": "English",
                "de": "German (Deutsch)",
                "es": "Spanish (Español)",
                "fr": "French (Français)",
                "it": "Italian (Italiano)",
                "pt": "Portuguese (Português)",
                "da": "Danish (Dansk)",
                "fi": "Finnish (Suomi)",
                "nl": "Dutch (Nederlands)",
                "sv": "Swedish (Svenska)",
            }.get(language, "English")

            # Add explicit language instruction to system prompt
            enhanced_system_prompt = f"{system_prompt}\n\nIMPORTANT: You MUST write ONLY in {language_name}. Do not include any content in other languages. The entire response must be in {language_name} only."

            messages = [
                {
                    "role": "system",
                    "content": f"{enhanced_system_prompt}\n{style_guide}",
                },
                {"role": "user", "content": current_prompt},
            ]

            try:
                # Log that we're making an API call
                logging.info(f"Calling OpenAI API with model {OPENAI_MODEL}")

                # Make the API call to OpenAI
                start_time = time.time()
                response = openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                )

                elapsed_time = time.time() - start_time

                # Log the response timing
                logging.info(f"OpenAI API response received: time={elapsed_time:.2f}s")

                # Extract content from response
                content = response.choices[0].message.content.strip()
                char_count = len(content)

                # Verifikation, dass der Inhalt in der richtigen Sprache ist
                # Sprachspezifische Marker definieren
                language_markers = {
                    "fi": ["ä", "ö", "Ä", "Ö"],
                    "sv": ["å", "ä", "ö", "Å", "Ä", "Ö"],
                    "da": ["æ", "ø", "å", "Æ", "Ø", "Å"],
                    "de": ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"],
                    "es": [
                        "ñ",
                        "¿",
                        "¡",
                        "á",
                        "é",
                        "í",
                        "ó",
                        "ú",
                        "Á",
                        "É",
                        "Í",
                        "Ó",
                        "Ú",
                    ],
                    "fr": [
                        "ç",
                        "à",
                        "â",
                        "ê",
                        "î",
                        "ô",
                        "û",
                        "ë",
                        "ï",
                        "ü",
                        "ÿ",
                        "é",
                        "è",
                        "ù",
                    ],
                    "it": ["à", "è", "é", "ì", "ò", "ù"],
                    "nl": ["ij", "IJ", "é", "ë", "ï", "ö", "ü"],
                    "pt": ["ã", "õ", "á", "à", "â", "é", "ê", "í", "ó", "ô", "ú", "ç"],
                }

                # Typische Wörter in jeder Sprache zum zusätzlichen Check
                common_words = {
                    "en": ["the", "and", "this", "was", "with"],
                    "de": ["der", "die", "das", "und", "ist", "von", "mit"],
                    "es": ["el", "la", "los", "las", "es", "por", "que"],
                    "fr": ["le", "la", "les", "et", "est", "pour", "avec"],
                    "it": ["il", "lo", "la", "e", "è", "per", "con"],
                    "pt": ["o", "a", "os", "as", "e", "para", "com"],
                    "da": ["det", "den", "er", "og", "at", "på", "med"],
                    "fi": ["on", "ja", "se", "että", "ovat", "kuin"],
                    "nl": ["de", "het", "een", "is", "en", "van", "voor"],
                    "sv": ["är", "och", "att", "det", "som", "med", "för"],
                }

                # Prüfen auf sprachspezifische Marker
                markers = language_markers.get(language, [])
                words = common_words.get(language, [])

                # Content in Kleinbuchstaben für Wort-Check
                content_lower = content.lower()

                # Überprüfen auf Marker und typische Wörter
                has_markers = not markers or any(
                    marker in content for marker in markers
                )
                has_words = not words or any(
                    f" {word} " in f" {content_lower} " for word in words
                )

                # Warnung, wenn der Text nicht in der richtigen Sprache zu sein scheint
                if not has_markers or not has_words:
                    logging.warning(
                        f"Warnung: Inhalt könnte nicht auf {language_name} sein!"
                    )
                    # Bei falscher Sprache neu versuchen, aber nur für die ersten Versuche
                    if attempt < 3 and not (has_markers and has_words):
                        print(
                            f"Versuch {attempt}: Inhalt scheint nicht auf {language_name} zu sein."
                        )
                        time.sleep(2)
                        continue  # Neuer Versuch mit stärkeren Sprachanweisungen
            except Exception as e:
                print(f"OpenAI API call failed: {str(e)}")
                time.sleep(5)  # Wait before retrying
                continue

            # Keep track of best attempt
            if char_count > best_char_count:
                # Store the best content in case we hit max attempts
                best_char_count = char_count
                # If we can't meet the minimum length after max attempts,
                # we'll return the best content we have

            # Return if content meets requirements
            if char_count >= char_min:
                print(
                    f"Success on attempt {attempt}: Generated {char_count} characters"
                )
                return content

            print(
                f"Attempt {attempt}: Content too short ({char_count}/{char_min} chars). Retrying..."
            )

            # Nach MAX_ATTEMPTS den besten Inhalt zurückgeben
            if attempt >= 5:
                if best_char_count > 0:
                    print(
                        f"Maximale Versuche erreicht, gebe besten Inhalt zurück ({best_char_count} Zeichen)"
                    )
                    # Sicherstellen, dass wir den besten Inhalt zurückgeben
                    return content if char_count == best_char_count else content
                else:
                    # Fallback für den Fall, dass wir gar keinen brauchbaren Inhalt haben
                    placeholder = (
                        f"[Inhalt für '{section_name}' konnte nicht generiert werden]"
                    )
                    return placeholder

        except Exception as e:
            print(f"Attempt {attempt} failed: {str(e)}")
            continue


def generate_content(category: str, language: str) -> str:
    """Generate or update content for a music category in a specific language.

    Now uses the complete content generation approach instead of section-by-section.

    Args:
        category: Music category name
        language: ISO 639-1 language code

    Returns:
        str: Status message indicating completion
    """
    logging.info(
        f"Starting content generation for category '{category}' in language '{language}'"
    )

    try:
        # Generate complete content in one API call
        content = generate_complete_content(category, language)

        # Save the complete content
        save_content(category, language, content, "a")
        logging.info(
            f"Successfully saved complete content for {category} in {language}"
        )

        return "Content generation completed"
    except Exception as e:
        logging.error(
            f"Failed to generate content for {category} in {language}: {str(e)}"
        )
        raise


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

    Uses the OpenAI API to generate language-specific, SEO-optimized title,
    description, and keywords for a music category page. Adapts content
    based on language-specific SEO best practices and cultural context.

    Args:
        category: Music category name
        language: ISO 639-1 language code

    Returns:
        Tuple[str, str, List[str]]: Title, description, and keywords
    """

    # Language-specific SEO guidelines
    seo_guidelines = {
        "en": {
            "title_length": 100,
            "desc_length": 250,
            "style": "Direct and action-oriented",
            "keyword_format": "Use natural phrases, include long-tail keywords",
            "min_keywords": 5,
        },
        "de": {
            "title_length": 100,  # German words tend to be longer
            "desc_length": 250,
            "style": "Precise and formal",
            "keyword_format": "Include compound words (Komposita) where appropriate",
            "min_keywords": 5,
        },
        "es": {
            "title_length": 100,  # Spanish needs slightly more space
            "desc_length": 250,
            "style": "Engaging and conversational",
            "keyword_format": "Include both singular and plural forms",
            "min_keywords": 5,
        },
        "fr": {
            "title_length": 100,
            "desc_length": 250,
            "style": "Elegant and refined",
            "keyword_format": "Consider gender variations in keywords",
            "min_keywords": 5,
        },
        "it": {
            "title_length": 100,
            "desc_length": 250,
            "style": "Expressive and dynamic",
            "keyword_format": "Include regional variations where relevant",
            "min_keywords": 5,
        },
        "pt": {
            "title_length": 100,
            "desc_length": 250,
            "style": "Engaging and natural",
            "keyword_format": "Include Brazilian and European Portuguese variations",
            "min_keywords": 5,
        },
    }

    # Get language-specific guidelines or use English defaults
    guidelines = seo_guidelines.get(language, seo_guidelines["en"])

    # No headers needed for OpenAI

    # Get category type for context
    category_type = get_category_type(category)

    # Get language-specific style guide
    style_guide = get_language_style_guide(language)

    # Get translations for the category name and type
    translations = get_translated_sections(language)
    translated_category = translations.get(category, category)
    translated_type = translations.get(category_type, category_type)

    prompt = f"""Generate SEO metadata for a music category page about {translated_category} in {language}.
    This is a {translated_type} category. The content must be in {language} and follow these guidelines:
    
    Language Style: {style_guide.get('style', 'Natural and engaging')} 
    Title Length: Maximum {guidelines['title_length']} characters
    Description Length: {guidelines['desc_length']} characters
    Writing Style: {guidelines['style']}
    Keyword Format: {guidelines['keyword_format']}
    
    Title requirements:
    - Make it emotionally engaging and powerful
    - Include relevant musical terms
    - Highlight unique aspects of {translated_category} 
    - Keep it natural and flowing
    - Add flair like "Ultimate Guide", "Definitive", or "Complete" where appropriate
    - IMPORTANT: Do not use colons (:) in the title as they break the YAML frontmatter
    - Use alternative punctuation like dashes (-) or vertical bars (|) instead of colons
    
    Description requirements:
    - Start with a hook or intriguing question
    - Use compelling language that resonates with music lovers
    - Include emotional triggers and value propositions
    - Add a clear call-to-action
    - Make it conversational yet authoritative
    - IMPORTANT: Do not use colons (:) in the title as they break the YAML frontmatter
    - Use alternative punctuation like dashes (-) or vertical bars (|) instead of colons
    
    Please provide:
    1. A captivating, emotion-rich title that drives interest (NO COLONS ALLOWED)
    2. An irresistible meta description that compels clicks and sparks curiosity
    3. A list of 5-7 relevant keywords/phrases specific to {language} speakers
    
    Format the response exactly like this:
    Title: [title]
    Description: [description]  
    Keywords: [keyword1, keyword2, keyword3, ...]
    """

    # Verbesserte Anweisungen für den Sprachberater
    # Sprachname für explizite Anweisungen
    language_name = {
        "en": "English",
        "de": "German (Deutsch)",
        "es": "Spanish (Español)",
        "fr": "French (Français)",
        "it": "Italian (Italiano)",
        "pt": "Portuguese (Português)",
        "da": "Danish (Dansk)",
        "fi": "Finnish (Suomi)",
        "nl": "Dutch (Nederlands)",
        "sv": "Swedish (Svenska)",
    }.get(language, "English")

    # Prepare messages for OpenAI API with explicit language instruction
    system_prompt = f"""You are an SEO expert specializing in {language_name} music content optimization.
    
    CRITICAL INSTRUCTION: You MUST write ONLY in {language_name}. The title, description, and all keywords MUST be in {language_name} only.
    DO NOT use English or any other language except {language_name}.
    """

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": prompt},
    ]

    attempt = 0
    while True:
        attempt += 1
        try:
            # Exponential backoff for retries, capped at 30 seconds
            if attempt > 1:
                wait_time = min(2 ** (attempt - 1), 30)
                print(f"Attempt {attempt}: Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

            try:
                # Make the API call to OpenAI
                start_time = time.time()
                response = openai_client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                )
                elapsed_time = time.time() - start_time
                logging.info(
                    f"OpenAI API response for SEO metadata: time={elapsed_time:.2f}s"
                )

                content = response.choices[0].message.content.strip()

                # Verifikation, dass der Inhalt in der richtigen Sprache ist
                # Sprachspezifische Marker definieren
                language_markers = {
                    "fi": ["ä", "ö", "Ä", "Ö"],
                    "sv": ["å", "ä", "ö", "Å", "Ä", "Ö"],
                    "da": ["æ", "ø", "å", "Æ", "Ø", "Å"],
                    "de": ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"],
                    "es": ["ñ", "¿", "¡", "á", "é", "í", "ó", "ú"],
                    "fr": [
                        "ç",
                        "à",
                        "â",
                        "ê",
                        "î",
                        "ô",
                        "û",
                        "ë",
                        "ï",
                        "ü",
                        "ÿ",
                        "é",
                        "è",
                    ],
                    "it": ["à", "è", "é", "ì", "ò", "ù"],
                    "nl": ["ij", "IJ", "é", "ë", "ï", "ö", "ü"],
                    "pt": ["ã", "õ", "á", "à", "â", "é", "ê", "í", "ó", "ô", "ú", "ç"],
                }

                # Typische Wörter in jeder Sprache zum zusätzlichen Check
                common_words = {
                    "en": ["the", "and", "this", "was", "with"],
                    "de": ["der", "die", "das", "und", "ist"],
                    "es": ["el", "la", "los", "las", "es"],
                    "fr": ["le", "la", "les", "et", "est"],
                    "it": ["il", "lo", "la", "e", "è"],
                    "pt": ["o", "a", "os", "as", "e"],
                    "da": ["det", "den", "er", "og", "at"],
                    "fi": ["on", "ja", "se", "että", "ovat"],
                    "nl": ["de", "het", "een", "is", "en", "van", "voor"],
                    "sv": ["är", "och", "att", "det", "som"],
                }

                # Prüfen auf sprachspezifische Marker
                markers = language_markers.get(language, [])
                words = common_words.get(language, [])

                # Content in Kleinbuchstaben für Wort-Check
                content_lower = content.lower()

                # Überprüfen auf Marker und typische Wörter
                has_markers = not markers or any(
                    marker in content for marker in markers
                )
                has_words = not words or any(
                    f" {word} " in f" {content_lower} " for word in words
                )

                # Warnung, wenn der Text nicht in der richtigen Sprache zu sein scheint
                if not has_markers or not has_words:
                    logging.warning(
                        f"Warnung: Frontmatter könnte nicht auf {language_name} sein!"
                    )
                    # Bei falscher Sprache neu versuchen, aber nur für die ersten Versuche
                    if attempt < 3 and not (has_markers and has_words):
                        print(
                            f"Versuch {attempt}: Frontmatter scheint nicht auf {language_name} zu sein."
                        )
                        # Verstärken der Sprachanweisung im Prompt
                        system_prompt += f"""
                        
                        WARNUNG: Der vorherige Output war NICHT in {language_name}! 
                        Es ist ABSOLUT NOTWENDIG, dass du NUR in {language_name} antwortest.
                        
                        KRITISCH: Der Titel, die Beschreibung und alle Keywords MÜSSEN in {language_name} sein.
                        """
                        messages[0]["content"] = system_prompt
                        time.sleep(2)
                        continue  # Neuer Versuch mit stärkeren Sprachanweisungen
            except Exception as api_error:
                print(f"API call failed: {str(api_error)}")
                # Continue to the next attempt
                continue

            # Parse the response
            lines = content.split("\n")
            title = ""
            description = ""
            keywords = []

            for line in lines:
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Description:"):
                    description = line.replace("Description:", "").strip()
                elif line.startswith("Keywords:"):
                    keywords_str = line.replace("Keywords:", "").strip()
                    keywords = [k.strip() for k in keywords_str.split(",")]

            # Ensure we have title, description and keywords
            if not title or not description or not keywords:
                print(f"Attempt {attempt}: Missing metadata components. Retrying...")
                continue

            # If we have valid content, return it
            print(f"Success on attempt {attempt}: Generated valid SEO metadata")
            return title, description, keywords

        except Exception as e:
            print(f"Attempt {attempt} failed: {str(e)}")
            continue


def create_empty_frontmatter(category: str, language: str) -> str:
    """Create empty YAML frontmatter for a new music category file.

    Creates basic frontmatter with empty/default values. The SEO metadata
    will be added later.

    Args:
        category: Music category name
        language: ISO 639-1 language code

    Returns:
        str: Formatted YAML frontmatter string
    """
    return f"""---
title: {category}
description: 
image: /category/{category.lower().replace(' ', '-')}.jpg
createdAt: {datetime.now().strftime('%Y-%m-%d')}
updatedAt: {datetime.now().strftime('%Y-%m-%d')}
keywords:
author: MelodyMind
locale: {language}
category:
  spotifyPlaylist: 
  deezerPlaylist: 
  appleMusicPlaylist: 
isPlayable: false
---

"""


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


def save_content(category: str, language: str, content: str, mode: str = "w") -> None:
    """Save or append content to a category's markdown file.

    Simply saves or appends the content as provided, without any modifications.

    Args:
        category: Music category name
        language: ISO 639-1 language code
        content: Content to write or append
        mode: File mode, 'w' for write or 'a' for append (default: 'w')
    """
    output_path = get_output_path(category, language)
    logging.info(f"Saving content to {output_path} (mode: {mode})")

    # Save or append to the file
    with open(output_path, mode, encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Successfully wrote {len(content)} characters to {output_path}")


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
        with open(output_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


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
    logging.info("Starting MelodyMind Content Generator")
    print_header("MelodyMind Content Generator")

    # Get available languages
    languages = get_available_languages()
    logging.info(f"Found {len(languages)} supported languages: {', '.join(languages)}")
    print_section(f"Languages: {len(languages)}")
    for lang in languages:
        print(f"✓ {lang}")

    # Read categories from sorted file
    logging.info("Reading categories from sorted file")
    with open(
        BASE_DIR / "scripts" / "category_headlines_sorted.txt", "r", encoding="utf-8"
    ) as f:
        content = f.readlines()

    # Parse categories by type
    logging.info("Parsing categories by type")
    categories_by_type: Dict[str, List[str]] = {}
    current_type = ""
    for line in content:
        line = line.strip()
        if line.startswith("#"):
            current_type = line[1:].strip()
            categories_by_type[current_type] = []
            logging.info(f"Found category type: {current_type}")
        elif line:
            categories_by_type[current_type].append(line)

    total_categories = sum(len(cats) for cats in categories_by_type.values())
    processed_categories = 0

    logging.info(f"Found {total_categories} total categories")
    print_section(f"Categories: {total_categories}")
    for category_type, categories in categories_by_type.items():
        print(f"\n{category_type}: {len(categories)}")
        for cat in categories:
            print(f"• {cat}")

    # Create content directory structure
    logging.info("Creating content directory structure")
    print_section("Creating Directory Structure")
    for language in languages:
        path = CONTENT_DIR / language
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")
        print(f"✓ {path}")

    # Process categories
    logging.info("Starting content generation")
    print_section("Generating Content")
    skipped = 0
    errors = 0
    generated = 0

    for category_type, categories in categories_by_type.items():
        logging.info(f"Processing category type: {category_type}")
        print(f"\n📂 {category_type}")
        for category in categories:
            processed_categories += 1
            logging.info(
                f"Processing category: {category} ({processed_categories}/{total_categories})"
            )
            print(f"\n🎵 {category}")

            for language in languages:
                output_path = get_output_path(category, language)
                if output_path.exists():
                    logging.info(f"Skipping {category} in {language}, file exists")
                    print(f"  ⏭️  Skipping {language}, file exists")
                    skipped += 1
                    continue

                logging.info(f"Generating content for {category} in {language}")

                try:
                    # 1. Generate SEO metadata and create frontmatter
                    logging.info(f"Generating frontmatter for {category} in {language}")
                    frontmatter = create_frontmatter(category, language)
                    save_content(category, language, frontmatter, mode="w")
                    logging.info(
                        f"Successfully created frontmatter for {category} in {language}"
                    )
                    print(f"  ✓ {language}: Frontmatter created")

                    # 2. Generate content
                    logging.info(f"Generating content for {category} in {language}")
                    generate_content(category, language)
                    logging.info(
                        f"Successfully generated content for {category} in {language}"
                    )
                    print(f"  ✓ {language}: Content generated")
                    generated += 1
                except Exception as e:
                    logging.error(
                        f"Failed to generate content for {category} in {language}: {str(e)}"
                    )
                    print(f"  ❌ {language}: Content generation failed - {str(e)}")
                    errors += 1

            print_progress(processed_categories, total_categories, "Overall Progress")

    # Print summary
    end_time = time.time()
    duration = end_time - start_time

    logging.info("Content generation complete")
    logging.info(f"Duration: {int(duration // 60)}m {int(duration % 60)}s")
    logging.info(f"Total Categories: {total_categories}")
    logging.info(f"Files Generated: {generated}")
    logging.info(f"Files Skipped: {skipped}")
    logging.info(f"Errors: {errors}")

    print_header("Generation Complete")
    print(f"Duration: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"Total Categories: {total_categories}")
    print(f"Files Generated: {generated}")
    print(f"Files Skipped: {skipped}")
    print(f"Errors: {errors}")
    print("=" * 80)


if __name__ == "__main__":
    main()
