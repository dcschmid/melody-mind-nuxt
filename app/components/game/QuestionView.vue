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
    gap: var(--padding-small);
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;
    padding: var(--padding-small);

    @media (min-width: 375px) {
        gap: var(--padding-medium);
        padding: var(--padding-medium);
    }

    @media (min-width: 640px) {
        gap: var(--padding-large);
    }
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
    font-size: clamp(1.25rem, 2.5vw, 1.75rem);
    font-weight: 600;
    color: var(--text-color);
    margin: 0;
    line-height: 1.5;
    text-align: left;
    letter-spacing: 0.01em;
}

.answers-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--padding-medium);
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
}

.answer-button {
    @include button-secondary;
    min-height: 64px;
    width: 100%;
    padding: var(--padding-medium);
    font-size: clamp(1.25rem, 2vw, 1.5rem);
    font-weight: 600;
    line-height: 1.5;
    text-align: center;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    position: relative;

    @media (min-width: 640px) {
        min-height: 80px;
        padding: var(--padding-medium) var(--padding-large);
    }

    &:hover:not(:disabled) {
        transform: translateY(-2px);
        border-color: var(--highlight-color);
    }

    &:focus-visible {
        outline: 3px solid var(--focus-outline-color);
        outline-offset: 2px;
        border-color: var(--highlight-color);
    }

    &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .answer-text {
        font-size: clamp(1rem, 2vw, 1.2rem);
        line-height: 1.5;
        letter-spacing: 0.01em;
    }
}

.section-title {
    font-size: clamp(1.25rem, 2.5vw, 1.5rem);
    font-weight: 600;
    color: var(--text-color);
    margin: 0 0 var(--padding-medium);
    line-height: 1.4;
    letter-spacing: 0.01em;
}

.phone-expert {
    @include surface-card;
    @include responsive-container;
    border: 2px solid var(--surface-color-light);

    h2 {
        @include section-title;
        font-size: clamp(1.25rem, 2.5vw, 1.5rem);
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
    }

    .expert-message {
        .expert-header {
            display: flex;
            align-items: center;
            gap: var(--padding-small);
            margin-bottom: var(--padding-medium);

            .phone-icon {
                color: var(--primary-color);
                font-size: 1.75rem;
            }

            .expert-name {
                font-size: 1.25rem;
                font-weight: 600;
                color: var(--text-color);
            }
        }

        .message-content {
            .expert-answer {
                margin: 0 0 var(--padding-medium);
                color: var(--text-color);
                font-style: italic;
                font-size: 1.1rem;
                line-height: 1.6;
                white-space: normal;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }

            .confidence-bar-container {
                .confidence-bar {
                    height: 8px;
                    background: var(--surface-color-light);
                    border-radius: 4px;
                    overflow: hidden;
                    margin-bottom: var(--padding-small);
                    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);

                    .confidence-level {
                        height: 100%;
                        width: var(--confidence);
                        transition: width 0.3s ease;
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
                    font-size: 1rem;
                    font-weight: 500;
                    color: var(--text-secondary);
                }
            }
        }
    }
}

.audience-opinion {
    @include surface-card;
    @include responsive-container;
    border: 2px solid var(--surface-color-light);

    h2 {
        @include section-title;
        font-size: clamp(1.25rem, 2.5vw, 1.5rem);
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
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
            @include progress-bar;
            height: 28px;
            background: var(--surface-color-alt);
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
            grid-column: 1;

            .percentage-bar {
                height: 100%;
                background: var(--primary-color);
                transition: width 0.3s ease;
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
    @include flex-stack;
    @include responsive-container;
    gap: clamp(var(--padding-small), 2vw, var(--padding-medium));
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;

    .joker-buttons {
        @include flex-row(clamp(var(--padding-small), 2vw, var(--padding-medium)));
        justify-content: center;
        width: 100%;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        padding-bottom: var(--padding-small);
    }

    .joker-button {
        @include icon-button;
        @include button-secondary;
        flex: 0 0 auto;
        min-width: 80px;
        max-width: 150px;
        min-height: 64px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
        padding: var(--padding-small);
        border: 2px solid transparent;
        font-weight: 500;
        
        .joker-icon {
            font-size: 1.75rem;
            color: currentColor;
        }

        .joker-label {
            font-size: 1rem;
            text-align: center;
            line-height: 1.2;
        }
        
        &:hover:not(:disabled) {
            background-color: var(--secondary-color-dark);
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
            border-color: var(--highlight-color);
        }
        
        &:focus-visible {
            outline: none;
            box-shadow: 0 0 0 3px var(--focus-outline-color),
                        var(--box-shadow);
            border-color: var(--highlight-color);
        }

        &:disabled {
            @include disabled-state;
            opacity: 0.7;
        }
    }

    .jokers-remaining {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 500;
        text-align: center;
        margin-top: var(--padding-small);
    }
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.move-transition {
    transition: transform 0.3s ease-out;
}

.fade-shrink-move,
.fade-shrink-enter-active,
.fade-shrink-leave-active {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-shrink-enter-from,
.fade-shrink-leave-to {
    opacity: 0;
    transform: scale(0.9);
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

.sr-only {
  @include sr-only;
}

.expert-answer {
  @include text-truncate;
  margin: 0 0 var(--padding-medium);
  color: var(--text-color);
  font-style: italic;
  font-size: 1.1rem;
  line-height: 1.6;
}

.audience-bar {
  @include progress-bar;
}

@include high-contrast {
    .option-button,
    .joker-button {
        border: 2px solid ButtonText;
        
        &:disabled {
            border-color: GrayText;
            color: GrayText;
        }
    }
}
</style>
