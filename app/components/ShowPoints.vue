<template>
    <div 
        class="points-display" 
        role="status"
        :aria-label="$t('points.statusLabel')"
        :class="{ 'reduce-motion': prefersReducedMotion }"
    >
        <div 
            class="points-container"
            :tabindex="0"
            @keydown.enter="announcePoints"
            @click="announcePoints"
        >
            <span 
                class="points" 
                :class="{ 'points-update': isAnimating && !prefersReducedMotion }"
                aria-atomic="true"
            >
                <span class="sr-only">{{ $t('points.current') }}:</span>
                {{ formattedPoints }}
            </span>
            <span class="points-label">{{ $t('points.label') }}</span>
        </div>
        <transition 
            :name="prefersReducedMotion ? '' : 'bonus'"
            @before-enter="onTransitionStart"
            @after-leave="onTransitionEnd"
        >
            <div 
                v-if="showBonus" 
                class="bonus-indicator"
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
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const points = ref(0)
const isAnimating = ref(false)
const showBonus = ref(false)
const latestBonus = ref(0)
const prefersReducedMotion = ref(false)
const isTransitioning = ref(false)

const formattedPoints = computed(() => {
    return points.value.toLocaleString()
})

onMounted(() => {
    // Check for reduced motion preference
    prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    // Listen for changes in motion preferences
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
        prefersReducedMotion.value = e.matches
    })
})

const announcePoints = () => {
    if (isTransitioning.value) return // Prevent announcement during transitions
    
    const message = t('points.announcement', { 
        points: formattedPoints.value,
        bonus: showBonus.value ? latestBonus.value : 0
    })
    const announcement = new CustomEvent('announce', { 
        detail: { message, priority: 'polite' }
    })
    document.dispatchEvent(announcement)
}

const onTransitionStart = () => {
    isTransitioning.value = true
}

const onTransitionEnd = () => {
    isTransitioning.value = false
}

const updatePoints = (newPoints: number) => {
    latestBonus.value = newPoints
    showBonus.value = true
    isAnimating.value = true

    points.value += newPoints

    // Announce points update
    const message = t('points.bonusAnnouncement', { 
        bonus: newPoints,
        total: points.value
    })
    const announcement = new CustomEvent('announce', { 
        detail: { message, priority: 'assertive' }
    })
    document.dispatchEvent(announcement)

    const animationDuration = prefersReducedMotion.value ? 0 : 2000
    setTimeout(() => {
        showBonus.value = false
        isAnimating.value = false
    }, animationDuration)
}

defineExpose({
    updatePoints
})
</script>

<style lang="scss" scoped>
.points-display {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--padding-small);
}

.points-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--padding-small);
    border-radius: var(--border-radius);
    background-color: var(--surface-color);
    cursor: pointer;

    &:focus {
        outline: 3px solid var(--focus-color);
        outline-offset: 2px;
    }

    &:hover {
        background-color: var(--surface-hover-color);
    }
}

.points {
    font-size: max(1.5rem, clamp(1.2rem, 3vw, 1.8rem)); // Ensuring minimum 24px for numbers
    font-weight: 700;
    color: var(--text-color);
    line-height: 1.5;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.01em;

    .reduce-motion & {
        transition: none;
    }

    &:not(.reduce-motion) {
        transition: transform 0.3s ease;
    }

    &.points-update {
        transform: scale(1.1);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: max(1.125rem, var(--body-font-size)); // Ensuring minimum 18px for AAA
    color: var(--text-color);
    font-weight: 500;
    line-height: 1.5;
    margin-top: 0.25rem;
}

.bonus-indicator {
    position: absolute;
    top: -24px;
    right: 0;
    color: var(--highlight-color);
    font-weight: 700;
    font-size: max(1.125rem, var(--body-font-size));
    text-shadow: 0 1px 2px rgb(0 0 0 / 20%);
    padding: 0.25rem 0.5rem;
    border-radius: var(--border-radius);
    background-color: var(--surface-color);
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all 0.5s ease;

    .reduce-motion & {
        transition: none;
    }
}

.bonus-enter-from {
    opacity: 0;
    transform: translateY(20px);
}

.bonus-leave-to {
    opacity: 0;
    transform: translateY(-20px);
}

/* High contrast mode improvements */
@media (forced-colors: active) {
    .points-container {
        border: 2px solid CanvasText;
        forced-color-adjust: none;
    }

    .points.points-update {
        color: Highlight;
    }

    .bonus-indicator {
        border: 1px solid CanvasText;
        color: Highlight;
    }
}

/* Dark mode improvements */
@media (prefers-color-scheme: dark) {
    .points-container {
        background-color: color-mix(in srgb, var(--surface-color) 85%, #000);
    }

    .bonus-indicator {
        background-color: color-mix(in srgb, var(--surface-color) 85%, #000);
    }
}

/* Print mode */
@media print {
    .points-container {
        background: none;
        border: 1px solid #000;
        print-color-adjust: exact;
    }

    .bonus-indicator {
        display: none;
    }
}

/* Increased contrast mode */
@media screen and (prefers-contrast: more) {
    .points {
        font-weight: 800;
    }

    .points-label {
        font-weight: 600;
    }

    .points-container {
        border: 2px solid currentColor;
    }
}

/* Mobile optimizations */
@media (max-width: 768px) {
    .points {
        font-size: max(1.25rem, clamp(1.1rem, 2.5vw, 1.5rem)); // Ensuring minimum 20px for mobile
    }

    .points-label {
        font-size: max(1rem, calc(var(--body-font-size) * 0.9)); // Ensuring minimum 16px for mobile
    }
}
</style>
