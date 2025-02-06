# Melody Mind

Challenge your musical knowledge with Melody Mind, an engaging and addictive music guessing game! Test your ability to recognize songs from short audio clips, compete with players worldwide, and climb the global leaderboard. Built with modern web technologies, Melody Mind offers a sleek, responsive interface and an immersive gaming experience.

## How to Play

1. 🤔 Choose from multiple possible answers
2. ⚡ The faster you answer, the more points you earn
3. 🏆 Compare your scores with players worldwide
4. 🔄 Play again to improve your score and climb the leaderboard

## Features

- Interactive music guessing gameplay
- Multi-language support (English, French, Italian, Spanish, German)
- Global highscore system
- Modern and responsive design
- Progressive Web App (PWA) support

## Technology Stack

- **Frontend Framework**: Nuxt.js 3
- **Language**: TypeScript
- **Styling**: SASS
- **Database**: LibSQL
- **Internationalization**: @nuxtjs/i18n
- **Icons**: nuxt-icon
- **State Management**: Vue Composition API with VueUse
- **Image Optimization**: @nuxt/image with Sharp

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager
- Python 3.x (for utility scripts)
- Java Runtime Environment (JRE) for LanguageTool

## Installation

### 1. Clone the repository:
```bash
git clone <repository-url>
cd melody-mind-nuxt
```

### 2. Set up Python environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install required spaCy language models
python -m spacy download de_core_news_lg
python -m spacy download en_core_web_lg
python -m spacy download fr_core_news_lg
python -m spacy download es_core_news_lg
python -m spacy download it_core_news_lg
python -m spacy download nl_core_news_lg
python -m spacy download pl_core_news_lg
python -m spacy download pt_core_news_lg
python -m spacy download ru_core_news_lg
python -m spacy download sv_core_news_lg
python -m spacy download fi_core_news_lg
python -m spacy download da_core_news_lg

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 3. Install LanguageTool:

```bash
# Create languagetool directory
mkdir languagetool
cd languagetool

# Download and extract LanguageTool
wget https://languagetool.org/download/LanguageTool-stable.zip
unzip LanguageTool-stable.zip
mv LanguageTool-*/* .
rm -r LanguageTool-*
cd ..
```

### 4. Install Node.js dependencies:
```bash
# Using npm
npm install

# Using yarn
yarn install
```

### 5. Environment Setup:

1. Create a `.env` file in the root directory:
```bash
cp .env.master .env
```

2. Update the following variables in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key (for translation scripts)
- Other environment-specific variables

### 6. Verify Installation:

```bash
# Test Python environment
python scripts/translate_correct_readability.py --help

# Test Node.js setup
npm run dev
```

## Environment Management

### Python Virtual Environment

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Deactivate when done
deactivate
```

### Updating Dependencies

```bash
# Update Python packages
pip install -r requirements.txt --upgrade

# Update Node.js packages
npm update  # or yarn upgrade
```

### Maintenance

```bash
# Clean Python cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Update spaCy models
python -m spacy validate
```

## Development

Start the development server:
```bash
# Using npm
npm run dev

# Using yarn
yarn dev
```

The application will be available at `http://localhost:3000`

## Utility Scripts

This section describes the utility scripts used for content management, translation, and maintenance tasks.

### Quick Reference

| Category | Script | Purpose |
|----------|---------|----------|
| **Translation** | `translate_correct_readability.py` | Text translation and grammar correction |
| | `translate_categories.py` | Category content translation with GPT-4 |
| **Content** | `generate_content.py` | Site content generation and updates |
| **Validation** | `check_preview_links.py` | Preview link validation |
| | `check_covers.sh` | Cover image verification |
| **Sync** | `sync_music_links.py` | Music link synchronization |

### Prerequisites

Make sure you have installed all dependencies:

```bash
# Python packages
pip install -r requirements.txt

# Language models
python -m spacy download en_core_web_lg  # and other required models

# External tools
./scripts/install_languagetool.sh  # if not already installed
```

### 1. Text Translation and Correction (`translate_correct_readability.py`)

**Purpose**: Provides automated translation and grammar correction for JSON and Markdown files.

