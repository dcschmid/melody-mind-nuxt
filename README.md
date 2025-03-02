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
- 📱 Modern and responsive design with Tailwind CSS
- 💫 Progressive Web App (PWA) support
- ♿ WCAG AAA conformity for maximum accessibility

### 🌍 Language Support

Melody Mind is available in multiple languages:

- 🇬🇧 English (en)
- 🇩🇪 German (de)
- 🇫🇷 French (fr)
- 🇮🇹 Italian (it)
- 🇪🇸 Spanish (es)
- 🇳🇱 Dutch (nl)
- 🇵🇹 Portuguese (pt)
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
- **Styling**: Tailwind CSS
- **State**: Vue Composition API with VueUse

### Backend & Database

- **API**: REST with Nuxt Server Routes

## 🛠️ Tools & Optimization

- **i18n**: @nuxtjs/i18n for multilingual support
- **Icons**: nuxt-icon for scalable icons
- **Images**: @nuxt/image with Sharp for optimized images
- **Linting**: ESLint, Prettier, and Python linting tools
- **Accessibility**: WCAG AAA compliance with Tailwind CSS

## 💻 Setup & Installation

### Prerequisites

- **Node.js**: v16 or higher
- **Package Manager**: npm or yarn
- **Python**: 3.8+ (for utility scripts)

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

### 3. Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Configure environment variables as needed
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

## 🛠️ Development Tools

### 🌍 Supported Languages

All development tools support the following languages:

- 🇩🇪 German (de)
- 🇬🇧 English (en)
- 🇪🇸 Spanish (es)
- 🇫🇷 French (fr)
- 🇮🇹 Italian (it)
- 🇳🇱 Dutch (nl)
- 🇵🇹 Portuguese (pt)
- 🇸🇪 Swedish (sv)
- 🇫🇮 Finnish (fi)
- 🇩🇰 Danish (da)

### 📝 Utility Scripts

| Script                     | Purpose                       | Key Features                               |
| -------------------------- | ----------------------------- | ------------------------------------------ |
| `generate_content.py`      | Content generation            | Multi-language, metadata                   |
| `check_covers.sh`          | Cover verification            | File checks, error reporting               |
| `check_preview_links.py`   | Link validation               | Multi-threaded checks, reports             |
| `sync_music_links.py`      | Link synchronization          | Cross-platform sync                        |
| `generate-sitemap-urls.js` | Sitemap generation            | Multi-language URLs                        |
| `generate-thumbhash.ts`    | Image optimization            | Blur hashes, placeholders                  |

#### Script Usage Guide

##### 1. `check_preview_links.py` - Music Preview Link Validator

Validates the accessibility of music preview links across different streaming services (Spotify, Apple Music, Deezer).

```bash
# Check all languages
python scripts/check_preview_links.py

# Check specific languages
python scripts/check_preview_links.py --languages en de fr

# Customize retry behavior
python scripts/check_preview_links.py --retries 5 --retry-delay 2.0

# Specify output report location
python scripts/check_preview_links.py --output-dir ./reports

# Run with increased verbosity
python scripts/check_preview_links.py --verbose

# Limit to specific streaming services
python scripts/check_preview_links.py --services spotify deezer
```

The script generates an HTML report with statistics and detailed error information, including:
- Total links checked per language and service
- Success/failure counts and percentages
- Detailed error listings with HTTP status codes
- Response time statistics
- Recommendations for fixing broken links

##### 2. `sync_music_links.py` - Music Link Synchronizer

Synchronizes music metadata and links across language-specific JSON files, using German (de) as the source of truth.

```bash
# Synchronize links and update files
python scripts/sync_music_links.py

# Check only mode (no changes)
python scripts/sync_music_links.py --check-only

# Specify source language (default is German)
python scripts/sync_music_links.py --source-lang de

# Synchronize specific target languages only
python scripts/sync_music_links.py --target-langs en fr es

# Specify fields to synchronize
python scripts/sync_music_links.py --fields coverSrc preview_link spotify_link

# Generate detailed report
python scripts/sync_music_links.py --report
```

Synchronized fields include: coverSrc, spotify_link, deezer_link, apple_music_link, and preview_link.

Output example:
```
Synchronizing music links from German (de) to other languages...
✓ English (en): 120 entries synchronized
✓ Spanish (es): 120 entries synchronized
✓ French (fr): 120 entries synchronized
...
Total changes: 47 fields updated across 10 languages
```

##### 3. `check_covers.sh` - Cover Image Validator

Verifies the existence of all cover images referenced in genre JSON files across all language directories.

```bash
# Check cover images
./scripts/check_covers.sh

# Check with detailed output
./scripts/check_covers.sh --verbose

# Check specific language directories
./scripts/check_covers.sh --langs de en fr

# Generate HTML report
./scripts/check_covers.sh --html-report

# Fix missing covers by copying from alternatives
./scripts/check_covers.sh --fix-missing
```

The script reports any missing cover images with their source JSON files.

