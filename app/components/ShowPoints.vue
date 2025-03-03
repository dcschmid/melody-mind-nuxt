<template>
  <div
    class="relative flex gap-2"
    role="status"
    :aria-label="$t('points.statusLabel')"
    :data-reduced-motion="prefersReducedMotion"
  >
    <!-- Points container with improved accessibility -->
    <div
      class="flex cursor-pointer flex-col items-center rounded-md bg-[rgb(var(--surface-color-rgb))]/95 p-2 shadow-sm backdrop-blur-sm transition-all hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:shadow-md focus:ring-2 focus:ring-[rgb(var(--highlight-color-rgb))] focus:ring-offset-2 focus:outline-none motion-safe:duration-300 dark:bg-[rgb(var(--surface-light-color-rgb))]/90 dark:hover:bg-[rgb(var(--surface-hover-color-rgb))]/80 print:border print:border-black print:bg-transparent"
      tabindex="0"
      aria-describedby="points-description"
      @keydown.enter="announcePoints"
      @click="announcePoints"
    >
      <!-- Current points value with animation -->
      <span
        class="text-lg leading-tight font-bold tracking-wide text-[rgb(var(--primary-color-rgb))] tabular-nums transition-transform motion-safe:duration-300 dark:text-[rgb(var(--primary-light-color-rgb))]"
        :class="{
          'scale-110 text-[rgb(var(--highlight-color-rgb))] dark:text-[rgb(var(--highlight-color-rgb))]':
            isAnimating && !prefersReducedMotion,
        }"
        aria-atomic="true"
      >
        <span class="sr-only">{{ $t('points.current') }}:</span>
        {{ formattedPoints }}
      </span>

      <!-- Points label -->
      <span
        id="points-description"
        class="mt-1 text-base leading-normal font-medium text-[rgb(var(--text-secondary-color-rgb))] dark:text-white/70"
      >
        {{ $t('points.label') }}
      </span>
    </div>

    <!-- Bonus points indicator with animation -->
    <transition
      :name="prefersReducedMotion ? '' : 'bonus'"
      @before-enter="onTransitionStart"
      @after-leave="onTransitionEnd"
    >
      <div
        v-if="showBonus"
        class="text-md absolute -top-6 right-0 rounded-md border border-[rgb(var(--highlight-color-rgb))]/20 bg-[rgb(var(--surface-color-rgb))]/95 px-2 py-1 font-bold text-[rgb(var(--highlight-color-rgb))] shadow-md backdrop-blur-sm dark:border-[rgb(var(--highlight-color-rgb))]/30 dark:bg-[rgb(var(--surface-light-color-rgb))]/90"
        role="alert"
        aria-live="assertive"
      >
        <span class="sr-only">{{ $t('points.bonus') }}</span>
        +{{ latestBonus }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

/**
 * ShowPoints Komponente
 *
 * Zeigt die aktuellen Punkte des Spielers an und animiert Bonuspunkte.
 * Enthält Verbesserungen für Barrierefreiheit, einschließlich Unterstützung für
 * reduzierte Bewegung, Screenreader-Ankündigungen und Hochkontrastmodus.
 */

const { t } = useI18n()
const points = ref(0)
const isAnimating = ref(false)
const showBonus = ref(false)
const latestBonus = ref(0)
const prefersReducedMotion = ref(false)
const isTransitioning = ref(false)

/**
 * Formatiert die Punkte mit Tausendertrennzeichen für bessere Lesbarkeit
 */
const formattedPoints = computed(() => {
  return points.value.toLocaleString()
})

onMounted(() => {
  // Prüfen auf Präferenz für reduzierte Bewegung
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  // Auf Änderungen der Bewegungspräferenzen hören
  window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
    prefersReducedMotion.value = e.matches
  })
})

/**
 * Kündigt den aktuellen Punktestand für Screenreader an
 */
const announcePoints = () => {
  if (isTransitioning.value) return // Verhindert Ankündigung während Übergängen

  const message = t('points.announcement', {
    points: formattedPoints.value,
    bonus: showBonus.value ? latestBonus.value : 0,
  })
  const announcement = new CustomEvent('announce', {
    detail: { message, priority: 'polite' },
  })
  document.dispatchEvent(announcement)
}

/**
 * Wird aufgerufen, wenn die Bonus-Animation beginnt
 */
const onTransitionStart = () => {
  isTransitioning.value = true
}

/**
 * Wird aufgerufen, wenn die Bonus-Animation endet
 */
const onTransitionEnd = () => {
  isTransitioning.value = false
}

/**
 * Aktualisiert die Punkte und zeigt eine Bonus-Animation an
 * @param newPoints Die hinzuzufügenden Bonuspunkte
 */
const updatePoints = (newPoints: number) => {
  latestBonus.value = newPoints
  showBonus.value = true
  isAnimating.value = true

  points.value += newPoints

  // Ankündigung der Punkteaktualisierung für Screenreader
  const message = t('points.bonusAnnouncement', {
    bonus: newPoints,
    total: points.value,
  })
  const announcement = new CustomEvent('announce', {
    detail: { message, priority: 'assertive' },
  })
  document.dispatchEvent(announcement)

  const animationDuration = prefersReducedMotion.value ? 0 : 2000
  setTimeout(() => {
    showBonus.value = false
    isAnimating.value = false
  }, animationDuration)
}

defineExpose({
  updatePoints,
})
</script>

<style scoped>
/* Animation classes for bonus indicator */
.bonus-enter-active,
.bonus-leave-active {
  @apply transition-all ease-in-out duration-300 motion-safe:duration-300;
}

.bonus-enter-from {
  @apply translate-y-5 opacity-0;
}

.bonus-leave-to {
  @apply -translate-y-5 opacity-0;
}

/* High contrast mode improvements */
@media (forced-colors: active) {
  div[tabindex='0'] {
    @apply border-2 border-[CanvasText];
  }

  div[role='alert'] {
    @apply border-2 border-[CanvasText];
  }
}

/* Increased contrast mode */
@media (prefers-contrast: more) {
  div[tabindex='0'] {
    @apply border-2 border-black bg-white shadow-none;
  }

  span[aria-atomic='true'] {
    @apply font-extrabold text-black;
  }

  span[id='points-description'] {
    @apply font-semibold text-black;
  }

  div[role='alert'] {
    @apply border-2 border-black bg-white font-extrabold text-black;
  }
}

/* Mobile optimizations */
@media (max-width: 768px) {
  span[aria-atomic='true'] {
    @apply text-base;
  }

  span[id='points-description'] {
    @apply text-sm;
  }
}

/* Print optimizations */
@media print {
  div[tabindex='0'] {
    @apply border border-black/80 bg-transparent shadow-none;
  }

  span[aria-atomic='true'] {
    @apply text-black;
  }

  span[id='points-description'] {
    @apply text-black;
  }

  div[role='alert'] {
    @apply hidden;
  }
}

  div[role='alert'] {
    @apply hidden;
  }
}
</style>
