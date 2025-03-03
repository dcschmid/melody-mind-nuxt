import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

// Get the directory name
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Path to the JSON directory
const jsonDir = path.join(__dirname, 'app/json')

// Function to fix a single JSON file
const fixJsonFile = (filePath) => {
  try {
    console.log(`Processing ${filePath}...`)

    // Read the file content
    const fileContent = fs.readFileSync(filePath, 'utf8')

    // Convert JavaScript object notation to valid JSON
    // This uses eval to parse the JS object notation and then stringify it as proper JSON
    const jsonArray = eval(`(${fileContent})`)
    const validJson = JSON.stringify(jsonArray, null, 2)

    // Write the valid JSON back to the file
    fs.writeFileSync(filePath, validJson, 'utf8')

    console.log(`✓ Fixed ${path.basename(filePath)}`)
    return true
  } catch (error) {
    console.error(`✗ Error fixing ${path.basename(filePath)}:`, error)
    return false
  }
}

// Process all language JSON files
const processLanguageFiles = () => {
  const languageFiles = fs
    .readdirSync(jsonDir)
    .filter((file) => file.endsWith('_categories.json'))
    .map((file) => path.join(jsonDir, file))

  console.log(`Found ${languageFiles.length} language files to process.`)

  let successCount = 0

  for (const file of languageFiles) {
    if (fixJsonFile(file)) {
      successCount++
    }
  }

  console.log(`\nSummary: Successfully fixed ${successCount} out of ${languageFiles.length} files.`)
}

// Run the script
processLanguageFiles()
