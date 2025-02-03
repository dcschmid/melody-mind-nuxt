#!/bin/bash

#######################################################################
# Cover Image Checker Script for MelodyMind
#
# This script validates the existence of all cover images referenced in
# the genre JSON files across all language directories. It helps ensure
# that all required cover images are present in the public directory.
#
# Features:
# - Checks all JSON files in all language directories
# - Tracks already checked covers to avoid duplicate checks
# - Provides clear error messages with file references
# - Cleans up temporary files automatically
#
# Dependencies:
# - jq: Required for parsing JSON files
# - find: Used for recursive file discovery
#
# Usage:
#   ./check_covers.sh
#
# Exit codes:
#   0: Success (all covers present or check completed)
#   1: Error (jq not installed)
#######################################################################

# Base paths for genre JSON files and public assets
GENRES_DIR="../app/json/genres"
BASE_PATH="../public"

# Check if jq is installed (required for JSON parsing)
# if ! command -v jq &> /dev/null; then
#     echo "Error: jq is not installed. Please install it using 'brew install jq'"
#     exit 1
# fi

# Create temporary file for tracking checked covers
# Uses mktemp for secure temporary file creation
TEMP_FILE=$(mktemp)
# Ensure temporary file is cleaned up on script exit
trap 'rm -f "$TEMP_FILE"' EXIT

# Function to check if a cover image exists and track its status
# 
# Arguments:
#   $1 - Cover image path (relative to BASE_PATH)
#   $2 - JSON file path where the cover is referenced
#
# Global variables used:
#   TEMP_FILE - Path to temporary file tracking checked covers
#   BASE_PATH - Base directory for public assets
#
# Output:
#   Prints error message if cover is missing
#
# Returns:
#   None (status tracked via global variables)
check_cover() {
    local cover="$1"
    local json_file="$2"
    
    # Skip if cover was already checked (prevents duplicate checks)
    if grep -q "^${cover}$" "$TEMP_FILE" 2>/dev/null; then
        return
    fi
    
    # Mark cover as checked for future reference
    echo "$cover" >> "$TEMP_FILE"
    
    # Check if cover file exists in public directory
    full_path="${BASE_PATH}${cover}"
    if [ ! -f "$full_path" ]; then
        echo "❌ Missing cover: $cover"
        echo "   Referenced in: $json_file"
    fi
}

# Main script execution

# Initialize progress indicator
echo "🔍 Searching for missing cover images..."
echo

# Track if any missing covers were found
found_missing=0

# Process all JSON files in all language directories
for json_file in $(find "$GENRES_DIR" -type f -name "*.json"); do
    # Extract relative path for cleaner output
    rel_path=${json_file#"$GENRES_DIR/"}
    
    # Extract all coverSrc paths from current JSON file
    # Uses jq to parse JSON and extract the coverSrc field from each entry
    jq -r '.[].coverSrc' "$json_file" > "$TEMP_FILE.covers"
    
    # Process each cover path from the JSON file
    while IFS= read -r cover; do
        # Skip empty lines (invalid entries)
        if [ -n "$cover" ]; then
            # Check if cover exists and track its status
            check_cover "$cover" "$rel_path"
            if [ ! -f "${BASE_PATH}${cover}" ]; then
                found_missing=1
            fi
        fi
    done < "$TEMP_FILE.covers"
    
    # Clean up temporary file for current JSON
    rm -f "$TEMP_FILE.covers"
done

# Display success message if all covers were found
if [ $found_missing -eq 0 ]; then
    echo "✅ All cover images are present!"
fi
