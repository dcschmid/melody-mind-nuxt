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
    return ["de", "en", "es", "fr", "it", "pt"]

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
    }
    return sections.get(language, sections["en"])  # Default to English if language not found

def get_section_limits(category, language="en"):
    # Language-specific adjustment factors for text length
    language_factors = {
        "de": 1.1,  # German tends to be longer
        "en": 1.0,  # English as base
        "es": 1.05, # Spanish slightly longer than English
        "fr": 1.05, # French slightly longer than English
        "it": 1.05, # Italian slightly longer than English
        "pt": 1.05, # Portuguese slightly longer than English
    }
    
    # Default factor if language not defined
    factor = language_factors.get(language, 1.0)
    
    # Base minimum length for all sections
    base_min_length = int(1000 * factor)
    
    category_type = get_category_type(category)
    base_limits = {}
    
    if category.endswith('s') and category[:-1].isdigit():  # Decades
        sections = {
            "en": {
                "Introduction": "Introduction",
                "Political and Social Background": "Political and Social Background",
                "Musical Developments": "Musical Developments",
                "Musical Diversity and Subgenres": "Musical Diversity and Subgenres",
                "Rhythm and Style": "Rhythm and Style",
                "Key Artists and Albums": "Key Artists and Albums",
                "Technical and Economic Aspects": "Technical and Economic Aspects",
                "Technological Innovations": "Technological Innovations",
                "Musical Innovation and New Markets": "Musical Innovation and New Markets",
                "Cultural Dimensions": "Cultural Dimensions",
                "Festivals and Live Culture": "Festivals and Live Culture",
                "Lyrics and Themes": "Lyrics and Themes",
                "Subcultures and Fashion": "Subcultures and Fashion",
                "Legacy and Outlook": "Legacy and Outlook",
                "Cultural Significance": "Cultural Significance",
                "Lasting Influences": "Lasting Influences",
                "Conclusion": "Conclusion"
            },
            "de": {
                "Introduction": "Einleitung",
                "Political and Social Background": "Politischer und sozialer Hintergrund",
                "Musical Developments": "Musikalische Entwicklungen",
                "Musical Diversity and Subgenres": "Musikalische Vielfalt und Subgenres",
                "Rhythm and Style": "Rhythmus und Stil",
                "Key Artists and Albums": "Wichtige Künstler und Alben",
                "Technical and Economic Aspects": "Technische und wirtschaftliche Aspekte",
                "Technological Innovations": "Technologische Innovationen",
                "Musical Innovation and New Markets": "Musikalische Innovation und neue Märkte",
                "Cultural Dimensions": "Kulturelle Dimensionen",
                "Festivals and Live Culture": "Festivals und Live-Kultur",
                "Lyrics and Themes": "Liedtexte und Themen",
                "Subcultures and Fashion": "Subkulturen und Mode",
                "Legacy and Outlook": "Vermächtnis und Ausblick",
                "Cultural Significance": "Kulturelle Bedeutung",
                "Lasting Influences": "Bleibende Einflüsse",
                "Conclusion": "Fazit"
            },
            "es": {
                "Introduction": "Introducción",
                "Political and Social Background": "Contexto político y social",
                "Musical Developments": "Desarrollos musicales",
                "Musical Diversity and Subgenres": "Diversidad musical y subgéneros",
                "Rhythm and Style": "Ritmo y estilo",
                "Key Artists and Albums": "Artistas y álbumes principales",
                "Technical and Economic Aspects": "Aspectos técnicos y económicos",
                "Technological Innovations": "Innovaciones tecnológicas",
                "Musical Innovation and New Markets": "Innovación musical y nuevos mercados",
                "Cultural Dimensions": "Dimensiones culturales",
                "Festivals and Live Culture": "Festivales y cultura en vivo",
                "Lyrics and Themes": "Letras y temas",
                "Subcultures and Fashion": "Subculturas y moda",
                "Legacy and Outlook": "Legado y perspectivas",
                "Cultural Significance": "Significado cultural",
                "Lasting Influences": "Influencias duraderas",
                "Conclusion": "Conclusión"
            },
            "fr": {
                "Introduction": "Introduction",
                "Political and Social Background": "Contexte politique et social",
                "Musical Developments": "Développements musicaux",
                "Musical Diversity and Subgenres": "Diversité musicale et sous-genres",
                "Rhythm and Style": "Rythme et style",
                "Key Artists and Albums": "Artistes et albums majeurs",
                "Technical and Economic Aspects": "Aspects techniques et économiques",
                "Technological Innovations": "Innovations technologiques",
                "Musical Innovation and New Markets": "Innovation musicale et nouveaux marchés",
                "Cultural Dimensions": "Dimensions culturelles",
                "Festivals and Live Culture": "Festivals et culture live",
                "Lyrics and Themes": "Paroles et thèmes",
                "Subcultures and Fashion": "Sous-cultures et mode",
                "Legacy and Outlook": "Héritage et perspectives",
                "Cultural Significance": "Importance culturelle",
                "Lasting Influences": "Influences durables",
                "Conclusion": "Conclusion"
            },
            "it": {
                "Introduction": "Introduzione",
                "Political and Social Background": "Contesto politico e sociale",
                "Musical Developments": "Sviluppi musicali",
                "Musical Diversity and Subgenres": "Diversità musicale e sottogeneri",
                "Rhythm and Style": "Ritmo e stile",
                "Key Artists and Albums": "Artisti e album principali",
                "Technical and Economic Aspects": "Aspetti tecnici ed economici",
                "Technological Innovations": "Innovazioni tecnologiche",
                "Musical Innovation and New Markets": "Innovazione musicale e nuovi mercati",
                "Cultural Dimensions": "Dimensioni culturali",
                "Festivals and Live Culture": "Festival e cultura dal vivo",
                "Lyrics and Themes": "Testi e temi",
                "Subcultures and Fashion": "Sottoculture e moda",
                "Legacy and Outlook": "Eredità e prospettive",
                "Cultural Significance": "Significato culturale",
                "Lasting Influences": "Influenze durature",
                "Conclusion": "Conclusione"
            },
            "pt": {
                "Introduction": "Introdução",
                "Political and Social Background": "Contexto político e social",
                "Musical Developments": "Desenvolvimentos musicais",
                "Musical Diversity and Subgenres": "Diversidade musical e subgêneros",
                "Rhythm and Style": "Ritmo e estilo",
                "Key Artists and Albums": "Artistas e álbuns principais",
                "Technical and Economic Aspects": "Aspectos técnicos e econômicos",
                "Technological Innovations": "Inovações tecnológicas",
                "Musical Innovation and New Markets": "Inovação musical e novos mercados",
                "Cultural Dimensions": "Dimensões culturais",
                "Festivals and Live Culture": "Festivais e cultura ao vivo",
                "Lyrics and Themes": "Letras e temas",
                "Subcultures and Fashion": "Subculturas e moda",
                "Legacy and Outlook": "Legado e perspectivas",
                "Cultural Significance": "Significado cultural",
                "Lasting Influences": "Influências duradouras",
                "Conclusion": "Conclusão"
            },
        }
        
        # Get the section titles for the current language
        section_titles = sections.get(language, sections["en"])
        
        # Define the base limits for each section
        base_limits = {
            section_titles["Introduction"]: 1500,
            section_titles["Political and Social Background"]: 2000,
            section_titles["Musical Developments"]: 1000,
            section_titles["Musical Diversity and Subgenres"]: 2000,
            section_titles["Rhythm and Style"]: 1500,
            section_titles["Key Artists and Albums"]: 2000,
            section_titles["Technical and Economic Aspects"]: 800,
            section_titles["Technological Innovations"]: 1500,
            section_titles["Musical Innovation and New Markets"]: 1500,
            section_titles["Cultural Dimensions"]: 800,
            section_titles["Festivals and Live Culture"]: 1500,
            section_titles["Lyrics and Themes"]: 1500,
            section_titles["Subcultures and Fashion"]: 1500,
            section_titles["Legacy and Outlook"]: 800,
            section_titles["Cultural Significance"]: 1500,
            section_titles["Lasting Influences"]: 1500,
            section_titles["Conclusion"]: 1000
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
                "Current Trends and Future": "Current Trends and Future"
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
                "Current Trends and Future": "Aktuelle Trends und Zukunft"
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
                "Current Trends and Future": "Tendencias actuales y futuro"
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
                "Current Trends and Future": "Tendances actuelles et avenir"
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
                "Current Trends and Future": "Tendenze attuali e futuro"
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
                "Current Trends and Future": "Tendências atuais e futuro"
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
            section_titles["Current Trends and Future"]: 1500
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
                "Practical Significance": "Practical Significance"
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
                "Practical Significance": "Praktische Bedeutung"
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
                "Practical Significance": "Significado práctico"
            },
            "fr": {
                "Introduction": "Introduction",
                "Music Psychology": "Psychologie de la musique",
                "Musical Characteristics": "Caractéristiques musicales",
                "Cross-Genre Examples": "Exemples inter-genres",
                "Cultural Perspectives": "Perspectives culturelles",
                "Therapeutic Applications": "Applications thérapeutiques",
                "Notable Works and Artists": "Œuvres et artistes notables",
                "Use in Media": "Utilisation dans les médias",
                "Modern Interpretations": "Interprétations modernes",
                "Practical Significance": "Signification pratique"
            },
            "it": {
                "Introduction": "Introduzione",
                "Music Psychology": "Psicologia della musica",
                "Musical Characteristics": "Caratteristiche musicali",
                "Cross-Genre Examples": "Esempi cross-genre",
                "Cultural Perspectives": "Prospettive culturali",
                "Therapeutic Applications": "Applicazioni terapeutiche",
                "Notable Works and Artists": "Opere e artisti di rilievo",
                "Use in Media": "Uso nei media",
                "Modern Interpretations": "Interpretazioni moderne",
                "Practical Significance": "Significato pratico"
            },
            "pt": {
                "Introduction": "Introdução",
                "Music Psychology": "Psicologia da música",
                "Musical Characteristics": "Características musicais",
                "Cross-Genre Examples": "Exemplos entre gêneros",
                "Cultural Perspectives": "Perspectivas culturais",
                "Therapeutic Applications": "Aplicações terapêuticas",
                "Notable Works and Artists": "Obras e artistas notáveis",
                "Use in Media": "Uso na mídia",
                "Modern Interpretations": "Interpretações modernas",
                "Practical Significance": "Significância prática"
            }
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
            section_titles["Practical Significance"]: 1500
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
                "International Perspectives": "International Perspectives"
            },
            "de": {
                "Introduction": "Einleitung",
                "Cultural Tradition": "Kulturelle Tradition",
                "Musical Characteristics": "Musikalische Merkmale",
                "Classical Compositions": "Klassische Kompositionen",
                "Popular Music": "Populäre Musik",
                "Festive Events": "Festliche Veranstaltungen",
                "Media Presence": "Medienpräsenz",
                "International Perspectives": "Internationale Perspektiven"
            },
            "es": {
                "Introduction": "Introducción",
                "Cultural Tradition": "Tradición cultural",
                "Musical Characteristics": "Características musicales",
                "Classical Compositions": "Composiciones clásicas",
                "Popular Music": "Música popular",
                "Festive Events": "Eventos festivos",
                "Media Presence": "Presencia en medios",
                "International Perspectives": "Perspectivas internacionales"
            },
            "fr": {
                "Introduction": "Introduction",
                "Cultural Tradition": "Tradition culturelle",
                "Musical Characteristics": "Caractéristiques musicales",
                "Classical Compositions": "Compositions classiques",
                "Popular Music": "Musique populaire",
                "Festive Events": "Événements festifs",
                "Media Presence": "Présence médiatique",
                "International Perspectives": "Perspectives internationales"
            },
            "it": {
                "Introduction": "Introduzione",
                "Cultural Tradition": "Tradizione culturale",
                "Musical Characteristics": "Caratteristiche musicali",
                "Classical Compositions": "Composizioni classiche",
                "Popular Music": "Musica popolare",
                "Festive Events": "Eventi festivi",
                "Media Presence": "Presenza nei media",
                "International Perspectives": "Prospettive internazionali"
            },
        
            "pt": {
                "Introduction": "Introdução",
                "Cultural Tradition": "Tradição cultural",
                "Musical Characteristics": "Características musicais",
                "Classical Compositions": "Composições clássicas",
                "Popular Music": "Música popular",
                "Festive Events": "Eventos festivos",
                "Media Presence": "Presença na mídia",
                "International Perspectives": "Perspectivas internacionais"
            }
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
            section_titles["International Perspectives"]: 1500
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
                "Legacy and Influence": "Legacy and Influence"
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
                "Legacy and Influence": "Vermächtnis und Einfluss"
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
                "Legacy and Influence": "Legado e influencia"
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
                "Legacy and Influence": "Héritage et influence"
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
                "Legacy and Influence": "Eredità e influenza"
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
                "Legacy and Influence": "Legado e influência"
            }
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
            section_titles["Legacy and Influence"]: 1500
        }
    
    # Anwenden des Sprachfaktors auf alle Limits
    adjusted_limits = {}
    for section, min_chars in base_limits.items():
        adjusted_limits[section] = int(min_chars * factor)
    
    return adjusted_limits

