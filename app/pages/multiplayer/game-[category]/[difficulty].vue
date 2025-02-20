<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main>
            <Transition name="slide" mode="out-in">
                <!-- Player Setup -->
                <div v-if="!gameStarted" class="player-setup" :key="'setup'">
                    <h2>{{ t('multiplayer.setup.title') }}</h2>
                    <div class="player-count-selector">
                        <button 
                            v-for="count in [2, 3, 4]" 
                            :key="count"
                            :class="{ active: playerCount === count }"
                            @click="playerCount = count"
                        >
                            {{ count }} {{ t('multiplayer.setup.players') }}
                        </button>
                    </div>
                    <div class="player-names">
                        <div v-for="n in playerCount" :key="n" class="player-input">
                            <label>{{ t('multiplayer.setup.playerName', { number: n }) }}</label>
                            <input 
                                v-model="playerNames[n-1]" 
                                type="text" 
                                :placeholder="t('multiplayer.setup.enterName')"
                            >
                        </div>
                    </div>
                    <button 
                        class="start-game" 
                        :disabled="!canStartGame"
                        @click="startGame"
                    >
                        {{ t('multiplayer.setup.startGame') }}
                    </button>
                </div>

                <!-- Game Content -->
                <div v-else-if="!gameFinished" class="game-content" :key="'game'">
                    <div class="game-header">
                        <div class="player-pills">
                            <div 
                                v-for="(player, index) in players" 
                                :key="index"
                                :class="{ 
                                    'player-pill': true,
                                    'active': currentPlayerIndex === index 
                                }"
                            >
                                <span class="name">{{ player.name }}</span>
                                <div class="stats">
                                    <span class="score">
                                        <Icon name="material-symbols:stars" class="icon" />
                                        {{ player.score }}
                                    </span>
                                    <span class="progress">
                                        {{ playerRounds[index] }}/{{ roundsPerPlayer }}
                                    </span>
                                </div>
                            </div>
                        </div>
                   </div>

                    <Transition name="slide" mode="out-in">
                        <!-- Question View -->
                        <div v-if="!showSolution" :key="'question'">
                            <GameQuestionView 
                                v-if="currentQuestion" 
                                :question="currentQuestion"
                                :current-options="currentOptions"
                                :hidden-options="hiddenOptions"
                                :disabled="showSolution"
                                :remaining-jokers="0"
                                :joker-used-for-current-question="true"
                                :phone-expert-opinion="null"
                                :audience-opinion="null"
                                @select-answer="selectAnswer"
                            />
                        </div>

                        <!-- Solution View -->
                        <SolutionView 
                            v-else-if="currentQuestion" 
                            :key="'solution'"
                            :is-correct-answer="isCorrectAnswer"
                            :current-round="usedQuestions.length"
                            :max-rounds="maxQuestions"
                            :question="currentQuestion"
                            :artist="currentArtist"
                            :is-playing="isPlaying"
                            :audio-loaded="audioLoaded"
                            :is-buffering="isBuffering"
                            :progress="progress"
                            :current-player-name="currentPlayer.name"
                            @toggle-play="togglePlay"
                            @next="nextTurn"
                        />
                    </Transition>
                </div>

                <!-- Game Over Screen -->
                <MultiplayerGameOverScreen 
                    v-else 
                    :players="players"
                    :max-questions="maxQuestions"
                    :key="'gameover'" 
                    @play-again="startGame"
                />
            </Transition>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { watch, nextTick, computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSeoMeta, useRequestURL, useRoute, useJsonld } from '#imports'
import MultiplayerGameOverScreen from '~/components/game/MultiplayerGameOverScreen.vue'
import SolutionView from '~/components/game/SolutionView.vue'

// Import composables
import { useGameAudio } from '~/composables/useGameAudio'
import { useQuestions } from '~/composables/useQuestions'
import { useJokers } from '~/composables/useJokers'
import { useGameState } from '~/composables/useGameState'
import { useArtist } from '~/composables/useArtist'
import { useGameScore } from '~/composables/useGameScore'
import { useGameNavigation } from '~/composables/useGameNavigation'

// Initialize core utilities
const route = useRoute()
const { t, locale } = useI18n()
const url = useRequestURL()

// --- Route Parameters ---
const category = route.params.category as string
const difficulty = route.params.difficulty as string

// --- Load Category Data ---
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = ref(categories.default.find((cat: any) => cat.slug === category))

// --- Multiplayer State ---
const gameStarted = ref(false)
const playerCount = ref(2)
const playerNames = ref<string[]>(['', '', '', ''])
const currentPlayerIndex = ref(0)
const currentRound = ref(1)
const players = ref<Array<{ name: string, points: number }>>([])

