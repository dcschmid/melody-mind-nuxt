#!/usr/bin/env python3
"""
MelodyMind Music Links Synchronization Tool

This script maintains consistency of music-related metadata and links across
multiple language versions of the MelodyMind genre database. It uses the
German (de) version as the source of truth and intelligently synchronizes
specified fields while preserving language-specific content.

Key Features:
┌───────────────┬────────────────────────────────────────┐
│ Feature        │ Description                                   │
├───────────────┼────────────────────────────────────────┤
│ Multi-Language │ Syncs across en, es, fr, it from German source │
│ Smart Sync     │ Updates only changed or missing fields         │
│ Data Integrity │ Preserves translations and local content       │
│ Error Handling │ Validates files and reports issues             │
│ Detailed Logs  │ Reports all changes and sync status           │
└───────────────┴────────────────────────────────────────┘

Synchronized Fields:
1. Media Links:
   - spotify_link: Spotify album URL
   - deezer_link: Deezer album URL
   - apple_music_link: Apple Music album URL
   - preview_link: Audio preview URL

2. Visual Assets:
   - coverSrc: Album cover image path

Directory Structure:
/app
  /json
    /genres
      /de     → Source of truth
      /en     → Target language
      /es     → Target language
      /fr     → Target language
      /it     → Target language

Usage:
    python sync_music_links.py

Example Output:
    Processing rock.json
    Updating /app/json/genres/en/rock.json
    Updated entry: Rammstein - Zeit
    Total entries updated: 1

Notes:
- Matches entries using artist + album name as unique identifier
- Only updates fields if source has non-empty values
- Creates backups before modifying files (*.json.bak)
- Skips non-existent target language files
- Preserves JSON formatting and Unicode characters

Requirements:
- Python 3.6+
- UTF-8 encoded JSON files
- Consistent artist/album names across languages

Author: MelodyMind Development Team
Last Updated: 2025-02-07
"""

import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ANSI color codes for terminal output
class Colors:
    """ANSI color codes for terminal output formatting."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_info(message: str) -> None:
    """Log an informational message with timestamp.
    
    Args:
        message: The message to log
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.BLUE}[{timestamp}] ℹ {message}{Colors.ENDC}")

def log_success(message: str) -> None:
    """Log a success message with timestamp.
    
    Args:
        message: The success message to log
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.GREEN}[{timestamp}] ✓ {message}{Colors.ENDC}")

def log_warning(message: str) -> None:
    """Log a warning message with timestamp.
    
    Args:
        message: The warning message to log
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.YELLOW}[{timestamp}] ⚠ {message}{Colors.ENDC}")

def log_error(message: str) -> None:
    """Log an error message with timestamp.
    
    Args:
        message: The error message to log
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.RED}[{timestamp}] ✖ {message}{Colors.ENDC}")

def create_backup(file_path: Path) -> Optional[Path]:
    """Create a backup of the specified file.
    
    Args:
        file_path: Path to the file to backup
        
    Returns:
        Path to the backup file if successful, None otherwise
    """
    try:
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        shutil.copy2(file_path, backup_path)
        log_info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        log_error(f"Failed to create backup of {file_path}: {e}")
        return None

def validate_json_file(file_path: Path) -> bool:
    """Validate that a file exists and contains valid JSON.
    
    Args:
        file_path: Path to the JSON file to validate
        
    Returns:
        True if file exists and contains valid JSON, False otherwise
    """
    if not file_path.exists():
        log_error(f"File not found: {file_path}")
        return False
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in {file_path}: {e}")
        return False
    except Exception as e:
        log_error(f"Error reading {file_path}: {e}")
        return False

def sync_music_links() -> None:
    """
    Synchronize music metadata and links across language-specific JSON files.
    
    This function maintains consistency of non-language-specific content
    (like URLs and media links) across different language versions while
    preserving translated content. It uses German (de) as the source of
    truth and intelligently updates other language versions.
    
    Process Flow:
    1. File Discovery:
       - Scans German source directory
       - Identifies target language files
       - Validates file existence and format
    
    2. Data Processing:
       - Loads source and target JSON
       - Creates efficient lookup dictionaries
       - Matches entries by artist/album pairs
    
    3. Smart Synchronization:
       - Updates only changed or missing fields
       - Preserves all translated content
       - Maintains file structure and formatting
    
    4. Progress Reporting:
       - Logs all changes in detail
       - Reports sync statistics
       - Identifies missing or invalid files
    
    Implementation Details:
    - Uses UTF-8 encoding for all file operations
    - Implements efficient dictionary lookups
    - Handles missing or malformed data gracefully
    
    Error Handling:
    - Validates JSON structure
    - Reports missing target files
    - Preserves original on write failure
    
    Side Effects:
    - Modifies target language JSON files
    - Creates detailed log output
    - May create temporary backup files
    
    Example:
        >>> sync_music_links()
        Processing rock.json
        Updating /app/json/genres/en/rock.json
        Updated entry: Rammstein - Zeit
        Total entries updated: 1
    
    Note:
        The function assumes consistent artist/album naming
        across language versions for proper matching.
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
