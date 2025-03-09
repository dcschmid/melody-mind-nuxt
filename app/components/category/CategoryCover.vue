<template>
  <div
    class="relative mx-auto w-full max-w-[clamp(17.5rem,35vw,25rem)]"
    :aria-labelledby="headlineId"
  >
    <h2 :id="headlineId" class="sr-only">
      {{ headline }}
    </h2>
    <div
      class="relative aspect-square w-full overflow-hidden rounded-xl shadow-md transition-all duration-300 focus-within:outline-3 focus-within:outline-offset-4 focus-within:outline-[rgb(130,87,229)] motion-safe:hover:-translate-y-0.5 motion-safe:hover:shadow-lg motion-reduce:transition-none print:border print:border-gray-300 print:shadow-none"
      role="img"
      :aria-label="imageAltText"
    >
      <img
        v-if="imageUrl"
        class="h-full w-full rounded-xl bg-[rgb(20,20,20)] object-cover"
        :src="imageUrl"
        :alt="imageAltText"
        width="280"
        height="280"
        loading="lazy"
      />
      <div
        v-else
        class="flex h-full w-full items-center justify-center rounded-xl bg-[rgb(20,20,20)] p-4 text-center text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-[1.6] font-medium text-white"
        role="img"
        :aria-label="t('category.noImage')"
      >
        {{ t('category.noImage') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
// Verwenden von i18n für Übersetzungen
const { t } = useI18n()

const props = defineProps<{
  imageUrl: string
  headline: string
}>()

const headlineId = computed(() => `category-${props.headline.toLowerCase().replace(/\s+/g, '-')}`)

const imageAltText = computed(() =>
  t('category.image.altText', {
    category: props.headline,
  })
)
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  [role='img'] {
    outline: 2px solid currentColor !important;
    outline-offset: 2px !important;
  }
}
</style>
