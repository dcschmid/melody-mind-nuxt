<template>
  <Button
    variant="icon"
    :aria-expanded="isActive"
    :aria-label="isActive ? closeLabel : openLabel"
    :class="[
      'relative flex min-h-[48px] min-w-[48px] flex-col items-center justify-center',
      'rounded-full p-3',
      'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
      'focus-visible:ring-[3px] focus-visible:ring-[rgb(var(--focus-color-rgb))] focus-visible:ring-offset-2',
      'group',
      isActive
        ? 'bg-[rgb(var(--surface-active-color-rgb))]'
        : 'bg-[rgb(var(--surface-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] active:bg-[rgb(var(--surface-active-color-rgb))]',
    ]"
    v-bind="$attrs"
  >
    <!-- Visuell versteckter Text für Screenreader -->
    <span class="sr-only">{{ isActive ? closeLabel : openLabel }}</span>

    <!-- Hamburger-Linien Container - verbessert Touch-Ziel -->
    <div class="relative flex h-6 w-6 flex-col items-center justify-center">
      <!-- Hamburger-Linien -->
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[2px] w-6 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'translate-y-0 rotate-45 bg-[rgb(var(--highlight-color-rgb))]'
            : 'translate-y-[-6px] bg-[rgb(var(--text-color-rgb))] group-hover:bg-[rgb(var(--highlight-color-rgb))]',
        ]"
      />
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[2px] w-6 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'scale-x-0 opacity-0'
            : 'bg-[rgb(var(--text-color-rgb))] opacity-100 group-hover:bg-[rgb(var(--highlight-color-rgb))]',
        ]"
      />
      <span
        aria-hidden="true"
        :class="[
          'absolute block h-[2px] w-6 rounded-full',
          'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
          isActive
            ? 'translate-y-0 -rotate-45 bg-[rgb(var(--highlight-color-rgb))]'
            : 'translate-y-[6px] bg-[rgb(var(--text-color-rgb))] group-hover:bg-[rgb(var(--highlight-color-rgb))]',
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
    height: 3px !important;
    width: 100% !important;
    border: 1px solid black !important;
    outline: 1px solid white !important;
  }

  :deep(button) {
    outline: 3px solid white !important;
    outline-offset: 3px !important;
    background-color: black !important;
    border: 2px solid white !important;
  }
}

/* Print-Optimierung */
@media print {
  :deep(button) {
    display: none !important;
  }
}
</style>
