<template>
  <div
    id="menu"
    ref="menuRef"
    class="fixed inset-0 z-[9999] h-full w-full overflow-y-auto bg-black/90 backdrop-blur-md motion-safe:transition-all motion-safe:duration-300 motion-safe:ease-in-out motion-reduce:transition-none print:hidden"
    :class="[isOpen ? 'visible opacity-100' : 'pointer-events-none invisible opacity-0']"
    tabindex="-1"
    role="dialog"
    aria-modal="true"
    :aria-label="menuLabel"
    @keydown.esc="$emit('close')"
  >
    <!-- Animierter Hintergrund -->
    <div
      class="motion-safe:animate-gradient-slow absolute inset-0 bg-gradient-to-tr from-[rgb(var(--primary-color-rgb))]/10 to-[rgb(var(--secondary-color-rgb))]/10 motion-reduce:bg-none"
    />

    <!-- Menü Container mit Glaseffekt -->
    <div
      class="relative mx-auto my-[calc(4rem+1rem)] w-full max-w-3xl overflow-y-auto rounded-xl border border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-rgb))]/80 p-6 shadow-xl backdrop-blur-md motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none md:p-8 [&>a]:flex [&>a]:min-h-[44px] [&>a]:min-w-[44px] [&>a]:items-center [&>a]:justify-center [&>a:focus-visible]:outline-[3px] [&>a:focus-visible]:outline-offset-2 [&>a:focus-visible]:outline-[rgb(var(--focus-color-rgb))] [&>button]:flex [&>button]:min-h-[44px] [&>button]:min-w-[44px] [&>button]:items-center [&>button]:justify-center [&>button:focus-visible]:outline-[3px] [&>button:focus-visible]:outline-offset-2 [&>button:focus-visible]:outline-[rgb(var(--focus-color-rgb))]"
      :class="[
        isOpen ? 'translate-y-0 scale-100 opacity-100' : 'translate-y-[-20px] scale-95 opacity-0',
      ]"
    >
      <!-- Shine effect -->
      <div class="pointer-events-none absolute inset-0 overflow-hidden rounded-xl">
        <div
          class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[rgb(var(--highlight-color-rgb))]/20 to-transparent"
        />
        <div
          class="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-transparent via-[rgb(var(--highlight-color-rgb))]/20 to-transparent"
        />
      </div>

      <!-- Verbesserter Close Button -->
      <Button
        ref="closeButtonRef"
        :aria-label="closeLabel"
        variant="icon"
        class-name="absolute top-4 right-4 min-w-[48px] min-h-[48px] rounded-full bg-[rgb(var(--surface-light-color-rgb))] border border-[rgb(var(--border-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] focus:ring-[3px] focus:ring-[rgb(var(--focus-color-rgb))] focus:ring-offset-2 motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none"
        @click="$emit('close')"
      >
        <Icon name="material-symbols:close" class="text-2xl" :aria-hidden="true" />
        <span class="sr-only">{{ closeLabel }}</span>
      </Button>

      <!-- Menü Inhalt mit verbesserten Abständen -->
      <div class="mt-8 space-y-8">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePreferredReducedMotion, useThrottleFn } from '@vueuse/core'
import { useFocusTrap } from '@vueuse/integrations/useFocusTrap'
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import Button from '../ui/Button.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  menuLabel: {
    type: String,
    default: 'Menü',
  },
  closeLabel: {
    type: String,
    default: 'Menü schließen',
  },
})

const emits = defineEmits(['close'])
const menuRef = ref<HTMLElement | null>(null)
const closeButtonRef = ref<HTMLElement | null>(null)
const reducedMotion = usePreferredReducedMotion()

// Verbesserte Fokus-Falle mit Zugänglichkeitsoptionen
const { activate, deactivate } = useFocusTrap(menuRef, {
  immediate: false,
  escapeDeactivates: true,
  allowOutsideClick: true,
  fallbackFocus: () => closeButtonRef.value as HTMLElement,
  initialFocus: () => closeButtonRef.value as HTMLElement,
  returnFocusOnDeactivate: true,
})

// Optimierte Beobachtung des Menü-Status
watch(
  () => props.isOpen,
  (isOpen) => {
    if (isOpen) {
      // Hintergrund-Scrolling verhindern, wenn Menü geöffnet ist
      document.body.classList.add('overflow-hidden')

      // Fokus-Falle aktivieren
      nextTick(() => {
        activate()

        // Verbesserte Zugänglichkeit: Optimale Verzögerung für Screen Reader
        // Gibt Screen Readern Zeit, den Dialog zu erkennen
        setTimeout(() => {
          closeButtonRef.value?.focus()
        }, 150)
      })
    } else {
      // Hintergrund-Scrolling wieder ermöglichen
      document.body.classList.remove('overflow-hidden')

      // Fokus-Falle deaktivieren
      deactivate()
    }
  }
)

// Throttled Event-Handler für bessere Performance
const handleKeyDown = useThrottleFn((event: KeyboardEvent) => {
  if (!props.isOpen) return

  // Escape-Taste zum Schließen
  if (event.key === 'Escape') {
    emits('close')
  }
}, 150)

onMounted(() => {
  // Menü-Status bei Komponenten-Mount initialisieren
  if (props.isOpen) {
    document.body.classList.add('overflow-hidden')
    nextTick(() => {
      activate()
      closeButtonRef.value?.focus()
    })
  }

  // Event-Listener für verbesserte Tastatur-Navigation
  window.addEventListener('keydown', handleKeyDown)

  // ARIA-Attribute dynamisch setzen für bessere Zugänglichkeit
  if (menuRef.value) {
    menuRef.value.setAttribute('aria-hidden', props.isOpen ? 'false' : 'true')
  }
})

onUnmounted(() => {
  // Aufräumen beim Unmount der Komponente
  document.body.classList.remove('overflow-hidden')
  deactivate()
  window.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* Animationen - optimiert für Performance */
@keyframes gradient-shift {
  0%,
  100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient-slow {
  animation: gradient-shift 15s ease infinite;
  background-size: 200% 200%;
}

/* Verbesserter Kontrast für WCAG AAA */
@media (prefers-contrast: more) {
  #menu {
    background-color: black !important;
    backdrop-filter: none !important;
  }

  button {
    border: 3px solid white !important;
    background-color: black !important;
    color: white !important;
    outline: 2px solid white !important;
    outline-offset: 2px !important;
  }

  button:focus-visible {
    outline-width: 4px !important;
    outline-style: solid !important;
    outline-color: white !important;
  }

  .backdrop-blur-md {
    background-color: rgba(0, 0, 0, 0.95) !important;
    backdrop-filter: none !important;
  }

  /* Verbesserte Sichtbarkeit für interaktive Elemente */
  a,
  button {
    text-decoration: underline !important;
  }
}

/* Print-Optimierung */
@media print {
  #menu {
    display: none !important;
  }
}

/* Unterstützung für prefers-reduced-motion - bereits durch Tailwind-Klassen abgedeckt */
</style>
