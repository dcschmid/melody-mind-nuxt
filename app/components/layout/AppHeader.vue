<template>
  <header
    role="banner"
    class="fixed inset-x-0 top-0 z-50 h-16 border-b border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-rgb))]/95 shadow-xs backdrop-blur-xs motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-out motion-reduce:transition-none print:hidden"
    :class="{ 'shadow-sm': scrolled }"
    aria-label="Haupt-Header"
  >
    <div class="container mx-auto flex h-full items-center justify-between px-4 md:px-6">
      <!-- Logo/Branding -->
      <div class="flex items-center gap-2">
        <slot name="left" />
      </div>

      <!-- Navigation -->
      <nav
        :aria-label="navLabel"
        class="flex items-center gap-4 [&>a]:flex [&>a]:min-h-[44px] [&>a]:min-w-[44px] [&>a]:items-center [&>a]:justify-center [&>a:focus-visible]:outline-[3px] [&>a:focus-visible]:outline-offset-2 [&>a:focus-visible]:outline-[rgb(var(--focus-color-rgb))] [&>button]:flex [&>button]:min-h-[44px] [&>button]:min-w-[44px] [&>button]:items-center [&>button]:justify-center [&>button:focus-visible]:outline-[3px] [&>button:focus-visible]:outline-offset-2 [&>button:focus-visible]:outline-[rgb(var(--focus-color-rgb))]"
      >
        <slot name="right" />
      </nav>
    </div>
  </header>

  <!-- Spacer für den Header - vermeidet visuelles Verschwinden von Inhalten unter dem Header -->
  <div class="h-16" aria-hidden="true" />
</template>

<script setup lang="ts">
import { useThrottleFn } from '@vueuse/core'
import { onMounted, onUnmounted, ref } from 'vue'

defineProps({
  navLabel: {
    type: String,
    default: 'Hauptnavigation',
  },
})

// Scroll-Effekt für den Header
const scrolled = ref(false)

// Prüfen, ob Bewegungsreduzierung aktiviert ist
const prefersReducedMotion = ref(false)

// Throttle für bessere Performance
const handleScroll = useThrottleFn(() => {
  // Nur Effekt anwenden, wenn keine Bewegungsreduzierung aktiviert ist
  if (!prefersReducedMotion.value) {
    scrolled.value = window.scrollY > 10
  }
}, 100)

// Media Query für Bewegungsreduzierung
const setupReducedMotionListener = () => {
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  prefersReducedMotion.value = mediaQuery.matches

  // Listener für Änderungen der Einstellung
  const updateMotionPreference = (e: MediaQueryListEvent) => {
    prefersReducedMotion.value = e.matches

    // Scroll-Effekt zurücksetzen, wenn Bewegungsreduzierung aktiviert wird
    if (e.matches) {
      scrolled.value = false
    }
  }

  // Event-Listener für Änderungen der Einstellung
  mediaQuery.addEventListener('change', updateMotionPreference)

  // Cleanup-Funktion zurückgeben
  return () => mediaQuery.removeEventListener('change', updateMotionPreference)
}

onMounted(() => {
  // Bewegungsreduzierungs-Listener einrichten
  const cleanupMotionListener = setupReducedMotionListener()

  // Scroll-Listener nur hinzufügen, wenn keine Bewegungsreduzierung aktiviert ist
  if (!prefersReducedMotion.value) {
    window.addEventListener('scroll', handleScroll, { passive: true })
  }

  // Cleanup bei Komponenten-Unmount
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
    cleanupMotionListener()
  })
})
</script>

<style scoped>
/* High Contrast Mode - Verbesserte Zugänglichkeit */
@media (prefers-contrast: more) {
  header {
    background-color: black !important;
    border-bottom: 3px solid white !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
  }

  /* Verbesserte Sichtbarkeit für interaktive Elemente im High-Contrast-Mode */
  nav a,
  nav button {
    outline: 2px solid white !important;
    outline-offset: 2px !important;
  }

  nav a:focus-visible,
  nav button:focus-visible {
    outline-width: 4px !important;
    outline-style: solid !important;
    outline-color: white !important;
  }
}

/* Print-Optimierung */
@media print {
  header {
    display: none !important;
  }
}
</style>
