<template>
    <div class="question-container" role="main" :aria-label="t('game.aria.quizQuestion')">
        <!-- Frage -->
        <div class="question-section" role="region" aria-labelledby="question-text">
            <h1 id="question-text" class="question-text">{{ question.question }}</h1>
        </div>

        <!-- Antwortmöglichkeiten -->
        <div class="answer-options" role="group" :aria-label="t('game.aria.answerOptions')">
            <TransitionGroup v-bind="transitionGroupProps">
                <button v-for="(option, index) in currentOptions" :key="option" 
                    class="answer-button"
                    v-show="!hiddenOptions.includes(option)" 
                    @click="$emit('select-answer', option)"
                    :disabled="disabled || hiddenOptions.includes(option)" 
                    :aria-label="t('game.selectAnswer', { answer: option })"
                    :aria-hidden="hiddenOptions.includes(option)"
                    :aria-disabled="disabled || hiddenOptions.includes(option)"
                    :tabindex="hiddenOptions.includes(option) ? -1 : 0"
                    :data-index="index + 1">
                    <span class="answer-text">{{ option }}</span>
                    <span class="visually-hidden">{{ t('game.option', { number: index + 1 }) }}</span>
                </button>
            </TransitionGroup>
        </div>

        <!-- Telefonjoker Antwort -->
        <div v-if="phoneExpertOpinion" class="phone-expert" role="region" :aria-label="t('game.aria.expertAdvice')" aria-labelledby="expert-title">
            <h2 id="expert-title" class="section-title">{{ t('game.expert.title') }}</h2>
            <div class="expert-message">
                <div class="expert-header">
                    <Icon name="material-symbols:call" class="phone-icon" aria-hidden="true" />
                    <span class="expert-name">{{ phoneExpertOpinion.expert }}</span>
                </div>
                <div class="message-content">
                    <p class="expert-answer">{{ phoneExpertOpinion.message }}</p>
                    <div class="confidence-bar-container" role="progressbar" 
                        :aria-valuenow="phoneExpertConfidence"
                        aria-valuemin="0" 
                        aria-valuemax="100"
                        :aria-label="t('game.expert.confidence', { value: phoneExpertConfidence })">
                        <div class="confidence-bar" :style="{ '--confidence': phoneExpertConfidence + '%' }" :class="{
                            'high': phoneExpertConfidence >= 80,
                            'medium': phoneExpertConfidence >= 60 && phoneExpertConfidence < 80,
                            'low': phoneExpertConfidence < 60
                        }">
                            <div class="confidence-level"></div>
                        </div>
                        <span class="confidence-text" aria-hidden="true">
                            {{ phoneExpertConfidence }}% {{ t('game.confidence') }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Publikumsjoker Antwort -->
        <div v-if="audienceOpinion && Object.keys(audienceOpinion).length > 0" 
            class="audience-opinion" 
            role="region"
            :aria-label="t('game.aria.audienceOpinion')"
            aria-labelledby="audience-title">
            <h2 id="audience-title" class="section-title">{{ t('game.jokers.audience.title') }}</h2>
            <div class="audience-results">
                <div v-for="(percentage, option) in audienceOpinion" :key="option" 
                    class="audience-bar-container"
                    role="progressbar" 
                    :aria-valuenow="percentage" 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                    :aria-label="t('game.jokers.audience.result', { option, percentage })">
                    <div class="option-label" aria-hidden="true">{{ option }}</div>
                    <div class="audience-bar">
                        <div class="percentage-bar" :style="{ width: percentage + '%' }"></div>
                    </div>
                    <div class="percentage-label" aria-hidden="true">{{ percentage }}%</div>
                </div>
            </div>
        </div>

        <!-- Joker -->
        <div class="jokers-section" role="group" :aria-label="t('game.jokers.title')">
            <h2 class="visually-hidden">{{ t('game.jokers.title') }}</h2>
            <div class="joker-buttons">
                <button class="joker-button" 
                    @click="$emit('use-fifty-fifty')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion" 
                    :aria-label="t('game.jokers.fiftyFifty.ariaLabel')"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:balance" />
                    </div>
                </button>
                <button class="joker-button" 
                    @click="$emit('use-audience')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="t('game.jokers.audience.ariaLabel')"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:group" />
                    </div>
                </button>
                <button class="joker-button" 
                    @click="$emit('use-phone')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="t('game.jokers.phone.ariaLabel')"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="tabler:phone" />
                    </div>
                </button>
            </div>
            <p class="jokers-remaining" role="status" aria-live="polite">
                {{ t('game.jokers.remainingCount', { count: remainingJokers }) }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { computed, shallowRef } from 'vue'

const { t } = useI18n()

// Optimiere Props mit shallowRef für komplexe Objekte
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

// Memoize computed properties
const phoneExpertConfidence = computed(() =>
    props.phoneExpertOpinion?.confidence ?? 0
)

// Optimiere Transitions
const transitionGroupProps = shallowRef({
    name: 'fade-shrink',
    tag: 'div',
    class: 'answers-grid',
    moveClass: 'move-transition'
})

defineEmits<{
    'select-answer': [answer: string]
    'use-fifty-fifty': []
    'use-audience': []
    'use-phone': []
}>()
</script>

<style scoped lang="scss">
@use '@/assets/scss/mixins' as *;

.question-container {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    width: 100%;
    margin: 0 auto;
    padding: var(--padding-medium) 0;
}

.question-section {
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    border: 2px solid var(--surface-color-light);
    box-shadow: var(--box-shadow);

    @media (min-width: 640px) {
        padding: var(--padding-large);
    }
}

.question-text {
    text-align: center;
    margin-bottom: var(--padding-medium);
    font-size: var(--font-size-responsive-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);
    line-height: var(--line-height-normal);
}

.answers-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--padding-medium);
    margin: 0 auto;
    width: 100%;
}

