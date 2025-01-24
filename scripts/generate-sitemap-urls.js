import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Pfade zu den Kategorie-JSON-Dateien
const languages = ['de', 'en', 'es', 'fr', 'it'];
const jsonDir = join(__dirname, '../app/json');

// Funktion zum Laden der JSON-Dateien
function loadCategories(lang) {
  const filePath = join(jsonDir, `${lang}_categories.json`);
  const fileContent = readFileSync(filePath, 'utf8');
  return JSON.parse(fileContent);
}

// Funktion zum Extrahieren der spielbaren Kategorien
function getPlayableCategories() {
  const deCategories = loadCategories('de');
  return deCategories
    .filter(cat => cat.isPlayable)
    .map(cat => cat.categoryUrl);
}

// Generiere URLs für alle Sprachen
function generateUrls() {
  const playableCategories = getPlayableCategories();
  const urls = playableCategories.flatMap(path => [
    path,
    ...languages.map(lang => `/${lang}${path}`)
  ]);
  
  console.log('export default ' + JSON.stringify(urls, null, 2) + ';');
}

generateUrls();
