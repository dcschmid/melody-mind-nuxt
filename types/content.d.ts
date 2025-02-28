import type { ContentDocument } from '~/app/content/schema'

declare module '@nuxt/content' {
  interface ParsedContent extends ContentDocument {}
}

export {}
