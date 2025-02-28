<template>
  <ul 
    class="pl-large md:pl-medium mb-medium max-w-prose text-base leading-relaxed"
    :class="customClass"
    role="list"
    :aria-label="title || $t('common.rulesList')"
  >
    <slot></slot>
  </ul>
</template>

<script setup lang="ts">
interface Props {
  title?: string;
  customClass?: string;
}

defineProps<Props>();
</script>

<style lang="scss">
/* Stilisierung der verschachtelten Listenelemente über Elternklasse, da Slot-Inhalte 
   nicht direkt mit den regulären scoped-Stilen erreichbar sind */
.pl-large > li {
  @apply relative mb-small text-text;
  @apply before:content-['•'] before:absolute before:-left-6 before:text-md before:text-text;
  
  /* Styling für verschachtelte starke Elemente */
  & strong {
    @apply text-text font-semibold;
  }
  
  /* Hochqualitative Links mit erweiterten Fokus-Zuständen */
  & a {
    @apply text-primary underline underline-offset-2 decoration-1 transition-colors duration-normal;
    @apply hover:text-primary-dark hover:decoration-2;
    @apply focus-visible:outline-[3px] focus-visible:outline-highlight focus-visible:outline-offset-4 focus-visible:rounded;
    @apply motion-reduce:transition-none;
  }
}

/* High Contrast Mode Optimierungen */
@media (prefers-contrast: more) {
  .pl-large > li {
    @apply text-white;
    @apply before:text-white;
    
    & strong {
      @apply text-white font-bold;
    }
    
    & a {
      @apply text-white bg-primary px-1 py-0.5 rounded-sm decoration-2;
      @apply hover:bg-primary-dark hover:decoration-[3px];
    }
  }
}

/* Für Bildschirm-Vorleseprogramme - verbessert die Nutzererfahrung mit ARIA-Live-Regionen */
.pl-large[aria-live] > li {
  @apply transition-opacity duration-300;
}
</style>
