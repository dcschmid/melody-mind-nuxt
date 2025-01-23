<template>
    <section 
        id="difficulty-levels" 
        class="difficulty-section"
        :aria-labelledby="sectionTitleId"
        role="region"
    >
        <h2 :id="sectionTitleId" class="section-title">
            {{ t('gameRules.difficultyLevels.title') }}
        </h2>

        <p 
            class="section-text" 
            :id="introTextId"
            aria-live="polite"
        >
            {{ t('gameRules.difficultyLevels.intro') }}
        </p>

        <div 
            class="difficulty-levels" 
            role="list" 
            :aria-labelledby="introTextId"
        >
            <div 
                v-for="level in difficultyLevels" 
                :key="level"
                role="listitem"
                class="difficulty-item"
                :class="level"
            >
                <div class="difficulty-header">
                    <span 
                        class="difficulty-icon" 
                        :class="level"
                        aria-hidden="true"
                    >
                        <Icon :name="difficultyIcons[level]" />
                    </span>
                    <h3 :id="`${level}-title`" class="difficulty-title">
                        {{ t(`gameRules.difficultyLevels.levels.${level}.title`) }}
                    </h3>
                </div>
                <p 
                    class="difficulty-description"
                    :aria-labelledby="`${level}-title`"
                >
                    {{ t(`gameRules.difficultyLevels.levels.${level}.description`) }}
                </p>
            </div>
        </div>

        <p 
            class="section-text titles-intro" 
            :id="titlesIntroId"
            aria-live="polite"
        >
            {{ t('gameRules.difficultyLevels.titles.intro') }}
        </p>

        <div 
            class="achievement-titles" 
            role="list" 
            :aria-labelledby="titlesIntroId"
        >
            <div 
                v-for="title in achievementTitles" 
                :key="title"
                role="listitem"
                class="achievement-item"
                :class="title"
            >
                <div class="achievement-header">
                    <span 
                        class="achievement-icon" 
                        :class="title"
                        aria-hidden="true"
                    >
                        <Icon :name="achievementIcons[title]" />
                    </span>
                    <h3 :id="`${title}-title`" class="achievement-title">
                        {{ t(`gameRules.difficultyLevels.titles.${title}.title`) }}
                    </h3>
                </div>
                <p 
                    class="achievement-description"
                    :aria-labelledby="`${title}-title`"
                >
                    {{ t(`gameRules.difficultyLevels.titles.${title}.description`) }}
                </p>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

// Unique IDs für ARIA-Attribute
const sectionTitleId = 'difficulty-levels-title'
const introTextId = 'difficulty-levels-intro'
const titlesIntroId = 'achievement-titles-intro'

// Schwierigkeitsgrade und Errungenschaften
const difficultyLevels = ['easy', 'medium', 'hard'] as const
const achievementTitles = ['novice', 'master', 'legend'] as const

// Icons für Schwierigkeitsgrade
const difficultyIcons = {
    easy: 'material-symbols:stars-outline',
    medium: 'material-symbols:stars',
    hard: 'material-symbols:stars-rounded'
} as const

// Icons für Errungenschaften
const achievementIcons = {
    novice: 'material-symbols:military-tech-outline',
    master: 'material-symbols:military-tech',
    legend: 'material-symbols:military-tech-rounded'
} as const
</script>

<style lang="scss" scoped>
.difficulty-section {
    max-width: 1200px;
    margin: 0 auto;
    padding: clamp(1.5rem, 4vw, 3rem);
}

.section-title {
    font-size: clamp(1.75rem, 3vw, 2.5rem);
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: clamp(1.5rem, 4vw, 2.5rem);
    text-align: center;
    line-height: 1.3;
    letter-spacing: -0.01em;
}

.section-text {
    font-size: clamp(1.125rem, 2vw, 1.25rem);
    line-height: 1.6;
    color: var(--text-color);
    margin-bottom: clamp(2rem, 5vw, 3rem);
    max-width: 70ch;
    margin-left: auto;
    margin-right: auto;
    text-align: center;

    &.titles-intro {
        margin-top: clamp(2rem, 5vw, 3rem);
    }
}

