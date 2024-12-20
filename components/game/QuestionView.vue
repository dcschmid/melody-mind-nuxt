<template>
    <div class="question-container" role="main" aria-label="Quiz Frage">
        <!-- Frage -->
        <div class="question" role="heading" aria-level="1">
            <h2 id="question-text">{{ question.question }}</h2>
        </div>

        <!-- Antwortmöglichkeiten -->
        <div class="options" role="group" aria-labelledby="question-text">
            <TransitionGroup name="fade-shrink">
                <button v-for="(option, index) in currentOptions" :key="option" class="button option-button"
                    v-show="!hiddenOptions.includes(option)" @click="$emit('select-answer', option)"
                    :disabled="disabled || hiddenOptions.includes(option)" :aria-label="option"
                    :aria-hidden="hiddenOptions.includes(option)" :tabindex="hiddenOptions.includes(option) ? -1 : 0">
                    {{ option }}
                </button>
            </TransitionGroup>
        </div>

        <!-- Telefonjoker Antwort -->
        <div v-if="phoneExpertOpinion" class="phone-expert" role="region" aria-label="Expertenrat">
            <h3 id="expert-title">{{ t('game.expert.title') }}</h3>
            <div class="expert-message" aria-labelledby="expert-title">
                <div class="expert-header">
                    <Icon name="material-symbols:phone" class="phone-icon" aria-hidden="true" />
                    <span class="expert-name">{{ phoneExpertOpinion.expert }}</span>
                </div>
                <div class="message-content">
                    <p class="expert-answer">{{ phoneExpertOpinion.message }}</p>
                    <div class="confidence-bar-container" role="progressbar" :aria-valuenow="phoneExpertConfidence"
                        aria-valuemin="0" aria-valuemax="100"
                        :aria-label="'Experten Konfidenz: ' + phoneExpertConfidence + '%'">
                        <div class="confidence-bar" :style="{ '--confidence': phoneExpertConfidence + '%' }" :class="{
                            'high': phoneExpertConfidence >= 80,
                            'medium': phoneExpertConfidence >= 60 && phoneExpertConfidence < 80,
                            'low': phoneExpertConfidence < 60
                        }">
                            <div class="confidence-level"></div>
                        </div>
                        <span class="confidence-text">
                            {{ phoneExpertConfidence }}% {{ t('game.confidence') }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Publikumsjoker Antwort -->
        <div v-if="audienceOpinion && Object.keys(audienceOpinion).length > 0" class="audience-opinion" role="region"
            aria-label="Publikumsmeinung">
            <h3 id="audience-title">{{ t('game.jokers.audience.title') }}</h3>
            <div class="audience-results" aria-labelledby="audience-title">
                <div v-for="(percentage, option) in audienceOpinion" :key="option" class="audience-bar-container"
                    role="progressbar" :aria-valuenow="percentage" aria-valuemin="0" aria-valuemax="100"
                    :aria-label="option + ': ' + percentage + '%'">
                    <div class="option-label">{{ option }}</div>
                    <div class="audience-bar">
                        <div class="percentage-bar" :style="{ width: percentage + '%' }">
                        </div>
                    </div>
                    <div class="percentage-label">{{ percentage }}%</div>
                </div>
            </div>
        </div>

        <!-- Joker -->
        <div class="jokers-section" role="group" aria-label="Verfügbare Joker">
            <div class="joker-buttons">
                <button class="button joker-button" @click="$emit('use-fifty-fifty')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion" aria-label="50:50 Joker"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:balance" />
                    </div>
                    <span class="joker-label">{{ t('game.jokers.fiftyFifty.title') }}</span>
                </button>
                <button class="button joker-button" @click="$emit('use-audience')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="t('game.audience') + ' Joker'"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:group" />
                    </div>
                    <span class="joker-label">{{ t('game.jokers.audience.title') }}</span>
                </button>
                <button class="button joker-button" @click="$emit('use-phone')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="t('game.phone') + ' Joker'"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="tabler:phone" />
                    </div>
                    <span class="joker-label">{{ t('game.jokers.phone.title') }}</span>
                </button>
            </div>
            <p class="jokers-remaining" role="status" aria-live="polite">
                {{ remainingJokers }} {{ t('game.jokers.remaining') }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

const { t } = useI18n()

const props = defineProps<{
    question: {
        question: string
        correctAnswer: string
        options: string[]
    }
    currentOptions: string[]
    hiddenOptions: string[]
    disabled: boolean
    remainingJokers: number
    jokerUsedForCurrentQuestion: boolean
    phoneExpertOpinion: {
        expert: string
        message: string
        confidence: number
    } | null
    audienceOpinion: Record<string, number> | null
}>()

const phoneExpertConfidence = computed(() =>
    props.phoneExpertOpinion?.confidence ?? 0
)

defineEmits<{
    'select-answer': [answer: string]
    'use-fifty-fifty': []
    'use-audience': []
    'use-phone': []
}>()
</script>

<style scoped lang="scss">
.question-container {
    max-width: var(--content-width);
    margin: 0 auto;
    padding: 0 var(--padding-small);
    display: flex;
    flex-direction: column;
    gap: clamp(var(--padding-medium), 4vw, var(--padding-large));

    &:focus-within {
        outline: none;
        box-shadow: 0 0 0 3px var(--focus-outline-color);
    }
}

.question {
    text-align: center;
    padding: clamp(var(--padding-small), 3vw, var(--padding-medium));
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);

    h2 {
        margin: 0;
        font-size: clamp(1rem, 2.5vw, 1.5rem);
        line-height: 1.4;
        color: var(--text-color);
        font-weight: 500;
        letter-spacing: var(--spacing-text);
    }

    &:focus-within {
        outline: none;
        box-shadow: 0 0 0 3px var(--focus-outline-color);
    }
}

.options {
    display: grid;
    gap: var(--padding-medium);
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;
    position: relative;
}

.option-button {
    width: 100%;
    min-height: clamp(50px, 8vh, 70px);
    padding: clamp(var(--padding-small), 2vw, var(--padding-medium));
    font-size: clamp(0.9rem, 2vw, var(--body-font-size));
    background: var(--surface-color);
    color: var(--text-color);
    border: 2px solid var(--primary-color);
    border-radius: var(--border-radius);
    transition: all var(--transition-speed) var(--transition-bounce);
    text-align: center;
    line-height: 1.4;
    letter-spacing: var(--spacing-text);
    white-space: pre-line;
    box-shadow: var(--box-shadow);

    &:hover:not(:disabled) {
        background: var(--primary-color);
        color: var(--button-text-color);
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }

    &:active:not(:disabled) {
        transform: translateY(0);
    }

    &:disabled {
        opacity: var(--opacity-disabled);
        cursor: not-allowed;
        background: var(--surface-color);
        color: var(--text-secondary);
        border-color: var(--text-secondary);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &:focus:hover {
        outline: none;
        box-shadow: 0 0 0 3px var(--focus-outline-color),
            var(--box-shadow-hover);
    }
}

.phone-expert {
    padding: clamp(var(--padding-small), 3vw, var(--padding-medium));
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    max-width: min(100%, 800px);
    margin: 0 auto;
    width: 100%;

    h3 {
        margin: 0 0 var(--padding-medium);
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        color: var(--text-color);
        text-align: center;
        letter-spacing: var(--spacing-text);
    }

    .expert-message {
        .expert-header {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-small);

            .phone-icon {
                color: var(--primary-color);
                font-size: clamp(1.2rem, 3vw, 1.5rem);
            }

            .expert-name {
                font-weight: 500;
                color: var(--text-color);
                font-size: clamp(0.9rem, 2vw, 1.1rem);
            }
        }

        .message-content {
            .expert-answer {
                margin: 0 0 var(--padding-medium);
                color: var(--text-color);
                font-style: italic;
                font-size: clamp(0.9rem, 2vw, 1rem);
                line-height: 1.6;
            }

            .confidence-bar-container {
                .confidence-bar {
                    height: 6px;
                    background: var(--surface-color);
                    border-radius: 3px;
                    overflow: hidden;
                    margin-bottom: var(--padding-small);
                    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);

                    .confidence-level {
                        height: 100%;
                        width: var(--confidence);
                        transition: width var(--transition-speed) var(--transition-bounce);
                    }

                    &.high .confidence-level {
                        background: var(--success-color);
                    }

                    &.medium .confidence-level {
                        background: var(--highlight-color);
                    }

                    &.low .confidence-level {
                        background: var(--error-color);
                    }
                }

                .confidence-text {
                    font-size: clamp(0.8rem, 1.8vw, 0.9rem);
                    color: var(--text-secondary);
                }
            }
        }
    }
}

