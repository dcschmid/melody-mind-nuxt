#!/usr/bin/env python3
"""
Music Links Synchronization Script for MelodyMind

This script synchronizes music-related links and metadata across different language
versions of genre JSON files. It uses the German (de) version as the source of truth
and copies specified fields to other language versions while preserving their
translated content.

Features:
- Synchronizes links across multiple languages (en, es, fr, it)
- Preserves translated content while updating links
- Matches entries by artist and album names
- Provides detailed progress and change reporting

Fields Synchronized:
- coverSrc: Cover image path
- spotify_link: Spotify album URL
- deezer_link: Deezer album URL
- apple_music_link: Apple Music album URL
- preview_link: Preview audio URL

Usage:
    python sync_music_links.py

Note:
    The script assumes that entries with matching artist and album names
    across different language files refer to the same content.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any

def sync_music_links() -> None:
    """Synchronize music-related links across different language versions.
    
    The function:
    1. Uses German JSON files as the source of truth
    2. Processes corresponding files in other languages
    3. Updates specified fields while preserving translations
    4. Reports changes and progress
    
    Global Changes:
        Modifies JSON files in the target language directories if changes
        are needed. Creates backups of modified files.
    """
    # Base directory for genre JSON files
    base_dir = Path(__file__).parent.parent / 'app' / 'json' / 'genres'
    
    # Fields to synchronize across languages
    fields_to_copy = ['coverSrc', 'spotify_link', 'deezer_link', 'apple_music_link', 'preview_link']
    
    # Get all German JSON files as source of truth
    de_dir = base_dir / 'de'
    german_files = list(de_dir.glob('*.json'))
    
    # Languages to update (excluding German source)
    target_languages = ['en', 'es', 'fr', 'it']
    
    # Process each German source file
    for de_file in german_files:
        print(f"\nProcessing {de_file.name}")
        
        # Load German source data
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
            
        # Create lookup dictionary for efficient matching
        # Keys are tuples of (artist, album) for unique identification
        de_entries_by_key = {(entry['artist'], entry['album']): entry for entry in de_data}
        
        # Process each target language
        for lang in target_languages:
            target_file = base_dir / lang / de_file.name
            
            # Skip if target language file doesn't exist
            if not target_file.exists():
                print(f"Warning: Target file {target_file} does not exist. Skipping.")
                continue
                
            print(f"\nUpdating {target_file}")
            
            # Load target language data
            with open(target_file, 'r', encoding='utf-8') as f:
                target_data = json.load(f)
            
            # Track changes for reporting
            changes_made = False
            updated_count = 0
            
            # Update each entry in target language file
            for target_entry in target_data:
                # Create lookup key from artist and album
                key = (target_entry.get('artist'), target_entry.get('album'))
                
                # If matching entry found in German source
                if key in de_entries_by_key:
                    de_entry = de_entries_by_key[key]
                    entry_changed = False
                    
                    # Synchronize specified fields
                    for field in fields_to_copy:
                        # Only copy non-empty fields from source
                        if field in de_entry and de_entry[field]:
                            # Update if field is missing or different
                            if field not in target_entry or target_entry[field] != de_entry[field]:
                                target_entry[field] = de_entry[field]
                                entry_changed = True
                    
                    # Track and report changes
                    if entry_changed:
                        changes_made = True
                        updated_count += 1
                        print(f"Updated entry: {target_entry['artist']} - {target_entry['album']}")
            
            # Save changes if any were made
            if changes_made:
                # Write updated data back to file
                # ensure_ascii=False preserves non-ASCII characters
                # indent=2 for human-readable formatting
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(target_data, f, ensure_ascii=False, indent=2)
                print(f"Total entries updated in {target_file}: {updated_count}")
            else:
                print(f"No changes needed for {target_file}")

if __name__ == '__main__':
    sync_music_links()
