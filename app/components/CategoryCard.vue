<template>
  <article
    :class="[
      'group/card relative w-full overflow-hidden',
      'motion-safe:transition-transform motion-safe:duration-300 motion-reduce:transition-none rounded-xl',
      !isPlayable ? 'cursor-not-allowed opacity-60' : 'cursor-pointer',
      'print:shadow-none print:border print:border-gray-300',
    ]"
    :aria-disabled="!isPlayable"
  >
    <!-- Spielbare Kategorie mit Link -->
    <NuxtLink
      v-if="isPlayable"
      :to="categoryUrl"
      :class="[
        'block h-full w-full text-inherit no-underline',
        'focus-visible:ring-[3px] focus-visible:ring-[rgb(var(--focus-color-rgb))] focus-visible:ring-offset-2 focus-visible:outline-none',
        'group/link',
      ]"
      :aria-label="t('gameHome.playCategory', { category: headline })"
      :aria-describedby="`${cardId}-description`"
      @keydown.enter="$emit('select')"
      @keydown.space.prevent="$emit('select')"
    >
      <!-- Das eigentliche Kartencontainer -->
      <div
        class="relative aspect-video h-full w-full overflow-hidden rounded-xl bg-[rgb(var(--surface-color-rgb))] shadow-md motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none print:bg-white print:shadow-none"
      >
        <!-- Karten-Inhalt mit Bild und Titel -->
        <div class="h-full w-full">
          <UnLazyImage
            :src="imageUrl"
            :alt="t('gameHome.categoryAlt', { category: headline })"
            loading="lazy"
            class="h-full w-full rounded-xl object-cover print:grayscale"
            auto-sizes
            :thumbhash="thumbHashUrl"
          />

          <!-- Kategorie-Titel mit verbessertem Kontrast -->
          <div
            class="absolute inset-0 z-10 flex items-center justify-center bg-black/80 backdrop-blur-sm print:bg-black print:bg-opacity-90"
          >
            <h2
              :id="`${cardId}-title`"
              class="m-0 p-4 text-center text-base font-semibold leading-tight text-white md:text-lg group-focus-visible/link:text-[rgb(var(--highlight-color-rgb))] print:text-white"
            >
              {{ headline }}
            </h2>
          </div>
        </div>

        <!-- Hover-Effekt-Überlagerung -->
        <div
          aria-hidden="true"
          class="absolute inset-0 bg-gradient-to-t from-[rgb(var(--primary-color-rgb))]/40 to-[rgb(var(--secondary-color-rgb))]/30 opacity-0 group-hover/link:opacity-100 motion-safe:transition-all motion-safe:duration-300 motion-reduce:hidden print:hidden"
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
        'rounded-xl bg-[rgb(var(--surface-color-rgb))] shadow-md',
        'focus-visible:ring-[3px] focus-visible:ring-[rgb(var(--focus-color-rgb))] focus-visible:ring-offset-2 focus-visible:outline-none',
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
          class="absolute inset-0 z-10 flex items-center justify-center bg-black/80 backdrop-blur-sm print:bg-black print:bg-opacity-90"
        >
          <h2
            :id="`${cardId}-title-disabled`"
            class="m-0 p-4 text-center text-base font-semibold leading-tight text-white/80 md:text-lg print:text-white"
          ></h2>
        </div>

        <!-- Sperrhinweis -->
        <div class="absolute inset-0 z-20 flex items-center justify-center">
          <div
            class="flex items-center gap-2 rounded-full border border-[rgb(var(--border-color-rgb))] bg-black/90 px-4 py-2 backdrop-blur-md print:border-black print:bg-white"
          >
            <Icon
              name="material-symbols:lock"
              class="text-[rgb(var(--primary-color-rgb))] print:text-black"
              size="20"
              aria-hidden="true"
            />
            <span class="text-sm font-medium text-white print:text-black">{{ t('gameHome.locked') }}</span>
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
    border: 3px solid white !important;
    outline: 1px solid black !important;
  }

  h2 {
    background-color: black !important;
    color: white !important;
    border: 2px solid white !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
  }

  img {
    filter: contrast(1.5) !important;
    border: 1px solid white !important;
  }

  [aria-disabled='true'] img {
    filter: grayscale(1) contrast(1.2) !important;
  }

  div[class*='badge'] {
    border: 2px solid white !important;
    background: black !important;
    color: white !important;
    font-weight: bold !important;
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
    font-weight: bold !important;
    font-size: 1.1rem !important;
  }
}
</style>
