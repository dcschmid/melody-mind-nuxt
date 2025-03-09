<template>
  <a
    href="#main-content"
    class="fixed left-[-9999px] top-4 z-[9999] flex min-h-[48px] min-w-[220px] items-center justify-center rounded-lg border-2 border-[rgb(var(--highlight-color-rgb))] bg-[rgb(var(--surface-color-rgb))] p-3 text-center text-base font-bold leading-normal text-[rgb(var(--text-color-rgb))] no-underline shadow-sm hover:cursor-pointer hover:bg-[rgb(var(--highlight-color-rgb))] hover:text-[rgb(var(--surface-color-rgb))] hover:underline focus:left-1/2 focus:-translate-x-1/2 focus:bg-[rgb(var(--highlight-color-rgb))] focus:text-[rgb(var(--surface-color-rgb))] focus:outline-none focus-visible:ring-4 focus-visible:ring-[rgb(var(--highlight-color-rgb))] focus-visible:ring-offset-2 focus-visible:underline active:translate-y-0.5 active:shadow-xs motion-safe:transition-all motion-safe:duration-300 print:hidden"
    role="link"
    :aria-hidden="!isVisible"
    :aria-label="t('accessibility.skipToMain')"
    data-testid="skip-link"
    @focus="onFocus"
    @blur="onBlur"
    @click.prevent="handleSkip"
    @keydown.enter="handleSkip"
    @keydown.space="handleSkip"
  >
    <span class="sr-only">{{ t('accessibility.skipToMain') }}</span>
    <span aria-hidden="true">{{ t('accessibility.skipToMain') }}</span>
  </a>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

/**
 * SkipLink Komponente
 *
 * Eine barrierefreie "Skip to Content"-Komponente, die es Tastaturnutzern ermöglicht,
 * direkt zum Hauptinhalt zu navigieren, ohne durch die Navigation gehen zu müssen.
 *
 * Unterstützt:
 * - Tastaturnavigation
 * - Screenreader
 * - Reduzierte Bewegung
 * - Hoher Kontrast
 * - Fokusindikatoren
 */

const { t } = useI18n()
const isVisible = ref(false)

/**
 * Wird aufgerufen, wenn der Link den Fokus erhält
 */
const onFocus = () => (isVisible.value = true)

/**
 * Wird aufgerufen, wenn der Link den Fokus verliert
 */
const onBlur = () => (isVisible.value = false)

/**
 * Behandelt die Skip-Link-Funktionalität
 * Verschiebt den Fokus zum Hauptinhaltsbereich und stellt sicher, dass er zugänglich ist
 */
const handleSkip = (event: Event) => {
  event.preventDefault()
  const mainContent = document.getElementById('main-content')

  if (mainContent) {
    // Stellt sicher, dass das Element fokussierbar ist
    if (!mainContent.hasAttribute('tabindex')) {
      mainContent.setAttribute('tabindex', '-1')
    }

    // Fügt vorübergehend einen sichtbaren Fokusindikator hinzu
    mainContent.style.outline = `3px solid rgb(var(--highlight-color-rgb))`
    mainContent.style.outlineOffset = '4px'

    // Scrollt zum Element unter Berücksichtigung der Präferenzen für reduzierte Bewegung
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    mainContent.scrollIntoView({
      behavior: prefersReducedMotion ? 'auto' : 'smooth',
      block: 'start',
    })

    // Setzt den Fokus
    mainContent.focus({ preventScroll: true })

    // Entfernt tabindex und Fokusstile nach dem Fokussieren
    setTimeout(() => {
      mainContent.removeAttribute('tabindex')
      // Entfernt Fokusstile nach einer Verzögerung
      setTimeout(() => {
        mainContent.style.outline = ''
        mainContent.style.outlineOffset = ''
      }, 1500)
    }, 100)
  }
}
</script>

<style scoped>
/* High Contrast Mode Support */
@media (forced-colors: active) {
  a[data-testid='skip-link'] {
    border: 3px solid ButtonText !important;
    background-color: Canvas !important;
    color: ButtonText !important;
  }

  a[data-testid='skip-link']:focus-visible {
    outline: 3px solid ButtonText !important;
    outline-offset: 4px !important;
    background-color: Highlight !important;
    color: HighlightText !important;
    text-decoration: underline !important;
  }
}

/* Increased contrast mode */
@media (prefers-contrast: more) {
  a[data-testid='skip-link'] {
    background-color: white !important;
    color: black !important;
    border: 3px solid black !important;
    font-weight: 900 !important;
  }

  a[data-testid='skip-link']:focus-visible,
  a[data-testid='skip-link']:hover {
    background-color: black !important;
    color: white !important;
    outline: 3px solid white !important;
    outline-offset: 4px !important;
    text-decoration: underline !important;
  }
}

/* Print mode - hide skip link */
@media print {
  a[data-testid='skip-link'] {
    display: none !important;
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  a[data-testid='skip-link'] {
    transition: none !important;
  }
}

/* Mobile optimizations */
@media (max-width: 768px) {
  a[data-testid='skip-link'] {
    min-width: 180px !important;
    font-size: 0.875rem !important;
  }
}
</style>
