/**
 * Sitemap URL Generator for MelodyMind
 * ===================================
 *
 * This script generates a comprehensive list of URLs for the MelodyMind application's sitemap.
 * It processes category JSON files for multiple languages and creates URLs for all
 * playable music categories. The output is formatted as a JavaScript module that
 * exports an array of URLs.
 *
 * Features:
 * - Multi-language support (de, en, es, fr, it)
 * - Intelligent filtering for playable categories only
 * - Generates both root and language-specific paths
 * - Outputs formatted JavaScript module code
 *
 * Dependencies:
 * - Node.js built-in modules: fs, path, url
 * - JSON category files in ../app/json/ directory
 *   Format: {lang}_categories.json (e.g., de_categories.json)
 *
 * Input Files:
 * - Language-specific category files in JSON format
 * - Each file contains an array of category objects with properties:
 *   - categoryUrl: string (e.g., '/rock-music')
 *   - isPlayable: boolean
 *   - [other metadata]
 *
 * Output:
 * - JavaScript module (../app/sitemap-urls.js)
 * - Exports an array of strings (URLs)
 * - Format: export default ['/', '/en', '/de', ...];
 *
 * Workflow:
 * 1. Loads German (de) category file as source of truth
 * 2. Filters for playable categories
 * 3. Generates root URLs and language variants
 * 4. Outputs formatted JavaScript module
 *
 * Usage:
 *   node generate-sitemap-urls.js > ../app/sitemap-urls.js
 *
 * Note: The German category file is used as the source of truth for
 * determining which categories are playable. This ensures consistency
 * across all language variants.
 */

import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

// Set up ES module compatible __dirname
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Configuration
/** @type {string[]} Supported language codes */
const languages = ['de', 'en', 'es', 'fr', 'it']
/** @type {string} Directory containing category JSON files */
const jsonDir = join(__dirname, '../app/json')

/**
 * Load and parse category data from a language-specific JSON file.
 *
 * @param {string} lang - ISO 639-1 language code (e.g., 'en', 'de')
 * @returns {Array<Object>} Array of category objects containing metadata
 * @throws {Error} If the JSON file cannot be read or parsed
 */
function loadCategories(lang) {
  const filePath = join(jsonDir, `${lang}_categories.json`)
  const fileContent = readFileSync(filePath, 'utf8')
  return JSON.parse(fileContent)
}

/**
 * Extract URLs of playable categories from the German category file.
 *
 * Uses the German (de) category file as the source of truth for
 * determining which categories are playable. Only categories with
 * isPlayable=true are included in the sitemap.
 *
 * @returns {string[]} Array of category URLs for playable categories
 */
function getPlayableCategories() {
  const deCategories = loadCategories('de')
  return deCategories.filter((cat) => cat.isPlayable).map((cat) => cat.categoryUrl)
}

/**
 * Generate and output the complete list of sitemap URLs.
 *
 * For each playable category, generates:
 * - A root URL (e.g., /rock-music)
 * - Language-specific URLs (e.g., /en/rock-music, /de/rock-music)
 *
 * The output is formatted as a JavaScript module that exports an array
 * of URLs. This can be directly used by the Nuxt.js application for
 * sitemap generation.
 *
 * @returns {void} Outputs JavaScript code to stdout
 */
function generateUrls() {
  const playableCategories = getPlayableCategories()
  const urls = playableCategories.flatMap((path) => [
    path,
    ...languages.map((lang) => `/${lang}${path}`),
  ])

  console.log('export default ' + JSON.stringify(urls, null, 2) + ';')
}

generateUrls()
