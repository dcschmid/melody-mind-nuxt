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
                            <ShowPoints ref="pointsDisplay" class="points-display" />
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
                                    <div class="option-text">{{ option }}</div>
                                    <div class="bar-container">
                                        <div class="bar" :style="{ width: `${percentage}%` }" :class="{
                                            'high': percentage >= 70,
                                            'medium': percentage >= 40 && percentage < 70,
                                            'low': percentage < 40
                                        }">
                                            <span class="percentage">{{ percentage }}%</span>
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
                                    title="50:50 Joker">
                                    <Icon name="material-symbols:balance" size="30" />
                                </button>

                                <!-- Publikumsjoker -->
                                <button class="button joker-button" @click="useAudienceJoker"
                                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                    title="Publikumsjoker">
                                    <Icon name="formkit:people" size="30" />
                                </button>

                                <!-- Telefonjoker -->
                                <button class="button joker-button" @click="usePhoneJoker"
                                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                    title="Telefonjoker">
                                    <Icon name="gg:phone" size="30" />
                                </button>
                            </div>
                            <span class="joker-count">Verbleibend: {{ remainingJokers }}</span>
                        </div>
                    </div>
                </div>
                <div v-else class="solution-container">
                    <div class="result-banner" :class="{ 'correct': isCorrectAnswer }">
                        <div class="result-content">
                            <div class="result-header">
                                <Icon
                                    :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                                    class="result-icon" aria-hidden="true" />
                                <h2>{{ isCorrectAnswer ? 'Richtig!' : 'Leider falsch!' }}</h2>
                            </div>

                            <div class="points-info">
                                <p v-if="isCorrectAnswer">
                                    <span class="base-points">+{{ BASE_POINTS }} Punkte</span>
                                </p>
                                <p v-else class="no-points">+0 Punkte</p>
                            </div>

                            <div class="correct-answer">
                                <div class="label">Richtige Antwort:</div>
                                <div class="answer">{{ currentQuestion.correctAnswer }}</div>
                            </div>
                        </div>
                    </div>

                    <div v-if="currentArtist" class="song-details">
                        <div class="cover-and-player">
                            <div class="cover-container" v-if="currentArtist.coverSrc">
                                <img :src="currentArtist.coverSrc"
                                    :alt="`${currentArtist.artist} - ${currentArtist.album}`">
                            </div>

                            <div class="preview-player">
                                <audio controls :src="currentArtist.preview_link"></audio>
                            </div>
                        </div>

                        <div class="song-info">
                            <div class="metadata">
                                <h3>{{ currentArtist.album }}</h3>
                                <p class="artist">{{ currentArtist.artist }}</p>
                                <p class="year">{{ currentArtist.year }}</p>
                            </div>

                            <div class="music-links">
                                <a v-if="currentArtist.spotify_link" :href="currentArtist.spotify_link" target="_blank"
                                    class="button music-link spotify">
                                    <Icon name="mdi:spotify" />
                                    <span>Auf Spotify hören</span>
                                </a>
                                <a v-if="currentArtist.apple_music_link" :href="currentArtist.apple_music_link"
                                    target="_blank" class="button music-link apple">
                                    <Icon name="mdi:apple" />
                                    <span>Auf Apple Music hören</span>
                                </a>
                                <a v-if="currentArtist.deezer_link" :href="currentArtist.deezer_link" target="_blank"
                                    class="button music-link deezer">
                                    <Icon name="simple-icons:deezer" />
                                    <span>Auf Deezer hören</span>
                                </a>
                            </div>
                        </div>

                        <div class="trivia">
                            <h3>Wusstest du schon?</h3>
                            <p>{{ currentQuestion.trivia }}</p>
                        </div>
                    </div>

                    <button @click="nextQuestion" class="button next-button">
                        <span>Nächste Frage</span>
                        <Icon name="material-symbols:arrow-forward-rounded" />
                    </button>
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
                            Unglaublich! Du hast eine Goldene LP gewonnen! 🏆
                            <br>Du bist ein absoluter Musik-Champion! Alle Fragen perfekt beantwortet - das schaffen nur
                            die Besten der Besten!
                        </template>
                        <template v-else-if="correctAnswers >= (maxQuestions * 0.75)">
                            Hervorragend! Du hast eine Silberne LP gewonnen! 🥈
                            <br>Was für eine starke Leistung! Du bist schon fast ein Musik-Experte. Mit ein bisschen
                            Feinschliff holst du dir beim nächsten Mal bestimmt Gold!
                        </template>
                        <template v-else-if="correctAnswers >= (maxQuestions * 0.5)">
                            Klasse! Du hast eine Bronzene LP gewonnen! 🥉
                            <br>Dein Musikwissen kann sich sehen lassen! Mach weiter so, und schon bald wirst du noch
                            mehr Hits erkennen und höhere Auszeichnungen gewinnen!
                        </template>
                        <template v-else>
                            Das war ein guter Anfang! 💪
                            <br>Jeder Musikexperte hat mal klein angefangen. Lass uns gleich noch eine Runde spielen -
                            mit jedem Versuch lernst du neue Songs kennen und wirst besser!
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

