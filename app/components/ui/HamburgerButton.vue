<template>
  <Button
    variant="icon"
    :aria-expanded="isActive"
    :aria-label="isActive ? closeLabel : openLabel"
    :class="[
      'relative flex min-h-[56px] min-w-[56px] flex-col items-center justify-center',
      'rounded-full p-3',
      'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
      'focus-visible:outline-[3px] focus-visible:outline-[rgb(var(--focus-color-rgb))] focus-visible:outline-offset-4',
      'group',
      isActive
        ? 'bg-[rgb(var(--surface-active-color-rgb))]'
        : 'bg-[rgb(var(--surface-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:scale-105 active:bg-[rgb(var(--surface-active-color-rgb))]',
    ]"
    data-testid="hamburger-button"
    v-bind="$attrs"
  >
    <!-- Visuell versteckter Text für Screenreader -->
    <span class="sr-only">{{ isActive ? closeLabel : openLabel }}</span>

    <!-- Hamburger-Linien Container - verbessert Touch-Ziel -->
    <div class="relative flex h-7 w-7 flex-col items-center justify-center" aria-hidden="true">
      <!-- Hamburger-Linien -->
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[3px] w-7 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'translate-y-0 rotate-45 bg-[rgb(var(--highlight-color-rgb))]'
            : 'translate-y-[-8px] bg-[rgb(var(--text-color-rgb))] group-hover:bg-[rgb(var(--highlight-color-rgb))]',
        ]"
      />
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[3px] w-7 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'scale-x-0 opacity-0'
            : 'bg-[rgb(var(--text-color-rgb))] opacity-100 group-hover:bg-[rgb(var(--highlight-color-rgb))]',
        ]"
      />
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[3px] w-7 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'translate-y-0 -rotate-45 bg-[rgb(var(--highlight-color-rgb))]'
            : 'translate-y-[8px] bg-[rgb(var(--text-color-rgb))] group-hover:bg-[rgb(var(--highlight-color-rgb))]',
        ]"
      />
    </div>
  </Button>
</template>

<script setup lang="ts">
import Button from './Button.vue'

defineProps({
  isActive: {
    type: Boolean,
    default: false,
  },
  openLabel: {
    type: String,
    default: 'Menü öffnen',
  },
  closeLabel: {
    type: String,
    default: 'Menü schließen',
  },
})
</script>

<style scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  :deep(button) span:not(.sr-only) {
    background-color: white !important;
    height: 4px !important;
    width: 100% !important;
    border: 1px solid black !important;
    outline: 2px solid white !important;
  }

  :deep(button) {
    outline: 4px solid white !important;
    outline-offset: 6px !important;
    background-color: black !important;
    border: 3px solid white !important;
    text-decoration: underline !important;
    text-decoration-thickness: 2px !important;
    font-weight: bold !important;
  }
}

/* Print-Optimierung */
@media print {
  :deep(button) {
    display: none !important;
  }
}
</style>
