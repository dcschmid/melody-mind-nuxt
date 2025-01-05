import json
import os
from pathlib import Path

def sync_music_links():
    # Base directory for genre JSON files
    base_dir = Path(__file__).parent.parent / 'app' / 'json' / 'genres'
    
    # Fields to copy
    fields_to_copy = ['coverSrc', 'spotify_link', 'deezer_link', 'apple_music_link', 'preview_link']
    
    # Get all German JSON files
    de_dir = base_dir / 'de'
    german_files = list(de_dir.glob('*.json'))
    
    # Define target languages
    target_languages = ['en', 'es', 'fr', 'it']
    
    for de_file in german_files:
        print(f"\nProcessing {de_file.name}")
        
        # Load German file
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
            
        # Create a dictionary of German entries by artist and album for faster lookup
        de_entries_by_key = {(entry['artist'], entry['album']): entry for entry in de_data}
        
        # Process each language
        for lang in target_languages:
            target_file = base_dir / lang / de_file.name
            
            if not target_file.exists():
                print(f"Warning: Target file {target_file} does not exist. Skipping.")
                continue
                
            print(f"\nUpdating {target_file}")
            
            # Load target language file
            with open(target_file, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
            
            # Update fields
            changes_made = False
            updated_count = 0
            
            for target_entry in target_data:
                key = (target_entry.get('artist'), target_entry.get('album'))
                if key in de_entries_by_key:
                    de_entry = de_entries_by_key[key]
                    entry_changed = False
                    
                    # Copy fields
                    for field in fields_to_copy:
                        if field in de_entry and de_entry[field]:
                            if field not in target_entry or target_entry[field] != de_entry[field]:
                                target_entry[field] = de_entry[field]
                                entry_changed = True
                                
                    if entry_changed:
                        changes_made = True
                        updated_count += 1
                        print(f"Updated entry: {target_entry['artist']} - {target_entry['album']}")
            
            if changes_made:
                # Save updated target file
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(target_data, f, ensure_ascii=False, indent=2)
                print(f"Total entries updated in {target_file}: {updated_count}")
            else:
                print(f"No changes needed for {target_file}")

if __name__ == '__main__':
    sync_music_links()
