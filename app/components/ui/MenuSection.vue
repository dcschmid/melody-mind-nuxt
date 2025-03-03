<template>
  <section
    :aria-labelledby="headingId"
    :class="[
      'bg-gradient-to-br from-[rgb(var(--surface-color-rgb))]/90 to-[rgb(var(--surface-color-light-rgb))]/90 backdrop-blur-sm',
      'rounded-xl border border-[rgb(var(--border-color-rgb))] p-6',
      'shadow-lg hover:shadow-xl motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
      'group relative overflow-hidden',
      'print:border print:border-gray-300 print:bg-white print:shadow-none',
    ]"
  >
    <!-- Hintergrund-Highlight-Effekt -->
    <div
      aria-hidden="true"
      class="absolute inset-0 bg-gradient-to-r from-[rgb(var(--primary-color-rgb))]/5 to-transparent opacity-0 group-hover:opacity-100 motion-safe:transition-opacity motion-safe:duration-500 motion-reduce:hidden print:hidden"
    ></div>

    <h2 v-if="title" :id="headingId" class="relative mb-4 flex items-center gap-2">
      <!-- Accent line -->
      <span 
        aria-hidden="true"
        class="mr-1 inline-block h-6 w-1.5 rounded-full bg-gradient-to-b from-[rgb(var(--primary-color-rgb))] to-[rgb(var(--primary-light-color-rgb))] shadow-[0_0_10px_rgba(var(--primary-color-rgb),0.5)] print:bg-black print:shadow-none"
      ></span>

      <span
        class="text-sm font-bold tracking-wider text-[rgb(var(--text-color-rgb))] uppercase print:text-black"
      >
        {{ title }}
      </span>

      <!-- Subtle line -->
      <span
        aria-hidden="true"
        class="ml-2 h-px flex-grow bg-gradient-to-r from-[rgb(var(--border-color-rgb))] to-transparent print:from-gray-300 print:to-white"
      ></span>
    </h2>

    <div
      :class="[
        'space-y-3 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
        'relative z-10', // Stellt sicher, dass der Inhalt über dem Hintergrund-Highlight liegt
      ]"
      :role="list ? 'list' : undefined"
      :aria-label="listLabel || title"
    >
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  // Indicates if the section contains a list
  list: {
    type: Boolean,
    default: true,
  },
  // Optional custom label for the list
  listLabel: {
    type: String,
    default: '',
  },
})

// Generate a unique ID for the heading
const headingId = computed(() => {
  return props.title ? `section-heading-${props.title.toLowerCase().replace(/\s+/g, '-')}` : ''
})
</script>

<style scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  section {
    background: black !important;
    border: 3px solid white !important;
    box-shadow: none !important;
    padding: 1.5rem !important;
  }

  h2 {
    color: white !important;
    border-bottom: 2px solid white !important;
    margin-bottom: 1.5rem !important;
    padding-bottom: 0.5rem !important;
    width: 100% !important;
  }

  h2 span:first-child {
    background: white !important;
    width: 8px !important;
    height: 24px !important;
    margin-right: 8px !important;
  }

  h2 span:last-child {
    display: none !important; /* Versteckt die subtile Linie im High-Contrast-Modus */
  }

  /* Verbesserte Sichtbarkeit für Listenelemente im High-Contrast-Modus */
  div[role='list'] {
    border-top: 1px solid white !important;
    padding-top: 0.5rem !important;
  }
}

/* Verbesserte Fokus-Sichtbarkeit für Tastaturnavigation */
:deep(*:focus-visible) {
  outline: 3px solid rgb(var(--focus-color-rgb)) !important;
  outline-offset: 3px !important;
  border-radius: 4px !important;
}

/* Print-Optimierung */
@media print {
  section {
    background: white !important;
    border: 1px solid #ddd !important;
    box-shadow: none !important;
    break-inside: avoid !important;
    margin-bottom: 1rem !important;
  }

  h2 {
    color: black !important;
    font-weight: bold !important;
    border-bottom: 1px solid #ddd !important;
  }

  div[role='list'] {
    padding-top: 0.5rem !important;
  }
}
</style>