Output example:
```
Checking cover images for all languages...

Language: de (German)
✓ All 120 cover images found

Language: en (English)
❌ Missing: public/images/covers/en/jazz-fusion.jpg
❌ Missing: public/images/covers/en/indie-folk.jpg

Summary:
- Total covers checked: 1200
- Missing covers: 2
- Success rate: 99.8%
```

##### 4. `generate-sitemap-urls.js` - Sitemap URL Generator

Generates a comprehensive list of URLs for the application's sitemap, processing category JSON files for multiple languages.

```bash
# Generate sitemap URLs
node scripts/generate-sitemap-urls.js > app/sitemap-urls.js

# Generate with specific base URL
node scripts/generate-sitemap-urls.js --base-url https://melodymind.app > app/sitemap-urls.js

# Generate for specific languages only
node scripts/generate-sitemap-urls.js --languages en,de,fr > app/sitemap-urls.js

# Generate with custom priority values
node scripts/generate-sitemap-urls.js --home-priority 1.0 --category-priority 0.8 > app/sitemap-urls.js

# Generate with specific change frequency
node scripts/generate-sitemap-urls.js --change-freq weekly > app/sitemap-urls.js
```

The output is a JavaScript module that exports an array of URLs for the Nuxt.js application.

Example output (app/sitemap-urls.js):
```javascript
export default [  
  { loc: '/', lastmod: '2025-03-01', changefreq: 'daily', priority: 1.0 },
  { loc: '/en', lastmod: '2025-03-01', changefreq: 'daily', priority: 0.9 },
  { loc: '/en/rock-music', lastmod: '2025-03-01', changefreq: 'weekly', priority: 0.8 },
  { loc: '/de', lastmod: '2025-03-01', changefreq: 'daily', priority: 0.9 },
  { loc: '/de/rock-musik', lastmod: '2025-03-01', changefreq: 'weekly', priority: 0.8 },
  // ... more URLs for all languages and categories
];
```

##### 5. `generate-thumbhash.ts` - ThumbHash Generator

Generates compact ThumbHash representations for all images in the public directory, providing lightweight placeholders during image loading.

```bash
# Generate ThumbHashes
npm run generate:thumbhash

# Or directly with ts-node
ts-node scripts/generate-thumbhash.ts

# Generate for specific directory only
ts-node scripts/generate-thumbhash.ts --dir public/images/covers

# Generate with specific output path
ts-node scripts/generate-thumbhash.ts --output public/thumbhashes.json

# Generate with specific image size
ts-node scripts/generate-thumbhash.ts --size 100

# Generate with verbose logging
ts-node scripts/generate-thumbhash.ts --verbose

# Skip existing hashes (faster updates)
ts-node scripts/generate-thumbhash.ts --skip-existing
```

ThumbHashes are saved to a JSON file and used by the UnLazy component for blur effects.

Example output (public/thumbhashes.json):
```json
{
  "images/covers/en/rock-music.jpg": "2DQZRpCLiHePeHeKeJd3d4iIiJh3",
  "images/covers/de/rock-musik.jpg": "1DQZRpCLiHePeHeKeJd3d4iIiJh3",
  "images/artists/queen.jpg": "9TQVRoCLiHePeHeKeJd3d4iIiJh3",
  // ... more image paths and their thumbhash values
}
```

##### 6. `generate_content.py` - Content Generator

Generates comprehensive, multilingual content for music categories with SEO-optimized metadata.

```bash
# Generate content for all languages
python scripts/generate_content.py

# Generate content for specific languages
python scripts/generate_content.py --languages en de fr

# Generate content for specific categories only
python scripts/generate_content.py --categories "rock music" "jazz" "1980s"

# Generate with increased verbosity
python scripts/generate_content.py --verbose

# Generate with custom API key
python scripts/generate_content.py --api-key YOUR_ARLI_API_KEY

# Generate with custom output directory
python scripts/generate_content.py --output-dir ./custom/content/path

# Update existing content only (skip if file exists)
python scripts/generate_content.py --update-only

# Force regeneration of all content
python scripts/generate_content.py --force

# Generate with custom section limits
python scripts/generate_content.py --section-limits "Introduction:500,Historical Background:800"
```

The script creates structured markdown files with consistent formatting across all supported languages.

**Language-Specific Examples:**

```bash
# German (de) - Generate content with German-specific style
python scripts/generate_content.py --languages de --style-guide "formal,detailed"

# English (en) - Generate content with specific SEO focus
python scripts/generate_content.py --languages en --seo-focus "high,us-market"

# Spanish (es) - Generate with regional dialect preferences
python scripts/generate_content.py --languages es --dialect "spain"

# French (fr) - Generate with cultural adaptation
python scripts/generate_content.py --languages fr --cultural-adaptation

# Italian (it) - Generate with specific tone
python scripts/generate_content.py --languages it --tone "conversational"

# Dutch (nl) - Generate with specific formatting
python scripts/generate_content.py --languages nl --formatting "extended"

# Portuguese (pt) - Generate with Brazilian Portuguese focus
python scripts/generate_content.py --languages pt --dialect "brazil"

# Swedish (sv) - Generate with simplified language
python scripts/generate_content.py --languages sv --simplify

# Finnish (fi) - Generate with technical focus
python scripts/generate_content.py --languages fi --technical-level "advanced"

# Danish (da) - Generate with casual tone
python scripts/generate_content.py --languages da --tone "casual"
```

