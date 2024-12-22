// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },
  app: {
    pageTransition: { name: 'page' }
  },
  nitro: {
    compressPublicAssets: {
      brotli: true,
      gzip: true
    },
    routeRules: {
      '/**': { 
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable'
        }
      }
    }
  },
  css: ["~/assets/scss/main.scss"],
  modules: ["@nuxt/icon", "@nuxtjs/i18n", "@pinia/nuxt"],
  runtimeConfig: {
    turso: {
      databaseUrl: "",
      authToken: "",
    },
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
        code: "es",
        name: "Español",
        file: "es.json",
      },
      {
        code: "fr",
        name: "Français",
        file: "fr.json",
      },
      {
        code: "it",
        name: "Italiano",
        file: "it.json",
      },
    ],
  },
});