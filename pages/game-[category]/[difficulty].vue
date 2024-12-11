<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="false" :show-coins="false">
        <main>
            <ShowPoints ref="pointsDisplay" class="game-points" />

            <div v-if="!showSolution" class="game-content">
                <div class="game-header">
                    <h1>{{ currentCategoryData?.name || category }}</h1>
                    <p class="round-counter">Runde: {{ usedQuestions.length }} / {{ maxQuestions }}</p>
                </div>

                <div v-if="currentQuestion" class="question-container">
                    <!-- Joker Section -->
                    <div class="joker-section">
                        <button class="button joker-button"
                                @click="useFiftyFiftyJoker"
                                :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                            50:50 Joker
                        </button>
                        <p class="joker-counter">Verbleibend: {{ remainingJokers }}</p>
                    </div>

                    <!-- Frage -->
                    <div class="question">
                        <h2>{{ currentQuestion.question }}</h2>
                    </div>

                    <!-- Antwortmöglichkeiten -->
                    <div class="options">
                        <button v-for="(option, index) in currentQuestion.options"
                                :key="index"
                                class="button option-button"
                                :class="{ 'hidden': hiddenOptions.includes(option) }"
                                @click="selectAnswer(option)">
                            <span>{{ option }}</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Lösungs-Ansicht -->
            <div v-else class="solution-container">
                <div class="result-banner" :class="{ 'correct': isCorrectAnswer, 'incorrect': !isCorrectAnswer }">
                    <h2>{{ isCorrectAnswer ? 'Richtig!' : 'Leider falsch!' }}</h2>
                    <p v-if="isCorrectAnswer">
                        +{{ BASE_POINTS }} Punkte
                        <span v-if="earnedPoints > BASE_POINTS" class="bonus-points">
                            + {{ earnedPoints - BASE_POINTS }} Bonus
                        </span>
                    </p>
                    <p v-else>+0 Punkte</p>
                </div>

                <div class="song-details">
                    <div class="cover-container">
                        <img :src="currentArtist.coverSrc" :alt="`${currentArtist.artist} - ${currentArtist.album}`">
                    </div>

                    <div class="preview-player">
                        <audio controls :src="currentArtist.preview_link"></audio>
                    </div>

                    <div class="music-links">
                        <a v-if="currentArtist.spotify_link"
                           :href="currentArtist.spotify_link"
                           target="_blank"
                           class="button music-link spotify">
                            <span>Auf Spotify hören</span>
                        </a>
                        <a v-if="currentArtist.apple_music_link"
                           :href="currentArtist.apple_music_link"
                           target="_blank"
                           class="button music-link apple">
                            <span>Auf Apple Music hören</span>
                        </a>
                        <a v-if="currentArtist.deezer_link"
                           :href="currentArtist.deezer_link"
                           target="_blank"
                           class="button music-link deezer">
                            <span>Auf Deezer hören</span>
                        </a>
                    </div>

                    <div class="metadata">
                        <h3>{{ currentArtist.album }}</h3>
                        <p class="artist">{{ currentArtist.artist }}</p>
                        <p class="year">{{ currentArtist.year }}</p>
                    </div>

                    <div class="trivia">
                        <h3>Wusstest du schon?</h3>
                        <p>{{ currentQuestion.trivia }}</p>
                    </div>
                </div>

                <button @click="nextQuestion" class="button next-button">
                    Nächste Frage
                </button>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

definePageMeta({
    middleware: 'auth'
})

const route = useRoute()
const { locale } = useI18n()
const category = route.params.category as string
const difficulty = route.params.difficulty as string
const { t } = useI18n()

// Referenzen für die Spiellogik
const currentQuestion = ref<any>(null)
const questions = ref<any[]>([])

// Neue Referenz für bereits gestellte Fragen
const usedQuestions = ref<number[]>([])

// Dynamischer Import der Kategorien basierend auf der aktuellen Sprache
const categories = await import(`~/json/${locale.value}_categories.json`)
const currentCategoryData = categories.default.find((cat: any) => cat.slug === category)

// Maximale Fragenanzahl basierend auf Schwierigkeit
const maxQuestions = computed(() => {
    switch (difficulty) {
        case 'easy': return 10
        case 'medium': return 15
        case 'hard': return 20
        default: return 10
    }
})

// Joker Logik
const remainingJokers = ref(difficulty === 'easy' ? 3 : difficulty === 'medium' ? 5 : 7)
const hiddenOptions = ref<string[]>([])
const jokerUsedForCurrentQuestion = ref(false)

