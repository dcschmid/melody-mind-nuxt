// https://nuxt.com/docs/api/configuration/nuxt-config
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4,
  },
  compatibilityDate: "2024-11-01",
  devtools: {
    enabled: true,

    timeline: {
      enabled: false,
    },
  },
  css: [
    "~/assets/scss/main.scss",
    "~/assets/css/tailwind.css"
  ],
  app: {
    pageTransition: { name: "page" },
    head: {
      htmlAttrs: {
        dir: "auto",
        lang: "de"
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com'
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: ''
        }
      ]
    }
  },
  runtimeConfig: {
    turso: {
      databaseUrl: process.env.NUXT_TURSO_DATABASE_URL,
      authToken: process.env.NUXT_TURSO_AUTH_TOKEN,
    }
  },
  nitro: {
    routeRules: {
      "/health": {
        headers: {
          "Cache-Control": "no-cache, no-store",
        },
      },
      // Static assets caching
      "/assets/**": {
        headers: {
          "Cache-Control": "public, max-age=31536000, immutable",
        },
      },
      // API routes caching
      "/api/**": {
        cache: {
          maxAge: 60
        }
      },
      // Content pages caching
      "/content/**": {
        cache: {
          maxAge: 120
        }
      },
    },
  },

  modules: [
    "nuxt-icon", 
    "@nuxtjs/i18n", 
    '@nuxt/content', 
    'nuxt-fathom', 
    '@nuxtjs/sitemap', 
    '@nuxtjs/robots', 
    'nuxt-jsonld', 
    '@nuxt/fonts', 
    '@nuxt/image', 
    '@unlazy/nuxt'
  ],
  unlazy: {
    ssr: true,
    placeholderSize: 32
  },
  fonts: {
    families: [
      {
        name: 'Inter',
        weights: [400, 500, 600, 700]
      }
    ]
  },
  content: {
    documentDriven: true,
    navigation: {
      fields: ['title', 'description', 'category']
    },
    experimental: {
      clientDB: true
    },
    markdown: {
      toc: {
        depth: 3,
        searchDepth: 3
      },
      anchorLinks: false
    }
  },
  fathom: {
    siteId: "RKHOWTTO",  
    config: {
      honorDNT: true
    },
  },
  sitemap: {
    enabled: true,
    autoLastmod: true,
    exclude: [
      '/game/**'
    ],
    urls: (await import('./app/sitemap-urls.js')).default
  },
  i18n: {
    strategy: "prefix",
    defaultLocale: "de",
    detectBrowserLanguage: {
      useCookie: true,
      fallbackLocale: "de",
      cookieKey: "melody-mind-locale",
      redirectOn: "root",
    },
    lazy: true,
    langDir: '../app/i18n/locales',
    locales: [
      {
        code: "de",
        name: "Deutsch",
        file: "de.json",
      },
      {
        code: "en",
        name: "English",
        file: "en.json",
      },
      {
        code: "fr",
        name: "Français",
        file: "fr.json",
      },
      {
        code: "es",
        name: "Español",
        file: "es.json",
      },
      {
        code: "pt",
        name: "Português",
        file: "pt.json",
      },
      {
        code: "it",
        name: "Italiano",
        file: "it.json",
      },
      {
        code: "nl",
        name: "Nederlands",
        file: "nl.json",
      },
      {
        code: "sv",
        name: "Svenska",
        file: "sv.json",
      },
      {
        code: "fi",
        name: "Suomi",
        file: "fi.json",
      },
      {
        code: "da",
        name: "Dansk",
        file: "da.json",
      },
    ],
  },
  vite: {
    plugins: [
      tailwindcss(),
    ],
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/assets/scss/_mixins.scss" as *;'
        }
      }
    }
  }
});
