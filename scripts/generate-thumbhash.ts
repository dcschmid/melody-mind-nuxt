import { readFileSync, writeFileSync } from 'fs'
import { join } from 'path'
import sharp from 'sharp'
import { rgbaToThumbHash } from 'thumbhash'
import * as glob from 'glob'

interface ThumbHashMap {
  [key: string]: string
}

async function generateThumbHash(imagePath: string): Promise<string> {
  try {
    // Load and resize image
    const imageBuffer = await sharp(imagePath)
      .resize(100, 100, { fit: 'inside' })
      .toFormat('png')
      .toBuffer()

    // Convert to raw pixel data
    const { data, info } = await sharp(imageBuffer)
      .ensureAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true })

    // Create thumbhash
    const hash = rgbaToThumbHash(
      info.width,
      info.height,
      Array.from(new Uint8Array(data.buffer)) as unknown as number[],
    )

    // Convert to base64
    return Buffer.from(hash).toString('base64')
  } catch (error) {
    console.error(`Error processing ${imagePath}:`, error)
    return ''
  }
}

async function main() {
  try {
    // Find all images
    const publicDir = join(process.cwd(), 'public')
    const imageFiles = glob.sync('**/*.{jpg,jpeg,png,webp,gif}', {
      cwd: publicDir,
      nodir: true,
    })

    const thumbHashes: ThumbHashMap = {}
    let processed = 0

    // Process each image
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

    // Save results
    const outputPath = join(process.cwd(), 'app/data/thumbhashes.json')
    writeFileSync(outputPath, JSON.stringify(thumbHashes, null, 2))
    console.log(`\nThumbHashes generated for ${processed} images and saved to ${outputPath}`)

  } catch (error) {
    console.error('Failed to process images:', error)
  }
}

main()
