"""
Language-specific grammar rules for all supported languages.
This module imports and provides access to grammar checking functions for various languages.
"""

from typing import List, Dict, Any
import spacy
import re

# Aktualisierte Sprachmodelle auf Large-Versionen
MODELS = {
    "da": "da_core_news_lg",  # Dänisch (large)
    "de": "de_core_news_lg",  # Deutsch (large)
    "en": "en_core_web_lg",   # Englisch (large)
    "es": "es_core_news_lg",  # Spanisch (large)
    "fi": "fi_core_news_lg",  # Finnisch (large)
    "fr": "fr_core_news_lg",  # Französisch (large)
    "it": "it_core_news_lg",  # Italienisch (large)
    "nl": "nl_core_news_lg",  # Niederländisch (large)
    "no": "nb_core_news_lg",  # Norwegisch (Bokmål) (large)
    "pt": "pt_core_news_lg",  # Portugiesisch (large)
    "sv": "sv_core_news_lg"   # Schwedisch (large)
}

# Erweiterte Satzstrukturen für alle Sprachen
SENTENCE_PATTERNS = {
    "da": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {verb} {object}",
        "complex": "Mens {subject} {verb} {object}, {subject2} {verb2}"
    },
    "de": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {object} {verb}",
        "complex": "Während {subject} {object} {verb}, {subject2} {verb2}"
    },
    "en": {
        "basic": "{subject} {verb} {object}", 
        "formal": "{subject} {verb} {object}",
        "complex": "While {subject} {verb} {object}, {subject2} {verb2}"
    },
    "es": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {verb} {object}",
        "complex": "Mientras {subject} {verb} {object}, {subject2} {verb2}"
    },
    "fi": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {object} {verb}",
        "complex": "Kun {subject} {verb} {object}, {subject2} {verb2}"
    },
    "fr": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {verb} {object}",
        "complex": "Pendant que {subject} {verb} {object}, {subject2} {verb2}"
    },
    "it": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {object} {verb}",
        "complex": "Mentre {subject} {verb} {object}, {subject2} {verb2}"
    },
    "nl": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {object} {verb}",
        "complex": "Terwijl {subject} {object} {verb}, {subject2} {verb2}"
    },
    "pt": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {verb} {object}",
        "complex": "Enquanto {subject} {verb} {object}, {subject2} {verb2}"
    },
    "sv": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {object} {verb}",
        "complex": "Medan {subject} {verb} {object}, {subject2} {verb2}"
    },
    "no": {
        "basic": "{subject} {verb} {object}",
        "formal": "{subject} {verb} {object}",
        "complex": "Mens {subject} {verb} {object}, {subject2} {verb2}"
    }
}