.difficulty-levels,
.achievement-titles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: clamp(1rem, 3vw, 2rem);
    margin-bottom: clamp(2rem, 5vw, 3rem);
}

.difficulty-item,
.achievement-item {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: clamp(1.25rem, 3vw, 2rem);
    box-shadow: var(--box-shadow);
    border: 2px solid transparent;
    transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out;

    @media (hover: hover) {
        &:hover {
            transform: translateY(-2px);
            border-color: var(--primary-color-light);
        }
    }

    &:focus-within {
        outline: 3px solid var(--focus-outline-color);
        outline-offset: 2px;
    }

    &.easy { border-color: var(--success-color-light); }
    &.medium { border-color: var(--warning-color-light); }
    &.hard { border-color: var(--error-color-light); }

    &.novice { border-color: var(--bronze-color-light); }
    &.master { border-color: var(--silver-color-light); }
    &.legend { border-color: var(--gold-color-light); }
}

.difficulty-header,
.achievement-header {
    display: flex;
    align-items: center;
    gap: clamp(0.75rem, 2vw, 1.25rem);
    margin-bottom: clamp(1rem, 2vw, 1.5rem);
}

.difficulty-icon,
.achievement-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(2.5rem, 5vw, 3.5rem);
    height: clamp(2.5rem, 5vw, 3.5rem);
    border-radius: 50%;
    background: var(--surface-color-light);
    font-size: clamp(1.25rem, 2.5vw, 1.75rem);

    &.easy { color: var(--success-color); }
    &.medium { color: var(--warning-color); }
    &.hard { color: var(--error-color); }

    &.novice { color: var(--bronze-color); }
    &.master { color: var(--silver-color); }
    &.legend { color: var(--gold-color); }
}

.difficulty-title,
.achievement-title {
    font-size: clamp(1.25rem, 2.5vw, 1.5rem);
    font-weight: 600;
    color: var(--text-color);
    margin: 0;
    line-height: 1.3;
}

.difficulty-description,
.achievement-description {
    font-size: clamp(1rem, 1.5vw, 1.125rem);
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0;
}

@media (prefers-reduced-motion: reduce) {
    .difficulty-item,
    .achievement-item {
        transition: none;

        &:hover {
            transform: none;
        }
    }
}

@media (prefers-contrast: more) {
    .section-title {
        color: var(--high-contrast-primary);
    }

    .section-text {
        color: var(--high-contrast-text);
    }

    .difficulty-item,
    .achievement-item {
        background: var(--high-contrast-surface);
        border-width: 3px;

        &:focus-within {
            outline-color: var(--high-contrast-focus);
        }
    }

    .difficulty-title,
    .achievement-title {
        color: var(--high-contrast-text);
    }

    .difficulty-description,
    .achievement-description {
        color: var(--high-contrast-text);
    }

    .difficulty-icon,
    .achievement-icon {
        background: var(--high-contrast-surface);
        border: 2px solid currentColor;

        &.easy { color: var(--high-contrast-success); }
        &.medium { color: var(--high-contrast-warning); }
        &.hard { color: var(--high-contrast-error); }

        &.novice { color: var(--high-contrast-bronze); }
        &.master { color: var(--high-contrast-silver); }
        &.legend { color: var(--high-contrast-gold); }
    }
}

@media screen and (max-width: 640px) {
    .difficulty-levels,
    .achievement-titles {
        grid-template-columns: 1fr;
    }

    .difficulty-item,
    .achievement-item {
        padding: var(--padding-medium);
    }

    .difficulty-header,
    .achievement-header {
        gap: var(--padding-small);
    }

    .difficulty-icon,
    .achievement-icon {
        width: 2.5rem;
        height: 2.5rem;
        font-size: 1.25rem;
    }
}
</style>