// Gemeinsamer Joker-Count
const totalJokers = difficulty === 'easy' ? 3 : difficulty === 'medium' ? 5 : 7
const remainingJokers = ref(totalJokers)

const audienceHelp = ref<{ [key: string]: number }>({})
const jokerUsedForCurrentQuestion = ref(false)
const hiddenOptions = ref<string[]>([])

const phoneExpertOpinion = ref('')
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
            option => option !== currentQuestion.value.correctAnswer
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
        audienceHelp.value = currentQuestion.value.options.reduce((acc, option, i) => {
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
                currentQuestion.value.options.find(o => o !== currentQuestion.value.correctAnswer)
            confidenceLevel = 'medium'
        } else {
            confidence = Math.floor(Math.random() * 25) + 35
            answer = Math.random() < 0.5 ? currentQuestion.value.correctAnswer :
                currentQuestion.value.options.find(o => o !== currentQuestion.value.correctAnswer)
            confidenceLevel = 'low'
        }

        const responses = expertResponses[confidenceLevel]
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
    jokerUsedForCurrentQuestion.value = false
    audienceHelp.value = {}
    hiddenOptions.value = []
    phoneExpertOpinion.value = ''
    phoneExpertConfidence.value = 0
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
        behavior: smoothScrollBehavior.value
    })
}

const totalPoints = ref(0)

// Funktion zum Berechnen der Punkte
const calculatePoints = () => {
    const basePoints = BASE_POINTS
    const timeBonus = calculateTimeBonus()
    return basePoints + timeBonus
}

// Prüfen ob currentArtist existiert bevor wir auf Properties zugreifen
const selectAnswer = async (selectedAnswer: string) => {
    if (showSolution.value) return

    isCorrectAnswer.value = selectedAnswer === currentQuestion.value.correctAnswer
    showSolution.value = true

    if (isCorrectAnswer.value) {
        correctAnswers.value++
        earnedPoints.value = calculatePoints()
        totalPoints.value += earnedPoints.value
        pointsDisplay.value?.updatePoints(earnedPoints.value)
    }

    // Lade Künstlerinformationen
    try {
        const response = await import(`~/json/genres/${locale.value}/${category}.json`)
        currentArtist.value = response.default.find((artist: any) =>
            artist.questions[difficulty].some((q: any) => q.id === currentQuestion.value.id)
        )
    } catch (error) {
        console.error('Fehler beim Laden der Künstlerinformationen:', error)
        currentArtist.value = null
    }

    // Warte kurz und scrolle dann nach oben
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

const gameFinished = computed(() => usedQuestions.value.length >= maxQuestions.value)
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
</script>

<style lang="scss">
// Gemeinsame Überschriften-Styles
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

.question-container {
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
    background: var(--surface-color);
    border-radius: var(--border-radius);
    margin: 0 var(--padding-small);

    .joker-buttons {
        display: flex;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-small);

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
}

.joker-count {
    font-size: clamp(0.875rem, 3vw, 1rem);
    color: var(--text-color);
    opacity: 0.8;
}

.solution-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-large);
    padding: 0 var(--padding-small);
    margin: 0 auto;
    width: 100%;

    @media (width >=768px) {
        padding: 0;
    }
}

