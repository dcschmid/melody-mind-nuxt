<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false" :show-coins="false">
        <main>
            <div v-if="!gameFinished" class="game-content">
                <div v-if="!showSolution">
                    <div class="game-header">
                        <div class="header-left">
                            <h1>{{ currentCategoryData?.name || category }}</h1>
                            <p class="round-counter">Runde: {{ usedQuestions.length }} / {{ maxQuestions }}</p>
                        </div>
                        <div class="header-right">
                            <div class="points-display">
                                <div class="points-container">
                                    <span class="points" :class="{ 'points-update': isAnimating }">
                                        {{ formattedPoints }}
                                    </span>
                                    <span class="points-label">Punkte</span>
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

                    <div v-if="currentQuestion" class="question-container">
                        <!-- Frage -->
                        <div class="question">
                            <h2>{{ currentQuestion.question }}</h2>
                        </div>

                        <!-- Antwortmöglichkeiten -->
                        <div class="options">
                            <button v-for="(option, index) in currentQuestion.options" :key="index"
                                class="button option-button" :class="{ 'hidden': hiddenOptions.includes(option) }"
                                @click="selectAnswer(option)">
                                <span>{{ option }}</span>
                            </button>
                        </div>

                        <!-- Telefonjoker Antwort -->
                        <div v-if="phoneExpertOpinion" class="phone-expert">
                            <h3>Experten-Meinung</h3>
                            <div class="expert-message">
                                <div class="expert-header">
                                    <Icon name="material-symbols:phone" class="phone-icon" />
                                    <span class="expert-name">{{ phoneExpertOpinion.expert }}</span>
                                </div>
                                <div class="message-content">
                                    <p class="expert-answer">{{ phoneExpertOpinion.message }}</p>
                                    <div class="confidence-bar-container">
                                        <div class="confidence-bar"
                                            :style="{ '--confidence': phoneExpertConfidence + '%' }" :class="{
                                                'high': phoneExpertConfidence >= 80,
                                                'medium': phoneExpertConfidence >= 60 && phoneExpertConfidence < 80,
                                                'low': phoneExpertConfidence < 60
                                            }">
                                            <div class="confidence-level"></div>
                                        </div>
                                        <span class="confidence-text">{{ phoneExpertConfidence }}% Sicherheit</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Publikumsjoker Ergebnis -->
                        <div v-if="Object.keys(audienceHelp).length > 0" class="audience-help">
                            <h3>Publikumsmeinung</h3>
                            <div class="audience-bars">
                                <div v-for="(percentage, option) in audienceHelp" :key="option" class="bar-item">
                                    <div class="option-label">
                                        <div class="option-text">{{ option }}</div>
                                        <div class="percentage-text">{{ percentage }}%</div>
                                    </div>
                                    <div class="bar-container">
                                        <div class="bar" :style="{ width: `${percentage}%` }" :class="{
                                            'high': percentage >= 70,
                                            'medium': percentage >= 40 && percentage < 70,
                                            'low': percentage < 40
                                        }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Joker Section -->
                        <div class="jokers-section">
                            <div class="joker-buttons">
                                <!-- 50:50 Joker -->
                                <button class="button joker-button" @click="useFiftyFiftyJoker"
                                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                    aria-label="50:50 Joker verwenden"
                                    :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                    <Icon name="material-symbols:balance" size="30" />
                                </button>

                                <!-- Publikumsjoker -->
                                <button class="button joker-button" @click="useAudienceJoker"
                                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                    aria-label="Publikumsjoker verwenden"
                                    :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                    <Icon name="formkit:people" size="30" />
                                </button>

                                <!-- Telefonjoker -->
                                <button class="button joker-button" @click="usePhoneJoker"
                                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                    aria-label="Telefonjoker verwenden"
                                    :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                    <Icon name="gg:phone" size="30" />
                                </button>
                            </div>
                            <span class="joker-count">Verbleibend: {{ remainingJokers }}</span>
                        </div>
                    </div>
                </div>
                <div v-else class="solution-container">
                    <!-- Ergebnis-Banner -->
                    <div class="result-banner" :class="{ 'correct': isCorrectAnswer }">
                        <div class="result-header">
                            <Icon :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                                class="result-icon" size="28" />
                            <h2>{{ isCorrectAnswer ? 'Richtig!' : 'Leider falsch!' }}</h2>
                        </div>
                        <div v-if="isCorrectAnswer" class="points-breakdown">
                            <div class="points">
                                Punkte: +{{ latestBonus.base }} + {{ latestBonus.time }} Bonuspunkte
                            </div>
                        </div>
                        <div v-else class="points">+0 Punkte</div>
                        <div class="correct-answer">
                            <span class="label">Richtige Antwort:</span>
                            <div class="text">{{ currentQuestion.correctAnswer }}</div>
                        </div>
                    </div>

                    <!-- Content Container -->
                    <div class="content-wrapper">

                        <!-- Album Info -->
                        <div v-if="currentArtist" class="album-box">
                            <div class="cover-wrapper">
                                <img :src="currentArtist.coverSrc"
                                    :alt="`${currentArtist.artist} - ${currentArtist.album}`" />
                            </div>
                            <div class="player-info-wrapper">
                                <div class="audio-player">
                                    <button @click="togglePlay" class="play-button"
                                        :disabled="!currentArtist?.preview_link"
                                        :title="currentArtist?.preview_link ? 'Play/Pause' : 'No audio available'">
                                        <Icon
                                            :name="isPlaying ? 'material-symbols:pause' : 'material-symbols:play-arrow'"
                                            size="36" />
                                    </button>
                                    <div class="progress-bar">
                                        <div class="progress" :style="{ width: `${(currentTime / duration) * 100}%` }">
                                        </div>
                                    </div>
                                </div>
                                <div class="info">
                                    <h3>{{ currentArtist.album }}</h3>
                                    <p class="artist">{{ currentArtist.artist }}</p>
                                    <p class="year">{{ currentArtist.year }}</p>
                                </div>
                            </div>
                            <div class="streaming-links">
                                <a v-if="currentArtist.spotify_link" :href="currentArtist.spotify_link" target="_blank"
                                    class="stream-link spotify" title="Auf Spotify hören">
                                    <Icon name="mdi:spotify" size="36" />
                                </a>
                                <a v-if="currentArtist.apple_music_link" :href="currentArtist.apple_music_link"
                                    target="_blank" class="stream-link apple" title="Auf Apple Music hören">
                                    <Icon name="mdi:apple" size="36" />
                                </a>
                                <a v-if="currentArtist.deezer_link" :href="currentArtist.deezer_link" target="_blank"
                                    class="stream-link deezer" title="Auf Deezer hören">
                                    <Icon name="simple-icons:deezer" size="36" />
                                </a>
                            </div>
                        </div>

                        <!-- Trivia Information -->
                        <div class="trivia-box">
                            <h3>Wusstest du schon?</h3>
                            <p>{{ currentQuestion.trivia }}</p>
                        </div>

                        <button @click="nextQuestion" class="next-button">
                            <span>Nächste Frage</span>
                            <Icon name="material-symbols:arrow-forward" />
                        </button>
                    </div>
                </div>
            </div>

            <!-- Endscreen -->
            <div v-else class="game-end-screen">
                <h2>Spiel beendet!</h2>

                <div class="final-score">
                    <h3>Deine Gesamtpunktzahl:</h3>
                    <p class="points">{{ totalPoints }} Punkte</p>
                </div>

                <div class="reward-section">
                    <div class="record-icon" :class="recordClass">
                        <Icon v-if="earnedRecord" :name="recordIcon" size="64" />
                    </div>
                    <p class="reward-text">
                        <template v-if="allQuestionsCorrect">
                            {{ goldMessages[Math.floor(Math.random() * goldMessages.length)] }}
                        </template>
                        <template v-else-if="correctAnswers >= (maxQuestions * 0.75)">
                            {{ silverMessages[Math.floor(Math.random() * silverMessages.length)] }}
                        </template>
                        <template v-else-if="correctAnswers >= (maxQuestions * 0.5)">
                            {{ bronzeMessages[Math.floor(Math.random() * bronzeMessages.length)] }}
                        </template>
                        <template v-else>
                            {{ participationMessages[Math.floor(Math.random() * participationMessages.length)] }}
                        </template>
                    </p>
                </div>

                <div class="end-actions">
                    <button @click="restartGame" class="button restart-button">
                        Nochmal spielen
                    </button>
                    <NuxtLink to="/gamehome" class="button home-button">
                        Zurück zum Hauptmenü
                    </NuxtLink>
                </div>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
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

