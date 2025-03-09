<template>
  <article
    :class="[
      'group/card relative w-full overflow-hidden',
      'motion-safe:transition-transform motion-safe:duration-300 motion-reduce:transition-none rounded-xl will-change-transform',
      !isPlayable ? 'cursor-not-allowed opacity-70' : 'cursor-pointer hover:scale-[1.02]',
      'print:shadow-none print:border print:border-gray-300',
    ]"
    :aria-disabled="!isPlayable"
    data-testid="category-card"
  >
    <!-- Spielbare Kategorie mit Link -->
    <NuxtLink
      v-if="isPlayable"
      :to="categoryUrl"
      :class="[
        'block h-full w-full text-inherit no-underline',
        'focus-visible:outline-[3px] focus-visible:outline-[rgb(var(--focus-color-rgb))] focus-visible:outline-offset-4',
        'group/link',
      ]"
      :aria-label="t('gameHome.playCategory', { category: headline })"
      :aria-describedby="`${cardId}-description`"
      @keydown.enter="$emit('select')"
      @keydown.space.prevent="$emit('select')"
    >
      <!-- Das eigentliche Kartencontainer -->
      <div
        class="relative aspect-video h-full w-full overflow-hidden rounded-xl bg-[rgb(var(--surface-color-rgb))] shadow-md motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none group-hover/link:shadow-lg print:bg-white print:shadow-none dark:bg-[rgb(var(--surface-dark-color-rgb,18,18,18))] will-change-transform"
        data-testid="category-card-container"
      >
        <!-- Karten-Inhalt mit Bild und Titel -->
        <div class="h-full w-full">
          <img
            :src="imageUrl"
            :alt="t('gameHome.categoryAlt', { category: headline })"
            loading="lazy"
            width="800"
            height="450"
            class="h-full w-full rounded-xl object-cover print:grayscale motion-safe:transition-transform motion-safe:duration-500 motion-reduce:transition-none group-hover/link:scale-105"
          />

          <!-- Kategorie-Titel mit verbessertem Kontrast -->
          <div
            class="absolute inset-0 z-10 flex items-center justify-center bg-black/85 print:bg-black print:bg-opacity-90"
            style="contain: layout paint;"
          >
            <h2
              :id="`${cardId}-title`"
              class="m-0 p-4 text-center text-base font-semibold leading-tight text-white md:text-lg group-focus-visible/link:text-[rgb(var(--highlight-color-rgb))] group-hover/link:text-[rgb(var(--highlight-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 motion-reduce:transition-none print:text-white dark:text-white"
            >
              {{ headline }}
            </h2>
          </div>
        </div>

        <!-- Hover-Effekt-Überlagerung -->
        <div
          aria-hidden="true"
          class="absolute inset-0 bg-gradient-to-t from-[rgb(var(--primary-color-rgb))]/60 to-[rgb(var(--secondary-color-rgb))]/40 opacity-0 group-hover/link:opacity-100 motion-safe:transition-all motion-safe:duration-500 motion-reduce:hidden print:hidden"
        ></div>
      </div>

      <!-- Beschreibung für Screen Reader -->
      <span :id="`${cardId}-description`" class="sr-only">
        {{ description }}
      </span>
    </NuxtLink>

    <!-- Nicht spielbare Kategorie (ohne Link) -->
    <div
      v-else
      :class="[
        'relative aspect-video h-full w-full overflow-hidden',
        'rounded-xl bg-[rgb(var(--surface-color-rgb))] shadow-md dark:bg-[rgb(var(--surface-dark-color-rgb,18,18,18))]',
        'focus-visible:outline-[3px] focus-visible:outline-[rgb(var(--focus-color-rgb))] focus-visible:outline-offset-4',
        'print:bg-white print:shadow-none print:border print:border-gray-300',
      ]"
      :aria-labelledby="`${cardId}-title-disabled`"
      :aria-describedby="`${cardId}-description-disabled`"
      tabindex="0"
    >
      <!-- Karten-Inhalt mit Bild und Titel -->
      <div class="h-full w-full">
        <UnLazyImage
          :src="imageUrl"
          :alt="t('gameHome.categoryAlt', { category: headline })"
          loading="lazy"
          class="h-full w-full rounded-xl object-cover grayscale print:contrast-125"
          auto-sizes
          :thumbhash="thumbHashUrl"
        />

        <!-- Kategorie-Titel mit verbessertem Kontrast -->
        <div
          class="absolute inset-0 z-10 flex items-center justify-center bg-black/80 backdrop-blur-xs print:bg-black print:bg-opacity-90"
        >
          <h2
            :id="`${cardId}-title-disabled`"
            class="m-0 p-4 text-center text-base font-bold leading-tight text-white/70 md:text-lg print:text-white"
          >
            {{ headline }}
          </h2>
        </div>

        <!-- Sperrhinweis -->
        <div class="absolute inset-0 z-20 flex items-center justify-center">
          <div
            class="flex gap-2 rounded-full border-2 border-[rgb(var(--border-color-rgb))] bg-black/90 px-4 py-2 backdrop-blur-md print:border-black print:bg-white shadow-md"
          >
            <Icon
              name="material-symbols:lock"
              class="text-[rgb(var(--primary-color-rgb))] print:text-black"
              size="20"
              aria-hidden="true"
            />
            <span class="text-sm font-bold text-white print:text-black">{{ t('gameHome.locked') }}</span>
          </div>
        </div>
      </div>

      <!-- Beschreibung für Screen Reader -->
      <span :id="`${cardId}-description-disabled`" class="sr-only">
        {{ t('gameHome.categoryLocked') }}
      </span>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useThumbHash } from '~/composables/useThumbHash'

const { t } = useI18n()

// Eindeutige ID für ARIA-Attribute
const cardId = `category-card-${Math.random().toString(36).substring(2, 9)}`

const props = defineProps({
  headline: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  imageUrl: {
    type: String,
    required: true,
  },
  thumbHash: {
    type: String,
    default: '',
  },
  categoryUrl: {
    type: String,
    required: true,
  },
  isPlayable: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['select'])

// ThumbHash für Bildvorschau
const { getThumbHash } = useThumbHash()
const thumbHashUrl = computed(() => {
  if (!props.thumbHash) return ''
  return getThumbHash(props.imageUrl)
})
</script>

<style scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  article {
    border: 4px solid white !important;
    outline: 3px solid black !important;
    border-radius: 0.5rem !important;
  }

  h2 {
    background-color: black !important;
    color: white !important;
    border: 3px solid white !important;

    font-size: 1.3rem !important;
    line-height: 1.5 !important;
    padding: 1rem !important;
    outline: 1px solid black !important;
    outline-offset: -2px !important;
  }

  img {
    filter: contrast(1.8) !important;
    border: 2px solid white !important;
  }

  [aria-disabled='true'] img {
    filter: grayscale(1) contrast(1.5) !important;
  }

  div[class*='badge'] {
    border: 3px solid white !important;
    background: black !important;
    color: white !important;

    padding: 0.5rem 1rem !important;
    border-radius: 2rem !important;
    box-shadow: 0 0 0 2px black !important;

  }
}

/* Print-Optimierung */
@media print {
  article {
    break-inside: avoid !important;
    margin-bottom: 1rem !important;
    border: 1px solid #000 !important;
  }

  h2 {
    color: black !important;

    font-size: 1.1rem !important;
  }
}
</style>
