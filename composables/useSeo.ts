import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '#imports'

interface SeoOptions {
  pageName: string;
  customTitle?: string;
  customDescription?: string;
  customKeywords?: string;
  imageUrl?: string;
  type?: 'website' | 'article' | 'product';
  noIndex?: boolean;
}

export const useSeo = () => {
  const { t, locale } = useI18n()

  const setupSeo = (options: SeoOptions) => {
    const {
      pageName,
      customTitle,
      customDescription,
      customKeywords,
      imageUrl,
      type = 'website',
      noIndex = false
    } = options

    const title = computed(() => customTitle || t(`meta.${pageName}Title`))
    const description = computed(() => customDescription || t(`meta.${pageName}Description`))
    const keywords = computed(() => customKeywords || t(`meta.${pageName}Keywords`))
    const url = computed(() => window?.location?.origin || '')

    const metaTags = [
      {
        name: 'description',
        content: description
      },
      {
        name: 'keywords',
        content: keywords
      },
      // Open Graph tags
      {
        property: 'og:title',
        content: title
      },
      {
        property: 'og:description',
        content: description
      },
      {
        property: 'og:type',
        content: type
      },
      {
        property: 'og:url',
        content: url
      }
    ]

    // Add image meta tags if provided
    if (imageUrl) {
      metaTags.push(
        {
          property: 'og:image',
          content: imageUrl
        },
        {
          name: 'twitter:image',
          content: imageUrl
        }
      )
    }

    // Add Twitter Card tags
    metaTags.push(
      {
        name: 'twitter:card',
        content: 'summary_large_image'
      },
      {
        name: 'twitter:title',
        content: title
      },
      {
        name: 'twitter:description',
        content: description
      }
    )

    // Add noindex tag if specified
    if (noIndex) {
      metaTags.push({
        name: 'robots',
        content: 'noindex, nofollow'
      })
    }

    useHead({
      title,
      meta: metaTags,
      link: [
        {
          rel: 'canonical',
          href: url
        }
      ],
      htmlAttrs: {
        lang: computed(() => locale.value)
      }
    })
  }

  return {
    setupSeo
  }
}
