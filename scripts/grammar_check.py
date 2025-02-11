"""
Grammar checking using LanguageTool
"""

import language_tool_python

def check_grammar(text: str, language: str = 'en-US') -> list:
    """
    Check grammar using LanguageTool
    
    Args:
        text: Text to check
        language: Language code (e.g. 'en-US', 'de-DE', 'fr', 'da')
        
    Returns:
        List of grammar mistakes with corrections
    """
    # Initialize tool for specified language
    tool = language_tool_python.LanguageTool(language)
    
    # Get matches (potential errors)
    matches = tool.check(text)
    
    # Format results
    corrections = []
    for match in matches:
        correction = {
            'message': match.message,
            'context': match.context,
            'offset': match.offset,
            'length': match.errorLength,
            'replacements': match.replacements,
            'rule_id': match.ruleId,
            'category': match.category
        }
        corrections.append(correction)
    
    return corrections

def apply_corrections(text: str, corrections: list) -> str:
    """
    Apply corrections to text
    
    Args:
        text: Original text
        corrections: List of corrections from check_grammar()
        
    Returns:
        Corrected text
    """
    # Sort corrections in reverse order to avoid offset issues
    corrections.sort(key=lambda x: x['offset'], reverse=True)
    
    # Apply corrections
    for correction in corrections:
        if correction['replacements']:
            start = correction['offset']
            end = start + correction['length']
            text = text[:start] + correction['replacements'][0] + text[end:]
    
    return text
