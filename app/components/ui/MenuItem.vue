<template>
  <component
    :is="to ? NuxtLink : tag"
    :to="to"
    :href="to ? undefined : href"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noopener noreferrer' : undefined"
    :aria-label="ariaLabel"
    :role="role || (list ? 'listitem' : undefined)"
    class="group bg-opacity-60 relative flex min-h-[56px] w-full items-center gap-4 overflow-hidden rounded-lg border border-white/5 bg-[rgb(var(--surface-color-rgb))] px-4 py-3 font-medium text-[rgb(var(--text-color-rgb))] no-underline shadow-sm backdrop-blur-sm hover:border-[rgb(var(--primary-light-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:pr-3 hover:pl-5 hover:shadow-md focus-visible:outline-[3px] focus-visible:outline-offset-4 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none print:border-gray-300 print:bg-white print:text-black print:shadow-none"
    data-testid="menu-item"
  >
    <!-- Shine Effect mit Pseudo-Element -->
    <span
      class="absolute inset-0 translate-x-[-100%] bg-gradient-to-r from-white/0 via-white/15 to-white/0 group-hover:translate-x-[100%] motion-safe:transition-transform motion-safe:duration-1000 motion-reduce:transition-none"
      aria-hidden="true"
    ></span>

    <!-- Icon Container mit Hintergrundeffekt -->
    <div v-if="icon" class="relative flex-shrink-0">
      <!-- Subtiler Hintergrund-Kreis -->
      <div
        class="absolute inset-0 -z-10 scale-0 transform rounded-full bg-[rgb(var(--primary-color-rgb))]/25 group-hover:scale-110 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
        aria-hidden="true"
      ></div>

      <Icon
        :name="icon"
        size="28"
        class="relative z-10 text-[rgb(var(--primary-color-rgb))] group-hover:text-[rgb(var(--highlight-color-rgb))] motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
        aria-hidden="true"
      />
    </div>

    <!-- Text mit eigener Transition -->
    <div
      class="flex-grow motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
    >
      <slot />
    </div>

    <!-- Pfeil-Icon rechts, wird bei Hover sichtbar -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      class="h-5 w-5 -translate-x-2 text-[rgb(var(--highlight-color-rgb))] opacity-0 group-hover:translate-x-0 group-hover:opacity-100 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
      aria-hidden="true"
    >
      <path
        fill-rule="evenodd"
        d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z"
        clip-rule="evenodd"
      />
    </svg>

    <!-- Für externe Links: Screen Reader Text -->
    <span v-if="external" class="sr-only">{{ externalLinkText }}</span>
  </component>
</template>

<script setup lang="ts">
import { NuxtLink } from '#components'

defineProps({
  icon: {
    type: String,
    default: '',
  },
  to: {
    type: [String, Object],
    default: null,
  },
  href: {
    type: String,
    default: null,
  },
  external: {
    type: Boolean,
    default: false,
  },
  tag: {
    type: String,
    default: 'a',
  },
  list: {
    type: Boolean,
    default: true,
  },
  role: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: '',
  },
  externalLinkText: {
    type: String,
    default: '(öffnet in neuem Tab)',
  },
})
</script>

<style scoped>
/* Enhanced accessibility for high contrast mode */
@media (prefers-contrast: more) {
  :deep(a),
  :deep(button) {
    background-color: black !important;
    color: white !important;
    border: 3px solid white !important;
    outline: 3px solid white !important;
    outline-offset: 3px !important;
    text-decoration: underline !important;
  }

  :deep(a:hover),
  :deep(button:hover) {
    background-color: #333 !important;
  }

  :deep(a:focus-visible),
  :deep(button:focus-visible) {
    outline-width: 4px !important;
    outline-offset: 4px !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5) !important;
  }
}

/* Print optimization */
@media print {
  :deep(a),
  :deep(button) {
    color: black !important;
    background: white !important;
    border: 1px solid #ddd !important;
    box-shadow: none !important;
    text-decoration: underline !important;
  }
}
</style>