**Key Features**:
- Offline translation via Argos Translate
- Grammar checking with LanguageTool
- Multi-language support (de, en, fr, es, pt, it, nl, sv, fi, da)
- Smart field handling for JSON files

**Usage**:
```bash
# For JSON files
python scripts/translate_correct_readability.py path/to/folder --type json

# For Markdown files
python scripts/translate_correct_readability.py path/to/folder --type md
```

**Configuration**:
- Protected fields: `categoryUrl`, `imageUrl`, `slug`, `knowledgeUrl`, `isPlayable`
- File naming: Use language prefixes (e.g., `de_categories.json`)
- Markdown structure: Place files in language folders (e.g., `/de/article.md`)

### 2. Category Translation (`translate_categories.py`)

**Purpose**: Translates category content using OpenAI's GPT-4 while maintaining structure and metadata.

**Key Features**:
- GPT-4 powered translations
- Smart content handling
- Progress auto-saving
- Update mode for efficient changes

**Usage**:
```bash
# Full translation
python scripts/translate_categories.py

# Update mode
python scripts/translate_categories.py --update

# Custom input
python scripts/translate_categories.py --input path/to/en_categories.json
```

**Supported Languages**: de, en, es, fr, it, pt

### 3. Preview Link Checker (`check_preview_links.py`)

**Purpose**: Validates the availability and correctness of preview links.

**Key Features**:
- Concurrent link checking
- Detailed status reporting
- Error logging

**Usage**:
```bash
python scripts/check_preview_links.py
```

### 4. Music Link Synchronization (`sync_music_links.py`)

**Purpose**: Ensures consistency of music links across different language versions.

**Key Features**:
- Cross-language link validation
- Automatic synchronization
- Error reporting

**Usage**:
```bash
python scripts/sync_music_links.py
```

### 5. Content Generation (`generate_content.py`)

**Purpose**: Generates and updates site content based on templates and data.

**Key Features**:
- Template-based generation
- Multi-language support
- Metadata handling

**Usage**:
```bash
python scripts/generate_content.py
```

### Common Features

All utility scripts share these characteristics:

**Safety**:
- Automatic backup creation
- Non-destructive operations
- Validation before changes

**Usability**:
- Progress indicators
- Detailed logging
- Help documentation

**Reliability**:
- Error handling
- Automatic retries
- Data validation

**Maintenance**:
- Code documentation
- Modular design
- Configuration files

### Best Practices

1. **Before Running Scripts**:
   - Activate virtual environment
   - Verify configuration
   - Backup important data

2. **During Execution**:
   - Monitor logs
   - Check progress indicators
   - Don't interrupt long-running processes

3. **After Completion**:
   - Verify output
   - Check logs for warnings
   - Test affected functionality

### Troubleshooting

**Common Issues**:
1. **Language Detection Fails**:
   - Ensure sufficient text length
   - Check character encoding

2. **Translation Errors**:
   - Verify API keys
   - Check network connection
   - Validate input format

3. **File Permission Issues**:
   - Check directory permissions
   - Verify file ownership

**Getting Help**:
- Check script help: `python script_name.py --help`
- Review logs in `logs/` directory
- Consult documentation

### Additional Scripts

#### Cover Image Verification (`check_covers.sh`)

**Purpose**: Verifies existence of referenced cover images in the music database.

**Key Features**:
- Scans all language versions (de, en, es, fr, it)
- Reports missing cover images
- Validates image references in JSON files

**Usage**:
```bash
./scripts/check_covers.sh
```

Features:
- Checks all language versions simultaneously
- Avoids duplicate reports for the same missing cover
- Shows which JSON file references a missing cover
- Only displays missing covers (no output for existing covers)
- Provides a success message when all covers are present

Requirements:
- bash shell
- jq (JSON processor, install via `brew install jq`)

Usage:
```bash
cd scripts
./check_covers.sh
```

Example output:
```bash
🔍 Searching for missing cover images...

❌ Missing cover: /bandcover/1950er/artist_album.jpg
   Referenced in: de/50er.json

✅ All cover images are present!  # (when no covers are missing)
```

