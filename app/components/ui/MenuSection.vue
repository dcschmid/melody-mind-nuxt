<template>
  <section
    :aria-labelledby="headingId"
    :class="[
      'bg-gradient-to-br from-[rgb(var(--surface-color-rgb))]/95 to-[rgb(var(--surface-color-light-rgb))]/95 backdrop-blur-sm',
      'rounded-xl border border-[rgb(var(--border-color-rgb))] p-6',
      'shadow-sm hover:shadow-md motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
      'group relative overflow-hidden',
      'print:border print:border-gray-300 print:bg-white print:shadow-none',
    ]"
    data-testid="menu-section"
  >
    <!-- Hintergrund-Highlight-Effekt -->
    <div
      aria-hidden="true"
      class="absolute inset-0 bg-gradient-to-r from-[rgb(var(--primary-color-rgb))]/10 to-transparent opacity-0 group-hover:opacity-100 motion-safe:transition-opacity motion-safe:duration-500 motion-reduce:hidden print:hidden"
    ></div>

    <h2 v-if="title" :id="headingId" class="relative mb-4 flex items-center gap-2">
      <!-- Accent line -->
      <span
        aria-hidden="true"
        class="mr-1 inline-block h-6 w-1.5 rounded-full bg-gradient-to-b from-[rgb(var(--primary-color-rgb))] to-[rgb(var(--primary-light-color-rgb))] shadow-[0_0_12px_rgba(var(--primary-color-rgb),0.6)] print:bg-black print:shadow-none"
      ></span>

      <span
        class="text-sm font-bold tracking-wider text-[rgb(var(--text-color-rgb))] uppercase print:text-black"
        data-testid="menu-section-title"
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
        'space-y-4 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
        'relative z-10', // Ensures content is above the background highlight
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
/* Enhanced accessibility for high contrast mode */
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
    display: none !important; /* Hides the subtle line in high contrast mode */
  }

  /* Enhanced visibility for list elements in high contrast mode */
  div[role='list'] {
    border-top: 1px solid white !important;
    padding-top: 0.5rem !important;
  }
}

/* Enhanced focus visibility for keyboard navigation */
:deep(*:focus-visible) {
  outline: 3px solid rgb(var(--focus-color-rgb)) !important;
  outline-offset: 4px !important;
  border-radius: 4px !important;
  text-decoration: underline !important;
  box-shadow: 0 0 0 3px rgba(var(--focus-color-rgb), 0.4) !important;
}

/* Print optimization */
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
