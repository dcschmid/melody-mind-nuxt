import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

// Get the directory name
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Path to the JSON file
const jsonFilePath = path.join(__dirname, 'app/json/de_categories.json')

try {
  // Read the file content
  const fileContent = fs.readFileSync(jsonFilePath, 'utf8')

  // Convert JavaScript object notation to valid JSON
  // This uses eval to parse the JS object notation and then stringify it as proper JSON
  const jsonArray = eval(`(${fileContent})`)
  const validJson = JSON.stringify(jsonArray, null, 2)

  // Write the valid JSON back to the file
  fs.writeFileSync(jsonFilePath, validJson, 'utf8')

  console.info('JSON file successfully fixed!')
} catch (error) {
  console.error('Error fixing JSON file:', error)
}