// Gemeinsamer Joker-Count
const totalJokers = difficulty === 'easy' ? 3 : difficulty === 'medium' ? 5 : 7
const remainingJokers = ref(totalJokers)

const audienceHelp = ref<{ [key: string]: number }>({})
const jokerUsedForCurrentQuestion = ref(false)
const hiddenOptions = ref<string[]>([])

const phoneExpertOpinion = ref<{ expert: string; message: string } | null>(null)
const phoneExpertConfidence = ref(0)

// Musikspezifische Experten-Antworten
const expertResponses = {
    high: [
        "Ohne jeden Zweifel - es ist '{answer}'. Ich habe die Original-Aufnahme-Session dokumentiert.",
        "Als langjähriger Produzent des Labels kann ich dir garantieren: Das ist '{answer}'.",
        "Oh, das kenne ich in- und auswendig! '{answer}' - darauf verwette ich meinen Plattenspieler.",
        "Diese Frage ist ein Heimspiel für mich. Eindeutig '{answer}', ich war beim Recording dabei.",
        "Das ist mein absolutes Lieblingsalbum! Natürlich ist es '{answer}'.",
        "Diese Aufnahme hat Geschichte geschrieben - definitiv '{answer}'.",
        "Ich habe den Song hunderte Male aufgelegt. Ohne Frage '{answer}'.",
        "Diese Produktion ist legendär! Kann nur '{answer}' sein.",
        "Da muss ich nicht mal nachdenken - '{answer}', zu 100%!",
        "Diese Aufnahme hat mein Leben verändert. Es ist '{answer}'.",
        "Diesen Sound würde ich unter Tausenden erkennen - '{answer}'!",
        "Das war damals DER Hit schlechthin. Eindeutig '{answer}'.",
        "Diese Frage ist fast zu einfach - natürlich '{answer}'!",
        "Oh ja, ein Klassiker! Definitiv '{answer}'.",
        "Diese Aufnahme ist unverkennbar - '{answer}'.",
        "Da bin ich mir absolut sicher: '{answer}'.",
        "Das ist einer meiner All-Time-Favorites: '{answer}'.",
        "Diese Session ist legendär - eindeutig '{answer}'.",
        "Ein Meilenstein der Musikgeschichte: '{answer}'.",
        "Diese Produktion ist einzigartig - kann nur '{answer}' sein."
    ],
    medium: [
        "Moment... ja, ich glaube das müsste '{answer}' sein. Die Produktion kommt mir sehr bekannt vor.",
        "Wenn mich mein Gehör nicht täuscht, würde ich auf '{answer}' tippen.",
        "Hmm, der Sound erinnert mich stark an '{answer}', aber lass mich kurz nachdenken...",
        "Das klingt sehr nach '{answer}', aber es gab damals einige ähnliche Produktionen.",
        "Ich würde zu 70% sagen '{answer}', aber nagel mich nicht darauf fest.",
        "Kenne ich aus dem Club - sollte '{answer}' sein, wenn ich mich recht erinnere.",
        "Hatte ich mal in meiner Sammlung... '{answer}', oder?",
        "Das läuft öfter im Radio - müsste '{answer}' sein.",
        "Ziemlich sicher '{answer}', aber keine Garantie.",
        "Erinnert mich stark an '{answer}', bin aber nicht ganz sicher.",
        "Mein Bauchgefühl sagt '{answer}', aber schwören würde ich nicht drauf.",
        "Klingt sehr nach '{answer}', könnte mich aber auch täuschen.",
        "War das nicht '{answer}'? Bin mir aber nicht hundertprozentig sicher.",
        "Ich tippe auf '{answer}', aber es gibt ähnliche Tracks.",
        "Das müsste '{answer}' sein, aber quote mich nicht darauf.",
        "Spontan würde ich '{answer}' sagen, aber lass mich nochmal überlegen...",
        "Klingt vertraut... wahrscheinlich '{answer}'.",
        "Ich tendiere zu '{answer}', aber ganz sicher bin ich nicht.",
        "Könnte gut '{answer}' sein, aber keine Gewähr.",
        "Ich meine, das ist '{answer}', aber don't quote me on that!"
    ],
    low: [
        "Puh, schwierige Frage... spontan würde ich '{answer}' raten, aber das ist echt nur geraten.",
        "Oh Mann, das ist nicht meine Ära... vielleicht '{answer}'?",
        "Musik ist normalerweise mein Ding, aber hier... '{answer}' maybe?",
        "*kratzt sich am Kopf* '{answer}'? Aber das ist wirklich nur eine Vermutung!",
        "Wenn ich jetzt raten müsste... '{answer}'? Aber ich bin mir echt unsicher.",
        "Das ist nicht meine Expertise, aber könnte '{answer}' sein?",
        "Uff, da fragst du den Falschen... '{answer}' vielleicht?",
        "Keine Ahnung, aber '{answer}' klingt plausibel?",
        "Schwer zu sagen... '{answer}'? Aber das ist echt nur geraten!",
        "Da bin ich überfragt... '{answer}' würde ich mal tippen.",
        "*nervöses Lachen* Vielleicht '{answer}'?",
        "Boah, das ist aber eine harte Nuss... '{answer}'?",
        "Mein Musikwissen lässt mich hier im Stich... '{answer}'?",
        "Das ist nicht meine Stärke, aber eventuell '{answer}'?",
        "Tut mir leid, aber da kann ich nur raten... '{answer}'?",
        "*schwitzt* Äh... '{answer}'?",
        "Oh je, das ist nicht mein Spezialgebiet... '{answer}'?",
        "Da muss ich passen... '{answer}' vielleicht?",
        "Schwierig... spontan würde ich '{answer}' sagen, aber...",
        "Ohne Gewähr, aber könnte '{answer}' sein?"
    ]
}