### Music Links Synchronization

The `scripts/sync_music_links.py` script helps maintain consistency across different language versions of the music database. It copies the following fields from the German version to other language versions:
- coverSrc
- spotify_link
- deezer_link
- apple_music_link
- preview_link

Features:
- Synchronizes links across all language versions (en, es, fr, it)
- Matches songs by artist and album name
- Only updates fields that are different or missing
- Shows detailed progress and changes made
- Preserves all other content in target files

Requirements:
- Python 3.x

Usage:
```bash
cd scripts
python3 sync_music_links.py
```

Example output:
```bash
Processing 50er.json

Updating /app/json/genres/en/50er.json
Updated entry: Miles Davis - Kind of Blue
Updated entry: Elvis Presley - Elvis Presley
Total entries updated in /app/json/genres/en/50er.json: 2

No changes needed for /app/json/genres/es/50er.json
```

### Preview Link Checker

The `scripts/check_preview_links.py` script verifies the accessibility of all preview audio links in the music database. It generates a detailed HTML report showing the status of each link across all language versions.

Features:
- Checks preview links across all language versions
- Automatic retries for failed requests with exponential backoff
- Service-specific handling for different streaming platforms (Apple Music, Deezer, Spotify)
- Detailed HTML report with:
  - Summary statistics
  - Service distribution
  - Detailed error information for inaccessible links
  - File locations for problematic entries
- Multi-threaded processing for faster checks
- Language filtering option

Requirements:
- Python 3.x
- `requests` library (`sudo apt install python3-requests` on Ubuntu/Debian)

Usage:
```bash
# Check all languages
python3 scripts/check_preview_links.py

# Check specific languages
python3 scripts/check_preview_links.py --languages en de fr

# Customize retry behavior
python3 scripts/check_preview_links.py --retries 5 --retry-delay 2.0
```

The script generates an HTML report in the `reports` directory with a timestamp in the filename. The report includes:
- Total number of links checked
- Number of accessible and inaccessible links
- Distribution of links by streaming service
- Detailed information about any inaccessible links, including:
  - Artist and album information
  - URL and error details
  - File path where the link was found
  - Content type information
  - Retry attempt details

### Sitemap URLs Generator

The `scripts/generate-sitemap-urls.js` script automatically generates sitemap URLs for all playable categories across all supported languages. It reads the category data from the JSON files and only includes categories marked as playable (`isPlayable: true`).

Features:
- Automatically detects playable categories
- Generates URLs for all supported languages (de, en, es, fr, it)
- Creates a JavaScript module with the generated URLs
- Integrates seamlessly with the Nuxt sitemap configuration

Usage:
```bash
# Generate sitemap URLs
node scripts/generate-sitemap-urls.js > app/sitemap-urls.js
```

The script will create a JavaScript module containing an array of all URLs for playable categories in all supported languages. This module is then automatically used by the Nuxt sitemap configuration to generate the final sitemap.xml.

Example output structure:
```javascript
export default [
  "/1950er",
  "/de/1950er",
  "/en/1950er",
  "/es/1950er",
  "/fr/1950er",
  "/it/1950er",
  // ... more categories
];
```

## Image Optimization

The project uses a combination of `@nuxt/image` and `@unlazy/nuxt` for optimal image loading and presentation. This setup provides:

- Automatic image optimization
- WebP conversion
- Responsive image sizes
- Beautiful blur effects during loading
- No content shifts
- Server-side rendering of placeholders

### ThumbHash Generation

We use ThumbHash to generate tiny placeholders for images that are shown while the actual image is loading. These placeholders are pre-generated during build time to ensure optimal performance.

#### How it works

1. The `generate:thumbhash` script scans all images in the `public` directory
2. For each image, it generates a ThumbHash (a compact representation of the image)
3. The ThumbHashes are stored in `app/data/thumbhashes.json`
4. During runtime, these ThumbHashes are used by the `UnLazyImage` component to show a blurred preview while loading the actual image

#### Usage

To generate ThumbHashes for all images:

```bash
yarn generate:thumbhash
```

Run this command:
- After adding new images
- After updating existing images
- Before building the project

