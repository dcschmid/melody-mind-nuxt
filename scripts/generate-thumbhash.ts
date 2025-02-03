/**
 * ThumbHash Generator for MelodyMind
 *
 * This script generates ThumbHash representations of all images in the public directory.
 * ThumbHash is a very compact representation of a thumbnail preview of an image,
 * which can be used to show a placeholder while the main image is loading.
 *
 * Features:
 * - Processes all common image formats (jpg, jpeg, png, webp, gif)
 * - Generates compact ThumbHash representations
 * - Maintains aspect ratios while resizing
 * - Saves results in a JSON file for easy lookup
 *
 * Dependencies:
 * - sharp: For image processing
 * - thumbhash: For generating the compact image representation
 * - glob: For file discovery
 *
 * Usage:
 *   ts-node generate-thumbhash.ts
 *
 * Output:
 *   Creates app/data/thumbhashes.json containing a mapping of
 *   image paths to their ThumbHash representations
 */

import { readFileSync, writeFileSync } from 'fs'
import { join } from 'path'
import sharp from 'sharp'
import { rgbaToThumbHash } from 'thumbhash'
import * as glob from 'glob'

/**
 * Interface representing the mapping of image paths to their ThumbHash values.
 * Keys are image paths relative to the public directory (starting with '/'),
 * values are base64-encoded ThumbHash strings.
 */
interface ThumbHashMap {
  [key: string]: string
}

/**
 * Generate a ThumbHash representation for a single image.
 *
 * The process involves:
 * 1. Loading and resizing the image to a maximum of 100x100 pixels
 * 2. Converting to PNG format with alpha channel
 * 3. Extracting raw pixel data
 * 4. Generating the ThumbHash
 * 5. Converting the result to base64
 *
 * @param imagePath - Absolute path to the image file
 * @returns Promise resolving to the base64-encoded ThumbHash,
 *          or empty string if processing fails
 *
 * @example
 * const hash = await generateThumbHash('/path/to/image.jpg')
 * // Returns: 'base64EncodedThumbHash...'
 */
async function generateThumbHash(imagePath: string): Promise<string> {
  try {
    // Load and resize image while maintaining aspect ratio
    const imageBuffer = await sharp(imagePath)
      .resize(100, 100, { fit: 'inside' })
      .toFormat('png')
      .toBuffer()

    // Convert to raw RGBA pixel data for ThumbHash generation
    const { data, info } = await sharp(imageBuffer)
      .ensureAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true })

    // Generate ThumbHash from pixel data
    const hash = rgbaToThumbHash(
      info.width,
      info.height,
      Array.from(new Uint8Array(data.buffer)) as unknown as number[],
    )

    // Convert binary hash to base64 for storage
    return Buffer.from(hash).toString('base64')
  } catch (error) {
    console.error(`Error processing ${imagePath}:`, error)
    return ''
  }
}

/**
 * Main execution function that processes all images and generates ThumbHashes.
 *
 * The function:
 * 1. Discovers all supported image files in the public directory
 * 2. Processes each image to generate its ThumbHash
 * 3. Tracks progress and handles errors for individual files
 * 4. Saves the results to a JSON file
 *
 * Supported image formats:
 * - JPEG (.jpg, .jpeg)
 * - PNG (.png)
 * - WebP (.webp)
 * - GIF (.gif)
 *
 * Error Handling:
 * - Individual file failures are logged but don't stop processing
 * - The script continues even if some images fail
 * - Only successful results are included in the output
 *
 * @returns Promise<void>
 */
async function main(): Promise<void> {
  try {
    // Find all supported image files recursively
    const publicDir = join(process.cwd(), 'public')
    const imageFiles = glob.sync('**/*.{jpg,jpeg,png,webp,gif}', {
      cwd: publicDir,
      nodir: true,
    })

    const thumbHashes: ThumbHashMap = {}
    let processed = 0

    // Process each image and track progress
    for (const file of imageFiles) {
      const imagePath = join(publicDir, file)
      try {
        const hash = await generateThumbHash(imagePath)
        if (hash) {
          thumbHashes['/' + file] = hash
          processed++
          console.log(`Processed ${processed}/${imageFiles.length}: ${file}`)
        }
      } catch (error) {
        console.error(`Failed to process ${file}:`, error)
      }
    }

    // Save results to JSON file
    const outputPath = join(process.cwd(), 'app/data/thumbhashes.json')
    writeFileSync(outputPath, JSON.stringify(thumbHashes, null, 2))
    console.log(`\nThumbHashes generated for ${processed} images and saved to ${outputPath}`)

  } catch (error) {
    console.error('Failed to process images:', error)
  }
}

main()