// Zufällige Expertenbezeichnungen
const expertTitles = [
    "Dr. Schmidt",
    "Thomas",
    "Sarah",
    "Michael",
    "Lisa",
    "Mark",
    "Alex",
    "Julia",
    "Chris",
    "Max",
    "Emma",
    "David",
    "Sophie",
    "Felix",
    "Laura"
]

const useFiftyFiftyJoker = () => {
    if (remainingJokers.value > 0 && !jokerUsedForCurrentQuestion.value) {
        const wrongOptions = currentQuestion.value.options.filter(
            (option: string) => option !== currentQuestion.value.correctAnswer
        )
        const shuffledWrongOptions = wrongOptions.sort(() => Math.random() - 0.5)
        hiddenOptions.value = shuffledWrongOptions.slice(0, 2)

        remainingJokers.value--
        jokerUsedForCurrentQuestion.value = true
    }
}

const useAudienceJoker = () => {
    if (remainingJokers.value > 0 && !jokerUsedForCurrentQuestion.value) {
        const correctIndex = currentQuestion.value.options.indexOf(currentQuestion.value.correctAnswer)
        const distribution = Array(currentQuestion.value.options.length).fill(0).map((_, i) => {
            return i === correctIndex ? Math.floor(Math.random() * 30) + 50 : Math.floor(Math.random() * 20)
        })

        const total = distribution.reduce((acc, val) => acc + val, 0)
        audienceHelp.value = currentQuestion.value.options.reduce((acc: { [key: string]: number }, option: string, i: number) => {
            acc[option] = Math.round((distribution[i] / total) * 100)
            return acc
        }, {} as { [key: string]: number })

        remainingJokers.value--
        jokerUsedForCurrentQuestion.value = true
    }
}

