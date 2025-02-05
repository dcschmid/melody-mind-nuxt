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
    return ["da", "de", "en", "es", "fi", "fr", "it", "nl", "pt", "sv"]

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
            "Legacy and Influence": "Legacy and Influence"
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
            "Legacy and Influence": "Arv og Indflydelse"
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
            "Legacy and Influence": "Perintö ja Vaikutus"
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
            "Legacy and Influence": "Erfenis en Invloed"
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
            "Legacy and Influence": "Arv och Inflytande"
        },
    }
    if language not in translations:
        raise ValueError(f"Translations not available for language: {language}")
        
    return translations[language]

def get_section_limits(category, language="en"):
    # Language-specific adjustment factors for text length
    language_factors = {
        "da": 1.05, # Danish slightly longer than English
        "de": 1.1,  # German tends to be longer
        "en": 1.0,  # English as base
        "es": 1.05, # Spanish slightly longer than English
        "fi": 1.1,  # Finnish tends to be longer
        "fr": 1.05, # French slightly longer than English
        "it": 1.05, # Italian slightly longer than English
        "nl": 1.05, # Dutch slightly longer than English
        "pt": 1.05, # Portuguese slightly longer than English
        "sv": 1.05, # Swedish slightly longer than English
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
                "Key Artists and Albums": "Key Artists and Albums",
                "Technical and Economic Aspects": "Technical and Economic Aspects",
                "Musical Innovation and Markets": "Musical Innovation and Markets",
                "Cultural Impact": "Cultural Impact",
                "Festivals and Live Culture": "Festivals and Live Culture",
                "Lyrics and Themes": "Lyrics and Themes",
                "Legacy and Influences": "Legacy and Influences",
                "Conclusion": "Conclusion"
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
                "Conclusion": "Fazit"
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
                "Key Artists and Albums": "Artistes et albums majeurs",
                "Technical and Economic Aspects": "Aspects techniques et économiques",
                "Musical Innovation and Markets": "Innovation musicale et marchés",
                "Cultural Impact": "Impact culturel",
                "Festivals and Live Culture": "Festivals et culture live",
                "Lyrics and Themes": "Paroles et thèmes",
                "Legacy and Influences": "Héritage et influences",
                "Conclusion": "Conclusion"
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
                "Conclusion": "Conclusione"
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
                "Conclusion": "Conclusão"
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
                "Conclusion": "Konklusion"
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
                "Conclusion": "Conclusie"
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
                "Conclusion": "Slutsats"
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
                "Conclusion": "Yhteenveto"
            }
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
            section_titles["Conclusion"]: 1000
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
                "Conclusion": "Conclusion"
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
                "Conclusion": "Fazit"
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
                "Conclusion": "Conclusión"
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
                "Conclusion": "Conclusion"
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
                "Conclusion": "Conclusione"
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
                "Conclusion": "Conclusão"
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
                "Conclusion": "Konklusion"
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
                "Conclusion": "Conclusie"
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
                "Conclusion": "Slutsats"
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
                "Conclusion": "Yhteenveto"
            }
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
                "Current Trends and Future": "Aktuelle tendenser og fremtid"
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
                "Current Trends and Future": "Huidige trends en toekomst"
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
                "Current Trends and Future": "Aktuella trender och framtid"
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
                "Current Trends and Future": "Nykyiset trendit ja tulevaisuus"
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
                "Music Psychology": "Psychologie musicale",
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
                "Music Psychology": "Psicologia musicale",
                "Musical Characteristics": "Caratteristiche musicali",
                "Cross-Genre Examples": "Esempi tra generi",
                "Cultural Perspectives": "Prospettive culturali",
                "Therapeutic Applications": "Applicazioni terapeutiche",
                "Notable Works and Artists": "Opere e artisti notevoli",
                "Use in Media": "Uso nei media",
                "Modern Interpretations": "Interpretazioni moderne",
                "Practical Significance": "Significato pratico"
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
                "Practical Significance": "Significado prático"
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
                "Practical Significance": "Praktisk betydning"
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
                "Practical Significance": "Praktische betekenis"
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
                "Practical Significance": "Praktisk betydelse"
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
                "Practical Significance": "Käytännön merkitys"
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
            },
            "da": {
                "Introduction": "Introduktion",
                "Cultural Tradition": "Kulturel tradition",
                "Musical Characteristics": "Musikalske karakteristika",
                "Classical Compositions": "Klassiske kompositioner",
                "Popular Music": "Populær musik",
                "Festive Events": "Festlige begivenheder",
                "Media Presence": "Tilstedeværelse i medierne",
                "International Perspectives": "Internationale perspektiver"
            },
            "nl": {
                "Introduction": "Inleiding",
                "Cultural Tradition": "Culturele traditie",
                "Musical Characteristics": "Muzikale kenmerken",
                "Classical Compositions": "Klassieke composities",
                "Popular Music": "Populaire muziek",
                "Festive Events": "Feestelijke evenementen",
                "Media Presence": "Aanwezigheid in de media",
                "International Perspectives": "Internationale perspectieven"
            },
            "sv": {
                "Introduction": "Introduktion",
                "Cultural Tradition": "Kulturell tradition",
                "Musical Characteristics": "Musikaliska egenskaper",
                "Classical Compositions": "Klassiska kompositioner",
                "Popular Music": "Populärmusik",
                "Festive Events": "Festliga evenemang",
                "Media Presence": "Medienärvaro",
                "International Perspectives": "Internationella perspektiv"
            },
            "fi": {
                "Introduction": "Johdanto",
                "Cultural Tradition": "Kulttuuriperinne",
                "Musical Characteristics": "Musiikilliset ominaisuudet",
                "Classical Compositions": "Klassiset sävellykset",
                "Popular Music": "Populaarimusiikki",
                "Festive Events": "Juhlatapahtumat",
                "Media Presence": "Medianäkyvyys",
                "International Perspectives": "Kansainväliset näkökulmat"
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
                "Legacy and Influence": "Arv og indflydelse"
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
                "Legacy and Influence": "Erfenis en invloed"
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
                "Legacy and Influence": "Arv och påverkan"
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
                "Legacy and Influence": "Perintö ja vaikutus"
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
        "da": {
            "style": "Akademisk dansk",
            "characteristics": "præcis musikologisk terminologi, akademisk tone, komplekse sætningsstrukturer",
            "prompt": """
            Opret indhold til sektionen '{section_name}' i musikkategorien '{category}'.
            
            SPROGLIGE KRAV:
            1. Brug udelukkende akademisk dansk
            2. Anvend præcis musikologisk terminologi
            3. Oprethold korrekt grammatik og syntaks
            4. Undgå talesprog og uformelle udtryk
            5. Brug akademiske skrivkonventioner
            
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
            """
        },
        "nl": {
            "style": "Academisch Nederlands",
            "characteristics": "nauwkeurige musicologische terminologie, wetenschappelijke toon, complexe zinsstructuren",
            "prompt": """
            Maak inhoud voor de sectie '{section_name}' in de muziekcategorie '{category}'.
            
            TAALKUNDIGE VEREISTEN:
            1. Gebruik uitsluitend academisch Nederlands
            2. Hanteer nauwkeurige musicologische terminologie
            3. Handhaaf correcte grammatica en syntax
            4. Vermijd spreektaal en informele uitdrukkingen
            5. Gebruik academische schrijfconventies
            
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
            """
        },
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
        "fi": {
            "style": "Akateeminen suomi",
            "characteristics": "tarkka musikologinen terminologia, tieteellinen sävy, monimutkaiset lauserakenteet",
            "prompt": """
            Luo sisältöä musiikkikategorian '{category}' osioon '{section_name}'.
            
            KIELELLISET VAATIMUKSET:
            1. Käytä yksinomaan akateemista suomea
            2. Käytä tarkkaa musikologista terminologiaa
            3. Ylläpidä moitteetonta kielioppia ja lauserakennetta
            4. Vältä puhekielisyyksiä ja epämuodollisia ilmaisuja
            5. Käytä akateemisia kirjoituskonventioita
            
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
            
            ESSENTIEL : Le nombre de caractères doit être au moins {char_min}.
            """
        },
        "it": {
            "style": "italiano accademico",
            "characteristics": "terminologia musicologica precisa, stile accademico rigoroso, strutture sintattiche complesse",
            "prompt": """
            Elabora un contenuto accademico per la sezione '{section_name}' della categoria musicale '{category}'.
            
            REQUISITI LINGUISTICI:
            1. Utilizza un italiano accademico rigoroso
            2. Impiega una terminologia musicologica precisa
            3. Mantieni uno stile formale e scientifico
            4. Adotta strutture sintattiche complesse
            5. Evita espressioni colloquiali e idiomatiche
            
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
            """
        },
        "nl": {
            "style": "Academisch Nederlands",
            "characteristics": "nauwkeurige musicologische terminologie, wetenschappelijke toon, complexe zinsstructuren",
            "prompt": """
            Maak inhoud voor de sectie '{section_name}' van de muziekcategorie '{category}'.
            
            TAALKUNDIGE VEREISTEN:
            1. Gebruik uitsluitend academisch Nederlands
            2. Hanteer nauwkeurige musicologische terminologie
            3. Handhaaf foutloze grammatica en syntaxis
            4. Vermijd spreektaal en informele uitdrukkingen
            5. Gebruik academische schrijfconventies
            
            INHOUDELIJKE SPECIFICATIES:
            1. Tekstlengte MOET minimaal {char_min} tekens zijn
            2. Focus uitsluitend op internationale muziek
            3. Structureer inhoud met duidelijke, logische alinea's
            4. Gebruik complexe maar begrijpelijke zinsstructuren
            5. Vermijd opsommingen ten gunste van vloeiend proza
            6. Integreer relevante cultuurhistorische contexten
            7. Gebruik nauwkeurige muzikale terminologie
            8. Articuleer muziektheoretische relaties duidelijk
            9. Implementeer passende overgangen tussen alinea's
            10. Handhaaf een consistente wetenschappelijke toon
            
            KRITISCH: Het aantal tekens MOET minimaal {char_min} zijn.
            """
        },
        "pt": {
            "style": "português académico",
            "characteristics": "terminologia musicológica precisa, estilo académico rigoroso, estruturas sintáticas complexas, metodologia científica",
            "prompt": """
            Elabore um conteúdo acadêmico para a seção '{section_name}' da categoria musical '{category}'.
            
            REQUISITOS LINGUÍSTICOS:
            1. Empregue um português acadêmico rigoroso
            2. Utilize terminologia musicológica precisa
            3. Mantenha um estilo formal e científico
            4. Adote estruturas sintáticas complexas
            5. Evite expressões coloquiais e modismos
            
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
            """
        },
        "sv": {
            "style": "Akademisk svenska",
            "characteristics": "precis musikologisk terminologi, vetenskaplig ton, komplexa meningsstrukturer",
            "prompt": """
            Skapa innehåll för sektionen '{section_name}' i musikkategorin '{category}'.
            
            SPRÅKLIGA KRAV:
            1. Använd uteslutande akademisk svenska
            2. Använd precis musikologisk terminologi
            3. Upprätthåll korrekt grammatik och syntax
            4. Undvik talspåk och informella uttryck
            5. Använd akademiska skrivkonventioner
            
            INNEHÅLLSKRAV:
            1. Texten MÅSTE vara minst {char_min} tecken
            2. Fokusera uteslutande på internationell musik
            3. Strukturera innehållet med tydliga, logiska stycken
            4. Använd komplexa men förståeliga meningsstrukturer
            5. Undvik punktlistor till förmån för flödande text
            6. Integrera relevanta kulturhistoriska sammanhang
            7. Använd precis musikalisk terminologi
            8. Artikulera musikteoretiska samband tydligt
            9. Implementera lämpliga övergångar mellan stycken
            10. Behåll en konsekvent vetenskaplig ton
            
            KRITISKT: Antalet tecken MÅSTE vara minst {char_min}.
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
    if category.endswith('s') and category[:-1].isdigit():  # Decades
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
    last_error = None
    best_content = ""
    best_char_count = 0
    
    for attempt in range(max_attempts):
        try:
            # Exponential backoff for retries
            if attempt > 0:
                wait_time = min(2 ** attempt, 30)  # Cap at 30 seconds
                time.sleep(wait_time)
            
            # Adjust temperature based on attempt number and previous results
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
            
            # Adjust max_tokens based on char_min
            max_tokens = max(2000, int(char_min / 2))  # Ensure enough tokens for content
            
            # Language-specific system prompts with enhanced instructions
            language_system_prompts = {
                "en": "You are an expert music historian writing in English. Focus on accuracy, clarity, and engaging narrative.",
                "de": "Sie sind ein Musikhistoriker, der auf Deutsch schreibt. Legen Sie Wert auf Präzision, Klarheit und fesselnde Erzählweise.",
                "es": "Eres un historiador musical que escribe en español. Enfócate en la precisión, claridad y narrativa cautivadora.",
                "fr": "Vous êtes un historien de la musique écrivant en français. Concentrez-vous sur la précision, la clarté et un récit engageant.",
                "it": "Sei uno storico della musica che scrive in italiano. Concentrati su precisione, chiarezza e narrativa coinvolgente.",
                "pt": "Você é um historiador musical escrevendo em português. Foque em precisão, clareza e narrativa envolvente."
            }
            
            # Get language-specific system prompt, default to English if not found
            system_prompt = language_system_prompts.get(language, language_system_prompts["en"])
            
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
                current_prompt += f"\n\nThis is a {category_type} category ({category})."
            
            if attempt > 0:
                current_prompt += "\n\nPrevious attempts were insufficient. Please ensure:"
                current_prompt += "\n1. Comprehensive coverage of the topic"
                current_prompt += "\n2. Detailed examples and analysis"
                current_prompt += "\n3. Clear progression of ideas"
                current_prompt += f"\n4. Minimum length of {char_min} characters"
            
            # Add language-specific style guide
            current_prompt += f"\n\nStyle Guide:\n{style_guide['style']}\n{style_guide['characteristics']}"
            
            data = {
                "model": "Llama-3.3-70B-Instruct",
                "messages": [
                    {"role": "system", "content": f"{system_prompt}\n{style_guide}"},
                    {"role": "user", "content": current_prompt}
                ],
                "temperature": temperature,
                "repetition_penalty": 1.1,
                "top_p": 0.9,
                "top_k": 40,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            # Increased timeout for larger content generation
            response = requests.post(
                "https://api.arliai.com/v1/chat/completions",
                headers=headers,
                json=data,
            )
            
            # Log the response status and timing
            logging.info(f"API response received: status={response.status_code}, time={response.elapsed.total_seconds():.2f}s")
            
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.text}")
            
            content = response.json()["choices"][0]["message"]["content"].strip()
            char_count = len(content)
            
            # Keep track of best attempt
            if char_count > best_char_count:
                best_content = content
                best_char_count = char_count
            
            # Return if content meets requirements
            if char_count >= char_min:
                return content
                
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            continue
    
    # If we've exhausted all attempts
    if best_char_count > 0:
        # Return best attempt if it's at least 80% of required length
        if best_char_count >= (char_min * 0.8):
            print(f"Warning: Returning content slightly shorter than requested ({best_char_count}/{char_min} chars)")
            return best_content
    
    # If all attempts failed or content is too short
    error_msg = f"Failed to generate content chunk {chunk_number}/{total_chunks}\n"
    error_msg += f"Section: {section_name}, Language: {language}\n"
    error_msg += f"Last error: {str(last_error)}\n"
    error_msg += f"Best attempt: {best_char_count}/{char_min} characters"
    raise Exception(error_msg)
    
    raise ValueError(f"Failed to generate content chunk {chunk_number}/{total_chunks} with correct length after {max_attempts} attempts")

def generate_content(category: str, language: str) -> str:
    """Generate or update content for a music category in a specific language.
    
    Args:
        category: Music category name
        language: ISO 639-1 language code
        
    Returns:
        str: Status message indicating completion
    """
    logging.info(f"Starting content generation for category '{category}' in language '{language}'")
    
    # Check if language is supported
    if language not in get_available_languages():
        logging.error(f"Language '{language}' is not supported")
        raise ValueError(f"Language '{language}' is not supported")
    
    # Get section limits and translations
    logging.info("Getting section limits and translations")
    section_limits = get_section_limits(category)
    translations = get_translated_sections(language)
    logging.info(f"Found {len(section_limits)} sections to generate")
    
    # Generate each section
    for section_name, char_min in section_limits.items():
        try:
            # Get translated section name
            translated_title = translations.get(section_name, section_name)
            logging.info(f"Generating section: {translated_title} (min chars: {char_min})")
            
            # Generate content
            section_content = generate_section(category, language, section_name, char_min)
            content = f"\n## {translated_title}\n\n{section_content}\n"
            logging.info(f"Generated {len(section_content)} characters for section {translated_title}")
            
            # Save content
            save_content(category, language, content, 'a')
            logging.info(f"Saved section: {translated_title}")
            
        except Exception as e:
            logging.error(f"Error generating section {translated_title}: {str(e)}")
            continue
    
    logging.info(f"Completed content generation for category '{category}' in language '{language}'")
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

def save_content(category: str, language: str, content: str, mode: str = 'w') -> None:
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
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

from datetime import datetime
from typing import Dict, List
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
            logging.info(f"Processing category: {category} ({processed_categories}/{total_categories})")
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
                    save_content(category, language, frontmatter, mode='w')
                    logging.info(f"Successfully created frontmatter for {category} in {language}")
                    print(f"  ✓ {language}: Frontmatter created")

                    # 2. Generate content
                    logging.info(f"Generating content for {category} in {language}")
                    generate_content(category, language)
                    logging.info(f"Successfully generated content for {category} in {language}")
                    print(f"  ✓ {language}: Content generated")
                    generated += 1
                except Exception as e:
                    logging.error(f"Failed to generate content for {category} in {language}: {str(e)}")
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