# Erweiterte Transformationsregeln für alle Sprachen
TRANSFORMATION_RULES = {
    "da": {
        "nominal_style": [
            (r"(\w+)e\b", r"\1ning"),
            (r"(\w+)ig\b", r"\1ighed")
        ],
        "verbal_style": [
            (r"(\w+)ning\b", r"\1e"),
            (r"(\w+)ighed\b", r"\1ig")
        ]
    },
    "de": {
        "nominal_style": [
            (r"(\w+)en\b", r"die \1ung"),
            (r"(\w+)ig\b", r"\1igkeit")
        ],
        "verbal_style": [
            (r"die (\w+)ung", r"\1en"),
            (r"(\w+)igkeit", r"\1ig")
        ]
    },
    "en": {
        "nominal_style": [
            (r"(\w+)ing\b", r"the \1ation"),
            (r"(\w+)e\b", r"\1ment")
        ],
        "verbal_style": [
            (r"the (\w+)ation", r"\1ing"),
            (r"(\w+)ment", r"\1e")
        ]
    },
    "es": {
        "nominal_style": [
            (r"(\w+)ar\b", r"\1ación"),
            (r"(\w+)er\b", r"\1imiento")
        ],
        "verbal_style": [
            (r"(\w+)ación", r"\1ar"),
            (r"(\w+)imiento", r"\1er")
        ]
    },
    "fi": {
        "nominal_style": [
            (r"(\w+)a\b", r"\1minen"),
            (r"(\w+)ä\b", r"\1minen")
        ],
        "verbal_style": [
            (r"(\w+)minen", r"\1a"),
            (r"(\w+)minen", r"\1ä")
        ]
    },
    "fr": {
        "nominal_style": [
            (r"(\w+)er\b", r"la \1ation"),
            (r"(\w+)ir\b", r"le \1issement")
        ],
        "verbal_style": [
            (r"la (\w+)ation", r"\1er"),
            (r"le (\w+)issement", r"\1ir")
        ]
    },
    "it": {
        "nominal_style": [
            (r"(\w+)are\b", r"\1azione"),
            (r"(\w+)ere\b", r"\1imento")
        ],
        "verbal_style": [
            (r"(\w+)azione", r"\1are"),
            (r"(\w+)imento", r"\1ere")
        ]
    },
    "nl": {
        "nominal_style": [
            (r"(\w+)en\b", r"de \1ing"),
            (r"(\w+)ig\b", r"\1igheid")
        ],
        "verbal_style": [
            (r"de (\w+)ing", r"\1en"),
            (r"(\w+)igheid", r"\1ig")
        ]
    },
    "pt": {
        "nominal_style": [
            (r"(\w+)ar\b", r"\1ação"),
            (r"(\w+)er\b", r"\1imento")
        ],
        "verbal_style": [
            (r"(\w+)ação", r"\1ar"),
            (r"(\w+)imento", r"\1er")
        ]
    },
    "sv": {
        "nominal_style": [
            (r"(\w+)a\b", r"\1ning"),
            (r"(\w+)ig\b", r"\1ighet")
        ],
        "verbal_style": [
            (r"(\w+)ning", r"\1a"),
            (r"(\w+)ighet", r"\1ig")
        ]
    },
    "no": {
        "nominal_style": [
            (r"(\w+)e\b", r"\1ing"),
            (r"(\w+)ig\b", r"\1het")
        ],
        "verbal_style": [
            (r"(\w+)ing\b", r"\1e"),
            (r"(\w+)het\b", r"\1ig")
        ]
    }
}

# Common grammar rule types
RULE_TYPES = {
    'subject_verb_agreement': 'Subject-verb agreement error',
    'article_agreement': 'Article-noun agreement error', 
    'case_agreement': 'Case agreement error',
    'gender_agreement': 'Gender agreement error',
    'number_agreement': 'Number agreement error',
    'tense_agreement': 'Tense agreement error',
    'mood_agreement': 'Mood agreement error',
    'aspect_agreement': 'Aspect agreement error'
}