.result-banner {
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    text-align: center;
    background: #B91C1C; // Dunkleres Rot für besseren Kontrast
    box-shadow: 0 4px 16px rgb(0 0 0 / 20%);
    margin: 0 auto;
    width: 100%;

    &.correct {
        background: #15803D; // Dunkleres Grün für besseren Kontrast
    }

    .result-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .result-header {
        display: flex;
        align-items: center;
        gap: var(--padding-small);

        .result-icon {
            font-size: clamp(1.5rem, 4vw, 1.8rem);
            color: #FFFFFF;
        }

        h2 {
            font-size: clamp(1.5rem, 4vw, 1.8rem);
            margin: 0;
            color: #FFFFFF;
        }
    }

    .points-info {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: #FFFFFF;

        .base-points {
            font-weight: 700;
        }
    }

    .correct-answer {
        font-size: clamp(1rem, 2.5vw, 1.1rem);
        background: rgb(0 0 0 / 20%);
        padding: var(--padding-small) var(--padding-medium);
        border-radius: var(--border-radius);
        color: #FFFFFF;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .label {
            opacity: 0.9;
        }

        .answer {
            font-weight: 600;
        }
    }
}

.song-details {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    border: 1px solid rgb(255 255 255 / 10%);

    .cover-and-player {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--padding-medium);
        margin-bottom: var(--padding-medium);

        @media (width >=768px) {
            flex-direction: row;
            justify-content: center;
        }
    }

    .cover-container {
        width: 100%;
        max-width: 300px;
        aspect-ratio: 1;
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--box-shadow);
        transition: transform var(--transition-speed);

        &:hover {
            transform: scale(1.05);
        }

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

    .song-info {
        text-align: center;
        margin-bottom: var(--padding-medium);
    }

    .metadata {
        margin-bottom: var(--padding-medium);

        h3 {
            font-size: clamp(1.2rem, 3.5vw, 1.5rem);
            margin-bottom: var(--padding-small);
        }

        .artist {
            font-size: clamp(1.1rem, 3vw, 1.3rem);
            font-weight: 600;
            margin-bottom: var(--padding-small);
        }

        .year {
            font-size: clamp(1rem, 2.5vw, 1.1rem);
            opacity: 0.8;
        }
    }

    .music-links {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
        max-width: 300px;
        margin: 0 auto;

        .music-link {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--padding-small);
            width: 100%;
            transition: all var(--transition-speed);

            &:hover {
                transform: translateY(-2px);
            }

            .icon {
                font-size: 1.2rem;
            }
        }
    }

    .trivia {
        background: rgb(255 255 255 / 5%);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        margin-top: var(--padding-medium);

        h3 {
            font-size: clamp(1.1rem, 3vw, 1.3rem);
            margin-bottom: var(--padding-small);
            text-align: center;
        }

        p {
            font-size: clamp(1rem, 2.5vw, 1.1rem);
            line-height: 1.6;
        }
    }
}

.next-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--padding-small);
    font-size: clamp(1.1rem, 3vw, 1.3rem);
    padding: var(--padding-medium) var(--padding-large);
    margin: 0 auto;

    .icon {
        font-size: 1.2em;
    }

    &:hover {
        transform: translateY(-2px);
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
    margin: var(--padding-medium) 0;

    h3 {
        @include section-heading;
    }

    .audience-bars {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .option-text {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: var(--text-color);
        text-align: left;
        padding: 0 var(--padding-small);
        font-weight: 500;
    }

    .bar-container {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        overflow: hidden;
        height: 24px;
        width: 100%;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .option-text {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: var(--text-color);
        text-align: left;
        padding: 0 var(--padding-small);
        font-weight: 500;
    }

    .bar-container {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        overflow: hidden;
        height: 24px;
        width: 100%;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .option-text {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: var(--text-color);
        text-align: left;
        padding: 0 var(--padding-small);
        font-weight: 500;
    }

    .bar-container {
        background: rgb(255 255 255 / 10%);
        border-radius: var(--border-radius);
        overflow: hidden;
        height: 24px;
        width: 100%;
    }

    .bar-item {
        display: flex;
        flex-direction: column;
        gap: var(--padding-small);
    }

    .option-text {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: var(--text-color);
        text-align: left;
        padding: 0 var(--padding-small);
        font-weight: 500;
    }
}

.phone-expert {
    background: var(--surface-color);
    border-radius: var(--border-radius);
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
</style>
