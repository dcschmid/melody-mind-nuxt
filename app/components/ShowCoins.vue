<template>
    <div 
        class="coinsContainer" 
        role="status" 
        :aria-label="$t('coins.statusLabel')"
        aria-live="polite" 
        data-coins
        :class="{ 'reduce-motion': prefersReducedMotion }"
    >
        <div 
            class="coinsDisplay"
            :tabindex="0"
            @keydown.enter="announceCoins"
            @click="announceCoins"
        >
            <Icon 
                name="iconoir:coins" 
                class="coinIcon" 
                size="24" 
                aria-hidden="true" 
            />
            <span class="coinsCount" aria-atomic="true">
                <span class="sr-only">{{ $t('coins.collected') }}:</span>
                <span class="count" ref="countRef">{{ coins }}</span>
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const coins = ref(0)
const prefersReducedMotion = ref(false)
const countRef = ref<HTMLElement | null>(null)

onMounted(() => {
    // Check for reduced motion preference
    prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    // Listen for changes in motion preferences
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
        prefersReducedMotion.value = e.matches
    })
})

const announceCoins = () => {
    const message = t('coins.announcement', { count: coins.value })
    const announcement = new CustomEvent('announce', { 
        detail: { message, priority: 'polite' }
    })
    document.dispatchEvent(announcement)
}
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.coinsContainer {
    @include surface-card;
    @include hover-lift;
    @include touch-optimized;
    width: auto;
    padding: var(--padding-small);
    min-width: var(--min-touch-target);
    max-width: min(120px, 100%);
    @include transition(transform var(--transition-speed) ease, box-shadow var(--transition-speed) ease);

    &:focus-within {
        outline: 3px solid var(--focus-color);
        outline-offset: 2px;
    }
}

.coinsDisplay {
    display: flex;
    gap: var(--padding-small);
    align-items: center;
    padding: calc(var(--padding-small) / 2);
    cursor: pointer;

    &:focus {
        outline: none; // outline is handled by focus-within on container
    }
}

.coinIcon {
    @include icon-base;
    color: var(--highlight-color);
    @include bounce-animation;

    .reduce-motion & {
        animation: none;
    }
}

.coinsCount {
    @include label-text;
    font-family: var(--font-family);
    font-size: max(1.125rem, var(--body-font-size)); // Ensuring minimum 18px for AAA
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    line-height: 1.5;
    color: var(--text-color);
    letter-spacing: 0.01em;

    .count {
        display: inline-block;
        min-width: 1.5ch;
        text-align: right;
    }
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0) translateZ(0);
    }
    50% {
        transform: translateY(-2px) translateZ(0);
    }
}

@media (forced-colors: active) {
    .coinsContainer {
        border: 2px solid CanvasText;
        forced-color-adjust: auto;
    }

    .coinIcon {
        color: LinkText;
        forced-color-adjust: none;
    }
}

@media (prefers-color-scheme: dark) {
    .coinsContainer {
        background-color: color-mix(in srgb, var(--secondary-color) 85%, #000);
    }

    .coinIcon {
        filter: drop-shadow(0 2px 4px rgb(0 0 0 / 30%));
    }
}

@media (width <= 768px) {
    .coinsContainer {
        padding: calc(var(--padding-small) * 0.75);
    }

    .coinsCount {
        font-size: max(1rem, calc(var(--body-font-size) * 0.9)); // Ensuring minimum 16px for mobile
    }
}

@media print {
    .coinsContainer {
        border: 1px solid #000;
        box-shadow: none;
        print-color-adjust: exact;
    }

    .coinIcon {
        color: #000;
    }
}

/* High contrast improvements */
@media screen and (prefers-contrast: more) {
    .coinsContainer {
        border: 2px solid currentColor;
    }
    
    .coinsCount {
        font-weight: 800;
    }
}
</style>