const usePhoneJoker = () => {
    if (remainingJokers.value > 0 && !jokerUsedForCurrentQuestion.value) {
        const random = Math.random()
        let answer, confidence, confidenceLevel

        if (random < 0.6) {
            confidence = Math.floor(Math.random() * 15) + 85
            answer = currentQuestion.value.correctAnswer
            confidenceLevel = 'high'
        } else if (random < 0.8) {
            confidence = Math.floor(Math.random() * 20) + 60
            answer = Math.random() < 0.8 ? currentQuestion.value.correctAnswer :
                currentQuestion.value.options.find((o: string) => o !== currentQuestion.value.correctAnswer)
            confidenceLevel = 'medium'
        } else {
            confidence = Math.floor(Math.random() * 25) + 35
            answer = Math.random() < 0.5 ? currentQuestion.value.correctAnswer :
                currentQuestion.value.options.find((o: string) => o !== currentQuestion.value.correctAnswer)
            confidenceLevel = 'low'
        }

        const responses = expertResponses[confidenceLevel as keyof typeof expertResponses]
        const responseTemplate = responses[Math.floor(Math.random() * responses.length)]
        const expertTitle = expertTitles[Math.floor(Math.random() * expertTitles.length)]

        phoneExpertOpinion.value = {
            expert: expertTitle,
            message: responseTemplate.replace('{answer}', answer)
        }
        phoneExpertConfidence.value = confidence

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
    jokerUsedForCurrentQuestion.value = false
    audienceHelp.value = {}
    hiddenOptions.value = []
    phoneExpertOpinion.value = null
    phoneExpertConfidence.value = 0
    startQuestionTimer()
}

const showSolution = ref(false)
const isCorrectAnswer = ref(false)

const currentArtist = ref<any>(null)

// Konstanten für Zeitbonus
const BASE_POINTS = 50
const MAX_TIME_BONUS = 100 // Erhöht auf 100
const TIME_LIMIT = 30000 // 30 Sekunden für maximalen Bonus

const questionStartTime = ref(0)

// Starte Timer wenn Frage angezeigt wird
const startQuestionTimer = () => {
    questionStartTime.value = Date.now()
}

const calculateTimeBonus = () => {
    const timeElapsed = Date.now() - questionStartTime.value
    const timePercentage = Math.max(0, 1 - (timeElapsed / TIME_LIMIT))
    const timeBonus = Math.floor(timePercentage * MAX_TIME_BONUS)
    return timeBonus
}

const pointsDisplay = ref<any>(null)

// Funktion zum Scrollen nach oben
const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: smoothScrollBehavior.value
    })
}

const totalPoints = ref(0)

// Funktion zum Laden der Künstlerinformationen
const loadCurrentArtist = async () => {
    try {

        // JSON-Datei laden
        const response = await import(`~/json/genres/${locale.value}/${category}.json`)
        currentArtist.value = response.default.find((artist: {
            artist: string;
            questions: { [key: string]: any[] }
        }) => {
            // Alle Fragen des Künstlers für die aktuelle Schwierigkeit
            const artistQuestions = artist.questions[difficulty]

            // Prüfen ob die aktuelle Frage in den Fragen des Künstlers vorkommt
            const hasQuestion = artistQuestions.some(q =>
                q.question === currentQuestion.value.question &&
                q.correctAnswer === currentQuestion.value.correctAnswer
            )

            return hasQuestion
        })


        // Audio initialisieren wenn Künstler gefunden
        if (currentArtist.value && audioPlayer.value) {
            audioPlayer.value.src = currentArtist.value.preview_link // Hier war der Fehler - preview_link statt audioSrc
            audioPlayer.value.load()
            currentTime.value = 0
            duration.value = 0
            isPlaying.value = false
        }
    } catch (error) {
        currentArtist.value = null
    }
}

// Wenn sich die Frage ändert, lade die entsprechenden Künstlerinformationen
watch(() => currentQuestion.value, (newQuestion) => {
    if (newQuestion) {
        loadCurrentArtist()
    }
}, { immediate: true })

// Bei der Antwortauswahl
const selectAnswer = async (selectedAnswer: string) => {
    if (showSolution.value) return

    isCorrectAnswer.value = selectedAnswer === currentQuestion.value.correctAnswer
    showSolution.value = true

    if (isCorrectAnswer.value) {
        const timeBonus = calculateTimeBonus()
        updatePoints(BASE_POINTS, timeBonus)
        correctAnswers.value++
    }

    await loadCurrentArtist()

    await nextTick()
    scrollToTop()
}

