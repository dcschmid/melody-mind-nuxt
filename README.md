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
