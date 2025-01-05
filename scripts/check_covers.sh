#!/bin/bash

# Base paths
GENRES_DIR="../app/json/genres"
BASE_PATH="../public"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it using 'brew install jq'"
    exit 1
fi

# Temporary file for tracking checked covers
TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT

# Function to check a cover image
check_cover() {
    local cover="$1"
    local json_file="$2"
    
    # Skip if cover was already checked
    if grep -q "^${cover}$" "$TEMP_FILE" 2>/dev/null; then
        return
    fi
    
    # Mark cover as checked
    echo "$cover" >> "$TEMP_FILE"
    
    # Check if file exists
    full_path="${BASE_PATH}${cover}"
    if [ ! -f "$full_path" ]; then
        echo "❌ Missing cover: $cover"
        echo "   Referenced in: $json_file"
    fi
}

# Find all JSON files in all language directories
echo "🔍 Searching for missing cover images..."
echo

found_missing=0

for json_file in $(find "$GENRES_DIR" -type f -name "*.json"); do
    # Extract relative path for output
    rel_path=${json_file#"$GENRES_DIR/"}
    
    # Extract all coverSrc paths from JSON file and store temporarily
    jq -r '.[].coverSrc' "$json_file" > "$TEMP_FILE.covers"
    
    # Process each line
    while IFS= read -r cover; do
        # Skip empty lines
        if [ -n "$cover" ]; then
            check_cover "$cover" "$rel_path"
            if [ ! -f "${BASE_PATH}${cover}" ]; then
                found_missing=1
            fi
        fi
    done < "$TEMP_FILE.covers"
    
    # Delete temporary covers file
    rm -f "$TEMP_FILE.covers"
done

# If no missing covers were found
if [ $found_missing -eq 0 ]; then
    echo "✅ All cover images are present!"
fi
