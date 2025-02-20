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
    transition: all var(--transition-speed) var(--transition-bounce);

    &:focus {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &:hover {
        background-color: var(--surface-color-hover);
    }
}

.points {
    font-size: var(--font-size-responsive-lg);
    font-weight: var(--font-weight-bold);
    color: var(--primary-color);
    line-height: var(--line-height-tight);
    font-variant-numeric: tabular-nums;
    letter-spacing: var(--spacing-text);

    .reduce-motion & {
        transition: none;
    }

    &:not(.reduce-motion) {
        transition: transform var(--transition-speed) var(--transition-bounce);
    }

    &.points-update {
        transform: scale(1.1);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    margin-top: var(--padding-small);
}

.bonus-indicator {
    position: absolute;
    top: -24px;
    right: 0;
    color: var(--highlight-color);
    font-weight: var(--font-weight-bold);
    font-size: var(--font-size-responsive-md);
    text-shadow: var(--box-shadow);
    padding: calc(var(--padding-small) / 2);
    border-radius: var(--border-radius);
    background-color: var(--surface-color);
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all var(--transition-speed) var(--transition-bounce);

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
        border: 2px solid var(--text-color);
    }

    .points.points-update {
        color: var(--highlight-color);
    }

    .bonus-indicator {
        border: 1px solid var(--text-color);
        color: var(--highlight-color);
    }
}

/* Dark mode improvements */
@media (prefers-color-scheme: dark) {
    .points-container {
        background-color: var(--surface-color-light);
    }

    .bonus-indicator {
        background-color: var(--surface-color-light);
    }
}

/* Print mode */
@media print {
    .points-container {
        background: none;
        border: 1px solid var(--button-text-color);
    }

    .bonus-indicator {
        display: none;
    }
}

/* Increased contrast mode */
@media screen and (prefers-contrast: more) {
    .points {
        font-weight: var(--font-weight-bold);
    }

    .points-label {
        font-weight: var(--font-weight-semibold);
    }

    .points-container {
        border: 2px solid currentColor;
    }
}

/* Mobile optimizations */
@media (max-width: 768px) {
    .points {
        font-size: var(--font-size-responsive-md);
    }

    .points-label {
        font-size: var(--font-size-responsive-sm);
    }
}
</style>
