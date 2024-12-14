<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false" :show-coins="false">
        <main>
            <Transition name="slide" mode="out-in">
                <!-- Game Content -->
                <div v-if="!gameFinished" class="game-content" :key="'game'">
                    <Transition name="slide" mode="out-in">
                        <!-- Question View -->
                        <div v-if="!showSolution" :key="'question'">
                            <div class="game-header">
                                <div class="header-left">
                                    <h1>{{ currentCategoryData?.name || category }}</h1>
                                    <p class="round-counter">{{ $t('game.round', {
                                        current: usedQuestions.length, max:
                                            maxQuestions
                                    }) }}</p>
                                </div>
                                <div class="header-right">
                                    <div class="points-display">
                                        <div class="points-container">
                                            <span class="points" :class="{ 'points-update': isAnimating }">
                                                {{ formattedPoints }}
                                            </span>
                                            <span class="points-label">{{ $t('game.points_label') }}</span>
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
                                        class="button option-button"
                                        :class="{ 'hidden': hiddenOptions.includes(option) }"
                                        @click="selectAnswer(option)">
                                        <span>{{ option }}</span>
                                    </button>
                                </div>

                                <!-- Telefonjoker Antwort -->
                                <div v-if="phoneExpertOpinion" class="phone-expert">
                                    <h3>{{ $t('game.expert.title') }}</h3>
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
                                                <span class="confidence-text">{{ phoneExpertConfidence }}% {{
                                                    $t('game.confidence') }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Publikumsjoker Ergebnis -->
                                <div v-if="Object.keys(audienceHelp).length > 0" class="audience-help">
                                    <h3>{{ $t('game.audienceOpinion') }}</h3>
                                    <div class="audience-bars">
                                        <div v-for="(percentage, option) in audienceHelp" :key="option"
                                            class="bar-item">
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
                                            :aria-label="$t('game.jokers.fiftyFifty')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="material-symbols:balance" size="30" />
                                        </button>

                                        <!-- Publikumsjoker -->
                                        <button class="button joker-button" @click="useAudienceJoker"
                                            :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                            :aria-label="$t('game.jokers.audience')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="formkit:people" size="30" />
                                        </button>

                                        <!-- Telefonjoker -->
                                        <button class="button joker-button" @click="usePhoneJoker"
                                            :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                                            :aria-label="$t('game.jokers.phone')"
                                            :class="{ 'disabled': remainingJokers === 0 || jokerUsedForCurrentQuestion }">
                                            <Icon name="gg:phone" size="30" />
                                        </button>
                                    </div>
                                    <span class="joker-count">{{ $t('game.jokers.remaining', { count: remainingJokers })
                                        }}</span>
                                </div>
                            </div>
                        </div>
                        <!-- Solution View -->
                        <div v-else :key="'solution'" class="solution-container">
                            <!-- Ergebnis-Banner -->
                            <div class="result-banner" :class="{ 'correct': isCorrectAnswer }">
                                <div class="result-header">
                                    <Icon
                                        :name="isCorrectAnswer ? 'material-symbols:check-circle' : 'material-symbols:cancel'"
                                        class="result-icon" size="28" />
                                    <h2>{{ isCorrectAnswer ? $t('game.correct') : $t('game.wrong') }}</h2>
                                </div>
                                <div v-if="isCorrectAnswer" class="points-breakdown">
                                    <div class="points">
                                        {{ $t('game.points', { base: latestBonus.base, time: latestBonus.time }) }}
                                    </div>
                                </div>
                                <div v-else class="points"> 0 {{ $t('game.points_label') }}</div>

                                <div class="correct-answer">
                                    <span class="label">{{ $t('game.correctAnswer') }}</span>
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
                                                :title="currentArtist?.preview_link ? (isPlaying ? $t('game.audio.pause') : $t('game.audio.play')) : $t('game.audio.noAudio')">
                                                <Icon
                                                    :name="isPlaying ? 'material-symbols:pause' : 'material-symbols:play-arrow'"
                                                    size="36" />
                                            </button>
                                            <div class="progress-bar">
                                                <div class="progress"
                                                    :style="{ width: `${(currentTime / duration) * 100}%` }">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="info">
                                            <p class="artist">{{ $t('game.album.artist') }}: {{ currentArtist.artist }}
                                            </p>
                                            <p class="year">{{ $t('game.album.year') }}: {{ currentArtist.year }}</p>
                                        </div>
                                    </div>
                                    <div class="streaming-links">
                                        <a v-if="currentArtist.spotify_link" :href="currentArtist.spotify_link"
                                            target="_blank" class="stream-link spotify"
                                            :title="$t('game.streaming.spotify')">
                                            <Icon name="mdi:spotify" size="36" />
                                        </a>
                                        <a v-if="currentArtist.apple_music_link" :href="currentArtist.apple_music_link"
                                            target="_blank" class="stream-link apple"
                                            :title="$t('game.streaming.apple')">
                                            <Icon name="mdi:apple" size="36" />
                                        </a>
                                        <a v-if="currentArtist.deezer_link" :href="currentArtist.deezer_link"
                                            target="_blank" class="stream-link deezer"
                                            :title="$t('game.streaming.deezer')">
                                            <Icon name="simple-icons:deezer" size="36" />
                                        </a>
                                    </div>
                                </div>

                                <!-- Trivia Information -->
                                <div class="trivia-box">
                                    <h3>{{ $t('game.didYouKnow') }}</h3>
                                    <p>{{ currentQuestion.trivia }}</p>
                                </div>

                                <button @click="nextQuestion" class="next-button">
                                    <span>{{ $t('game.nextQuestion') }}</span>
                                    <Icon name="material-symbols:arrow-forward" />
                                </button>
                            </div>
                        </div>
                    </Transition>
                </div>
                <!-- Game Over Screen -->
                <div v-else class="game-end-screen" :key="'gameover'">
                    <div class="end-content">
                        <div class="end-header">
                            <h2>{{ $t('game.gameOver.title') }}</h2>
                            <div class="final-score-container">
                                <div class="score-circle">
                                    <div class="score-inner">
                                        <span class="points">{{ totalPoints }}</span>
                                        <span class="points-label">{{ $t('game.points_label') }}</span>
                                    </div>
                                </div>
                                <div class="stats">
                                    <div class="stat-item">
                                        <span class="stat-label">{{ $t('game.gameOver.correctAnswers') }}</span>
                                        <span class="stat-value">{{ correctAnswers }} / {{ maxQuestions }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="reward-section" :class="recordClass">
                            <div class="record-icon">
                                <Icon v-if="earnedRecord" :name="recordIcon" size="64" />
                            </div>
                            <p class="reward-text">
                                {{ resultMessage }}
                            </p>
                        </div>

                        <div class="end-actions">
                            <NuxtLink to="/gamehome" class="button home-button">
                                <Icon name="material-symbols:home" size="36" />
                                <span>{{ $t('game.gameOver.backToMenu') }}</span>
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </Transition>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client';

definePageMeta({
    middleware: 'auth'
})

const session = authClient.useSession()

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

interface ExpertResponses {
    high: string[];
    medium: string[];
    low: string[];
}

type LocaleResponses = Record<string, ExpertResponses>;

const expertResponsesByLocale: LocaleResponses = {
    de: {
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
            "Diese Aufnahme hat mein Leben verändert. Es ist '{answer}'."
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
            "Erinnert mich stark an '{answer}', bin aber nicht ganz sicher."
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
            "Da bin ich überfragt... '{answer}' würde ich mal tippen."
        ]
    },
    en: {
        high: [
            "Without any doubt - it's '{answer}'. I documented the original recording session.",
            "As a long-time producer of the label, I can guarantee you: This is '{answer}'.",
            "Oh, I know this inside out! '{answer}' - I'd bet my turntable on it.",
            "This question is home turf for me. Clearly '{answer}', I was there during the recording.",
            "This is my absolute favorite album! Of course it's '{answer}'.",
            "This recording made history - definitely '{answer}'.",
            "I've played this song hundreds of times. No question '{answer}'.",
            "This production is legendary! Can only be '{answer}'.",
            "I don't even need to think about it - '{answer}', 100%!",
            "This recording changed my life. It's '{answer}'."
        ],
        medium: [
            "Hold on... yes, I think it must be '{answer}'. The production sounds very familiar.",
            "If my ears don't deceive me, I'd say '{answer}'.",
            "Hmm, the sound strongly reminds me of '{answer}', but let me think for a moment...",
            "This sounds a lot like '{answer}', but there were several similar productions back then.",
            "I'd say 70% it's '{answer}', but don't hold me to that.",
            "I know it from the club - should be '{answer}', if I remember correctly.",
            "Used to have it in my collection... '{answer}', right?",
            "It plays often on the radio - must be '{answer}'.",
            "Pretty sure it's '{answer}', but no guarantee.",
            "Strongly reminds me of '{answer}', but I'm not entirely sure."
        ],
        low: [
            "Phew, tough question... spontaneously I'd guess '{answer}', but that's really just a guess.",
            "Oh man, this isn't my era... maybe '{answer}'?",
            "Music is usually my thing, but here... '{answer}' maybe?",
            "*scratches head* '{answer}'? But that's really just a guess!",
            "If I had to guess now... '{answer}'? But I'm really not sure.",
            "This isn't my expertise, but could be '{answer}'?",
            "Ugh, you're asking the wrong person... '{answer}' perhaps?",
            "No idea, but '{answer}' sounds plausible?",
            "Hard to say... '{answer}'? But that's really just guessing!",
            "I'm stumped here... I'd guess '{answer}'."
        ]
    },
    es: {
        high: [
            "¡Increíble! ¡Has ganado un LP de Oro! 🏆\n¡Eres un campeón absoluto de la música! Todas las preguntas perfectamente respondidas - ¡solo los mejores de los mejores lo logran!",
            "¡Sensacional! ¡El LP de Oro es tuyo! 🏆\n¡Tu conocimiento musical es verdaderamente extraordinario - una actuación impecable!",
            "¡Asombroso! ¡El LP de Oro te pertenece! 🏆\n¡Eres una enciclopedia musical andante! Una ronda perfecta - ¡simplemente magnífico!",
            "¡Fantástico! ¡Te has ganado más que merecidamente el LP de Oro! 🏆\n¡Tu actuación fue simplemente impecable - eres un verdadero virtuoso de la música!",
            "¡Magistral! ¡El LP de Oro es tuyo! 🏆\n¡Una ronda perfecta - definitivamente eres un genio de la música!",
            "¡Brillante! ¡Un LP de Oro para ti! 🏆\n¡Tu experiencia musical es verdaderamente impresionante - todas las preguntas correctas!",
            "¡Fenomenal! ¡El LP de Oro te pertenece! 🏆\n¡Eres un verdadero conocedor de la música - una actuación impecable!",
            "¡Magnífico! ¡Te has ganado el LP de Oro! 🏆\n¡Una ronda perfecta - tu conocimiento musical es imbatible!",
            "¡Sobresaliente! ¡El LP de Oro es tuyo! 🏆\n¡Eres un profesional absoluto de la música - todas las preguntas respondidas perfectamente!",
            "¡Legendario! ¡Has ganado el LP de Oro! 🏆\n¡Una actuación perfecta - eres un verdadero maestro de la música!"
        ],
        medium: [
            "Espera... sí, creo que debe ser '{answer}'. La producción me suena muy familiar.",
            "Si mis oídos no me engañan, diría '{answer}'.",
            "Hmm, el sonido me recuerda mucho a '{answer}', pero déjame pensar un momento...",
            "Esto suena mucho a '{answer}', pero hubo varias producciones similares en ese entonces.",
            "Diría con un 70% de seguridad que es '{answer}', pero no me hagas caso del todo.",
            "Lo conozco del club - debería ser '{answer}', si mal no recuerdo.",
            "Lo tenía en mi colección... '{answer}', ¿verdad?",
            "Suena a menudo en la radio - debe ser '{answer}'.",
            "Bastante seguro de que es '{answer}', pero sin garantías.",
            "Me recuerda mucho a '{answer}', pero no estoy completamente seguro."
        ],
        low: [
            "Uf, pregunta difícil... espontáneamente diría '{answer}', pero es solo una suposición.",
            "Oh vaya, esta no es mi época... ¿tal vez '{answer}'?",
            "La música suele ser lo mío, pero aquí... ¿'{answer}' quizás?",
            "*se rasca la cabeza* ¿'{answer}'? ¡Pero es realmente solo una suposición!",
            "Si tuviera que adivinar... ¿'{answer}'? Pero realmente no estoy seguro.",
            "Esta no es mi especialidad, pero ¿podría ser '{answer}'?",
            "Uf, le preguntas a la persona equivocada... ¿'{answer}' tal vez?",
            "Ni idea, pero ¿'{answer}' suena plausible?",
            "Difícil de decir... ¿'{answer}'? ¡Pero esto es solo una suposición!",
            "Estoy perdido aquí... Yo diría '{answer}'."
        ]
    },
    fr: {
        high: [
            "Incroyable ! Tu as gagné un LP d'Or ! 🏆\nTu es un champion absolu de la musique ! Toutes les questions parfaitement répondues - seuls les meilleurs y parviennent !",
            "Sensationnel ! Le LP d'Or est à toi ! 🏆\nTes connaissances musicales sont vraiment extraordinaires - une performance impeccable !",
            "Fantastique ! Le LP d'Or t'appartient ! 🏆\nTu es une encyclopédie musicale vivante ! Une manche parfaite - simplement grandiose !",
            "Fantastique ! Tu as plus que mérité le LP d'Or ! 🏆\nTa performance était simplement impeccable - tu es un véritable virtuose de la musique !",
            "Magistral ! Le LP d'Or est à toi ! 🏆\nUne manche parfaite - tu es définitivement un génie de la musique !",
            "Brillant ! Un LP d'Or pour toi ! 🏆\nTon expertise musicale est vraiment impressionnante - toutes les réponses correctes !",
            "Phénoménal ! Le LP d'Or t'appartient ! 🏆\nTu es un véritable connaisseur de musique - une performance impeccable !",
            "Magnifique ! Tu as gagné le LP d'Or ! 🏆\nUne manche parfaite - tes connaissances musicales sont imbattables !",
            "Exceptionnel ! Le LP d'Or est à toi ! 🏆\nTu es un pro absolu de la musique - toutes les questions parfaitement répondues !",
            "Légendaire ! Tu as gagné le LP d'Or ! 🏆\nUne performance parfaite - tu es un véritable maestro de la musique !"
        ],
        medium: [
            "Attends... oui, je pense que ça doit être '{answer}'. La production me semble très familière.",
            "Si mes oreilles ne me trompent pas, je dirais '{answer}'.",
            "Hmm, le son me rappelle fortement '{answer}', mais laisse-moi réfléchir un moment...",
            "Ça ressemble beaucoup à '{answer}', mais il y avait plusieurs productions similaires à l'époque.",
            "Je dirais à 70% que c'est '{answer}', mais ne me prends pas au mot.",
            "Je le connais du club - ça devrait être '{answer}', si je me souviens bien.",
            "Je l'avais dans ma collection... '{answer}', non ?",
            "Ça passe souvent à la radio - ça doit être '{answer}'.",
            "Assez sûr que c'est '{answer}', mais pas de garantie.",
            "Ça me rappelle beaucoup '{answer}', mais je ne suis pas totalement sûr."
        ],
        low: [
            "Ouf, question difficile... spontanément je dirais '{answer}', mais c'est vraiment juste une supposition.",
            "Oh là là, ce n'est pas mon époque... peut-être '{answer}' ?",
            "La musique c'est généralement mon truc, mais là... '{answer}' peut-être ?",
            "*se gratte la tête* '{answer}' ? Mais c'est vraiment juste une supposition !",
            "Si je devais deviner... '{answer}' ? Mais je ne suis vraiment pas sûr.",
            "Ce n'est pas mon domaine d'expertise, mais ça pourrait être '{answer}' ?",
            "Aïe, tu demandes à la mauvaise personne... '{answer}' peut-être ?",
            "Aucune idée, mais '{answer}' semble plausible ?",
            "Difficile à dire... '{answer}' ? Mais c'est vraiment juste une supposition !",
            "Je sèche là... Je dirais '{answer}'."
        ]
    },
    it: {
        high: [
            "Incredibile! Hai vinto un LP d'Oro! 🏆\nSei un campione assoluto della musica! Tutte le domande perfettamente risposte - solo i migliori dei migliori ci riescono!",
            "Sensazionale! L'LP d'Oro è tuo! 🏆\nLa tua conoscenza musicale è davvero straordinaria - una performance impeccabile!",
            "Fantastico! L'LP d'Oro è tuo! 🏆\nSei un'enciclopedia musicale ambulante! Un round perfetto - semplicemente grandioso!",
            "Fantastico! Ti sei più che meritato l'LP d'Oro! 🏆\nLa tua performance è stata semplicemente impeccabile - sei un vero virtuoso della musica!",
            "Magistrale! L'LP d'Oro è tuo! 🏆\nUn round perfetto - sei decisamente un genio della musica!",
            "Brillante! Un LP d'Oro per te! 🏆\nLa tua competenza musicale è davvero impressionante - tutte le risposte corrette!",
            "Fenomenale! L'LP d'Oro è tuo! 🏆\nSei un vero intenditore di musica - una performance impeccabile!",
            "Magnifico! Ti sei guadagnato l'LP d'Oro! 🏆\nUn round perfetto - la tua conoscenza musicale è imbattibile!",
            "Eccezionale! L'LP d'Oro è tuo! 🏆\nSei un professionista assoluto della musica - tutte le domande risposte perfettamente!",
            "Leggendario! Hai vinto l'LP d'Oro! 🏆\nUna performance perfetta - sei un vero maestro della musica!"
        ],
        medium: [
            "Aspetta... sì, penso che debba essere '{answer}'. La produzione mi suona molto familiare.",
            "Se le mie orecchie non mi ingannano, direi '{answer}'.",
            "Hmm, il suono mi ricorda molto '{answer}', ma fammi pensare un momento...",
            "Suona molto come '{answer}', ma c'erano diverse produzioni simili all'epoca.",
            "Direi al 70% che è '{answer}', ma non prenderlo per certo.",
            "Lo conosco dal club - dovrebbe essere '{answer}', se ricordo bene.",
            "Lo avevo nella mia collezione... '{answer}', giusto?",
            "Passa spesso alla radio - deve essere '{answer}'.",
            "Abbastanza sicuro che sia '{answer}', ma nessuna garanzia.",
            "Mi ricorda molto '{answer}', ma non sono del tutto sicuro."
        ],
        low: [
            "Uff, domanda difficile... spontaneamente direi '{answer}', ma è davvero solo un'ipotesi.",
            "Oh cavolo, questa non è la mia epoca... forse '{answer}'?",
            "La musica di solito è il mio forte, ma qui... '{answer}' forse?",
            "*si gratta la testa* '{answer}'? Ma è davvero solo un'ipotesi!",
            "Se dovessi indovinare... '{answer}'? Ma non sono proprio sicuro.",
            "Questa non è la mia specialità, ma potrebbe essere '{answer}'?",
            "Uff, stai chiedendo alla persona sbagliata... '{answer}' forse?",
            "Non ne ho idea, ma '{answer}' suona plausibile?",
            "Difficile da dire... '{answer}'? Ma è solo un'ipotesi!",
            "Sono in difficoltà qui... Direi '{answer}'."
        ]
    }
};

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

        try {
            // Nutze die aktuelle Sprache
            const currentLocale = locale.value || 'de'
            const responses = expertResponsesByLocale[currentLocale][confidenceLevel as keyof ExpertResponses]

            if (!Array.isArray(responses)) {
                console.error('Responses is not an array:', responses)
                return
            }

            const responseTemplate = responses[Math.floor(Math.random() * responses.length)]
            const expertTitle = expertTitles[Math.floor(Math.random() * expertTitles.length)]

            phoneExpertOpinion.value = {
                expert: expertTitle,
                message: responseTemplate.replace('{answer}', answer)
            }
            phoneExpertConfidence.value = confidence

            remainingJokers.value--
            jokerUsedForCurrentQuestion.value = true

        } catch (error) {
            console.error('Error in usePhoneJoker:', error)
        }
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

const goldMessages = {
    de: [
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
    ],
    en: [
        "Incredible! You've won a Gold LP! 🏆\nYou're an absolute music champion! All questions answered perfectly - only the best of the best achieve this!",
        "Sensational! A Gold LP is yours! 🏆\nYour music knowledge is truly extraordinary - a flawless performance!",
        "Amazing! The Gold LP belongs to you! 🏆\nYou're a walking music encyclopedia! A perfect round - simply magnificent!",
        "Fantastic! You've more than earned the Gold LP! 🏆\nYour performance was simply flawless - you're a true music virtuoso!",
        "Masterful! The Gold LP is yours! 🏆\nA perfect round - you're definitely a music genius!",
        "Brilliant! A Gold LP for you! 🏆\nYour music expertise is truly impressive - all questions correct!",
        "Phenomenal! The Gold LP belongs to you! 🏆\nYou're a true music connoisseur - a flawless performance!",
        "Magnificent! You've earned yourself the Gold LP! 🏆\nA perfect round - your music knowledge is unbeatable!",
        "Outstanding! The Gold LP is yours! 🏆\nYou're an absolute music pro - all questions answered perfectly!",
        "Legendary! You've won the Gold LP! 🏆\nA perfect performance - you're a true music maestro!"
    ],
    es: [
        "¡Increíble! ¡Has ganado un LP de Oro! 🏆\n¡Eres un campeón absoluto de la música! Todas las preguntas perfectamente respondidas - ¡solo los mejores de los mejores lo logran!",
        "¡Sensacional! ¡El LP de Oro es tuyo! 🏆\n¡Tu conocimiento musical es verdaderamente extraordinario - una actuación impecable!",
        "¡Asombroso! ¡El LP de Oro te pertenece! 🏆\n¡Eres una enciclopedia musical andante! Una ronda perfecta - ¡simplemente magnífico!",
        "¡Fantástico! ¡Te has ganado más que merecidamente el LP de Oro! 🏆\n¡Tu actuación fue simplemente impecable - eres un verdadero virtuoso de la música!",
        "¡Magistral! ¡El LP de Oro es tuyo! 🏆\n¡Una ronda perfecta - definitivamente eres un genio de la música!",
        "¡Brillante! ¡Un LP de Oro para ti! 🏆\n¡Tu experiencia musical es verdaderamente impresionante - todas las preguntas correctas!",
        "¡Fenomenal! ¡El LP de Oro te pertenece! 🏆\n¡Eres un verdadero conocedor de la música - una actuación impecable!",
        "¡Magnífico! ¡Te has ganado el LP de Oro! 🏆\n¡Una ronda perfecta - tu conocimiento musical es imbatible!",
        "¡Sobresaliente! ¡El LP de Oro es tuyo! 🏆\n¡Eres un profesional absoluto de la música - todas las preguntas respondidas perfectamente!",
        "¡Legendario! ¡Has ganado el LP de Oro! 🏆\n¡Una actuación perfecta - eres un verdadero maestro de la música!"
    ],
    fr: [
        "Incroyable ! Tu as gagné un LP d'Or ! 🏆\nTu es un champion absolu de la musique ! Toutes les questions parfaitement répondues - seuls les meilleurs y parviennent !",
        "Sensationnel ! Le LP d'Or est à toi ! 🏆\nTes connaissances musicales sont vraiment extraordinaires - une performance impeccable !",
        "Fantastique ! Le LP d'Or t'appartient ! 🏆\nTu es une encyclopédie musicale vivante ! Une manche parfaite - simplement grandiose !",
        "Fantastique ! Tu as plus que mérité le LP d'Or ! 🏆\nTa performance était simplement impeccable - tu es un véritable virtuose de la musique !",
        "Magistral ! Le LP d'Or est à toi ! 🏆\nUne manche parfaite - tu es définitivement un génie de la musique !",
        "Brillant ! Un LP d'Or pour toi ! 🏆\nTon expertise musicale est vraiment impressionnante - toutes les réponses correctes !",
        "Phénoménal ! Le LP d'Or t'appartient ! 🏆\nTu es un véritable connaisseur de musique - une performance impeccable !",
        "Magnifique ! Tu as gagné le LP d'Or ! 🏆\nUne manche parfaite - tes connaissances musicales sont imbattables !",
        "Exceptionnel ! Le LP d'Or est à toi ! 🏆\nTu es un pro absolu de la musique - toutes les questions parfaitement répondues !",
        "Légendaire ! Tu as gagné le LP d'Or ! 🏆\nUne performance parfaite - tu es un véritable maestro de la musique !"
    ],
    it: [
        "Incredibile! Hai vinto un LP d'Oro! 🏆\nSei un campione assoluto della musica! Tutte le domande perfettamente risposte - solo i migliori dei migliori ci riescono!",
        "Sensazionale! L'LP d'Oro è tuo! 🏆\nLa tua conoscenza musicale è davvero straordinaria - una performance impeccabile!",
        "Fantastico! L'LP d'Oro è tuo! 🏆\nSei un'enciclopedia musicale ambulante! Un round perfetto - semplicemente grandioso!",
        "Fantastico! Ti sei più che meritato l'LP d'Oro! 🏆\nLa tua performance è stata semplicemente impeccabile - sei un vero virtuoso della musica!",
        "Magistrale! L'LP d'Oro è tuo! 🏆\nUn round perfetto - sei decisamente un genio della musica!",
        "Brillante! Un LP d'Oro per te! 🏆\nLa tua competenza musicale è davvero impressionante - tutte le risposte corrette!",
        "Fenomenale! L'LP d'Oro è tuo! 🏆\nSei un vero intenditore di musica - una performance impeccabile!",
        "Magnifico! Ti sei guadagnato l'LP d'Oro! 🏆\nUn round perfetto - la tua conoscenza musicale è imbattibile!",
        "Eccezionale! L'LP d'Oro è tuo! 🏆\nSei un professionista assoluto della musica - tutte le domande risposte perfettamente!",
        "Leggendario! Hai vinto l'LP d'Oro! 🏆\nUna performance perfetta - sei un vero maestro della musica!"
    ]
}

const silverMessages = {
    de: [
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
    ],
    en: [
        "Excellent! You've won a Silver LP! 🥈\nWhat a strong performance! You're almost a music expert. With a bit of fine-tuning, you'll surely get gold next time!",
        "Great! A Silver LP for you! 🥈\nYour music knowledge is remarkable! Just a small step away from the Gold LP!",
        "Awesome! The Silver LP is yours! 🥈\nYou really know your stuff! Next time you'll surely achieve a perfect round!",
        "Well done! A Silver LP is yours! 🥈\nYour music knowledge is impressive! Gold is within reach!",
        "Excellent! You've won the Silver LP! 🥈\nThat was a very strong performance! Almost perfect!",
        "Great! A Silver LP for your performance! 🥈\nYou're on your way to becoming a music champion!",
        "Strong! You've earned the Silver LP! 🥈\nYour music knowledge is impressive! Gold is the next goal!",
        "Excellent! A Silver LP for you! 🥈\nYou're a true music expert! Just a small step away from perfection!",
        "Respect! The Silver LP is yours! 🥈\nYour performance was really good! Gold is within reach!",
        "Impressive! You've earned yourself the Silver LP! 🥈\nThat was a great performance! You'll get gold next time!"
    ],
    es: [
        "¡Excelente! ¡Has ganado un LP de Plata! 🥈\n¡Qué actuación tan fuerte! Casi eres un experto en música. ¡Con un poco más de práctica, seguro que conseguirás el oro la próxima vez!",
        "¡Genial! ¡Un LP de Plata para ti! 🥈\n¡Tu conocimiento musical es notable! ¡Solo un pequeño paso hasta el LP de Oro!",
        "¡Increíble! ¡El LP de Plata es tuyo! 🥈\n¡Realmente sabes tu material! ¡La próxima vez seguro que logras una ronda perfecta!",
        "¡Bien hecho! ¡Un LP de Plata es tuyo! 🥈\n¡Tu conocimiento musical es impresionante! ¡El oro está al alcance!",
        "¡Excelente! ¡Has ganado el LP de Plata! 🥈\n¡Esa fue una actuación muy fuerte! ¡Casi perfecto!",
        "¡Genial! ¡Un LP de Plata por tu actuación! 🥈\n¡Estás en camino de convertirte en un campeón de la música!",
        "¡Fuerte! ¡Te has ganado el LP de Plata! 🥈\n¡Tu conocimiento musical es impresionante! ¡El oro es el siguiente objetivo!",
        "¡Excelente! ¡Un LP de Plata para ti! 🥈\n¡Eres un verdadero experto en música! ¡Solo un pequeño paso hasta la perfección!",
        "¡Respeto! ¡El LP de Plata es tuyo! 🥈\n¡Tu actuación fue realmente buena! ¡El oro está al alcance!",
        "¡Impresionante! ¡Te has ganado el LP de Plata! 🥈\n¡Esa fue una gran actuación! ¡Conseguirás el oro la próxima vez!"
    ],
    fr: [
        "Excellent ! Tu as gagné un LP d'Argent ! 🥈\nQuelle performance ! Tu es presque un expert en musique. Avec un peu plus de pratique, tu décrocheras sûrement l'or la prochaine fois !",
        "Génial ! Un LP d'Argent pour toi ! 🥈\nTes connaissances musicales sont remarquables ! Plus qu'un petit pas jusqu'au LP d'Or !",
        "Super ! Le LP d'Argent est à toi ! 🥈\nTu t'y connais vraiment ! La prochaine fois, tu feras sûrement un sans-faute !",
        "Bravo ! Un LP d'Argent est à toi ! 🥈\nTes connaissances musicales sont impressionnantes ! L'or est à portée de main !",
        "Excellent ! Tu as gagné le LP d'Argent ! 🥈\nC'était une très belle performance ! Presque parfait !",
        "Génial ! Un LP d'Argent pour ta performance ! 🥈\nTu es en route pour devenir un champion de la musique !",
        "Solide ! Tu as mérité le LP d'Argent ! 🥈\nTes connaissances musicales sont impressionnantes ! L'or est le prochain objectif !",
        "Excellent ! Un LP d'Argent pour toi ! 🥈\nTu es un vrai expert en musique ! Plus qu'un petit pas vers la perfection !",
        "Respect ! Le LP d'Argent est à toi ! 🥈\nTa performance était vraiment bonne ! L'or est à portée !",
        "Impressionnant ! Tu as gagné le LP d'Argent ! 🥈\nC'était une super performance ! Tu décrocheras l'or la prochaine fois !"
    ],
    it: [
        "Eccellente! Hai vinto un LP d'Argento! 🥈\nChe performance! Sei quasi un esperto di musica. Con un po' più di pratica, sicuramente otterrai l'oro la prossima volta!",
        "Ottimo! Un LP d'Argento per te! 🥈\nLa tua conoscenza musicale è notevole! Solo un piccolo passo fino all'LP d'Oro!",
        "Fantastico! L'LP d'Argento è tuo! 🥈\nTe ne intendi davvero! La prossima volta sicuramente farai un round perfetto!",
        "Ben fatto! Un LP d'Argento è tuo! 🥈\nLa tua conoscenza musicale è impressionante! L'oro è a portata di mano!",
        "Eccellente! Hai vinto l'LP d'Argento! 🥈\nÈ stata una performance molto forte! Quasi perfetto!",
        "Grandioso! Un LP d'Argento per la tua performance! 🥈\nSei sulla strada per diventare un campione della musica!",
        "Forte! Ti sei guadagnato l'LP d'Argento! 🥈\nLa tua conoscenza musicale è impressionante! L'oro è il prossimo obiettivo!",
        "Eccellente! Un LP d'Argento per te! 🥈\nSei un vero esperto di musica! Solo un piccolo passo verso la perfezione!",
        "Rispetto! L'LP d'Argento è tuo! 🥈\nLa tua performance è stata davvero buona! L'oro è a portata di mano!",
        "Impressionante! Ti sei guadagnato l'LP d'Argento! 🥈\nÈ stata una grande performance! Otterrai l'oro la prossima volta!"
    ]
}

const bronzeMessages = {
    de: [
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
    ],
    en: [
        "Great! You've won a Bronze LP! 🥉\nYour music knowledge is impressive! Keep it up, and soon you'll recognize even more hits!",
        "Well done! A Bronze LP for you! 🥉\nYou're on the right track! Keep going, and silver will be yours soon!",
        "Nice! The Bronze LP belongs to you! 🥉\nYou've got some skills! With a bit more practice, you'll achieve even more!",
        "Bravo! A Bronze LP is yours! 🥉\nYou're developing into a real music expert! Keep at it!",
        "Super! You've won the Bronze LP! 🥉\nYour music knowledge is growing! Keep it up!",
        "Great! A Bronze LP for your performance! 🥉\nYou're on the right path! Keep going!",
        "Nice! You've earned the Bronze LP! 🥉\nYou're making progress! Keep at it!",
        "Very good! A Bronze LP for you! 🥉\nYou already know quite a bit! Keep going!",
        "Great! The Bronze LP is yours! 🥉\nYou're on the right track! Keep it up!",
        "Good! You've earned yourself the Bronze LP! 🥉\nYour music knowledge is developing nicely! Stay with it!"
    ],
    es: [
        "¡Genial! ¡Has ganado un LP de Bronce! 🥉\n¡Tu conocimiento musical es impresionante! ¡Sigue así, y pronto reconocerás aún más éxitos!",
        "¡Bien hecho! ¡Un LP de Bronce para ti! 🥉\n¡Vas por buen camino! ¡Sigue así, y pronto conseguirás la plata!",
        "¡Bien! ¡El LP de Bronce es tuyo! 🥉\n¡Ya tienes algunas habilidades! ¡Con un poco más de práctica, lograrás aún más!",
        "¡Bravo! ¡Un LP de Bronce es tuyo! 🥉\n¡Te estás convirtiendo en un verdadero experto en música! ¡Sigue así!",
        "¡Súper! ¡Has ganado el LP de Bronce! 🥉\n¡Tu conocimiento musical está creciendo! ¡Sigue así!",
        "¡Genial! ¡Un LP de Bronce por tu actuación! 🥉\n¡Estás en el camino correcto! ¡Continúa así!",
        "¡Bien! ¡Te has ganado el LP de Bronce! 🥉\n¡Estás progresando! ¡Sigue adelante!",
        "¡Muy bien! ¡Un LP de Bronce para ti! 🥉\n¡Ya sabes bastante! ¡Sigue así!",
        "¡Genial! ¡El LP de Bronce es tuyo! 🥉\n¡Vas por buen camino! ¡Sigue así!",
        "¡Bien! ¡Te has ganado el LP de Bronce! 🥉\n¡Tu conocimiento musical se está desarrollando bien! ¡Continúa así!"
    ],
    fr: [
        "Super ! Tu as gagné un LP de Bronze ! 🥉\nTes connaissances musicales sont impressionnantes ! Continue comme ça, et bientôt tu reconnaîtras encore plus de hits !",
        "Bien joué ! Un LP de Bronze pour toi ! 🥉\nTu es sur la bonne voie ! Continue ainsi, et l'argent sera bientôt à toi !",
        "Bien ! Le LP de Bronze est à toi ! 🥉\nTu as déjà du talent ! Avec un peu plus de pratique, tu iras encore plus loin !",
        "Bravo ! Un LP de Bronze est à toi ! 🥉\nTu deviens un véritable expert en musique ! Continue comme ça !",
        "Super ! Tu as gagné le LP de Bronze ! 🥉\nTes connaissances musicales grandissent ! Continue ainsi !",
        "Génial ! Un LP de Bronze pour ta performance ! 🥉\nTu es sur la bonne voie ! Continue !",
        "Bien ! Tu as mérité le LP de Bronze ! 🥉\nTu fais des progrès ! Continue comme ça !",
        "Très bien ! Un LP de Bronze pour toi ! 🥉\nTu en sais déjà beaucoup ! Continue ainsi !",
        "Super ! Le LP de Bronze est à toi ! 🥉\nTu es sur la bonne voie ! Continue comme ça !",
        "Bien ! Tu as gagné le LP de Bronze ! 🥉\nTes connaissances musicales se développent bien ! Continue ainsi !"
    ],
    it: [
        "Ottimo! Hai vinto un LP di Bronzo! 🥉\nLa tua conoscenza musicale è impressionante! Continua così, e presto riconoscerai ancora più successi!",
        "Ben fatto! Un LP di Bronzo per te! 🥉\nSei sulla strada giusta! Continua così, e presto l'argento sarà tuo!",
        "Bene! L'LP di Bronzo è tuo! 🥉\nHai già delle capacità! Con un po' più di pratica, otterrai ancora di più!",
        "Bravo! Un LP di Bronzo è tuo! 🥉\nTi stai sviluppando in un vero esperto di musica! Continua così!",
        "Super! Hai vinto l'LP di Bronzo! 🥉\nLa tua conoscenza musicale sta crescendo! Continua così!",
        "Ottimo! Un LP di Bronzo per la tua performance! 🥉\nSei sulla strada giusta! Continua così!",
        "Bene! Ti sei guadagnato l'LP di Bronzo! 🥉\nStai facendo progressi! Continua così!",
        "Molto bene! Un LP di Bronzo per te! 🥉\nSai già parecchio! Continua così!",
        "Ottimo! L'LP di Bronzo è tuo! 🥉\nSei sulla strada giusta! Continua così!",
        "Bene! Ti sei guadagnato l'LP di Bronzo! 🥉\nLa tua conoscenza musicale si sta sviluppando bene! Continua così!"
    ]
}

const participationMessages = {
    de: [
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
    ],
    en: [
        "That was a good start! 💪\nEvery music expert started small. Let's play another round right away!",
        "Keep going! 💪\nWith each round you'll learn new songs. Try again right away!",
        "Don't give up! 💪\nYou're on the right track! Practice makes perfect!",
        "Chin up! 💪\nEveryone starts somewhere! Your music knowledge will grow with time!",
        "Stay with it! 💪\nYou learn with every round! Try again right away!",
        "You'll get there! 💪\nPractice makes the music master! On to the next round!",
        "Good try! 💪\nYou'll get better with time! Keep going!",
        "Not bad! 💪\nEvery start is a step forward! Keep going!",
        "This is just the beginning! 💪\nYour knowledge grows with every round! Stay with it!",
        "Keep going! 💪\nYou learn something new from every game! Next round!"
    ],
    es: [
        "¡Fue un buen comienzo! 💪\nTodo experto en música empezó desde abajo. ¡Juguemos otra ronda ahora mismo!",
        "¡Sigue así! 💪\nCon cada ronda aprenderás nuevas canciones. ¡Inténtalo de nuevo!",
        "¡No te rindas! 💪\n¡Vas por buen camino! ¡La práctica hace al maestro!",
        "¡Ánimo! 💪\n¡Todos empiezan desde algún punto! ¡Tu conocimiento musical crecerá con el tiempo!",
        "¡Persiste! 💪\n¡Aprendes con cada ronda! ¡Inténtalo de nuevo!",
        "¡Lo conseguirás! 💪\n¡La práctica hace al maestro de la música! ¡A por la siguiente ronda!",
        "¡Buen intento! 💪\n¡Mejorarás con el tiempo! ¡Sigue así!",
        "¡No está mal! 💪\n¡Cada comienzo es un paso adelante! ¡Continúa así!",
        "¡Este es solo el comienzo! 💪\n¡Tu conocimiento crece con cada ronda! ¡No te rindas!",
        "¡Sigue adelante! 💪\n¡Aprendes algo nuevo en cada partida! ¡Siguiente ronda!"
    ],
    fr: [
        "C'était un bon début ! 💪\nChaque expert en musique a commencé petit. Jouons tout de suite une autre partie !",
        "Continue comme ça ! 💪\nÀ chaque partie tu découvres de nouvelles chansons. Essaie encore !",
        "Ne lâche pas ! 💪\nTu es sur la bonne voie ! C'est en forgeant qu'on devient forgeron !",
        "Garde la tête haute ! 💪\nTout le monde débute un jour ! Tes connaissances musicales grandiront avec le temps !",
        "Persévère ! 💪\nTu apprends à chaque partie ! Réessaie tout de suite !",
        "Tu y arriveras ! 💪\nC'est en pratiquant qu'on devient musicien ! En route pour la prochaine partie !",
        "Bon essai ! 💪\nTu t'amélioreras avec le temps ! Continue comme ça !",
        "Pas mal ! 💪\nChaque début est un pas en avant ! Continue ainsi !",
        "Ce n'est que le début ! 💪\nTes connaissances grandissent à chaque partie ! Persévère !",
        "Continue ! 💪\nTu apprends quelque chose de nouveau à chaque partie ! Prochaine manche !"
    ],
    it: [
        "È stato un buon inizio! 💪\nOgni esperto di musica ha iniziato da piccolo. Giochiamo subito un'altra partita!",
        "Continua così! 💪\nCon ogni partita imparerai nuove canzoni. Prova di nuovo subito!",
        "Non mollare! 💪\nSei sulla strada giusta! La pratica rende perfetti!",
        "Su con la testa! 💪\nTutti iniziano da qualche parte! La tua conoscenza musicale cresce con il tempo!",
        "Persevera! 💪\nImpari con ogni partita! Prova di nuovo subito!",
        "Ce la farai! 💪\nLa pratica rende maestri! Avanti con la prossima partita!",
        "Buon tentativo! 💪\nMigliorerai con il tempo! Continua così!",
        "Non male! 💪\nOgni inizio è un passo avanti! Continua così!",
        "Questo è solo l'inizio! 💪\nLa tua conoscenza cresce con ogni partita! Non mollare!",
        "Continua così! 💪\nImpari qualcosa di nuovo da ogni partita! Prossimo round!"
    ]
}

const { saveGameResult } = useGameScore()

// At game end
const finishGame = async () => {
    try {
        if (!session.value?.data?.user?.id) {
            console.error('No active session')
            return
        }

        let earnedLP = ''
        let message = ''

        // Bestimme LP und wähle passende Nachricht
        if (allQuestionsCorrect.value) {
            earnedLP = 'gold'
            message = goldMessages[locale.value][Math.floor(Math.random() * goldMessages[locale.value].length)]
        } else if (correctAnswers.value >= (maxQuestions.value * 0.75)) {
            earnedLP = 'silver'
            message = silverMessages[locale.value][Math.floor(Math.random() * silverMessages[locale.value].length)]
        } else if (correctAnswers.value >= (maxQuestions.value * 0.5)) {
            earnedLP = 'bronze'
            message = bronzeMessages[locale.value][Math.floor(Math.random() * bronzeMessages[locale.value].length)]
        } else {
            message = participationMessages[locale.value][Math.floor(Math.random() * participationMessages[locale.value].length)]
        }

        // Zeige die Nachricht im Modal
        resultMessage.value = message

        await saveGameResult(
            category,
            totalPoints.value,
            earnedLP,
            locale.value
        )
    } catch (error) {
        console.error('Error saving game results:', error)
    }
}

watch(() => gameFinished.value, (isFinished) => {
    if (isFinished) {
        finishGame()
    }
})

const resultMessage = ref('')

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
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--padding-large);

    .end-content {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-large);
        box-shadow: var(--box-shadow);
        border: 1px solid rgb(255 255 255 / 10%);
        max-width: 600px;
        width: 100%;
        animation: slideUp 0.5s var(--transition-bounce);
    }

    .end-header {
        text-align: center;
        margin-bottom: var(--padding-large);

        h2 {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            margin-bottom: var(--padding-large);
            background: linear-gradient(to right, var(--primary-color), var(--highlight-color));
            -webkit-background-clip: text;
            color: transparent;
        }
    }

    .final-score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--padding-large);

        @media (min-width: 768px) {
            flex-direction: row;
            justify-content: center;
        }
    }

    .score-circle {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary-color), var(--highlight-color));
        padding: 4px;
        animation: pulse 2s infinite;

        .score-inner {
            width: 100%;
            height: 100%;
            background: var(--surface-color);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .points {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(to right, var(--primary-color), var(--highlight-color));
            -webkit-background-clip: text;
            color: transparent;
        }

        .points-label {
            font-size: 1rem;
            opacity: 0.8;
        }
    }

    .stats {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);

        .stat-item {
            background: rgb(255 255 255 / 5%);
            padding: var(--padding-medium);
            border-radius: var(--border-radius);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .stat-label {
            font-size: 0.9rem;
            opacity: 0.7;
        }

        .stat-value {
            font-size: 1.2rem;
            font-weight: 600;
        }
    }

    .reward-section {
        text-align: center;
        margin: var(--padding-large) 0;
        padding: var(--padding-large);
        border-radius: var(--border-radius);
        background: rgb(255 255 255 / 5%);

        &.gold {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.2));
        }

        &.silver {
            background: linear-gradient(135deg, rgba(192, 192, 192, 0.1), rgba(192, 192, 192, 0.2));
        }

        &.bronze {
            background: linear-gradient(135deg, rgba(205, 127, 50, 0.1), rgba(205, 127, 50, 0.2));
        }

        .record-icon {
            margin-bottom: var(--padding-medium);

            .icon {
                filter: drop-shadow(0 0 8px currentColor);
            }
        }

        .reward-text {
            font-size: 1.1rem;
            line-height: 1.6;
        }
    }

    .end-actions {
        display: flex;
        justify-content: center;
        margin-top: var(--padding-large);

        .home-button {
            background: var(--primary-color);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--padding-small);
            padding: var(--padding-medium) var(--padding-large);
            font-size: 1.1rem;
            font-weight: 600;
            transition: all var(--transition-speed);
            border-radius: var(--border-radius);

            &:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
                box-shadow: var(--box-shadow-hover);
            }
        }
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0.4);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(var(--primary-color-rgb), 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0);
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

// Slide transition
.slide-enter-active,
.slide-leave-active {
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

.slide-leave-to {
    opacity: 0;
    transform: translateX(-30px);
}

// Optional: Add some base styling to prevent layout shifts
.game-content,
.game-end-screen {
    position: relative;
    min-height: 400px; // Adjust based on your content
}
</style>