const currentPlayer = computed(() => players.value[currentPlayerIndex.value])
const canStartGame = computed(() => {
    const activeNames = playerNames.value.slice(0, playerCount.value)
    return activeNames.every(name => name.trim() !== '')
})

// --- Initialize Game Composables ---
const questions = useQuestions(category, difficulty)     // Question management
const jokers = useJokers(difficulty)                    // Lifeline/joker system
const gameState = useGameState(questions.maxQuestions.value)  // Game state tracking
const artist = useArtist()                             // Artist/music info handling
const gameAudio = useGameAudio()                       // Audio playback management

// Navigation utilities
const { scrollToTop } = useGameNavigation({
    usedQuestions: questions.usedQuestions,
    maxQuestions: questions.maxQuestions,
    gameFinished: gameState.gameFinished,
    showSolution: gameState.showSolution
})

// --- Game State ---
const roundsPerPlayer = computed(() => difficulty === 'easy' ? 10 : difficulty === 'medium' ? 15 : 20)
const playerRounds = ref(new Array(4).fill(0)) // Track rounds for each player

const gameFinished = computed(() => playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value)
const showSolution = computed(() => gameState.showSolution.value)
const isCorrectAnswer = computed(() => gameState.isCorrectAnswer.value)

// --- Audio State ---
const isPlaying = ref(false)
const audioLoaded = ref(false)
const isBuffering = ref(false)
const progress = ref(0)

// --- Computed Properties ---
const currentQuestion = computed(() => questions.currentQuestion.value)
const currentOptions = computed(() => questions.currentOptions.value)
const hiddenOptions = computed(() => jokers.hiddenOptions.value)
const currentArtist = computed(() => artist.currentArtist.value)
const usedQuestions = computed(() => questions.usedQuestions.value)
const maxQuestions = computed(() => questions.maxQuestions.value)

// --- Game Logic ---
const startGame = () => {
    // Initialize players
    players.value = playerNames.value
        .slice(0, playerCount.value)
        .map(name => ({ name, score: 0, correctAnswers: 0 }))
    
        // Set rounds based on difficulty
    roundsPerPlayer.value = difficulty === 'easy' ? 10 : difficulty === 'medium' ? 15 : 20
    
    // Reset player rounds
    playerRounds.value = new Array(playerCount.value).fill(0)
    
    // Start game
    gameStarted.value = true
    currentRound.value = 1
    questions.loadQuestions()
}

const nextTurn = async () => {
    // Increment rounds for current player
    playerRounds.value[currentPlayerIndex.value]++
    currentRound.value++

    // Check if current player has finished their rounds
    if (playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value) {
        // Find next player who hasn't finished their rounds
        let nextPlayerFound = false
        for (let i = 1; i < playerCount.value; i++) {
            const nextIndex = (currentPlayerIndex.value + i) % playerCount.value
            if (playerRounds.value[nextIndex] < roundsPerPlayer.value) {
                currentPlayerIndex.value = nextIndex
                nextPlayerFound = true
                break
            }
        }
        
        // If no next player found, game is over
        if (!nextPlayerFound) {
            gameState.gameFinished.value = true
            return
        }
    } else {
        // Move to next player
        currentPlayerIndex.value = (currentPlayerIndex.value + 1) % playerCount.value
        
        // Skip players who have finished their rounds
        while (playerRounds.value[currentPlayerIndex.value] >= roundsPerPlayer.value) {
            currentPlayerIndex.value = (currentPlayerIndex.value + 1) % playerCount.value
        }
    }

    // Get a new question for the next player
    await questions.selectRandomQuestion()
    gameState.showSolution.value = false
    gameState.isCorrectAnswer.value = false
    scrollToTop()
}

const nextQuestion = async () => {
    await questions.selectRandomQuestion()
    gameState.showSolution.value = false
    gameState.isCorrectAnswer.value = false
    scrollToTop()
}


const selectAnswer = async (selectedAnswer: string) => {
    if (gameState.showSolution.value) return
    if (!questions.currentQuestion.value) return

    const isCorrect = selectedAnswer === questions.currentQuestion.value.correctAnswer
    gameState.setAnswer(isCorrect)

    if (isCorrect) {
        // Fixed points for correct answer in multiplayer
        const points = 100
        players.value[currentPlayerIndex.value].score += points
        players.value[currentPlayerIndex.value].correctAnswers++
    }

    await artist.loadCurrentArtist(category, difficulty, questions.currentQuestion)
    await nextTick()
    scrollToTop()
}

