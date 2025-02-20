<template>
    <div class="game-header" role="banner">
        <div class="header-left">
            <h1 id="category-name" class="game-title">{{ categoryName }}</h1>
            <p class="round-counter header-text" aria-live="polite">
                {{ roundText }}
            </p>
        </div>
        <div class="header-right">
            <div class="points-display">
                <div class="points-container" role="status" aria-live="polite" aria-atomic="true">
                    <span class="points" :class="{ 'points-update': isAnimating }">
                        {{ formattedPoints }}
                    </span>
                    <span class="points-label header-text">{{ t('game.points_label') }}</span>
                </div>
                <transition v-bind="bonusTransitionProps">
                    <div v-if="showBonus" class="bonus-indicator" role="alert">
                        <div class="bonus-total game-subtitle">+{{ latestBonus.base }}</div>
                        <div class="bonus-breakdown header-text">
                            <span class="time">+{{ latestBonus.time }} Bonus</span>
                        </div>
                    </div>
                </transition>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { computed, shallowRef } from 'vue'

const { t } = useI18n()

// Optimiere Props mit shallowRef für komplexe Objekte
const props = defineProps<{
    categoryName: string
    currentRound: number
    maxRounds: number
    points: number
    isAnimating: boolean
    showBonus: boolean
    latestBonus: {
        base: number
        time: number
    }
}>()

// Memoize computed properties mit Dependency Tracking
const roundText = computed(() => {
    return t('game.round', {
        aktuell: props.currentRound,
        max: props.maxRounds
    })
})

// Optimiere Number Formatting
const formattedPoints = computed(() => {
    return new Intl.NumberFormat(undefined, {
        maximumFractionDigits: 0
    }).format(props.points)
})

// Optimiere Transition Properties
const bonusTransitionProps = shallowRef({
    name: 'bonus',
    mode: 'out-in'
})
</script>

<style scoped lang="scss">
.game-header {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    padding: var(--padding-medium);
    transition: all var(--transition-speed) var(--transition-bounce);
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    border: 2px solid var(--surface-color-light);
    box-shadow: var(--box-shadow);
    text-align: center;

    @media (min-width: 640px) {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        padding: var(--padding-medium) var(--padding-large);
        text-align: left;
    }

    .header-left {
        h1.game-title {
            margin: 0;
            font-size: var(--font-size-responsive-xl);
            font-weight: var(--font-weight-bold);
            color: var(--text-color);
            letter-spacing: var(--spacing-text);
            line-height: var(--line-height-tight);
        }

        .round-counter.header-text {
            margin: var(--padding-small) 0 0;
            color: var(--text-color);
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-medium);
            line-height: var(--line-height-normal);
        }
    }

    .points-display {
        position: relative;
        text-align: center;

        @media (min-width: 640px) {
            text-align: right;
        }

        .points-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: var(--padding-small);

            @media (min-width: 640px) {
                align-items: flex-end;
            }
        }

        .points {
            font-size: var(--font-size-responsive-xl);
            font-weight: var(--font-weight-semibold);
            color: var(--primary-color);
            letter-spacing: var(--spacing-text);
            transition: transform var(--transition-speed) var(--transition-bounce);
            line-height: var(--line-height-tight);

            &.points-update {
                transform: scale(1.1);
                color: var(--success-color);
            }
        }

        .points-label.header-text {
            color: var(--text-color);
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-medium);
            line-height: var(--line-height-normal);
        }
    }
}

.bonus-indicator {
    position: absolute;
    top: auto;
    bottom: -60px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--surface-color);
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    color: var(--text-color);
    font-size: var(--font-size-base);
    white-space: nowrap;
    border: 2px solid var(--success-color);
    min-width: 120px;
    text-align: center;
    z-index: var(--z-index-overlay);

    @media (min-width: 640px) {
        bottom: auto;
        top: -60px;
        left: auto;
        right: 0;
        transform: none;
    }

    .bonus-total.game-subtitle {
        font-weight: var(--font-weight-bold);
        color: var(--success-color);
        font-size: var(--font-size-responsive-md);
        line-height: var(--line-height-normal);
    }

    .bonus-breakdown.header-text {
        font-size: var(--font-size-base);
        color: var(--text-secondary);
        margin-top: var(--padding-small);
        line-height: var(--line-height-normal);
    }
}

// Bonus Animation
.bonus-enter-active,
.bonus-leave-active {
    transition: all var(--transition-speed) var(--transition-bounce);
}

.bonus-enter-from,
.bonus-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
