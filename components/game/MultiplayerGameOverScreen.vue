<template>
    <div class="game-over">
        <h1>{{ t('multiplayer.gameOver.title') }}</h1>
        
        <div class="results">
            <div 
                v-for="(player, index) in sortedPlayers" 
                :key="index"
                class="player-result"
                :class="{ 'winner': index === 0 }"
            >
                <div class="position">{{ index + 1 }}</div>
                <div class="player-info">
                    <div class="name">{{ player.name }}</div>
                    <div class="points">{{ player.points }} {{ t('multiplayer.gameOver.points') }}</div>
                </div>
            </div>
        </div>

        <div class="actions">
            <NuxtLink 
                :to="localePath('/multiplayer/game-' + route.params.category + '/' + route.params.difficulty)" 
                class="action-button"
            >
                {{ t('multiplayer.gameOver.playAgain') }}
            </NuxtLink>
            
            <NuxtLink 
                :to="localePath('/')" 
                class="action-button secondary"
            >
                {{ t('multiplayer.gameOver.backToMenu') }}
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useLocalePath } from '#imports'

const route = useRoute()
const { t } = useI18n()
const localePath = useLocalePath()

const props = defineProps<{
    players: Array<{ name: string, points: number }>,
    maxQuestions: number
}>()

const sortedPlayers = computed(() => {
    return [...props.players].sort((a, b) => b.points - a.points)
})
</script>

<style lang="scss" scoped>
.game-over {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    background: var(--surface-color);
    border-radius: 8px;
    box-shadow: var(--shadow-elevation-medium);
    text-align: center;

    h1 {
        margin-bottom: 2rem;
        color: var(--primary-color);
    }

    .results {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 2rem;

        .player-result {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: var(--background-color);
            border-radius: 4px;
            transition: transform 0.3s ease;

            &.winner {
                background: var(--primary-color);
                color: var(--surface-color);
                transform: scale(1.05);

                .position {
                    background: var(--surface-color);
                    color: var(--primary-color);
                }
            }

            .position {
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--primary-color);
                color: var(--surface-color);
                border-radius: 50%;
                font-weight: bold;
                font-size: 1.2em;
            }

            .player-info {
                flex: 1;
                text-align: left;

                .name {
                    font-weight: bold;
                    margin-bottom: 0.25rem;
                }

                .points {
                    font-size: 0.9em;
                    opacity: 0.8;
                }
            }
        }
    }

    .actions {
        display: flex;
        flex-direction: column;
        gap: 1rem;

        .action-button {
            padding: 1rem;
            border-radius: 4px;
            font-weight: bold;
            text-decoration: none;
            transition: opacity 0.3s ease;

            &:hover {
                opacity: 0.9;
            }

            &:not(.secondary) {
                background: var(--primary-color);
                color: var(--surface-color);
            }

            &.secondary {
                background: var(--background-color);
                color: var(--text-color);
            }
        }
    }
}
</style>