.answer-button {
    @include button-secondary;
    min-height: var(--min-touch-target);
    width: 100%;
    padding: var(--padding-medium);
    font-size: var(--font-size-responsive-md);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-normal);
    text-align: center;
    border: 2px solid transparent;
    transition: all var(--transition-speed) var(--transition-bounce);
    position: relative;

    &:hover:not(:disabled) {
        transform: translateY(-2px);
        border-color: var(--highlight-color);
        box-shadow: var(--box-shadow-hover);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
        border-color: var(--highlight-color);
    }

    &:disabled {
        opacity: var(--opacity-disabled);
        cursor: not-allowed;
    }
}

.section-title {
    font-size: var(--font-size-responsive-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
    line-height: var(--line-height-tight);
    letter-spacing: var(--spacing-text);
}

.phone-expert {
    @include surface-card;
    border: 2px solid var(--surface-color-light);
    padding: var(--padding-medium);
    margin: var(--padding-medium) 0;

    .expert-message {
        .expert-header {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-medium);

            .phone-icon {
                color: var(--primary-color);
                font-size: var(--font-size-responsive-xl);
            }

            .expert-name {
                font-size: var(--font-size-responsive-md);
                font-weight: var(--font-weight-semibold);
                color: var(--text-color);
            }
        }

        .confidence-bar-container {
            .confidence-bar {
                height: 8px;
                background: var(--surface-color-light);
                border-radius: calc(var(--border-radius) / 2);
                overflow: hidden;
                margin-bottom: var (--padding-small);
                box-shadow: var(--box-shadow);

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
                font-size: var(--font-size-base);
                font-weight: var(--font-weight-medium);
                color: var(--text-secondary);
            }
        }
    }
}

.audience-opinion {
    @include surface-card;
    border: 2px solid var(--surface-color-light);
    padding: var(--padding-medium);
    margin: var(--padding-medium) 0;

    .audience-results {
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
    }

    .audience-bar-container {
        .audience-bar {
            height: var(--min-touch-target);
            background: var(--surface-color-light);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--box-shadow);

            .percentage-bar {
                height: 100%;
                background: var(--primary-color);
                transition: width var(--transition-speed) var(--transition-bounce);
                border-radius: var(--border-radius);
            }
        }

        .percentage-label {
            font-size: var(--font-size-responsive-md);
            color: var(--text-color);
            font-weight: var(--font-weight-semibold);
        }
    }
}

.jokers-section {
    @include flex-stack;
    gap: var(--padding-medium);
    width: 100%;
    margin: var(--padding-medium) auto;

    .joker-buttons {
        display: flex;
        justify-content: center;
        gap: var(--padding-medium);
        flex-wrap: wrap;
    }

    .joker-button {
        @include button-secondary;
        min-width: var(--min-touch-target);
        min-height: var(--min-touch-target);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all var(--transition-speed) var(--transition-bounce);

        &:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
        }

        &:disabled {
            opacity: var(--opacity-disabled);
        }

        .joker-icon {
            font-size: var(--font-size-responsive-xl);
            color: var(--text-color);
        }
    }

    .jokers-remaining {
        color: var(--text-secondary);
        font-size: var(--font-size-base);
        font-weight: var(--font-weight-medium);
        text-align: center;
    }
}

@media (prefers-reduced-motion: reduce) {
    .answer-button,
    .joker-button,
    .confidence-level,
    .percentage-bar {
        transition: none;
    }

    .answer-button:hover:not(:disabled),
    .joker-button:hover:not(:disabled) {
        transform: none;
    }
}

.visually-hidden {
    @include sr-only;
}

.move-transition {
    transition: transform var(--transition-speed) var(--transition-bounce);
}

.fade-shrink-move,
.fade-shrink-enter-active,
.fade-shrink-leave-active {
    transition: all var(--transition-speed) var(--transition-bounce);
}

.fade-shrink-enter-from,
.fade-shrink-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

.fade-shrink-leave-active {
    position: absolute;
}
</style>