const nextQuestion = () => {
    if (usedQuestions.value.length >= maxQuestions.value) {
        gameFinished.value = true
        return
    }

    showSolution.value = false
    hiddenOptions.value = []
    phoneExpertOpinion.value = null
    audienceHelp.value = {}
    jokerUsedForCurrentQuestion.value = false

    selectRandomQuestion()
    scrollToTop()
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

const correctAnswers = ref(0)

const gameFinished = ref(false)

watch(() => usedQuestions.value.length, (newLength) => {
    if (newLength >= maxQuestions.value) {
        gameFinished.value = true
    }
})

const allQuestionsCorrect = computed(() => correctAnswers.value === maxQuestions.value)

const restartGame = () => {
    usedQuestions.value = []
    correctAnswers.value = 0
    totalPoints.value = 0
    pointsDisplay.value?.resetPoints()
    loadQuestions()
}

const earnedRecord = computed(() => correctAnswers.value >= (maxQuestions.value * 0.5))
const recordIcon = computed(() => {
    if (allQuestionsCorrect.value) return 'material-symbols:album-gold'
    if (correctAnswers.value >= (maxQuestions.value * 0.75)) return 'material-symbols:album-silver'
    if (correctAnswers.value >= (maxQuestions.value * 0.5)) return 'material-symbols:album-bronze'
    return ''
})

const recordClass = computed(() => {
    if (allQuestionsCorrect.value) return 'gold'
    if (correctAnswers.value >= (maxQuestions.value * 0.75)) return 'silver'
    if (correctAnswers.value >= (maxQuestions.value * 0.5)) return 'bronze'
    return ''
})

// Audio Player Refs und Computed Properties
const audioPlayer = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const audioLoaded = ref(false)

// Debug-Funktion
const logAudioState = () => {
    console.log('Audio State:', {
        src: audioPlayer.value?.src,
        isPlaying: isPlaying.value,
        currentTime: currentTime.value,
        duration: duration.value,
        loaded: audioLoaded.value,
        readyState: audioPlayer.value?.readyState,
        artist: currentArtist.value?.artist,
        preview_link: currentArtist.value?.preview_link
    })
}

// Audio Player initialisieren
onMounted(() => {
    audioPlayer.value = new Audio()

    // Event Listener
    audioPlayer.value.addEventListener('loadeddata', () => {
        audioLoaded.value = true
    })

    audioPlayer.value.addEventListener('timeupdate', () => {
        if (audioPlayer.value) {
            currentTime.value = audioPlayer.value.currentTime
        }
    })

    audioPlayer.value.addEventListener('ended', () => {
        isPlaying.value = false
        currentTime.value = 0
    })

    audioPlayer.value.addEventListener('error', (e) => {
        isPlaying.value = false
        audioLoaded.value = false
    })
})

// Play/Pause Toggle
const togglePlay = async () => {
    if (!audioPlayer.value || !currentArtist.value?.preview_link) {
        return
    }

    try {
        // Wenn die Audio-Quelle sich geändert hat oder noch nicht gesetzt wurde
        if (audioPlayer.value.src !== currentArtist.value.preview_link) {
            audioPlayer.value.src = currentArtist.value.preview_link
            await audioPlayer.value.load()
            audioLoaded.value = false
        }

        if (isPlaying.value) {
            await audioPlayer.value.pause()
        } else {
            const playPromise = audioPlayer.value.play()
            if (playPromise !== undefined) {
                await playPromise
            }
        }

        isPlaying.value = !isPlaying.value
    } catch (error) {
        isPlaying.value = false
    }
}

// Watch für currentArtist
watch(() => currentArtist.value, (newArtist) => {
    if (audioPlayer.value && newArtist?.preview_link) {
        audioPlayer.value.pause()
        isPlaying.value = false
        currentTime.value = 0
        audioLoaded.value = false

        audioPlayer.value.src = newArtist.preview_link
        audioPlayer.value.load()
    }
}, { immediate: true })

// Cleanup
onUnmounted(() => {
    if (audioPlayer.value) {
        audioPlayer.value.pause()
        audioPlayer.value.src = ''
        audioPlayer.value.remove()
    }
})

// Wenn zur nächsten Frage gewechselt wird, Audio stoppen
watch(() => currentQuestion.value, () => {
    if (audioPlayer.value) {
        audioPlayer.value.pause()
        isPlaying.value = false
        currentTime.value = 0

        // Neuen Audio Player für die neue Frage erstellen
        if (currentArtist.value?.audioSrc) {
            audioPlayer.value.src = currentArtist.value.audioSrc
            audioPlayer.value.load()
        }
    }
})

// Progress Bar Update verbessern
const updateProgress = () => {
    if (audioPlayer.value) {
        currentTime.value = audioPlayer.value.currentTime
        duration.value = audioPlayer.value.duration
    }
}

// Event Listener für Progress Bar
onMounted(() => {
    audioPlayer.value = new Audio()

    // Bestehende Event Listener
    audioPlayer.value.addEventListener('loadeddata', () => {
        audioLoaded.value = true
        if (audioPlayer.value) {
            duration.value = audioPlayer.value.duration
        }
    })

    // Progress Bar Update häufiger ausführen
    audioPlayer.value.addEventListener('timeupdate', updateProgress)

})


const points = ref(0)
const isAnimating = ref(false)
const showBonus = ref(false)
const latestBonus = ref<{ base: number; time: number; total: number }>({ base: 0, time: 0, total: 0 })

const formattedPoints = computed(() => {
    return points.value.toLocaleString()
})

const updatePoints = (basePoints: number, timeBonus: number) => {
    latestBonus.value = {
        base: basePoints,
        time: timeBonus,
        total: basePoints + timeBonus
    }
    showBonus.value = true
    isAnimating.value = true

    points.value += latestBonus.value.total
    totalPoints.value = points.value

    setTimeout(() => {
        showBonus.value = false
        isAnimating.value = false
    }, 2000)
}

const goldMessages = [
    "Unglaublich! Du hast eine Goldene LP gewonnen! 🏆\nDu bist ein absoluter Musik-Champion! Alle Fragen perfekt beantwortet - das schaffen nur die Besten der Besten!",
    "Sensationell! Eine Goldene LP ist dein! 🏆\nDeine Musikkenntnis ist wirklich außergewöhnlich - eine makellose Vorstellung!",
    "Wahnsinn! Die Goldene LP gehört dir! 🏆\nDu bist ein wandelndes Musik-Lexikon! Eine perfekte Runde - einfach grandios!",
    "Fantastisch! Du hast die Goldene LP mehr als verdient! 🏆\nDeine Performance war einfach makellos - du bist ein echter Musik-Virtuose!",
    "Meisterhaft! Die Goldene LP ist dein! 🏆\nEine perfekte Runde - du bist definitiv ein Musik-Genie!",
    "Brillant! Eine Goldene LP für dich! 🏆\nDeine Musikexpertise ist wirklich beeindruckend - alle Fragen richtig!",
    "Phänomenal! Die Goldene LP gehört dir! 🏆\nDu bist ein wahrer Musik-Kenner - eine makellose Vorstellung!",
    "Grandios! Du hast dir die Goldene LP erspielt! 🏆\nEine perfekte Runde - dein Musikwissen ist unschlagbar!",
    "Überragend! Die Goldene LP ist dein! 🏆\nDu bist ein absoluter Musik-Profi - alle Fragen fehlerfrei beantwortet!",
    "Legendär! Du hast die Goldene LP gewonnen! 🏆\nEine perfekte Performance - du bist ein echter Musik-Maestro!"
]

const silverMessages = [
    "Hervorragend! Du hast eine Silberne LP gewonnen! 🥈\nWas für eine starke Leistung! Du bist schon fast ein Musik-Experte. Mit ein bisschen Feinschliff holst du dir beim nächsten Mal bestimmt Gold!",
    "Klasse! Eine Silberne LP für dich! 🥈\nDein Musikwissen ist beachtlich! Nur noch ein kleiner Schritt bis zur Goldenen LP!",
    "Super! Die Silberne LP gehört dir! 🥈\nDu kennst dich richtig gut aus! Beim nächsten Mal schaffst du bestimmt die perfekte Runde!",
    "Toll gemacht! Eine Silberne LP ist dein! 🥈\nDeine Musikkenntnis ist beeindruckend! Gold ist zum Greifen nah!",
    "Ausgezeichnet! Du hast die Silberne LP gewonnen! 🥈\nDas war eine sehr starke Vorstellung! Fast perfekt!",
    "Großartig! Eine Silberne LP für deine Leistung! 🥈\nDu bist auf dem besten Weg zum Musik-Champion!",
    "Stark! Die Silberne LP hast du dir verdient! 🥈\nDein Musikwissen kann sich sehen lassen! Gold ist das nächste Ziel!",
    "Prima! Eine Silberne LP für dich! 🥈\nDu bist ein echter Musik-Kenner! Nur noch ein kleiner Schritt bis zur Perfektion!",
    "Respekt! Die Silberne LP ist dein! 🥈\nDeine Performance war richtig gut! Gold ist in Reichweite!",
    "Beeindruckend! Du hast dir die Silberne LP erspielt! 🥈\nDas war eine tolle Leistung! Beim nächsten Mal holst du dir Gold!"
]

const bronzeMessages = [
    "Klasse! Du hast eine Bronzene LP gewonnen! 🥉\nDein Musikwissen kann sich sehen lassen! Mach weiter so, und schon bald wirst du noch mehr Hits erkennen!",
    "Gut gemacht! Eine Bronzene LP für dich! 🥉\nDu bist auf einem guten Weg! Weiter so, dann klappt's auch bald mit Silber!",
    "Prima! Die Bronzene LP gehört dir! 🥉\nDu hast schon einiges drauf! Mit etwas Übung erreichst du noch mehr!",
    "Bravo! Eine Bronzene LP ist dein! 🥉\nDu entwickelst dich zum echten Musikkenner! Bleib dran!",
    "Super! Du hast die Bronzene LP gewonnen! 🥉\nDein Musikwissen wächst! Mach weiter so!",
    "Toll! Eine Bronzene LP für deine Leistung! 🥉\nDu bist auf dem richtigen Weg! Weiter so!",
    "Schön! Die Bronzene LP hast du dir verdient! 🥉\nDu machst Fortschritte! Bleib am Ball!",
    "Sehr gut! Eine Bronzene LP für dich! 🥉\nDu kennst dich schon gut aus! Weiter so!",
    "Klasse! Die Bronzene LP ist dein! 🥉\nDu bist auf einem guten Weg! Mach weiter so!",
    "Gut! Du hast dir die Bronzene LP erspielt! 🥉\nDein Musikwissen entwickelt sich prima! Bleib dran!"
]

const participationMessages = [
    "Das war ein guter Anfang! 💪\nJeder Musikexperte hat mal klein angefangen. Lass uns gleich noch eine Runde spielen!",
    "Weiter so! 💪\nMit jeder Runde lernst du neue Songs kennen. Probier's gleich nochmal!",
    "Nicht aufgeben! 💪\nDu bist auf dem richtigen Weg! Übung macht den Meister!",
    "Kopf hoch! 💪\nJeder fängt mal an! Mit der Zeit wird dein Musikwissen wachsen!",
    "Bleib dran! 💪\nMit jeder Runde lernst du dazu! Versuch's gleich nochmal!",
    "Das wird schon! 💪\nÜbung macht den Musik-Meister! Auf in die nächste Runde!",
    "Guter Versuch! 💪\nMit der Zeit wirst du immer besser! Mach weiter so!",
    "Nicht schlecht! 💪\nJeder Start ist ein Schritt nach vorn! Weiter so!",
    "Das ist der Anfang! 💪\nMit jeder Runde wächst dein Wissen! Bleib dran!",
    "Mach weiter! 💪\nAus jedem Spiel lernst du etwas Neues! Nächste Runde!"
]


</script>

<style lang="scss" scoped>
@mixin section-heading {
    font-size: clamp(1.2rem, 3.5vw, 1.5rem);
    color: var(--text-color);
    text-align: center;
    margin-bottom: var(--padding-medium);
}

.game-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--padding-small);
    padding: 0 var(--padding-small);

    .header-left {
        text-align: left;

        h1 {
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            color: var(--text-color);
            margin: 0;
            margin-bottom: var(--padding-small);
        }

        .round-counter {
            font-size: clamp(1.1rem, 3.5vw, 1.5rem);
            color: var(--text-color);
            margin: 0;
            font-weight: 600;
        }
    }

    .header-right {
        display: flex;
        align-items: flex-start;
        font-size: clamp(1.2rem, 3vw, 1.8rem);
    }
}


