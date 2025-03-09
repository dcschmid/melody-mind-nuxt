/**
 * Composable for adding JSON-LD structured data to pages
 * Improves SEO by providing structured data for search engines
 * Follows WCAG best practices for accessibility
 */
import { useHead } from '#imports'
import type { MaybeRefOrGetter } from 'vue'
import { unref, computed, watch } from 'vue'

/**
 * Type for JSON-LD data with required context field
 */
export interface JsonLd {
  '@context': string | Record<string, string>
  '@type': string | string[]
  [key: string]: unknown
}

/**
 * Adds JSON-LD structured data to the page head
 * @param data - The JSON-LD data to add to the page
 * @returns A computed ref containing the processed JSON-LD data
 */
export function useJsonld(data: MaybeRefOrGetter<Partial<JsonLd>>) {
  const jsonLd = computed(() => {
    const unwrappedData = unref(data)
    if (!unwrappedData) return null

    // Clone the object to avoid modifying the original
    const processedData = { ...unwrappedData } as Partial<JsonLd>

    // Make sure @context is present
    if (!processedData['@context']) {
      processedData['@context'] = 'https://schema.org'
    }

    return processedData as JsonLd
  })

  // Add JSON-LD to page head when it changes
  watch(jsonLd, (value) => {
    if (!value) return

    useHead({
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify(value),
        },
      ],
    })
  }, { immediate: true })

  return jsonLd
}
