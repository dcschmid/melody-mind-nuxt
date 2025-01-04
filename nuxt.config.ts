// https://nuxt.com/docs/api/configuration/nuxt-config
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
  app: {
    pageTransition: { name: "page" },
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
    },
  },
  css: ["~/assets/scss/main.scss"],
  modules: ["nuxt-icon", "@nuxtjs/i18n"],
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
    langDir: "./i18n/locales",
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