**Output Example (English):**

```markdown
---
title: "Rock Music: Evolution, Influence, and Cultural Impact"
description: "Explore the rich history of rock music, from its blues origins to modern variations, influential artists, and cultural significance worldwide."
category: "Rock Music"
image: "/images/covers/en/rock-music.jpg"
createdAt: "2025-03-01T12:00:00.000Z"
updatedAt: "2025-03-01T12:00:00.000Z"
keywords:
  - rock music
  - rock history
  - rock genres
  - rock bands
  - rock evolution
author: "MelodyMind Team"
locale: "en"
spotify_playlist: ""
deezer_playlist: ""
apple_music_playlist: ""
---

## Introduction

Rock music stands as one of the most influential and enduring musical genres of the modern era...

## Historical Background

The roots of rock music can be traced back to the late 1940s and early 1950s when elements of rhythm and blues...

## Musical Characteristics

Rock music is characterized by a strong backbeat, distorted electric guitars...

## Subgenres and Variations

Over decades of evolution, rock music has spawned numerous subgenres...

## Key Figures and Important Works

Countless artists have shaped the landscape of rock music...
```

**Output Example (German):**

```markdown
---
title: "Rock-Musik: Entwicklung, Einfluss und kulturelle Bedeutung"
description: "Entdecken Sie die reiche Geschichte der Rock-Musik, von ihren Blues-Ursprüngen bis zu modernen Variationen, einflussreichen Künstlern und kultureller Bedeutung weltweit."
category: "Rock-Musik"
image: "/images/covers/de/rock-musik.jpg"
createdAt: "2025-03-01T12:00:00.000Z"
updatedAt: "2025-03-01T12:00:00.000Z"
keywords:
  - Rock-Musik
  - Rock-Geschichte
  - Rock-Genres
  - Rockbands
  - Rock-Entwicklung
author: "MelodyMind Team"
locale: "de"
spotify_playlist: ""
deezer_playlist: ""
apple_music_playlist: ""
---

## Einführung

Rock-Musik gilt als eines der einflussreichsten und beständigsten Musikgenres der modernen Ära...

## Historischer Hintergrund

Die Wurzeln der Rock-Musik lassen sich bis in die späten 1940er und frühen 1950er Jahre zurückverfolgen...

## Musikalische Eigenschaften

Rock-Musik zeichnet sich durch einen starken Backbeat und verzerrte E-Gitarren aus...

## Subgenres und Variationen

Im Laufe der jahrzehntelangen Entwicklung hat die Rock-Musik zahlreiche Subgenres hervorgebracht...

## Schlüsselfiguren und wichtige Werke

Unzählige Künstler haben die Landschaft der Rock-Musik geprägt...
```

### 🔧 Code Quality Tools

#### Python Linting and Formatting

The project uses the following Python tools for code quality:

- **Black**: Code formatting with consistent style
- **isort**: Import sorting and organization
- **Flake8**: Style guide enforcement
- **mypy**: Static type checking
- **Ruff**: Fast linting and auto-fixing

Configuration is maintained in:
- `.flake8` - Flake8 configuration
- `.pre-commit-config.yaml` - Pre-commit hooks
- `.vscode/settings.json` - VS Code integration

#### JavaScript/TypeScript Linting

- **ESLint**: Code quality and best practices
- **Prettier**: Code formatting with Tailwind CSS plugin

Configuration is maintained in:
- `eslint.config.mjs` - ESLint configuration
- `.prettierrc` - Prettier configuration

## ♿ Accessibility

Melody Mind is committed to providing an accessible experience for all users. The application follows WCAG AAA conformity standards with these key features:

- **High contrast** between text and background colors
- **Keyboard navigation** with clear focus indicators
- **Semantic HTML** structure with proper ARIA attributes
- **Responsive design** that works on all device sizes
- **Reduced motion** support for users with vestibular disorders
- **Screen reader** compatibility with descriptive text

The migration from SCSS to Tailwind CSS has improved accessibility through:

- Consistent color contrast ratios
- Properly sized interactive elements (min-height: 44px)
- Focus-visible outlines with ring utilities
- Motion-reduction classes (motion-reduce:transition-none)
- Semantic markup with appropriate labels and IDs

## 💻 VS Code Extensions

For the optimal development experience, the following VS Code extensions are recommended:

### Essential Extensions

- **ESLint**: Code quality and linting
- **Prettier**: Code formatting
- **Vue Language Features (Volar)**: Vue 3 support

### Recommended Extensions

- **Tailwind CSS IntelliSense**: Autocomplete for Tailwind classes
- **i18n Ally**: Translation management
- **Iconify IntelliSense**: Icon preview and search
- **Markdown Preview Enhanced**: Documentation preview

These extensions are configured in the `.vscode/extensions.json` file and will be automatically suggested when opening the project in VS Code.

## 📚 License

Melody Mind is licensed under the MIT License. See the LICENSE file for details.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
