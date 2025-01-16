<template>
    <div class="question-container" role="main" aria-label="Quiz Frage">
        <!-- Frage -->
        <div class="question" role="heading" aria-level="1">
            <h2 id="question-text">{{ question.question }}</h2>
        </div>

        <!-- Antwortmöglichkeiten -->
        <div class="options" role="group" aria-labelledby="question-text">
            <TransitionGroup name="fade-shrink">
                <button v-for="(option, index) in currentOptions" :key="option" 
                    class="option-button"
                    v-show="!hiddenOptions.includes(option)" 
                    @click="$emit('select-answer', option)"
                    :disabled="disabled || hiddenOptions.includes(option)" 
                    :aria-label="$t('game.selectAnswer', { answer: option })"
                    :aria-hidden="hiddenOptions.includes(option)"
                    :aria-disabled="disabled || hiddenOptions.includes(option)"
                    :tabindex="hiddenOptions.includes(option) ? -1 : 0">
                    {{ option }}
                </button>
            </TransitionGroup>
        </div>

        <!-- Telefonjoker Antwort -->
        <div v-if="phoneExpertOpinion" class="phone-expert" role="region" aria-label="Expertenrat">
            <h3 id="expert-title">{{ t('game.expert.title') }}</h3>
            <div class="expert-message" aria-labelledby="expert-title">
                <div class="expert-header">
                    <Icon name="material-symbols:call" class="phone-icon" aria-hidden="true" />
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
                <button class="joker-button" 
                    @click="$emit('use-fifty-fifty')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion" 
                    :aria-label="$t('game.jokers.fiftyFifty.ariaLabel')"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:balance" />
                    </div>
                    <span class="joker-label">{{ t('game.jokers.fiftyFifty.title') }}</span>
                </button>
                <button class="joker-button" 
                    @click="$emit('use-audience')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="$t('game.jokers.audience.ariaLabel')"
                    :aria-disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion">
                    <div class="joker-icon" aria-hidden="true">
                        <Icon name="material-symbols:group" />
                    </div>
                    <span class="joker-label">{{ t('game.jokers.audience.title') }}</span>
                </button>
                <button class="joker-button" 
                    @click="$emit('use-phone')"
                    :disabled="remainingJokers === 0 || jokerUsedForCurrentQuestion"
                    :aria-label="$t('game.jokers.phone.ariaLabel')"
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
@use '@/assets/scss/mixins' as *;

.question-container {
    @include flex-stack;
    @include container;
    @include spacing-y(2rem);
    gap: clamp(var(--padding-medium), 4vw, var(--padding-large));
    margin-top: 2rem;
}

.question {
    @include surface-card;
    text-align: center;

    h2 {
        margin: 0;
        @include responsive-text(1rem, 1.5rem);
        color: var(--text-color);
        font-weight: 500;
    }

    &:focus-within {
        outline: none;
        box-shadow: 0 0 0 3px var(--focus-outline-color);
    }
}

.options {
    display: grid;
    @include custom-scrollbar;
    gap: var(--padding-medium);
    width: 100%;
    max-width: min(100%, 800px);
    margin: 0 auto;
    position: relative;
    max-height: 60vh;
    overflow-y: auto;
}

.option-button {
    @include button-primary;
    width: 100%;
    max-width: min(100%, 800px);
    min-height: var(--min-touch-target);
    font-size: clamp(1rem, 2.5vw, 1.2rem);
    text-align: center;
    padding: clamp(var(--padding-small), 2vw, var(--padding-medium));
    background-color: var(--primary-color);
    color: var(--button-text-color);
    border: none;
    box-shadow: var(--box-shadow);
    transition: all 0.3s ease;
    
    &:hover:not(:disabled) {
        background-color: var(--primary-color-dark);
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }
    
    &:active:not(:disabled) {
        transform: translateY(0);
    }
    
    &:focus-visible {
        outline: none;
        box-shadow: 0 0 0 var(--focus-outline-width) var(--focus-outline-color),
                    var(--box-shadow);
    }

    &:disabled {
        @include disabled-state;
        background-color: var(--surface-color);
        color: var(--text-secondary);
        box-shadow: none;
    }
}

.phone-expert {
    @include surface-card;
    @include responsive-container;

    h3 {
        @include section-title;
        @include responsive-text(1rem, 1.2rem);
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
                @include label-text;
                @include responsive-text(0.9rem, 1.1rem);
            }
        }

        .message-content {
            .expert-answer {
                @include text-truncate;
                margin: 0 0 var(--padding-medium);
                color: var(--text-color);
                font-style: italic;
                font-size: clamp(0.9rem, 2vw, 1rem);
                line-height: 1.6;
            }

            .confidence-bar-container {
                .confidence-bar {
                    @include progress-bar;
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
    @include surface-card;
    @include responsive-container;

    h3 {
        @include section-title;
        @include responsive-text(1.1rem, 1.3rem);
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
    }

    .joker-button {
        @include icon-button;
        @include button-secondary;
        flex: 1;
        min-width: 120px;
        max-width: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        
        &:hover:not(:disabled) {
            background-color: var(--secondary-color-dark);
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
        }
        
        &:active:not(:disabled) {
            transform: translateY(0);
        }
        
        &:focus-visible {
            outline: none;
            box-shadow: 0 0 0 var(--focus-outline-width) var(--focus-outline-color),
                        var(--box-shadow);
        }

        &:disabled {
            @include disabled-state;
            background-color: var(--surface-color);
            color: var(--text-secondary);
            box-shadow: none;
        }
        
        .joker-icon {
            font-size: 1.5rem;
        }
        
        .joker-label {
            font-size: 0.9rem;
            text-align: center;
        }
    }

    .jokers-remaining {
        @include secondary-text;
        text-align: center;
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

.sr-only {
  @include sr-only;
}

.expert-answer {
  @include text-truncate;
  margin: 0 0 var(--padding-medium);
  color: var(--text-color);
  font-style: italic;
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