.audience-opinion {
    padding: clamp(var(--padding-small), 3vw, var(--padding-medium));
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    max-width: min(100%, 800px);
    margin: 0 auto;
    width: 100%;

    h3 {
        margin: 0 0 var(--padding-large);
        font-size: clamp(1.1rem, 2.5vw, 1.3rem);
        color: var(--text-color);
        text-align: center;
        letter-spacing: var(--spacing-text);
        font-weight: 600;
    }

    .audience-results {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        padding: 0 var(--padding-small);
    }

    .audience-bar-container {
        display: grid;
        grid-template-columns: 1fr 70px;
        align-items: center;
        gap: var(--padding-small);
        padding: var(--padding-medium) var(--padding-small);
        border-bottom: 1px solid var(--border-color);
        position: relative;

        &:last-child {
            border-bottom: none;
        }

        .option-label {
            font-size: clamp(1rem, 2vw, 1.1rem);
            color: var(--text-color);
            font-weight: 500;
            margin-bottom: var(--padding-small);
            grid-column: 1 / -1;
            line-height: 1.4;
        }

        .audience-bar {
            height: 28px;
            background: var(--surface-color-alt);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
            grid-column: 1;

            .percentage-bar {
                height: 100%;
                background: var(--primary-color);
                transition: width var(--transition-speed) var(--transition-bounce);
                border-radius: var(--border-radius);
            }
        }

        .percentage-label {
            font-size: clamp(1rem, 2vw, 1.1rem);
            color: var(--text-color);
            text-align: right;
            font-weight: 600;
            grid-column: 2;
        }
    }
}

