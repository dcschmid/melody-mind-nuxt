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

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd melody-mind-nuxt
```

2. Install dependencies:
```bash
# Using npm
npm install

# Using yarn
yarn install
```

3. Create a `.env` file in the root directory with the required environment variables (see `.env.master` for reference)

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

### Categories Translator

The `scripts/translate_categories.py` script automates the translation of category content from English to multiple languages using OpenAI's GPT-4 model. It handles translations for all music categories while preserving the JSON structure and maintaining language-specific nuances.

Supported Languages:
- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Portuguese (pt)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Russian (ru)

Features:
- Smart field handling:
  - Translates content fields: `introSubline` and `text`
  - Intelligent headline handling:
    - Preserves genre names (e.g., 'Chamber Metal', 'Progressive Metal')
    - Keeps decade names (e.g., '1950s', '1960s')
    - Only translates general terms when appropriate
  - Preserves technical fields: `categoryUrl`, `imageUrl`, `slug`, and `isPlayable`
  - Ensures consistency of URLs and identifiers across all languages
- Automatic progress saving:
  - Saves after each category translation
  - Prevents loss of work if interrupted
  - Enables easy resume of interrupted translations
- Smart update mode with enhanced functionality:
  - Detects and adds missing categories in target languages
  - Only translates modified content in existing categories
  - Preserves unchanged translations
  - Reports detailed progress of additions and updates
- Maintains all metadata (URLs, images, etc.)
- Rate limiting to prevent API overload
- Cross-language consistency checking

Requirements:
- Python 3.x
- OpenAI API key
- Python virtual environment (recommended)

Setup:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install openai

# Set OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

Usage:
```bash
# Full translation (translates everything)
python scripts/translate_categories.py

# Smart update mode
python scripts/translate_categories.py --update

# Specify custom input file
python scripts/translate_categories.py --input path/to/en_categories.json
```

Update Mode Features:
- Scans for categories missing in target language files
- Reports number and names of new categories to be added
- Identifies and updates modified categories
- Preserves unchanged translations to maintain consistency
- Maintains technical field integrity:
  - Never modifies URLs or identifiers
  - Ensures cross-language navigation consistency
  - Preserves file and routing structures

Output:
- Creates/updates language-specific JSON files (e.g., `de_categories.json`, `fr_categories.json`)
- Provides detailed progress information:
  - Lists new categories being added
  - Shows which categories are being updated
  - Indicates when existing translations are reused
- Reports success or any errors encountered


### Cover Image Checker

The `scripts/check_covers.sh` script verifies that all cover images referenced in the music database actually exist in the project. It scans all JSON files across all language versions (de, en, es, fr, it) and reports any missing cover images.

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

### Content Generation

The `scripts/generate_content.py` script is used to generate structured content about music categories in multiple languages. It supports the following features:

#### Supported Languages
- Arabic (ar)
- German (de)
- English (en) - Base language
- Spanish (es)
- French (fr)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh)

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
- Asian languages (Chinese, Japanese) are allocated 70% due to their more concise nature
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
