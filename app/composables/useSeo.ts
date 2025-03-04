/**
 * SEO Management Module
 * This module provides functionality for managing SEO-related meta tags, social media cards,
 * and other head elements in a Nuxt.js application.
 */

import { computed } from 'vue'
import type { ComputedRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '#imports'

/**
 * Configuration options for SEO setup
 */
interface SeoOptions {
  /** The base name of the page used for i18n key lookups */
  pageName: string
  /** Optional custom title override */
  customTitle?: string
  /** Optional custom description override */
  customDescription?: string
  /** Optional custom keywords override */
  customKeywords?: string
  /** Optional URL for social media preview image */
  imageUrl?: string
  /** Content type for Open Graph tags */
  type?: 'website' | 'article' | 'product'
  /** Whether search engines should index this page */
  noIndex?: boolean
  /** Optional canonical URL override */
  canonicalUrl?: string
}

/**
 * Represents a meta tag structure for HTML head
 */
type MetaTag = {
  /** Meta tag name attribute */
  name?: string
  /** Open Graph property attribute */
  property?: string
  /** Meta tag content (can be static or computed) */
  content: string | ComputedRef<string>
}

/**
 * Composable for managing SEO-related functionality
 * @returns Object containing SEO setup function
 */
export const useSeo = () => {
  const { t, locale } = useI18n()

  /**
   * Creates a meta tag object with the specified name/property and content
   * @param nameOrProperty - Object containing either name or property attribute
   * @param content - Content value for the meta tag
   * @returns MetaTag object
   */
  const createMetaTag = (
    nameOrProperty: { name?: string; property?: string },
    content: string | ComputedRef<string>
  ): MetaTag => ({
    ...(nameOrProperty.name ? { name: nameOrProperty.name } : {}),
    ...(nameOrProperty.property ? { property: nameOrProperty.property } : {}),
    content: content,
  })

  /**
   * Creates social media meta tags for Open Graph and Twitter
   * @param title - Computed title for social cards
   * @param description - Computed description for social cards
   * @param imageUrl - Optional image URL for social cards
   * @returns Array of meta tags for social media
   */
  const createSocialMetaTags = (
    title: ComputedRef<string>,
    description: ComputedRef<string>,
    imageUrl?: string
  ): MetaTag[] => {
    const tags: MetaTag[] = [
      createMetaTag({ property: 'og:title' }, title),
      createMetaTag({ property: 'og:description' }, description),
      createMetaTag({ name: 'twitter:title' }, title),
      createMetaTag({ name: 'twitter:description' }, description),
      createMetaTag({ name: 'twitter:card' }, 'summary_large_image'),
    ]

    if (imageUrl) {
      tags.push(
        createMetaTag({ property: 'og:image' }, imageUrl),
        createMetaTag({ name: 'twitter:image' }, imageUrl)
      )
    }

    return tags
  }

  /**
   * Sets up all SEO-related meta tags and head elements for a page
   * @param options - Configuration options for SEO setup
   */
  const setupSeo = (options: SeoOptions) => {
    const {
      pageName,
      customTitle,
      customDescription,
      customKeywords,
      imageUrl,
      type = 'website',
      noIndex = false,
      canonicalUrl,
    } = options

    const title = computed(() => customTitle || t(`meta.${pageName}Title`))
    const description = computed(() => customDescription || t(`meta.${pageName}Description`))
    const keywords = computed(() => customKeywords || t(`meta.${pageName}Keywords`))
    const url = computed(() => canonicalUrl || window?.location?.href || '')

    const baseMetaTags = computed(() => [
      createMetaTag({ name: 'description' }, description.value),
      createMetaTag({ name: 'keywords' }, keywords.value),
      createMetaTag({ property: 'og:type' }, type),
      createMetaTag({ property: 'og:url' }, url.value),
      ...(noIndex ? [createMetaTag({ name: 'robots' }, 'noindex,nofollow')] : []),
      ...createSocialMetaTags(title, description, imageUrl),
    ])

    useHead({
      title: title.value,
      meta: baseMetaTags.value,
      link: [
        {
          rel: 'canonical',
          href: url.value,
        },
        {
          rel: 'alternate',
          hreflang: locale.value,
          href: url.value,
        },
      ],
      htmlAttrs: {
        lang: locale.value,
      },
    })
  }

  return {
    setupSeo,
  }
}
