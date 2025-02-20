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
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-large);
}

.section-title {
    text-align: center;
    margin-bottom: var(--padding-large);
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-bold);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.section-text {
    font-size: var(--font-size-responsive-md);
    line-height: var(--line-height-relaxed);
    color: var(--text-color);
    margin-bottom: var(--padding-large);
    max-width: var(--max-line-length);
    margin-left: auto;
    margin-right: auto;
    text-align: center;

    &.titles-intro {
        margin-top: var(--padding-large);
    }
}

.difficulty-levels,
.achievement-titles {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--padding-medium);
    margin-bottom: var(--padding-large);
}

.difficulty-item,
.achievement-item {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    box-shadow: var(--box-shadow);
    border: 2px solid transparent;
    transition: all var(--transition-speed) var(--transition-bounce);

    @media (hover: hover) {
        &:hover {
            transform: translateY(-2px);
            box-shadow: var(--box-shadow-hover);
            border-color: var(--primary-color);
        }
    }

    &:focus-within {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &.easy { border-color: var(--success-color); }
    &.medium { border-color: var(--highlight-color); }
    &.hard { border-color: var(--error-color); }

    &.novice { border-color: var(--color-bronze); }
    &.master { border-color: var(--color-silver); }
    &.legend { border-color: var(--color-gold); }
}

.difficulty-header,
.achievement-header {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    margin-bottom: var(--padding-medium);
}

.difficulty-icon,
.achievement-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: var(--min-touch-target);
    height: var(--min-touch-target);
    border-radius: 50%;
    background: var(--surface-color-light);
    font-size: var(--font-size-responsive-lg);

    &.easy { color: var(--success-color); }
    &.medium { color: var(--highlight-color); }
    &.hard { color: var(--error-color); }

    &.novice { color: var(--color-bronze); }
    &.master { color: var(--color-silver); }
    &.legend { color: var(--color-gold); }
}

.difficulty-title,
.achievement-title {
    font-size: var(--font-size-responsive-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);
    margin-bottom: var(--padding-small);
    line-height: var(--line-height-tight);
}

.difficulty-description,
.achievement-description {
    font-size: var(--font-size-responsive-sm);
    color: var(--text-secondary);
    margin-bottom: var(--padding-medium);
    line-height: var(--line-height-normal);
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

@media (width <= 640px) {
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
        width: var(--min-touch-target);
        height: var(--min-touch-target);
        font-size: var(--font-size-responsive-md);
    }
}
</style>
