import re

def count_section_chars(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by markdown headers (including the first section with metadata)
    sections = re.split(r'(^|\n)##\s+', content)
    
    # Process each section
    for section in sections[1:]:  # Skip the first empty split
        if section.strip():
            # Get the section title (first line)
            lines = section.split('\n')
            title = lines[0].strip()
            # Get the content (rest of the lines)
            content = '\n'.join(lines[1:]).strip()
            # Count characters
            char_count = len(content)
            print(f"'{title}': {char_count} characters")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        count_section_chars(sys.argv[1])
