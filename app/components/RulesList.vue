<template>
  <ul
    class="mb-6 max-w-prose text-base leading-relaxed text-[rgb(var(--text-color-rgb))] print:text-black"
    :class="[customClass, listClass]"
    role="list"
    :aria-label="title || $t('common.rulesList')"
    aria-describedby="rules-description"
  >
    <span id="rules-description" class="sr-only">{{
      $t('common.rulesListDescription') || 'List of important rules and information'
    }}</span>
    <slot />
  </ul>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  customClass?: string
  /** Bestimmt den Abstand der Listenpunkte. Standardmäßig 'pl-large' */
  listClass?: 'pl-large' | 'pl-medium' | 'pl-small'
}

const props = withDefaults(defineProps<Props>(), {
  listClass: 'pl-large',
})
</script>

<style>
/* Modern styling for list items using Tailwind's layer directive for proper specificity */
@layer components {
  /* Base list item styling with improved accessibility */
  .pl-large > li {
    @apply relative mb-3 text-[rgb(var(--text-color-rgb))];
    @apply -ml-7 pl-7; /* Improved spacing for bullet points */
    @apply before:absolute before:left-0 before:text-lg before:text-[rgb(var(--text-color-rgb))] before:content-['•'];
    @apply before:leading-[1.5] before:tracking-wide; /* Better bullet alignment */

    /* Enhanced focus states for keyboard navigation within list items */
    &:focus-within {
      @apply rounded-sm ring-2 ring-[rgb(var(--highlight-color-rgb))] ring-offset-2 outline-none;
    }
  }

  /* Medium size list variant */
  .pl-medium > li {
    @apply relative mb-2 text-[rgb(var(--text-color-rgb))];
    @apply -ml-6 pl-6; /* Slightly smaller spacing */
    @apply before:absolute before:left-0 before:text-base before:text-[rgb(var(--text-color-rgb))] before:content-['•'];
    @apply before:leading-[1.5] before:tracking-wide;
  }

  /* Small size list variant */
  .pl-small > li {
    @apply relative mb-2 text-[rgb(var(--text-color-rgb))];
    @apply -ml-5 pl-5; /* Smaller spacing */
    @apply before:absolute before:left-0 before:text-sm before:text-[rgb(var(--text-color-rgb))] before:content-['•'];
    @apply before:leading-[1.5] before:tracking-wide;
  }

  /* Improved strong element styling for better readability */
  .pl-large > li strong,
  .pl-medium > li strong,
  .pl-small > li strong {
    @apply font-semibold text-[rgb(var(--text-color-rgb))];
    @apply tracking-wide; /* Improved letter spacing for better readability */
  }

  /* Enhanced link styling with WCAG AAA compliant focus states */
  .pl-large > li a,
  .pl-medium > li a,
  .pl-small > li a {
    @apply font-medium text-[rgb(var(--primary-color-rgb))] underline decoration-1 decoration-from-font underline-offset-4;
    @apply motion-safe:transition-all motion-safe:duration-300;
    @apply hover:text-[rgb(var(--primary-dark-color-rgb))] hover:decoration-2;
    @apply focus-visible:rounded-sm focus-visible:ring-2 focus-visible:ring-[rgb(var(--highlight-color-rgb))] focus-visible:ring-offset-4 focus-visible:outline-none;
    /* Ensure sufficient color contrast ratio (7:1 for AAA) */
  }
}

/* Print mode optimizations */
@media print {
  .pl-large > li,
  .pl-medium > li,
  .pl-small > li {
    @apply text-black;
    @apply before:text-black;

    & strong {
      @apply font-bold text-black;
    }

    & a {
      @apply font-bold text-black underline;
    }
  }
}

/* Enhanced high contrast mode optimizations */
@media (prefers-contrast: more) {
  .pl-large > li,
  .pl-medium > li,
  .pl-small > li {
    @apply text-white;
    @apply before:text-white;

    /* Improved strong element styling for high contrast */
    & strong {
      @apply border-b-2 border-white font-bold text-white; /* Additional visual cue */
    }

    /* Enhanced link styling for high contrast mode */
    & a {
      @apply rounded-sm bg-[rgb(var(--primary-color-rgb))] px-2 py-1 text-white decoration-2;
      @apply hover:bg-[rgb(var(--primary-dark-color-rgb))] hover:decoration-[3px];
      @apply focus-visible:ring-4 focus-visible:ring-white focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-black;
    }
  }
}

/* Screen reader optimizations with ARIA live regions */
.pl-large[aria-live] > li,
.pl-medium[aria-live] > li,
.pl-small[aria-live] > li {
  @apply motion-safe:transition-opacity motion-safe:duration-300;
}
</style>
