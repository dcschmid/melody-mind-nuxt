// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  modules: [
    '@nuxt/icon',
    '@nuxtjs/i18n',
    '@nuxtjs/sitemap',
    '@nuxtjs/robots',
    '@nuxt/content',
    'nuxt-fathom',
    'nuxt-jsonld',
    '@nuxt/fonts',
    '@nuxt/image',
    '@unlazy/nuxt',
    '@nuxt/eslint',
  ],
  devtools: {
    enabled: true,

    timeline: {
      enabled: false,
    },
  },
  app: {
    pageTransition: { name: 'page' },
    head: {
      htmlAttrs: {
        dir: 'auto',
        lang: 'de',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
      link: [
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com',
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: '',
        },
      ],
    },
  },
  css: ['./app/assets/css/main.css'],
  content: {
    documentDriven: true,
    navigation: {
      fields: ['title', 'description', 'category'],
    },
    experimental: {
      clientDB: true,
    },
    markdown: {
      toc: {
        depth: 3,
        searchDepth: 3,
      },
      anchorLinks: false,
    },
  },
  runtimeConfig: {
    turso: {
      databaseUrl: process.env.NUXT_TURSO_DATABASE_URL,
      authToken: process.env.NUXT_TURSO_AUTH_TOKEN,
    },
  },
  future: {
    compatibilityVersion: 4,
  },
  compatibilityDate: '2024-11-01',
  nitro: {
    routeRules: {
      '/health': {
        headers: {
          'Cache-Control': 'no-cache, no-store',
        },
      },
      // Static assets caching
      '/assets/**': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
        },
      },
      // API routes caching
      '/api/**': {
        cache: {
          maxAge: 60,
        },
      },
      // Content pages caching
      '/content/**': {
        cache: {
          maxAge: 120,
        },
      },
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  vite: {
    plugins: [tailwindcss()],
  },
  eslint: {
    config: {
      stylistic: true,
    },
    lintOnStart: true,
  },
  fathom: {
    siteId: 'RKHOWTTO',
    config: {
      honorDNT: true,
    },
  },
  fonts: {
    families: [
      {
        name: 'Inter',
        weights: [400, 500, 600, 700],
      },
    ],
  },
  i18n: {
    strategy: 'prefix',
    defaultLocale: 'de',
    detectBrowserLanguage: {
      useCookie: true,
      fallbackLocale: 'de',
      cookieKey: 'melody-mind-locale',
      redirectOn: 'root',
    },
    lazy: true,
    langDir: '../app/i18n/locales',
    locales: [
      {
        code: 'de',
        name: 'Deutsch',
        file: 'de.json',
      },
      {
        code: 'en',
        name: 'English',
        file: 'en.json',
      },
      {
        code: 'fr',
        name: 'Français',
        file: 'fr.json',
      },
      {
        code: 'es',
        name: 'Español',
        file: 'es.json',
      },
      {
        code: 'pt',
        name: 'Português',
        file: 'pt.json',
      },
      {
        code: 'it',
        name: 'Italiano',
        file: 'it.json',
      },
      {
        code: 'nl',
        name: 'Nederlands',
        file: 'nl.json',
      },
      {
        code: 'sv',
        name: 'Svenska',
        file: 'sv.json',
      },
      {
        code: 'fi',
        name: 'Suomi',
        file: 'fi.json',
      },
      {
        code: 'da',
        name: 'Dansk',
        file: 'da.json',
      },
    ],
  },
  sitemap: {
    enabled: true,
    autoLastmod: true,
    exclude: ['/game/**'],
    urls: (await import('./app/sitemap-urls.js')).default,
  },

  unlazy: {
    ssr: true,
    placeholderSize: 32,
  },
})