/* Add scoped styles here */
.difficulty {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
}

.question {
    h2 {
        font-size: clamp(1.2rem, 3.5vw, 1.5rem);
        text-align: center;
        margin-bottom: var(--padding-medium);
    }
}

.options {
    display: flex;
    flex-direction: column;
    gap: var(--padding-small);
    width: 100%;
    margin-bottom: var(--padding-medium);
}

.option-button {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    font-weight: 600;
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    padding: var(--padding-small) var(--padding-medium);

    &::before {
        content: '';
        position: absolute;
        inset: 0;
        background: var(--highlight-color);
        opacity: 0;
        transition: opacity var(--transition-speed);
        z-index: -1;
    }

    &:hover::before,
    &:focus-visible::before {
        opacity: 0.2;
    }

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }
}

.jokers-section {
    display: flex;
    flex-direction: column;
    align-items: center;

    .joker-buttons {
        display: flex;
        gap: var(--padding-medium);
        margin: var(--padding-small) 0;

        @media (width >=768px) {
            gap: var(--padding-large);
        }
    }

    @media (width >=768px) {
        margin: 0;
    }
}

.joker-button {
    border-radius: 50%;
    background: var(--primary-color);
    transition: all var(--transition-speed);
    padding: 1rem;

    .icon {
        transition: color var(--transition-speed);
    }

    &:not(:disabled):hover {
        transform: translateY(-2px);
        background: var(--highlight-color);
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    &.disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: var(--surface-color);
        border: 1px solid rgb(255 255 255 / 10%);
        color: rgb(255 255 255 / 50%);
    }
}

