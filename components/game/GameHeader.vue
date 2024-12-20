<template>
    <div class="game-header">
        <div class="header-left">
            <h1>{{ categoryName }}</h1>
            <p class="round-counter">{{ roundText }}</p>
        </div>
        <div class="header-right">
            <div class="points-display">
                <div class="points-container">
                    <span class="points" :class="{ 'points-update': isAnimating }">
                        {{ formattedPoints }}
                    </span>
                    <span class="points-label">{{ t('game.points_label') }}</span>
                </div>
                <transition name="bonus">
                    <div v-if="showBonus" class="bonus-indicator">
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
        current: props.currentRound,
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
    padding: calc(var(--padding-medium) * 1.5) var(--padding-medium);
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: var(--menu-transition);

    .header-left {
        h1 {
            margin: 0;
            font-size: clamp(1.25rem, 3vw, 1.5rem);
            color: var(--text-color);
            letter-spacing: var(--spacing-text);
        }

        .round-counter {
            margin: 0.25rem 0 0;
            color: var(--text-secondary);
            font-size: clamp(0.8rem, 2vw, 0.9rem);
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
            font-size: clamp(1.5rem, 4vw, 1.8rem);
            font-weight: bold;
            color: var(--primary-color);
            letter-spacing: var(--spacing-text);
            transition: transform var(--transition-speed) var(--transition-bounce);

            &.points-update {
                transform: scale(1.2);
            }
        }

        .points-label {
            margin-top: 0.25rem;
            font-size: clamp(0.7rem, 2vw, 0.8rem);
            color: var(--text-secondary);
        }
    }
}

.bonus-indicator {
    position: absolute;
    top: -40px;
    right: 0;
    background: var(--overlay-background);
    padding: var(--padding-small);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    backdrop-filter: var(--overlay-blur);
    color: var(--text-color);
    font-size: clamp(0.8rem, 2vw, 0.9rem);
    white-space: nowrap;

    .bonus-total {
        font-weight: bold;
        color: var(--success-color);
    }

    .bonus-breakdown {
        font-size: 0.8em;
        opacity: 0.8;
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
