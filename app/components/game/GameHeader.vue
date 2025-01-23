<template>
    <div class="game-header" role="banner">
        <div class="header-left">
            <h1 id="category-name">{{ categoryName }}</h1>
            <p class="round-counter" aria-live="polite">
                {{ roundText }}
            </p>
        </div>
        <div class="header-right">
            <div class="points-display">
                <div class="points-container" role="status" aria-live="polite" aria-atomic="true">
                    <span class="points" :class="{ 'points-update': isAnimating }">
                        {{ formattedPoints }}
                    </span>
                    <span class="points-label">{{ t('game.points_label') }}</span>
                </div>
                <transition name="bonus">
                    <div v-if="showBonus" class="bonus-indicator" role="alert">
                        <div class="bonus-total">+{{ latestBonus.base }}</div>
                        <div class="bonus-breakdown">
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

const { t } = useI18n()

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

const roundText = computed(() => {
    return t('game.round', {
        aktuell: props.currentRound,
        max: props.maxRounds
    })
})

const formattedPoints = computed(() => {
    return props.points.toLocaleString()
})
</script>

<style scoped lang="scss">
.game-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: calc(var(--padding-small) * 1.5) var(--padding-medium);
    transition: var(--menu-transition);
    background-color: var(--surface-color);
    border-radius: var(--border-radius);

    .header-left {
        h1 {
            margin: 0;
            font-size: clamp(1.5rem, 3vw, 1.75rem);
            color: var(--text-color);
            letter-spacing: var(--spacing-text);
            font-weight: 600;
        }

        .round-counter {
            margin: 0.5rem 0 0;
            color: var(--text-secondary);
            font-size: clamp(0.875rem, 2vw, 1rem);
            font-weight: 500;
        }
    }

    .points-display {
        position: relative;
        text-align: right;

        .points-container {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }

        .points {
            font-size: clamp(1.75rem, 4vw, 2rem);
            font-weight: bold;
            color: var(--primary-color);
            letter-spacing: var(--spacing-text);
            transition: transform var(--transition-speed) var(--transition-bounce);

            &.points-update {
                transform: scale(1.2);
            }
        }

        .points-label {
            margin-top: 0.5rem;
            font-size: clamp(0.875rem, 2vw, 1rem);
            color: var(--text-secondary);
            font-weight: 500;
        }
    }
}

.bonus-indicator {
    position: absolute;
    top: -48px;
    right: 0;
    background: var(--surface-color);
    padding: var(--padding-small) var(--padding-medium);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    color: var(--text-color);
    font-size: clamp(0.875rem, 2vw, 1rem);
    white-space: nowrap;
    border: 1px solid var(--success-color);

    .bonus-total {
        font-weight: bold;
        color: var(--success-color);
        font-size: 1.1em;
    }

    .bonus-breakdown {
        font-size: 0.9em;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
}

// Bonus Animation
.bonus-enter-active,
.bonus-leave-active {
    transition: var(--menu-transition);
}

.bonus-enter-from,
.bonus-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