class GrammarChecker:
    """Handles grammar checking and sentence transformation for different languages."""
    
    def __init__(self, language: str):
        """Initialize grammar checker for specified language."""
        self.language = language
        try:
            self.nlp = spacy.load(MODELS[language])
        except OSError:
            print(f"Downloading language model for {language}...")
            spacy.cli.download(MODELS[language])
            self.nlp = spacy.load(MODELS[language])

    def check_sentence(self, text: str) -> List[Dict[str, Any]]:
        """Check grammar rules for a sentence."""
        doc = self.nlp(text)
        errors = []
        
        # Sprachspezifische Grammatikprüfungen
        if self.language == "de":
            self._check_german_grammar(doc, errors)
        elif self.language == "en":
            self._check_english_grammar(doc, errors)
        elif self.language == "fr":
            self._check_french_grammar(doc, errors)
        # ...weitere Sprachen...
        
        return errors
    
    def _check_german_grammar(self, doc, errors):
        """Deutsche Grammatikregeln"""
        for token in doc:
            # Kasus-Kongruenz
            if token.dep_ == "sb" and token.head.pos_ == "VERB":
                if not self._check_case_agreement(token, token.head):
                    errors.append({
                        "type": "case_agreement",
                        "message": "Kasusfehler zwischen Subjekt und Verb",
                        "token": token.text
                    })
                    
            # Genus-Kongruenz bei Artikeln
            if token.pos_ == "DET" and token.head.pos_ == "NOUN":
                if not self._check_gender_agreement(token, token.head):
                    errors.append({
                        "type": "gender_agreement",
                        "message": "Genusfehler zwischen Artikel und Nomen",
                        "token": token.text
                    })

    def _check_english_grammar(self, doc, errors):
        """Englische Grammatikregeln"""
        for token in doc:
            # Subject-Verb Agreement
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                if not self._check_subject_verb_agreement(token, token.head):
                    errors.append({
                        "type": "subject_verb_agreement",
                        "message": "Subject-verb agreement error",
                        "token": token.text
                    })

    def _check_french_grammar(self, doc, errors):
        """Französische Grammatikregeln"""
        for token in doc:
            # Accord sujet-verbe
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                if not self._check_french_agreement(token, token.head):
                    errors.append({
                        "type": "agreement",
                        "message": "Erreur d'accord sujet-verbe",
                        "token": token.text
                    })

    def _check_case_agreement(self, token, head) -> bool:
        """Check case agreement between token and its head."""
        try:
            token_feats = token.morph
            head_feats = head.morph
            
            # Get case information if available
            token_case = token_feats.get("Case", [""])[0]
            head_case = head_feats.get("Case", [""])[0]
            
            # Consider agreement valid if either doesn't have case or they match
            return not token_case or not head_case or token_case == head_case
        except:
            return True

    def _check_gender_agreement(self, token, head) -> bool:
        """Check gender agreement between token and its head."""
        try:
            token_feats = token.morph
            head_feats = head.morph
            
            # Get gender information if available
            token_gender = token_feats.get("Gender", [""])[0]
            head_gender = head_feats.get("Gender", [""])[0]
            
            # Consider agreement valid if either doesn't have gender or they match
            return not token_gender or not head_gender or token_gender == head_gender
        except:
            return True

    def _check_subject_verb_agreement(self, token, head) -> bool:
        """Check number agreement between subject and verb."""
        try:
            token_feats = token.morph
            head_feats = head.morph
            
            # Get number information if available
            token_number = token_feats.get("Number", [""])[0]
            head_number = head_feats.get("Number", [""])[0]
            
            # Consider agreement valid if either doesn't have number or they match
            return not token_number or not head_number or token_number == head_number
        except:
            return True

    def _check_french_agreement(self, token, head) -> bool:
        """Check French-specific agreements (gender and number)."""
        try:
            token_feats = token.morph
            head_feats = head.morph
            
            # Check both gender and number agreement
            gender_ok = self._check_gender_agreement(token, head)
            number_ok = self._check_subject_verb_agreement(token, head)
            
            return gender_ok and number_ok
        except:
            return True

    # ...weitere sprachspezifische Prüfmethoden...

    def transform_sentence(self, text: str, style: str = "formal") -> str:
        """Transform sentence according to language-specific rules."""
        doc = self.nlp(text)
        
        if style == "formal":
            # Anwenden der Nominalisierungsregeln
            for pattern, replacement in TRANSFORMATION_RULES[self.language]["nominal_style"]:
                text = re.sub(pattern, replacement, text)
                
        elif style == "simple":
            # Anwenden der Verbalisierungsregeln
            for pattern, replacement in TRANSFORMATION_RULES[self.language]["verbal_style"]:
                text = re.sub(pattern, replacement, text)
        
        return text

def get_grammar_checker(language: str) -> GrammarChecker:
    """Factory function to get a grammar checker instance."""
    return GrammarChecker(language)

# Standardisierte Grammatikprüffunktionen für jede Sprache
def check_grammar(text: str, language: str) -> List[Dict[str, Any]]:
    """Unified grammar check function for all languages."""
    checker = get_grammar_checker(language)
    return checker.check_sentence(text)

# Update GRAMMAR_CHECKERS to use local functions
GRAMMAR_CHECKERS = {
    'en': lambda text: check_grammar(text, 'en'),
    'de': lambda text: check_grammar(text, 'de'),
    'fr': lambda text: check_grammar(text, 'fr'),
    'es': lambda text: check_grammar(text, 'es'),
    'it': lambda text: check_grammar(text, 'it'),
    'nl': lambda text: check_grammar(text, 'nl'),
    'pt': lambda text: check_grammar(text, 'pt'),
    'da': lambda text: check_grammar(text, 'da'),
    'sv': lambda text: check_grammar(text, 'sv'),
    'fi': lambda text: check_grammar(text, 'fi'),
    'no': lambda text: check_grammar(text, 'no')
}

# ...rest of existing code...