const useFiftyFiftyJoker = () => {
    if (remainingJokers.value > 0 && !jokerUsedForCurrentQuestion.value) {
        const wrongOptions = currentQuestion.value.options.filter(
            option => option !== currentQuestion.value.correctAnswer
        )

        // Zufällig zwei falsche Antworten auswählen
        const shuffledWrongOptions = wrongOptions.sort(() => Math.random() - 0.5)
        hiddenOptions.value = shuffledWrongOptions.slice(0, 2)

        remainingJokers.value--
        jokerUsedForCurrentQuestion.value = true
    }
}

// Funktion zum Laden der Fragen für die ausgewählte Schwierigkeit
const loadQuestions = async () => {
    try {
        const response = await import(`~/json/genres/${locale.value}/${category}.json`)
        // Sammle alle Fragen der gewählten Schwierigkeit von allen Künstlern
        const allQuestions = response.default.reduce((acc: any[], artist: any) => {
            const difficultyQuestions = artist.questions[difficulty] || []
            return [...acc, ...difficultyQuestions]
        }, [])

        questions.value = allQuestions
        console.log('Questions:', questions.value)
        selectRandomQuestion()
    } catch (error) {
        console.error('Fehler beim Laden der Fragen:', error)
    }
}

// Verbesserte Funktion zum Auswählen einer zufälligen Frage
const selectRandomQuestion = () => {
    // Wenn alle Fragen verwendet wurden, setze zurück
    if (usedQuestions.value.length === questions.value.length) {
        usedQuestions.value = []
    }

    // Finde eine noch nicht verwendete Frage
    let randomIndex
    do {
        randomIndex = Math.floor(Math.random() * questions.value.length)
    } while (usedQuestions.value.includes(randomIndex))

    // Markiere die Frage als verwendet
    usedQuestions.value.push(randomIndex)
    currentQuestion.value = questions.value[randomIndex]

    // Reset Joker state for new question
    hiddenOptions.value = []
    jokerUsedForCurrentQuestion.value = false
    startQuestionTimer()
}

const showSolution = ref(false)
const isCorrectAnswer = ref(false)

const currentArtist = ref<any>(null)

const BASE_POINTS = 50
const MAX_TIME_BONUS = 50
const TIME_LIMIT = 10000 // 10 Sekunden für maximalen Bonus

const questionStartTime = ref(0)
const earnedPoints = ref(0)

// Starte Timer wenn Frage angezeigt wird
const startQuestionTimer = () => {
    questionStartTime.value = Date.now()
}

const calculateTimeBonus = () => {
    const timeElapsed = Date.now() - questionStartTime.value
    const timeBonus = Math.max(0, Math.floor((1 - timeElapsed / TIME_LIMIT) * MAX_TIME_BONUS))
    return timeBonus
}

const layout = ref<any>(null)

const pointsDisplay = ref<any>(null)

// Funktion zum Scrollen nach oben
const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
}

const selectAnswer = async (selectedAnswer: string) => {
    isCorrectAnswer.value = selectedAnswer === currentQuestion.value.correctAnswer

    if (isCorrectAnswer.value) {
        const timeBonus = calculateTimeBonus()
        earnedPoints.value = BASE_POINTS + timeBonus
        pointsDisplay.value?.updatePoints(earnedPoints.value)
    }

    const response = await import(`~/json/genres/${locale.value}/${category}.json`)
    currentArtist.value = response.default.find((artist: any) => {
        return artist.questions[difficulty].some((q: any) => q.question === currentQuestion.value.question)
    })
    showSolution.value = true
    scrollToTop() // Scroll nach oben wenn Lösung angezeigt wird
}

const nextQuestion = () => {
    showSolution.value = false
    selectRandomQuestion()
    scrollToTop() // Scroll nach oben wenn neue Frage angezeigt wird
}

// Lade die Fragen beim Mounten der Komponente
loadQuestions()

// Initial Timer starten
onMounted(() => {
    startQuestionTimer()
    scrollToTop()
})

// Optional: Für Nutzer, die reduced motion bevorzugen
const smoothScrollBehavior = computed(() => {
    const mediaQuery = window?.matchMedia('(prefers-reduced-motion: reduce)')
    return mediaQuery?.matches ? 'auto' : 'smooth'
})
</script>