// --- SEO Meta Tags ---
useSeoMeta({
    title: computed(() => t('multiplayer.meta.title', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    description: computed(() => t('multiplayer.meta.description', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogTitle: computed(() => t('multiplayer.meta.title', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogDescription: computed(() => t('multiplayer.meta.description', { 
        category: currentCategoryData.value?.name || category,
        difficulty: difficulty 
    })),
    ogType: 'website',
    robots: 'noindex, follow'
})

// --- Watchers & Lifecycle Hooks ---
watch(() => artist.currentArtist.value, (newArtist) => {
    if (newArtist) {
        gameAudio.handleArtistChange(newArtist)
    }
})
</script>

<style lang="scss" scoped>
.player-setup {
    max-width: var(--content-width);
    margin: var(--padding-large) auto;
    padding: var(--padding-large);
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);

    h2 {
        text-align: center;
        margin-bottom: var(--padding-large);
        font-size: var(--font-size-responsive-xl);
        font-weight: var(--font-weight-bold);
        color: var(--text-color);
        line-height: var(--line-height-tight);
    }

    .player-count-selector {
        display: flex;
        justify-content: center;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-large);

        button {
            padding: var(--padding-small) var(--padding-medium);
            border: var(--border-width) solid var(--primary-color);
            border-radius: var(--border-radius);
            background: transparent;
            color: var(--text-color);
            cursor: pointer;
            transition: all var(--transition-speed) var(--transition-bounce);
            min-height: var(--min-touch-target);

            &.active {
                background: var(--primary-color);
                color: var(--button-text-color);
            }

            &:focus-visible {
                outline: var(--focus-outline-width) solid var(--focus-outline-color);
                outline-offset: var(--focus-outline-offset);
            }
        }
    }

    .player-names {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-large);

        .player-input {
            display: flex;
            flex-direction: column;
            gap: var(--padding-small);

            input {
                padding: var(--padding-small);
                border: var(--border-width) solid var(--surface-color-light);
                border-radius: var(--border-radius);
                background: var(--background-color);
                color: var(--text-color);
                min-height: var(--min-touch-target);
                font-size: var(--font-size-base);

                &:focus {
                    outline: var(--focus-outline-width) solid var(--focus-outline-color);
                    outline-offset: var(--focus-outline-offset);
                    border-color: var(--primary-color);
                }
            }
        }
    }

    .start-game {
        width: 100%;
        min-height: var(--min-touch-target);
        padding: var(--padding-medium);
        background: var(--primary-color);
        color: var(--button-text-color);
        border: none;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: var(--font-weight-bold);
        font-size: var(--font-size-responsive-md);
        transition: all var(--transition-speed) var(--transition-bounce);

        &:disabled {
            opacity: var(--opacity-disabled);
            cursor: not-allowed;
        }

        &:hover:not(:disabled) {
            background: var(--primary-color-dark);
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
        }
    }
}

.game-header {
    margin-bottom: var(--padding-large);
}

.player-pills {
    display: flex;
    justify-content: center;
    gap: var(--padding-small);
    flex-wrap: wrap;
    padding: var(--padding-small);
    margin-bottom: var(--padding-medium);

    .player-pill {
        display: flex;
        align-items: center;
        gap: var(--padding-medium);
        padding: var(--padding-small) var(--padding-medium);
        background: var(--surface-color);
        border-radius: var(--border-radius-full);
        transition: all var(--transition-speed) var(--transition-bounce);
        min-width: var(--min-touch-target);

        &.active {
            background: var(--primary-color);
            box-shadow: var(--box-shadow);

            .name, .score, .progress, .icon {
                color: var(--button-text-color);
            }
        }

        .name {
            font-weight: var(--font-weight-semibold);
            font-size: var(--font-size-responsive-md);
            line-height: var(--line-height-normal);
        }

        .stats {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            margin-left: auto;

            .score {
                display: flex;
                align-items: center;
                gap: calc(var(--padding-small) / 2);
                color: var(--primary-color);
                font-weight: var(--font-weight-semibold);
            }

            .progress {
                color: var(--text-secondary);
                font-size: var(--font-size-responsive-sm);
            }
        }
    }
}

@media (prefers-reduced-motion: reduce) {
    .player-setup button,
    .player-pill,
    .start-game {
        transition: none;
        transform: none;
    }
}

@media (width <= 640px) {
    .player-pills {
        flex-direction: column;
        
        .player-pill {
            width: 100%;
        }
    }
}

.game-content {
    margin: 0 auto;
    max-width: var(--content-width);
    padding: 0 var(--padding-medium);
}
</style>
