<template>
  <section
    :aria-labelledby="id"
    :class="[
      'mb-8 w-full max-w-prose last:mb-0 print:my-6 print:break-inside-avoid',
      background
        ? 'rounded-lg p-6 bg-[rgba(var(--surface-color-rgb),0.95)] shadow-md backdrop-blur-sm md:p-6 print:border print:border-black print:bg-transparent'
        : '',
      centered ? 'text-center' : '',
    ]"
    :data-centered="centered"
  >
    <!-- Verbesserte Überschrift mit besserem Kontrast und Abständen -->
    <h2
      :id="id"
      class="mb-6 text-2xl font-bold tracking-tight text-[rgb(var(--text-color-rgb))] md:mb-5 md:text-xl focus-within:rounded-sm focus-within:outline-none focus-within:ring-2 focus-within:ring-[rgb(var(--highlight-color-rgb))] focus-within:ring-offset-2 print:text-black"
    >
      <slot name="title" />
    </h2>
    <!-- Verbesserter Inhaltscontainer mit optimierter Textlesbarkeit -->
    <div
      class="space-y-4 text-base leading-relaxed text-[rgb(var(--text-color-rgb))] print:text-black"
      aria-live="polite"
    >
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  /** Eindeutige ID für die Sektion, wird für aria-labelledby verwendet */
  id: string
  /** Ob die Sektion einen Hintergrund haben soll */
  background?: boolean
  /** Ob der Inhalt zentriert werden soll */
  centered?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  background: false,
  centered: false,
})
</script>

<style>
/* Modern styling using Tailwind's layer directive for proper specificity */
@layer components {
  /* Verbesserte Basis-Styling für Sektionen */
  section[aria-labelledby] {
    @apply relative;
    @apply focus-within:rounded focus-within:outline-none focus-within:ring-2 focus-within:ring-[rgba(var(--highlight-color-rgb),0.7)] focus-within:ring-offset-4;
  }

  /* Verbesserte Link-Styling mit WCAG AAA-konformen Fokuszuständen */
  section[aria-labelledby] a {
    @apply font-medium text-[rgb(var(--primary-color-rgb))] underline decoration-1 decoration-from-font underline-offset-4;
    @apply motion-safe:transition-all motion-safe:duration-300;
    @apply hover:text-[rgb(var(--primary-dark-color-rgb))] hover:decoration-2 hover:underline-offset-4;
    @apply focus-visible:rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgb(var(--highlight-color-rgb))] focus-visible:ring-offset-4;
    @apply print:text-black print:underline;
  }

  /* Verbesserte strong- und emphasis-Elemente */
  section[aria-labelledby] strong,
  section[aria-labelledby] em {
    @apply font-semibold tracking-wide text-[rgb(var(--text-color-rgb))];
    @apply print:font-bold print:text-black;
  }

  /* Verbesserte Absatzabstände */
  section[aria-labelledby] p {
    @apply mb-4 last:mb-0;
  }

  /* Verbesserte Listenstyling */
  section[aria-labelledby] ul,
  section[aria-labelledby] ol {
    @apply my-4 pl-6;
  }

  section[aria-labelledby] li {
    @apply mb-2 last:mb-0;
  }
}

/* Print-Optimierungen */
@media print {
  section[aria-labelledby] {
    @apply my-4 border border-black/80 p-4;
  }

  section[aria-labelledby] h2 {
    @apply mb-4 border-b border-black/80 pb-2 text-black;
  }

  section[aria-labelledby] p,
  section[aria-labelledby] div {
    @apply text-black;
  }
}

/* Verbesserte Optimierungen für hohen Kontrast */
@media (prefers-contrast: more) {
  section[aria-labelledby] {
    @apply border-2 border-black bg-white shadow-none;
  }

  section[aria-labelledby] h2 {
    @apply border-b-2 border-black pb-2 text-black;
  }

  section[aria-labelledby] div {
    @apply text-black;
  }

  section[aria-labelledby] a {
    @apply rounded-sm bg-[rgb(var(--primary-dark-color-rgb))] px-1 py-0.5 text-black underline decoration-2;
    @apply hover:bg-black hover:text-white hover:decoration-white hover:decoration-[0.2em];
    @apply focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white focus-visible:ring-4 focus-visible:ring-black;
  }

  section[aria-labelledby] strong,
  section[aria-labelledby] em {
    @apply border-b border-black font-bold text-black;
  }
}
</style>