.joker-count {
    font-size: clamp(0.875rem, 3vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
}

.solution-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.content-wrapper {
    background: var(--background-secondary);
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result-banner {
    background: var(--error-color, #ff4757);
    color: white;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 20px;
    margin-left: auto;
    margin-right: auto;

    .result-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;

        h2 {
            margin: 0;
            font-size: 1.125em;
        }

        .result-icon {
            flex-shrink: 0;
        }
    }

    .points {
        font-size: 1.1em;
        opacity: 0.9;
        margin-bottom: 8px;
    }

    .correct-answer {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);

        .label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 6px;
            display: block;
        }

        .text {
            font-size: 1em;
            font-weight: 500;
        }
    }

    &.correct {
        background: #0D7A3D;
    }
}

.answer-box {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

    .label {
        display: block;
        color: var(--text-secondary);
        margin-bottom: 8px;
        font-size: 0.9em;
    }

    .text {
        color: var(--text-primary);
        font-size: 1.2em;
        font-weight: 600;
    }
}

.album-box {
    max-width: 320px;
    margin: 0 auto 20px;

    .cover-wrapper {
        position: relative;
        margin-bottom: 8px;

        img {
            width: 100%;
            height: auto;
            border-radius: 4px;
            display: block;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
    }

    .player-info-wrapper {
        padding: 0 4px;
    }

    .audio-player {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 4px;
        margin: 8px 0;

        .play-button {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            padding: 0;

            &:hover:not(:disabled) {
                background: var(--primary-dark);
                transform: scale(1.05);
            }

            &:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
        }

        .progress-bar {
            flex-grow: 1;
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            overflow: hidden;
            cursor: pointer;
            position: relative;

            &:hover {
                height: 6px;
                margin: -1px 0;
            }

            .progress {
                height: 100%;
                background: var(--primary-color);
                transition: width 0.1s linear;
                position: absolute;
                left: 0;
                top: 0;
            }
        }
    }

    .info {
        text-align: center;
        color: white;

        h3 {
            margin: 0 0 2px 0;
            font-size: 0.9em;
            font-weight: 600;
        }

        .artist {
            margin: 0 0 1px 0;
            font-size: 0.8em;
            opacity: 0.9;
        }

        .year {
            margin: 0;
            font-size: 0.75em;
            opacity: 0.7;
        }
    }

    .streaming-links {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);

        .stream-link {
            color: rgba(255, 255, 255, 0.7);
            transition: all 0.2s ease;
            padding: 6px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;

            &:hover {
                color: white;
                transform: translateY(-1px);
            }

            .icon {
                width: 20px;
                height: 20px;
            }

            &.spotify:hover {
                color: #1DB954;
            }

            &.apple:hover {
                color: #FA57C1;
            }

            &.deezer:hover {
                color: #FF0092;
            }
        }
    }
}

