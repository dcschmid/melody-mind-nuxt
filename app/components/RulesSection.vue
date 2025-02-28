<template>
  <section
    :aria-labelledby="id"
    :class="[
      'mb-8 w-full max-w-prose print:my-6 print:break-inside-avoid last:mb-0',
      background ? 'bg-surface rounded-lg p-6 shadow-md dark:shadow-none print:bg-transparent print:border print:border-black md:p-4 dark:border-white/10' : '',
    ]"
  >
    <h2
      :id="id"
      :class="[
        'text-2xl font-bold leading-tight text-text mb-8 md:text-xl md:mb-4 print:text-black',
        centered ? 'text-center' : ''
      ]"
    >
      <slot name="title"></slot>
    </h2>
    <div
      :class="[
        'text-base leading-relaxed text-text print:text-black',
        centered ? 'text-center' : ''
      ]"
    >
      <slot></slot>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  id: string
  background?: boolean
  centered?: boolean
}

defineProps<Props>()
</script>

<style lang="scss">
/* Spezifische Stile für verschachtelte Elemente, die mit Tailwind schwieriger sind */
.rules-section a {
  @apply text-primary underline underline-offset-2 transition-colors hover:text-primary-dark hover:underline-offset-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:rounded;
  @apply print:text-black print:underline;
  @apply dark:text-primary-light dark:hover:text-primary-lighter;
}

.rules-section strong,
.rules-section em {
  @apply font-semibold text-text dark:text-white print:text-black print:font-bold dark:text-white/90;
}

/* Unterstützung für High Contrast Mode */
@media (prefers-contrast: more) {
  .rules-section {
    @apply border-2 border-high-contrast shadow-none;
  }
  
  .rules-section h2 {
    @apply text-high-contrast;
  }
  
  .rules-section div {
    @apply text-high-contrast;
  }
  
  .rules-section a {
    @apply text-link-high-contrast underline decoration-[0.125em] hover:text-link-hover-high-contrast hover:decoration-[0.2em];
  }
  
  .rules-section strong,
  .rules-section em {
    @apply font-bold text-high-contrast;
  }
}

/* Reduzierte Bewegung */
@media (prefers-reduced-motion: reduce) {
  .rules-section a {
    @apply transition-none;
  }
}
</style>
