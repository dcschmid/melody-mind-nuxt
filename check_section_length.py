import re

def count_characters_in_section(section_text):
    # Entferne Überschrift und Leerzeilen am Anfang und Ende
    content = section_text.strip()
    content = re.sub(r'^##[^\n]*\n', '', content)
    content = content.strip()
    return len(content)

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Teile den Inhalt in Abschnitte auf
    sections = re.split(r'\n##\s+', content)
    
    # Entferne den Frontmatter vom ersten Abschnitt
    sections[0] = sections[0].split('---\n')[-1]

    # Analysiere jeden Abschnitt
    for section in sections:
        if section.strip():
            # Extrahiere den Titel
            title = section.split('\n')[0].strip()
            if not title:
                continue
                
            # Zähle die Zeichen
            char_count = count_characters_in_section(section)
            
            status = "OK" if 4000 <= char_count <= 4400 else "ZU KURZ" if char_count < 4000 else "ZU LANG"
            print(f"{title}: {char_count} Zeichen - {status}")

if __name__ == "__main__":
    analyze_file('/home/daniel/projects/melody-mind-nuxt/content/knowledge/es/anos-2010.md')
