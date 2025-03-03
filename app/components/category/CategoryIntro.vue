<template>
  <section
    v-if="category"
    class="mx-auto max-w-4xl px-4 text-center print:px-0"
    :aria-labelledby="headlineId"
    role="region"
  >
    <h1
      :id="headlineId"
      class="group mb-6 text-center text-[clamp(2.25rem,3.2vw+1rem,2.75rem)] leading-[1.4] font-bold tracking-[0.025em] text-[rgb(130,87,229)] focus-visible:ring-2 focus-visible:ring-[rgb(130,87,229)] focus-visible:ring-offset-2 focus-visible:outline-none"
    >
      <span
        class="mr-1 inline-block group-hover:text-[#6d46c4] motion-safe:transition-colors motion-safe:duration-300 motion-reduce:transition-none sm:mr-2 md:mr-3"
      >
        {{ category.headline }}
      </span>
      <span
        class="font-semibold text-white max-sm:mt-2 max-sm:block max-sm:text-[0.9em] sm:ml-0 sm:inline-block"
      >
        {{ t('category.selected') }}
      </span>
    </h1>

    <p
      :id="descriptionId"
      class="mx-auto mb-6 max-w-[65ch] text-center text-[clamp(1.5rem,1.7vw+1rem,1.75rem)] leading-[1.8] text-white max-sm:text-[clamp(1.25rem,1.2vw+1rem,1.5rem)]"
      aria-live="polite"
    >
      {{ category.introSubline }}
    </p>

    <div
      v-if="category.description"
      class="mt-6 text-center text-[clamp(1.25rem,1.2vw+1rem,1.5rem)] leading-[1.8] text-[#f0f0f0] contrast-more:text-white"
      :aria-labelledby="descriptionId"
    >
      <p class="mx-auto max-w-[65ch]">
        {{ category.description }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

interface Category {
  headline: string
  introSubline: string
  description?: string
}

const props = defineProps<{
  category: Category | null
}>()

const { t } = useI18n()

const headlineId = computed(() =>
  props.category
    ? `category-${props.category.headline.toLowerCase().replace(/\s+/g, '-')}-title`
    : ''
)

const descriptionId = computed(() =>
  props.category
    ? `category-${props.category.headline.toLowerCase().replace(/\s+/g, '-')}-desc`
    : ''
)
</script>

<style>
/* High contrast mode support */
@media (prefers-contrast: more) {
  h1 {
    text-decoration: underline !important;
    text-underline-offset: 4px !important;
  }

  p {
    color: white !important;
  }
}

/* Print styles */
@media print {
  h1,
  p {
    color: black !important;
  }

  h1 {
    font-size: 18pt !important;
    margin-bottom: 12pt !important;
  }

  p {
    font-size: 12pt !important;
    line-height: 1.5 !important;
  }
}
</style>