.jokers-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(var(--padding-small), 2vw, var(--padding-medium));
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;

    .joker-buttons {
        display: flex;
        gap: clamp(var(--padding-small), 2vw, var(--padding-medium));
        justify-content: center;
        flex-wrap: wrap;
        width: 100%;
    }

    .joker-button {
        flex: 1;
        min-width: clamp(80px, 20vw, 120px);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--padding-small);
        padding: clamp(var(--padding-small), 2vw, var(--padding-medium));
        background: var(--surface-color);
        border-radius: var(--border-radius);
        color: var(--text-color);
        transition: all var(--transition-speed) var(--transition-bounce);
        box-shadow: var(--box-shadow);

        &:hover:not(:disabled) {
            transform: translateY(-2px);
            background: var(--primary-color);
            color: var(--button-text-color);
            box-shadow: var(--box-shadow-hover);
        }

        &:active:not(:disabled) {
            transform: translateY(0);
        }

        &:disabled {
            opacity: var(--opacity-disabled);
            cursor: not-allowed;
            background: var(--surface-color);
            color: var(--text-secondary);
            border-color: var(--text-secondary);
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
        }

        &:focus:hover {
            outline: none;
            box-shadow: 0 0 0 3px var(--focus-outline-color),
                var(--box-shadow-hover);
        }

        .joker-icon {
            font-size: clamp(1.2rem, 3vw, 1.5rem);
        }

        .joker-label {
            font-size: clamp(0.8rem, 1.8vw, 0.9rem);
            text-align: center;
            white-space: nowrap;
        }
    }

    .jokers-remaining {
        margin: 0;
        font-size: clamp(0.8rem, 1.8vw, 0.9rem);
        color: var(--text-secondary);
        text-align: center;
    }
}

.fade-shrink-move,
.fade-shrink-enter-active,
.fade-shrink-leave-active {
    transition: all 0.4s ease;
}

.fade-shrink-enter-from,
.fade-shrink-leave-to {
    opacity: 0;
    transform: scale(0.6);
}

.fade-shrink-leave-active {
    position: absolute;
}

@media (forced-colors: active) {

    .option-button,
    .joker-button {
        border: 2px solid ButtonText;

        &:disabled {
            opacity: 1;
            border: 2px solid GrayText;
            color: GrayText;
        }
    }

    .confidence-bar {
        border: 1px solid ButtonText;

        .confidence-level {
            background: Highlight;
        }
    }
}

@media (prefers-reduced-motion: reduce) {

    .option-button,
    .joker-button {
        transition: none;

        &:hover:not(:disabled) {
            transform: none;
        }
    }

    .confidence-level {
        transition: none;
    }
}

@media (forced-colors: active) {
    .audience-bar {
        border: 1px solid ButtonText;

        .percentage-bar {
            background: Highlight;
        }
    }
}

@media (prefers-reduced-motion: reduce) {
    .percentage-bar {
        transition: none;
    }
}
</style>
