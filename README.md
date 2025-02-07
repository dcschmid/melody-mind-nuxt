# 🎵 Melody Mind

Challenge your musical knowledge with Melody Mind, an engaging and addictive music guessing game! Test your ability to recognize songs from short audio clips, compete with players worldwide, and climb the global leaderboard. Built with modern web technologies, Melody Mind offers a sleek, responsive interface and an immersive gaming experience.

## 🎮 How to Play

1. 🤔 Choose from multiple possible answers
2. ⚡ The faster you answer, the more points you earn
3. 🏆 Compare your scores with players worldwide
4. 🔄 Play again to improve your score and climb the leaderboard

## ✨ Features

- 🎯 Interactive music guessing gameplay
- 🏆 Global highscore system
- 📱 Modern and responsive design
- 💫 Progressive Web App (PWA) support

### 🌍 Language Support

Melody Mind is available in multiple languages:

- 🇬🇧 English (en)
- 🇩🇪 German (de)
- 🇫🇷 French (fr)
- 🇮🇹 Italian (it)
- 🇪🇸 Spanish (es)
- 🇳🇱 Dutch (nl)
- 🇵🇱 Polish (pl)
- 🇵🇹 Portuguese (pt)
- 🇷🇺 Russian (ru)
- 🇸🇪 Swedish (sv)
- 🇫🇮 Finnish (fi)
- 🇩🇰 Danish (da)

All languages feature:
- 🎵 Music content in the respective language
- 📝 Localized UI elements
- ✍️ Grammar-checked translations
- 🔍 Language-specific search optimization

## 🛠️ Technology Stack

### Frontend
- **Framework**: Nuxt.js 3
- **Language**: TypeScript
- **Styling**: SASS
- **State**: Vue Composition API with VueUse

### Backend & Database
- **API**: REST with Nuxt Server Routes

### Tools & Optimization
- **i18n**: @nuxtjs/i18n
- **Icons**: nuxt-icon
- **Images**: @nuxt/image with Sharp

## 💻 Setup & Installation

### Prerequisites

- **Node.js**: v16 or higher
- **Package Manager**: npm or yarn
- **Python**: 3.x (for utility scripts)
- **Java**: JRE (for LanguageTool)

### 1. Clone & Setup

```bash
# Clone repository
git clone <repository-url>
cd melody-mind-nuxt

# Install Node.js dependencies
npm install
```

### 2. Python Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Language Models

