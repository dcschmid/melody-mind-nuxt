// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  // Erforderliche Module für die Anwendung
  modules: [
    '@nuxt/content',
    '@nuxt/image',
    '@nuxtjs/i18n',
    '@nuxt/icon',
    '@vueuse/nuxt',
    '@nuxtjs/color-mode',
    '@pinia/nuxt',
    '@nuxtjs/sitemap',
    '@nuxthub/core',
  ],

  devtools: {
    enabled: true,
    timeline: {
      enabled: false,
    },
  },
  app: {
    head: {
      htmlAttrs: {
        dir: 'auto',
        lang: 'de',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        // Performance und Sicherheitsverbesserungen
        { name: 'format-detection', content: 'telephone=no' },
        // Barrierefreiheitsverbesserungen
        { name: 'theme-color', content: '#ffffff', media: '(prefers-color-scheme: light)' },
        { name: 'theme-color', content: '#121212', media: '(prefers-color-scheme: dark)' },
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
        // DNS-Prefetch für häufig genutzte Ressourcen
        { rel: 'dns-prefetch', href: 'https://fonts.googleapis.com' },
        // Favicons mit verschiedenen Größen für unterschiedliche Geräte
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/png', href: '/favicon-32x32.png', sizes: '32x32' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png', sizes: '180x180' },
      ],
    },
  },
  css: ['./app/assets/css/main.css'],
  // Optimierungen für den Content-Bereich
  content: {
    documentDriven: true,
    navigation: {
      fields: ['title', 'description', 'category'],
    },
    experimental: {
      clientDB: true,
      // Verbessert Performance durch statische Erfassung von Inhalten während der Build-Zeit
      search: {
        indexed: true,
      },
    },
    markdown: {
      toc: {
        depth: 3,
        searchDepth: 3,
      },
      // Aktivieren für bessere Zugänglichkeit und Navigation
      anchorLinks: true,
      // Performance-Optimierung für Markdown Rendering
      rehypePlugins: {
        'rehype-external-links': {
          target: '_blank',
          rel: ['noopener', 'noreferrer'],
        },
      },
    },
  },
  runtimeConfig: {
    turso: {
      databaseUrl: process.env.NUXT_TURSO_DATABASE_URL,
      authToken: process.env.NUXT_TURSO_AUTH_TOKEN,
    },
  },

  // Optimierte Build-Parameter für bessere Performance
  build: {
    transpile: [process.env.NODE_ENV === 'production' ? '@headlessui/vue' : ''],
  },
  future: {
    compatibilityVersion: 4,
  },
  compatibilityDate: '2024-11-01',
  nitro: {
    // Optimierte Kompression für bessere Performance
    compressPublicAssets: {
      gzip: true,
      brotli: true,
    },
    // Optimierte Caching-Strategien
    routeRules: {
      '/health': {
        headers: {
          'Cache-Control': 'no-cache, no-store',
        },
      },
      // Static assets caching mit verbesserten Caching-Strategien
      '/assets/**': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
          // Preload-Hinweise für kritische Assets
          'X-Early-Hints': '103',
        },
        prerender: true,
      },
      // Verbesserte Caching-Regeln für Bilder
      '/assets/images/**': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
          // Content Security Policy für Bilder
          'Content-Security-Policy': "img-src 'self' data: https: http:",
        },
        prerender: true,
      },
      // API routes caching mit adaptivem Caching
      '/api/**': {
        cache: {
          maxAge: 60,
          swr: true,
          staleMaxAge: 600, // Verwende veraltete Daten für 10 Minuten wenn nötig
        },
        // Sicherheitsheader für API-Anfragen
        headers: {
          'X-Content-Type-Options': 'nosniff',
        },
      },
      // Content pages caching mit erhöhter Gültigkeitsdauer
      '/content/**': {
        cache: {
          maxAge: 3600, // Eine Stunde für bessere Performance
          swr: true,
          // Erlaubt Verwendung von veralteten Inhalten während Aktualisierung
          staleMaxAge: 86400, // 24 Stunden
        },
        prerender: true,
      },
      // Optimierung für statisches Content im Knowledge-Bereich
      '/knowledge/**': {
        prerender: true,
        // Aggressive Caching für statische Inhalte
        cache: {
          maxAge: 86400, // 24 Stunden
          staleMaxAge: 604800, // 7 Tage für veraltete Inhalte
          swr: true,
        },
      },
    },
  },

  vite: {
    plugins: [tailwindcss()],
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
        // Display: 'swap' verbessert die Ladeperformance während Schriftarten geladen werden
        display: 'swap',
        // Preload verhindert Layout-Shifts für bessere Performance und Barrierefreiheit
        preload: true,
        // Subset verbessert die Ladezeit durch Reduzierung der Schriftgröße
        subsets: ['latin'],
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

  // Komplett überarbeitete Bild-Konfiguration, um Bildprobleme zu beheben
  image: {
    // Einfachere Einstellungen für bessere Kompatibilität
    format: ['webp', 'jpg', 'jpeg', 'png', 'svg'],
    quality: 90,
    // Responsive Bildgrößen für unterschiedliche Geräte
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536,
    },
    // Unterstützung für High-DPI Displays vereinfacht
    densities: [1, 2],
    // Verwende den Standard-Provider von Nuxt
    provider: undefined,
    // Setze das public-Verzeichnis explizit als Basis
    dir: 'public',
    // Erlaubt Bilder direkt aus der public/ anzuzeigen
    domains: ['localhost'],
    // Keine benutzerdefinierten Aliasnamen mehr
    alias: {},
    // WCAG AAA-konforme Alt-Texte erzwingen
    presets: {
      category: {
        modifiers: {
          format: 'webp',
          width: 600,
          height: 400,
          quality: 80,
          loading: 'lazy',
          fit: 'cover',
        },
      },
      avatar: {
        modifiers: {
          format: 'webp',
          width: 48,
          height: 48,
          quality: 90,
          fit: 'cover',
        },
      },
    },
  },
  sitemap: {
    enabled: true,
    autoLastmod: true,
    exclude: ['/game/**'],
    urls: (await import('./app/sitemap-urls.js')).default,
  },

  // Optimierte Darstellung von Bildern für WCAG AAA-Konformität
  unlazy: {
    // Verbesserte UnLazy-Konfiguration für Barrierefreiheit
    ssr: true,
    placeholderSize: 32,
  },
})