.trivia-box {
    background: var(--background-secondary);
    border-radius: 12px;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h3 {
        color: var(--primary-color);
        margin: 0 0 12px 0;
        font-size: 1.2em;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-color);
        font-size: 1em;
    }
}

.play-button {
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);

    &:hover {
        transform: scale(1.05);
        background: var(--primary-dark);
    }
}

.trivia-box {
    background: white;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

    h3 {
        @include section-heading;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-secondary);
        font-size: 1.1em;
    }
}

.next-button {
    width: 100%;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 1.2em;
    font-weight: 600;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    &:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
    }

    .icon {
        font-size: 24px;
    }
}

.game-end-screen {
    text-align: center;
    max-width: var(--content-width);
    margin: 0 auto;

    .reward-section {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-large);
        box-shadow: var(--box-shadow);
        border: 1px solid rgb(255 255 255 / 10%);

        .record-icon {
            transition: transform var(--transition-speed);

            &:hover {
                transform: rotate(20deg);
            }
        }
    }

}

.audience-help {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-large);
    margin: var(--padding-medium) 0;

    h3 {
        font-size: clamp(1.2rem, 3.5vw, 1.5rem);
        margin-bottom: var(--padding-medium);
        text-align: center;
    }

    .audience-bars {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        margin: 0 auto;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .option-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 4px;
    }

    .option-text {
        font-size: 1.25rem;
    }

    .percentage-text {
        font-size: 0.9rem;
        opacity: 0.8;
    }

    .bar-container {
        background: rgb(255 255 255 / 8%);
        border-radius: 4px;
        height: 12px;
        overflow: hidden;
    }

    .bar {
        height: 100%;
        transition: width 1s ease;

        &.high {
            background-color: var(--success-color);
        }

        &.medium {
            background-color: var(--primary-color);
        }

        &.low {
            background-color: var(--error-color);
        }
    }
}

.phone-expert {
    margin: var(--padding-medium) 0;

    h3 {
        @include section-heading;
    }

    .expert-message {
        background: rgb(255 255 255 / 5%);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        border: 1px solid rgb(255 255 255 / 10%);
    }

    .expert-header {
        display: flex;
        align-items: center;
        gap: var(--padding-small);
        margin-bottom: var(--padding-medium);
        padding-bottom: var(--padding-small);
        border-bottom: 1px solid rgb(255 255 255 / 10%);

        .phone-icon {
            font-size: clamp(1.5rem, 4vw, 2rem);
            color: var(--primary-color);
        }

        .expert-name {
            font-size: clamp(1.1rem, 3vw, 1.3rem);
            font-weight: 600;
            color: var(--text-color);
        }
    }

    .message-content {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
    }

    .confidence-bar-container {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .confidence-bar {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        height: 8px;
        overflow: hidden;
        position: relative;

        .confidence-level {
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: var(--confidence);
            transition: width 1s var(--transition-bounce);

            .high & {
                background: linear-gradient(90deg, var(--success-color), var(--highlight-color));
            }

            .medium & {
                background: linear-gradient(90deg, var(--primary-color), var(--highlight-color));
            }

            .low & {
                background: linear-gradient(90deg, var(--error-color), var(--secondary-color));
            }
        }
    }
}

.confidence-text {
    font-size: clamp(0.9rem, 2.5vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
    text-align: right;
}


.trivia-box {
    background: var(--background-secondary);
    border-radius: 12px;
    margin-top: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    h3 {
        color: var(--primary-color);
        margin: 0 0 12px 0;
        font-size: 1.2em;
        text-align: center;
    }

    p {
        margin: 0;
        line-height: 1.6;
        color: var(--text-color);
        font-size: 1em;
    }
}

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
}

.points {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: bold;
    color: var(--text-color);
    transition: transform 0.3s ease;

    &.points-update {
        transform: scale(1.2);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: var(--body-font-size);
    color: var(--text-color);
}

.bonus-indicator {
    position: absolute;
    top: -40px;
    right: 0;
    background: rgba(0, 0, 0, 0.8);
    padding: 8px 12px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    .bonus-total {
        color: #FFD700;
        font-weight: bold;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 4px;
    }

    .bonus-breakdown {
        display: flex;
        gap: 8px;
        font-size: 0.8em;

        .time {
            color: var(--highlight-color);
        }
    }
}

.points-breakdown {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;

    .points-row {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;

        &:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        &.total {
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 4px;
            padding-top: 8px;
            border-top: 2px solid rgba(255, 255, 255, 0.2);
        }
    }
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.bonus-enter-from {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
}

.bonus-leave-to {
    opacity: 0;
    transform: translateY(-20px) scale(0.8);
}

.points-update {
    animation: pointsPulse 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes pointsPulse {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.2);
        color: var(--highlight-color);
    }

    100% {
        transform: scale(1);
    }
}
</style>
