import thumbHashes from '~/data/thumbhashes.json'

export function useThumbHash() {
  function getThumbHash(imageUrl: string): string | undefined {
    // Wenn die URL einen Query-Parameter hat, diesen entfernen
    const cleanUrl = imageUrl.split('?')[0]
    return (thumbHashes as Record<string, string>)[cleanUrl]
  }

  return {
    getThumbHash,
  }
}