```bash
# Install spaCy models
python -m spacy download en_core_web_lg
python -m spacy download de_core_news_lg
python -m spacy download fr_core_news_lg
python -m spacy download es_core_news_lg
python -m spacy download it_core_news_lg

# Install NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 4. LanguageTool Setup

```bash
# Download and setup LanguageTool
mkdir languagetool && cd languagetool
wget https://languagetool.org/download/LanguageTool-stable.zip
unzip LanguageTool-stable.zip
mv LanguageTool-*/* . && rm -r LanguageTool-*
cd ..
```

### 5. Environment Configuration

1. Create environment file:
```bash
cp .env.master .env
```

2. Configure variables in `.env`:
```env
OPENAI_API_KEY=your_api_key_here
# Add other environment variables as needed
```

## 💻 Development

### Starting the Application

```bash
# Development server
npm run dev

# Production build
npm run build
npm run start
```

Access the application at `http://localhost:3000`

### Environment Management

```bash
# Activate Python environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Update dependencies
npm update               # Node.js packages
pip install -r requirements.txt --upgrade  # Python packages

# Maintenance
find . -type d -name "__pycache__" -exec rm -r {} +  # Clean Python cache
python -m spacy validate  # Verify language models
```

## 🛠️ Development Tools

### 🌍 Supported Languages

All development tools support the following languages:

- 🇩🇪 German (de)
- 🇬🇧 English (en)
- 🇪🇸 Spanish (es)
- 🇫🇷 French (fr)
- 🇮🇹 Italian (it)
- 🇳🇱 Dutch (nl)
- 🇵🇱 Polish (pl)
- 🇵🇹 Portuguese (pt)
- 🇷🇺 Russian (ru)
- 🇸🇪 Swedish (sv)
- 🇫🇮 Finnish (fi)
- 🇩🇰 Danish (da)

### 📋 Script Overview

| Category | Script | Purpose | Key Features |
|----------|---------|----------|------------|
| **Content** | `generate_content.py` | Content generation | Multi-language, metadata |
| **Media** | `check_covers.sh` | Cover verification | File checks, error reporting |
| | `generate-thumbhash.ts` | Image optimization | Thumbnails, blur hashes |
| **Links** | `check_preview_links.py` | Link validation | Multi-threaded checks, reports |
| | `sync_music_links.py` | Link synchronization | Cross-platform sync |
| **SEO** | `generate-sitemap-urls.js` | Sitemap generation | Multi-language URLs |
| **Translation** | `translate_correct_readability.py` | Text translation & correction | Multi-language, grammar check, readability |

### 🔧 Setup & Dependencies

```bash
# Install all dependencies
npm install                    # Node.js packages
pip install -r requirements.txt # Python packages

# Install language models
python -m spacy download en_core_web_lg

# Install external tools
./scripts/install_languagetool.sh
```

### 📄 Translation & Grammar Checking

The `translate_correct_readability.py` script provides comprehensive translation and text quality enhancement:

#### Features
- 🌐 Multi-language translation
- ✅ Grammar correction
- 📋 Style improvements
- 📖 Readability scoring
- 🔄 Format preservation

#### Usage

1. Process a single file:
```bash
# Translate/check Markdown file
python translate_correct_readability.py \
  --file path/to/file.md \
  --type md \
  --target-lang de

# Translate/check JSON file
python translate_correct_readability.py \
  --file path/to/file.json \
  --type json \
  --target-lang fr
```

2. Process entire folders:
```bash
# Process Markdown folder
python translate_correct_readability.py \
  --folder content/blog \
  --type md

# Process JSON folder (categories)
python translate_correct_readability.py \
  --folder locales \
  --type json \
  --content categories

# Process JSON folder (locales)
python translate_correct_readability.py \
  --folder locales \
  --type json \
  --content locales
```

#### Supported Languages
- 🇩🇪 German (de)
- 🇬🇧 English (en)
- 🇫🇷 French (fr)
- 🇪🇸 Spanish (es)
- 🇮🇹 Italian (it)
- 🇳🇱 Dutch (nl)
- 🇵🇱 Polish (pl)
- 🇵🇹 Portuguese (pt)
- 🇷🇺 Russian (ru)
- 🇸🇪 Swedish (sv)
- 🇫🇮 Finnish (fi)
- 🇩🇰 Danish (da)

### 💻 Script Usage

#### Content Management
```bash
# Generate content
python generate_content.py --languages de en fr

# Verify cover images
./check_covers.sh

# Generate image thumbnails
npm run generate-thumbhash
```

#### Link Management
```bash
# Check preview links
python check_preview_links.py --languages de en

# Sync music links
python sync_music_links.py --check-only
```

#### SEO & Translation
```bash
# Generate sitemap
node generate-sitemap-urls.js > app/sitemap-urls.js

# Translate content
python translate_correct_readability.py --source de --target en
```

### ✅ Best Practices

#### Before Running
- 🔍 Verify configurations
- 📁 Backup data if needed
- 🔧 Check dependencies
- ⚡ Activate virtual environment

#### During Execution
- 📊 Monitor progress
- ⚠️ Don't interrupt long processes
- 📝 Check logs regularly

#### After Completion
- ✅ Verify outputs
- 🧹 Clean up temp files
- 📄 Document any issues

### ❗ Troubleshooting

#### Common Issues
1. **Language Issues**
   - Check text length
   - Verify encoding
   - Validate language codes

2. **Link Problems**
   - Check API access
   - Verify network connection
   - Validate URL format

3. **File Issues**
   - Check permissions
   - Verify paths
   - Check disk space

#### Getting Help
```bash
# View script help
python script_name.py --help

# Check logs
cat logs/latest.log
```

### 📝 Script Details

#### Content Generation

##### `generate_content.py`
- **Purpose**: Generates and updates site content
- **Features**:
  - Multi-language content generation
  - Category and subcategory management
  - Automatic metadata generation
- **Supported Languages**:
  - German (de)
  - English (en)
  - Spanish (es)
  - French (fr)
  - Italian (it)
  - Dutch (nl)
  - Polish (pl)
  - Portuguese (pt)
  - Russian (ru)
  - Swedish (sv)
  - Finnish (fi)
  - Danish (da)
- **Usage**: `python generate_content.py [--languages LANG1 LANG2]`

#### Validation Scripts

##### `check_preview_links.py`
- **Purpose**: Validates music preview links across streaming services
- **Features**:
  - Multi-threaded link checking
  - Service-specific request handling (Apple Music, Deezer, Spotify)
  - Detailed HTML report generation with statistics and error details
  - Automatic retries with exponential backoff
  - Language filtering options (de, en, es, fr, it, nl, pl, pt, ru, sv, fi, da)
- **Report Contents**:
  - Total links checked and status
  - Service distribution breakdown
  - Detailed error information
  - File locations and content types
- **Usage**: 
  ```bash
  # Check all languages
  python check_preview_links.py
  
  # Check specific languages
  python check_preview_links.py --languages en de fr
  
  # Customize retry behavior
  python check_preview_links.py --retries 5 --retry-delay 2.0
  ```

##### `check_covers.sh`
- **Purpose**: Verifies existence of cover images
- **Features**:
  - Checks all JSON files in language directories
  - Tracks duplicate checks to avoid redundant reporting
  - Clear error reporting with file references
  - Success message when all covers are present
  - Handles special characters in filenames
- **Requirements**:
  - bash shell
  - jq (JSON processor)
- **Example Output**:
  ```bash
  🔍 Searching for missing cover images...
  
  ❌ Missing cover: /bandcover/1950er/artist_album.jpg
     Referenced in: de/50er.json
  
  ✅ All cover images are present!
  ```

#### Media Processing

##### `generate-thumbhash.ts`
- **Purpose**: Generates image thumbnails and blur hashes
- **Features**:
  - Efficient image compression
  - Blur hash generation for loading states
  - Multiple format support
- **Usage**: `npm run generate-thumbhash`

#### SEO Tools

##### `generate-sitemap-urls.js`
- **Purpose**: Generates complete sitemap for all playable categories
- **Features**:
  - Multi-language URL generation (de, en, es, fr, it, nl, pl, pt, ru, sv, fi, da)
  - Dynamic route handling
  - Automatic playable category detection
  - Nuxt sitemap integration
- **Output**: JavaScript module with URLs array
- **Example**:
  ```javascript
  export default [
    "/1950er",
    "/de/1950er",
    "/en/1950er",
    // ... more URLs
  ];
  ```
- **Usage**: `node generate-sitemap-urls.js > app/sitemap-urls.js`

#### Synchronization

##### `sync_music_links.py`
- **Purpose**: Synchronizes music links across platforms
- **Features**:
  - Multi-platform link validation
  - Automatic link updates
  - Detailed progress reporting
  - Preserves other content in target files
  - Supports all languages (de, en, es, fr, it, nl, pl, pt, ru, sv, fi, da)
- **Synchronized Fields**:
  - coverSrc
  - spotify_link
  - deezer_link
  - apple_music_link
  - preview_link
- **Example Output**:
  ```bash
  Processing 50er.json
  
  Updating /app/json/genres/en/50er.json
  Updated entry: Miles Davis - Kind of Blue
  Updated entry: Elvis Presley - Elvis Presley
  Total entries updated: 2
  ```
- **Usage**: `python sync_music_links.py [--check-only]`

#### Translation

##### `translate_correct_readability.py`
- **Purpose**: Translates and corrects text content
- **Features**:
  - Offline translation support
  - Grammar checking with LanguageTool
  - Multi-language support
- **Usage**: `python translate_correct_readability.py [--source LANG] [--target LANG]`

### 🔧 Prerequisites

Ensure you have all required dependencies installed:

```bash
# Node.js dependencies
npm install

# Python packages
pip install -r requirements.txt

# Language models
python -m spacy download en_core_web_lg  # and other required models

# External tools
./scripts/install_languagetool.sh  # for translation tools
```


### Common Features & Best Practices

#### Shared Characteristics
- 📔 Comprehensive documentation
- 🔒 Safe, non-destructive operations
- 📈 Progress tracking and logging
- ♻️ Automatic retries and error handling
- 📚 Modular and maintainable code

#### Before Running Scripts
- ✅ Activate virtual environment
- 🔍 Verify configurations
- 📁 Backup important data
- 🔧 Check dependencies

#### During Execution
- 📃 Monitor logs
- ⏳ Watch progress indicators
- ⚠️ Avoid interrupting long processes
- 📄 Check output for errors

#### After Completion
- ✅ Verify output files
- 📄 Check log files
- 🔄 Clean up temporary files
- 📑 Document any issues

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



## Image Optimization

The project uses a combination of `@nuxt/image` and `@unlazy/nuxt` for optimal image loading and presentation. This setup provides:

- 📷 Automatic image optimization
- 📦 WebP conversion
- 📱 Responsive image sizes
- 🌫️ Beautiful blur effects
- 🔄 No content shifts
- ⚡ Server-side rendering

We use ThumbHash for efficient image loading and optimization:

#### Features
- 🖼️ Tiny placeholders (30-100 bytes)
- 🌫️ Blur effects while loading
- ⚡ Pre-generated at build time
- 🔄 Smooth transitions
- 📱 No layout shifts
- 🔍 SEO-friendly

#### Usage
```bash
# Generate ThumbHashes
yarn generate:thumbhash

# Run after:
# - Adding new images
# - Updating images
# - Before building
```

#### Component Usage
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
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  unlazy: {
    ssr: true,          // Server-side rendering
    placeholderSize: 32  // Placeholder size
  }
})
```


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
