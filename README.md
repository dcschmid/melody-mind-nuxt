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