#### Implementation Details

The system consists of three main parts:

1. **Generation Script** (`scripts/generate-thumbhash.ts`):
   - Processes all images in the `public` directory
   - Generates optimized ThumbHashes
   - Saves them to a JSON file

2. **Composable** (`app/composables/useThumbHash.ts`):
   - Provides easy access to ThumbHashes
   - Handles URL normalization

3. **Component Integration**:
   ```vue
   <UnLazyImage 
     :src="imageUrl"
     :alt="imageAlt"
     :thumbhash="getThumbHash(imageUrl)"
     auto-sizes
     loading="lazy"
   />
   ```

#### Configuration

The ThumbHash generation can be configured in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  unlazy: {
    ssr: true,          // Enable server-side rendering of placeholders
    placeholderSize: 32 // Size of the decoded placeholder image
  }
})
```

### Benefits

1. **Better User Experience**:
   - Immediate visual feedback through blur effects
   - Smooth transitions from placeholder to actual image
   - No layout shifts during loading

2. **Performance**:
   - Tiny placeholder sizes (typically < 100 bytes)
   - Pre-generated at build time
   - Optimized image loading

3. **SEO**:
   - Server-side rendered placeholders
   - Proper image attributes
   - Fast loading times

### Technical Details

The ThumbHash generation process:
1. Resizes images to a smaller size (100x100px)
2. Converts them to RGBA format
3. Generates a compact hash representation
4. Converts the hash to base64 for storage

The resulting ThumbHash is typically 30-100 bytes per image, making it efficient to include in the initial page load.

**Usage**:
```bash
python scripts/generate_content.py
```

### Content Generation (`generate_content.py`)

**Purpose**: Generates structured content about music categories in multiple languages.

**Key Features**:

#### Supported Languages
- German (de)
- English (en) - Base language
- Spanish (es)
- French (fr)
- Italian (it)
- Portuguese (pt)

#### Content Structure
The script generates content for different types of music categories:
- **Decades** (1950s to 2010s)
- **Music Genres** (e.g., Rock, Jazz, Metal subgenres)
- **Countries and Regional Genres** (e.g., Brazilian, Irish)
- **Emotional Genres** (e.g., Happy)
- **Seasonal Genres** (e.g., Holiday, Summer Hits)
- **Situational and Activity-Based Genres** (e.g., Party, Road Trip)

Each category includes multiple sections with specified character limits, such as:
- Introduction
- Historical Background
- Musical Characteristics
- Key Figures and Important Works
- Cultural Significance
- and more...

#### Language Adaptation
The script automatically adjusts content length based on language characteristics:
- German text is allocated 110% of the base length

- Other languages have specific adjustments based on their typical text lengths

#### Setup and Installation

The script requires Python 3.x and the Arli AI API. Follow these steps to set up:

1. Create and activate a Python virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install required dependencies:
```bash
pip install requests python-dotenv
```

3. Set up your environment variables by creating a `.env` file in the project root:
```bash
ARLI_API_KEY=your-arli-api-key-here
```

#### Usage

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

2. Run the script:
```bash
python3 scripts/generate_content.py
```

The script will:
- Create necessary directory structure in `content/knowledge`
- Generate SEO-optimized metadata for each category:
  - Engaging, keyword-rich titles (max 60 characters)
  - Compelling meta descriptions (150-160 characters)
  - Relevant keywords and phrases
- Generate comprehensive content for all categories in all supported languages
- Skip existing files to avoid overwriting content
- Show a progress bar and detailed statistics
- Maintain consistent structure while respecting language-specific requirements

#### Output
Generated content is stored as markdown files in the `content/knowledge` directory, organized by language. Each file follows the naming pattern `category-slug.md` (e.g., `rock-n-roll.md`) and includes YAML frontmatter with metadata such as:
- title
- description
- image path
- creation and update dates
- keywords
- author
- locale
- category-specific playlist links
- playability status

## Production

Build the application for production:
```bash
# Using npm
npm run build

# Using yarn
yarn build
```

Preview the production build:
```bash
# Using npm
npm run preview

# Using yarn
yarn preview
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