<style lang="scss">
.game-header {
    text-align: center;
    margin-bottom: var(--padding-large);
    padding: 0 var(--padding-small);

    @media (width >=768px) {
        padding: 0;
    }

    h1 {
        font-size: var(--header-font-size);
        color: var(--text-color);
        margin: 0;
        margin-bottom: var(--padding-small);
    }

    .round-counter {
        font-size: var(--body-font-size);
        color: var(--text-color);
        margin: 0;
    }
}

.question-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
    margin: 0 auto;
    padding: 0 var(--padding-small);

    @media (width >=768px) {
        max-width: var(--max-line-length);
        padding: 0;
    }
}

.question {
    text-align: center;

    h2 {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-color);
        margin: 0;

        @media (width >=768px) {
            font-size: calc(var(--body-font-size) * 1.2);
        }
    }
}

.options {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    width: 100%;

    @media (width >=768px) {
        gap: var(--padding-large);
    }
}

.option-button {
    width: 100%;
    min-height: var(--min-touch-target);
    padding: var(--padding-medium);
    justify-content: flex-start;

    font-size: var(--body-font-size);
    text-align: left;
    color: var(--button-text-color);

    background-color: var(--highlight-color);
    border: none;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);

    @media (width >=768px) {
        padding: var(--padding-medium) var(--padding-large);
        min-height: calc(var(--min-touch-target) * 1.2);
    }

    &:hover {
        background-color: var(--button-hover-color);
        transform: translateY(-2px);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    @media (hover: hover) {
        &:hover {
            transform: translateY(-2px);
        }
    }

    @media (hover: none) {
        &:active {
            background-color: var(--button-hover-color);
        }
    }

    &.hidden {
        display: none;
    }
}

.loading {
    text-align: center;
    padding: var(--padding-medium);
    color: var(--text-color);
}

.joker-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-small);
    margin-bottom: var(--padding-medium);
}

.joker-button {
    background-color: var(--highlight-color);
    min-width: 150px;

    &:disabled {
        opacity: var(--opacity-disabled);
        cursor: not-allowed;
        transform: none;
    }
}

.joker-counter {
    font-size: var(--body-font-size);
    color: var(--text-color);
    margin: 0;
}

.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
    padding: 0 var(--padding-small);

    @media (width >= 768px) {
        padding: 0;
    }
}

.result-banner {
    text-align: center;
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    margin-bottom: var(--padding-medium);

    h2 {
        margin: 0;
        font-size: var(--header-font-size);
    }

    p {
        margin: var(--padding-small) 0 0;
        font-size: var(--body-font-size);
    }

    &.correct {
        background-color: #4caf50;
        color: white;
    }

    &.incorrect {
        background-color: var(--error-color);
        color: white;
    }
}

.song-details {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    align-items: center;
}

.cover-container {
    width: 100%;
    max-width: 300px;
    aspect-ratio: 1;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--box-shadow);

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

.preview-player {
    width: 100%;
    max-width: 300px;

    audio {
        width: 100%;
    }
}

.music-links {
    display: flex;
    flex-direction: column;
    gap: var(--padding-small);
    width: 100%;
    max-width: 300px;

    .music-link {
        width: 100%;
        justify-content: center;

        &.spotify {
            background-color: #1DB954;
        }

        &.apple {
            background-color: #FA57C1;
        }

        &.deezer {
            background-color: #00C7F2;
        }
    }
}

.metadata {
    text-align: center;
    margin: var(--padding-medium) 0;

    h3 {
        font-size: var(--header-font-size);
        margin: 0 0 var(--padding-small);
    }

    p {
        margin: var(--padding-small) 0;
        font-size: var(--body-font-size);
    }

    .artist {
        font-weight: bold;
    }
}

.trivia {
    text-align: center;
    padding: var(--padding-medium);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);

    h3 {
        margin: 0 0 var(--padding-small);
        font-size: calc(var(--body-font-size) * 1.1);
    }

    p {
        margin: 0;
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
    }
}

.next-button {
    margin-top: var(--padding-medium);
    width: 100%;
    max-width: 300px;
    align-self: center;
}

.bonus-points {
    color: #FFD700;
    font-weight: bold;
    margin-left: var(--padding-small);
}

.game-points {
    position: fixed;
    top: var(--padding-medium);
    right: var(--padding-medium);
    z-index: var(--layer-above);
    background-color: var(--background-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    padding: var(--padding-small);
}
</style>
