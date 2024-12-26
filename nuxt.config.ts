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
    pageTransition: { name: "page" },
  },
  nitro: {
    preset: 'node-server',
    routeRules: {
      "/health": {
        headers: {
          "Cache-Control": "no-cache, no-store",
        },
      },
    },
  },
  css: ["~/assets/scss/main.scss"],
  modules: ["@nuxt/icon", "@nuxtjs/i18n"],
  runtimeConfig: {
    public: {},
    turso: {
      databaseUrl: process.env.NUXT_TURSO_DATABASE_URL || "",
      authToken: process.env.NUXT_TURSO_AUTH_TOKEN || "",
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