def get_language_prompts(language):
    prompts = {
        "de": {
            "style": "Akademisches Hochdeutsch",
            "characteristics": "präzise Fachterminologie, komplexe Satzstrukturen, formelle Ausdrucksweise, musikwissenschaftliche Genauigkeit",
            "prompt": """
            Erstelle Inhalte für den Abschnitt '{section_name}' der Musikkategorie '{category}'.
            
            SPRACHLICHE ANFORDERUNGEN:
            1. Verwende ausschließlich standardisiertes Hochdeutsch
            2. Nutze präzise musikwissenschaftliche Fachterminologie
            3. Achte auf korrekte Grammatik, Rechtschreibung und Zeichensetzung
            4. Vermeide Anglizismen und umgangssprachliche Ausdrücke
            5. Verwende eine akademisch angemessene Ausdrucksweise
            
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
            """
        },
        "en": {
            "style": "Academic British English",
            "characteristics": "precise musicological terminology, scholarly tone, complex sentence structures, formal academic style",
            "prompt": """
            Create content for the section '{section_name}' of the music category '{category}'.
            
            LINGUISTIC REQUIREMENTS:
            1. Use formal British English exclusively
            2. Employ precise musicological terminology
            3. Maintain impeccable grammar and syntax
            4. Avoid colloquialisms and informal expressions
            5. Use academic writing conventions
            
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
            """
        },
        "es": {
            "style": "español académico",
            "characteristics": "terminología musicológica precisa, estilo académico riguroso, estructuras sintácticas complejas",
            "prompt": """
            Elabore un contenido académico para la sección '{section_name}' de la categoría musical '{category}'.
            
            REQUISITOS LINGÜÍSTICOS:
            1. Emplee un español académico riguroso
            2. Utilice terminología musicológica precisa
            3. Mantenga un estilo formal y científico
            4. Adopte estructuras sintácticas complejas
            5. Evite expresiones coloquiales y modismos
            
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
            """
        },
        "fr": {
            "style": "français académique",
            "characteristics": "terminologie musicologique précise, style académique rigoureux, structures syntaxiques complexes",
            "prompt": """
            Élaborez un contenu académique pour la section '{section_name}' de la catégorie musicale '{category}'.
            
            EXIGENCES LINGUISTIQUES:
            1. Employez un français académique rigoureux
            2. Utilisez une terminologie musicologique précise
            3. Maintenez un style formel et scientifique
            4. Adoptez des structures syntaxiques complexes
            5. Évitez les expressions familières et argotiques
            
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
            
            ESSENTIEL : Le décompte des caractères doit être au moins {char_min}.
            """
        },
        "pt": {
            "style": "português académico",
            "characteristics": "terminologia musicológica precisa, estilo académico rigoroso, estruturas sintáticas complexas, metodologia científica",
            "prompt": """
            Elabore um conteúdo académico para a seção '{section_name}' da categoria musical '{category}'.
            
            REQUISITOS LINGUÍSTICOS:
            1. Utilize português académico rigoroso
            2. Empregue terminologia musicológica precisa
            3. Mantenha um estilo formal e científico
            4. Adote estruturas sintáticas complexas
            5. Evite expressões coloquiais e idiomáticas
            6. Respeite as normas de citação académica
            
            REQUISITOS DE CONTEÚDO:
            1. Respeite rigorosamente o mínimo de caracteres: {char_min}
            2. Desenvolva uma análise académica da música internacional
            3. Estruture o texto com parágrafos logicamente articulados
            4. Integre aspectos teóricos e contexto histórico
            5. Privilegie a argumentação sobre a enumeração
            6. Incorpore referências culturais pertinentes
            7. Aplique a terminologia musical com precisão
            8. Mantenha um registo académico constante
            9. Utilize citações segundo as normas académicas
            10. Preserve uma abordagem metodológica rigorosa
            
            ESSENCIAL: A contagem de caracteres deve ser pelo menos {char_min}.
            """
        },
        "it": {
            "style": "italiano accademico",
            "characteristics": "terminologia musicologica precisa, stile accademico rigoroso, strutture sintattiche complesse",
            "prompt": """
            Elabora un contenuto accademico per la sezione '{section_name}' della categoria musicale '{category}'.
            
            REQUISITI LINGUISTICI:
            1. Utilizza un italiano accademico rigoroso
            2. Impiega terminologia musicologica precisa
            3. Mantieni uno stile formale e scientifico
            4. Adotta strutture sintattiche complesse
            5. Evita espressioni colloquiali e gergali
            6. Rispetta le norme di citazione accademica
            
            REQUISITI CONTENUTISTICI:
            1. Rispetta rigorosamente il minimo di caratteri: {char_min}
            2. Sviluppa un'analisi accademica della musica internazionale
            3. Struttura il testo con paragrafi logicamente concatenati
            4. Integra aspetti teorici e contesto storico
            5. Privilegia l'argomentazione rispetto all'elencazione
            6. Incorpora riferimenti culturali pertinenti
            7. Applica la terminologia musicale con precisione
            8. Mantieni un registro accademico costante
            9. Utilizza citazioni secondo gli standard accademici
            10. Preserva un approccio metodologicamente rigoroso
            
            ESSENZIALE: Il conteggio dei caratteri deve essere almeno {char_min}.
            """
        },
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
                   char_min: int) -> str:
    """Generate content for a specific section of a music category.
    
    Uses the Arli AI API to generate language-specific content that adheres
    to style guidelines and meets minimum length requirements. For longer sections,
    splits the generation into multiple chunks and combines them.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        section_name: Name of the section to generate
        char_min: Minimum character count for the content
        
    Returns:
        str: Generated content for the section
        
    Raises:
        ValueError: If ARLI_API_KEY is not set or content generation fails
        Exception: For API errors or other issues
    """
    if not ARLI_API_KEY:
        raise ValueError("ARLI_API_KEY environment variable not set")
    
    # Generate content in one go
    return generate_section_chunk(
        category=category,
        language=language,
        section_name=section_name,
        char_min=char_min,
        chunk_number=1,
        total_chunks=1
    )


def generate_section_chunk(category: str, language: str, section_name: str,
                         char_min: int, chunk_number: int,
                         total_chunks: int) -> str:
    """Generate a chunk of content for a section.
    
    Helper function that handles the actual API calls and retries for
    generating a single chunk of content.
    """
    headers = {
        "Authorization": f"Bearer {ARLI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    style_guide = get_language_style_guide(language)
    language_prompts = get_language_prompts(language)
    
    # Add historical accuracy guidelines
    historical_accuracy = """
    Important historical guidelines:
    - Ensure strict historical accuracy for the specific time period, genre, or region being discussed
    - Only mention artists, bands, and cultural phenomena that were active/present during the relevant time period
    - Pay careful attention to when specific music styles, technologies, and cultural movements emerged
    - Be precise with dates and chronological order of events - never mention artists or developments before they emerged
    - Consider the geographical and cultural context of musical developments
    - Verify the accuracy of technological developments and their impact on music
    - When discussing influences, ensure they are chronologically possible and historically accurate
    - For decade-specific content, focus only on artists and trends that were actually prominent during that specific time
    - Acknowledge regional variations in how musical styles developed and spread
    - Consider the social and cultural context of the time period being discussed
    - For country-specific content, focus primarily on artists who are actually from or significantly influenced that country's music scene
    - For genre-specific content, only mention artists who genuinely contributed to or performed in that genre
    - Respect and maintain the cultural authenticity of regional music styles and their development
    - When discussing musical innovations, verify their historical emergence and adoption
    - For cross-cultural influences, ensure they were actually possible given the historical context
    - When mentioning music technology, verify it was available during the discussed time period
    """

    # Format the base prompt
    base_prompt = language_prompts["prompt"].format(
        section_name=section_name,
        category=category,
        char_min=char_min
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
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            # Adjust temperature based on attempt number
            if attempt == 0:
                temperature = 0.7
            elif attempt == 1:
                temperature = 0.8
            elif attempt == 2:
                temperature = 0.6
            elif attempt == 3:
                temperature = 0.75
            else:
                temperature = 0.65
            
            # Set a generous max_tokens limit
            max_tokens = 2000
            
            # Language-specific system prompts
            language_system_prompts = {
                "en": "You are an expert music historian writing in English. Use clear, engaging language suitable for English readers.",
                "de": "Sie sind ein Musikhistoriker, der auf Deutsch schreibt. Verwenden Sie eine klare, ansprechende Sprache für deutschsprachige Leser.",
                "es": "Eres un historiador musical que escribe en español. Utiliza un lenguaje claro y atractivo para lectores hispanohablantes.",
                "fr": "Vous êtes un historien de la musique écrivant en français. Utilisez un langage clair et engageant pour les lecteurs francophones.",
                "it": "Sei uno storico della musica che scrive in italiano. Usa un linguaggio chiaro e coinvolgente per i lettori italiani.",
                "pt": "Você é um historiador musical escrevendo em português. Use linguagem clara e envolvente para leitores lusófonos."
            }
            
            # Get language-specific system prompt, default to English if not found
            system_prompt = language_system_prompts.get(language, language_system_prompts["en"])
            
            # Add language-specific style guide
            base_prompt += f"\n\nStyle Guide:\n{style_guide['style']}\n{style_guide['characteristics']}"
            
            data = {
                "model": "Llama-3.3-70B-Instruct",
                "messages": [
                    {"role": "system", "content": f"{system_prompt}\n{style_guide}"},
                    {"role": "user", "content": base_prompt}
                ],
                "temperature": temperature,
                "repetition_penalty": 1.1,
                "top_p": 0.9,
                "top_k": 40,
                "max_tokens": max_tokens,
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
            
            # Check if content meets minimum length requirement
            char_count = len(content)
            if char_count >= char_min:
                return content
            
            # Content is too short, provide guidance for next attempt
            base_prompt += f"\n\nThe text needs to be longer. Current: {char_count}, Target: at least {char_min} characters."
            base_prompt += "\nPlease expand with more details and examples about:"
            base_prompt += "\n- Historical developments and their significance"
            base_prompt += "\n- Key artists and their contributions"
            base_prompt += "\n- Cultural impact and lasting influence"
            
            # Add a short pause between attempts to avoid rate limiting
            time.sleep(2)
                
        except Exception as e:
            if attempt == max_attempts - 1:  # Last attempt
                error_msg = f"Failed to generate content chunk {chunk_number}/{total_chunks}\n"
                error_msg += f"Section: {section_name}, Language: {language}\n"
                error_msg += f"Error: {str(e)}"
                raise ValueError(error_msg)
            
            print(f"  Attempt {attempt + 1} failed for chunk {chunk_number}/{total_chunks}: {str(e)}")
            time.sleep(3)  # Add longer pause after an error
            continue
    
    raise ValueError(f"Failed to generate content chunk {chunk_number}/{total_chunks} with correct length after {max_attempts} attempts")

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
    
    # Get the translated section titles for this language
    translations = get_translated_sections(language)
    
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
                    # Store with the original (untranslated) section name as key
                    original_section = next((k for k, v in translations[language].items() if v == current_section), current_section)
                    existing_sections[original_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            # Store with the original (untranslated) section name as key
            original_section = next((k for k, v in translations[language].items() if v == current_section), current_section)
            existing_sections[original_section] = '\n'.join(current_content)
    else:
        existing_sections = {}
        # Create new file with frontmatter
        save_content(category, language, '', 'w')
    
    # Generate or skip each section
    for section_name, char_min in section_limits.items():
        if section_name in existing_sections:
            print(f"  Skipping existing section: {translations[language].get(section_name, section_name)}")
            continue
            
        print(f"  Generating section: {translations[language].get(section_name, section_name)}...")
        try:
            section_content = generate_section(category, language, section_name, char_min)
            
            # Use translated section title in the markdown
            translated_title = translations[language].get(section_name, section_name)
            content = f"\n## {translated_title}\n\n{section_content}\n"
            
            # Append the new section to the file
            save_content(category, language, content, 'a')
            print(f"  ✓ Saved section: {translations.get(section_name, section_name)}")
            
        except Exception as e:
            print(f"  ✗ Error generating section {translations.get(section_name, section_name)}: {str(e)}")
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
    
    Uses the Arli AI API to generate language-specific, SEO-optimized title,
    description, and keywords for a music category page. Adapts content
    based on language-specific SEO best practices and cultural context.
    
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
    
    # Language-specific SEO guidelines
    seo_guidelines = {
        "en": {
            "title_length": 60,
            "desc_length": 155,
            "style": "Direct and action-oriented",
            "keyword_format": "Use natural phrases, include long-tail keywords",
            "min_keywords": 5
        },
        "de": {
            "title_length": 55,  # German words tend to be longer
            "desc_length": 150,
            "style": "Precise and formal",
            "keyword_format": "Include compound words (Komposita) where appropriate",
            "min_keywords": 5
        },
        "es": {
            "title_length": 65,  # Spanish needs slightly more space
            "desc_length": 160,
            "style": "Engaging and conversational",
            "keyword_format": "Include both singular and plural forms",
            "min_keywords": 5
        },
        "fr": {
            "title_length": 65,
            "desc_length": 160,
            "style": "Elegant and refined",
            "keyword_format": "Consider gender variations in keywords",
            "min_keywords": 5
        },
        "it": {
            "title_length": 65,
            "desc_length": 160,
            "style": "Expressive and dynamic",
            "keyword_format": "Include regional variations where relevant",
            "min_keywords": 5
        },
        "pt": {
            "title_length": 65,
            "desc_length": 160,
            "style": "Engaging and natural",
            "keyword_format": "Include Brazilian and European Portuguese variations",
            "min_keywords": 5
        }
    }
    
    # Get language-specific guidelines or use English defaults
    guidelines = seo_guidelines.get(language, seo_guidelines["en"])
    
    headers = {
        "Authorization": f"Bearer {ARLI_API_KEY}",
        "Content-Type": "application/json"
    }
    
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
    
    Please provide:
    1. An engaging, keyword-rich title that reflects the language style
    2. A compelling meta description that includes main keywords and encourages clicks
    3. A list of 5-7 relevant keywords/phrases specific to {language} speakers
    
    Format the response exactly like this:
    Title: [title]
    Description: [description]
    Keywords: [keyword1, keyword2, keyword3, ...]
    """
    
    data = {
        "model": "Llama-3.3-70B-Instruct",
        "messages": [
            {"role": "system", "content": f"You are an SEO expert specializing in {language} music content optimization."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "repetition_penalty": 1.1,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False
    }
    
    max_attempts = 5
    for attempt in range(max_attempts):
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
            
            # Ensure we have title, description and keywords
            if not title or not description or not keywords:
                print(f"\nRetrying due to missing metadata")
                continue
            
            # Validate and truncate if necessary
            guidelines = seo_guidelines.get(language, seo_guidelines["en"])
            if len(title) > guidelines['title_length']:
                title = title[:guidelines['title_length']].rsplit(' ', 1)[0]
            
            if len(description) > guidelines['desc_length']:
                description = description[:guidelines['desc_length']].rsplit(' ', 1)[0] + '...'
            
            # Validate and ensure minimum required keywords
            min_keywords = guidelines.get('min_keywords', 5)
            
            # Language-specific basic keywords
            music_terms = {
                'en': 'music',
                'de': 'Musik',
                'es': 'música',
                'fr': 'musique',
                'it': 'musica',
                'pt': 'música'
            }
            music_term = music_terms.get(language, 'music')
            
            # Initialize basic keywords
            basic_keywords = []
            
            if len(keywords) < min_keywords:
                basic_keywords = [category, music_term, f"{category} {music_term}"]
            
            # For languages that read right-to-left (e.g., Arabic)
            if language == 'ar':
                basic_keywords.append(f"{music_term} {category}")
            
            # Use basic keywords as is
            valid_basic_keywords = basic_keywords
            
            keywords.extend(valid_basic_keywords)
            keywords = list(dict.fromkeys(keywords))  # Remove duplicates
            
            # If we have valid content, return it
            return title, description, keywords
            
        except Exception as e:
            print(f"Error in attempt {attempt + 1}: {str(e)}")
            if attempt == max_attempts - 1:
                # Language-specific fallback values
                fallbacks = {
                    "de": (f"{category} Musik", f"Entdecken Sie {category} Musik", [f"{category}", "Musik", f"{category} Musik"]),
                    "es": (f"Música {category}", f"Descubre la música {category}", [f"{category}", "música", f"música {category}"]),
                    "fr": (f"Musique {category}", f"Découvrez la musique {category}", [f"{category}", "musique", f"musique {category}"]),
                    "it": (f"Musica {category}", f"Scopri la musica {category}", [f"{category}", "musica", f"musica {category}"]),
                    "en": (f"{category} Music", f"Discover {category} Music", [f"{category}", "music", f"{category} music"]),
                    "pt": (f"Música {category}", f"Descubra a música {category}", [f"{category}", "música", f"música {category}"])
                }
                
                # Get fallback values for the current language, defaulting to English
                title, description, keywords = fallbacks.get(language, fallbacks["en"])
                
                # Use English fallback if language not supported
                if language not in fallbacks:
                    title, description, keywords = fallbacks["en"]
                    
                # Use the keywords as is
                valid_keywords = keywords
                
                # If no keywords, use English fallback
                if not valid_keywords:
                    valid_keywords = fallbacks["en"][2]
                
                return title, description, valid_keywords
            
            time.sleep(1)  # Short delay before retrying

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
