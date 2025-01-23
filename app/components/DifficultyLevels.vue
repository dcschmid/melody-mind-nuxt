<template>
    <RulesSection 
        id="difficulty-levels" 
        :aria-labelledby="sectionTitleId"
        role="region"
    >
        <template #title>
            <h2 :id="sectionTitleId" class="section-title">
                {{ t('gameRules.difficultyLevels.title') }}
            </h2>
        </template>

        <p 
            class="section-text" 
            :id="introTextId"
        >
            {{ t('gameRules.difficultyLevels.intro') }}
        </p>

        <div 
            class="difficulty-levels" 
            role="list" 
            :aria-labelledby="introTextId"
        >
            <div 
                v-for="level in ['easy', 'medium', 'hard']" 
                :key="level"
                role="listitem"
                class="difficulty-item"
            >
                <div class="difficulty-header">
                    <span 
                        class="difficulty-icon" 
                        :class="level"
                        aria-hidden="true"
                    >
                        <Icon :name="difficultyIcons[level]" />
                    </span>
                    <strong :id="`${level}-title`" class="difficulty-title">
                        {{ t(`gameRules.difficultyLevels.levels.${level}.title`) }}
                    </strong>
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
        >
            {{ t('gameRules.difficultyLevels.titles.intro') }}
        </p>

        <div 
            class="achievement-titles" 
            role="list" 
            :aria-labelledby="titlesIntroId"
        >
            <div 
                v-for="title in ['novice', 'master', 'legend']" 
                :key="title"
                role="listitem"
                class="achievement-item"
            >
                <div class="achievement-header">
                    <span 
                        class="achievement-icon" 
                        :class="title"
                        aria-hidden="true"
                    >
                        <Icon :name="achievementIcons[title]" />
                    </span>
                    <strong :id="`${title}-title`" class="achievement-title">
                        {{ t(`gameRules.difficultyLevels.titles.${title}.title`) }}
                    </strong>
                </div>
                <p 
                    class="achievement-description"
                    :aria-labelledby="`${title}-title`"
                >
                    {{ t(`gameRules.difficultyLevels.titles.${title}.description`) }}
                </p>
            </div>
        </div>
    </RulesSection>
</template>

<script setup lang="ts">
const { t } = useI18n()

// Unique IDs für ARIA-Attribute
const sectionTitleId = 'difficulty-levels-title'
const introTextId = 'difficulty-levels-intro'
const titlesIntroId = 'achievement-titles-intro'

// Icons für Schwierigkeitsgrade
const difficultyIcons = {
    easy: 'material-symbols:stars-outline',
    medium: 'material-symbols:stars',
    hard: 'material-symbols:stars-rounded'
}

// Icons für Errungenschaften
const achievementIcons = {
    novice: 'material-symbols:military-tech-outline',
    master: 'material-symbols:military-tech',
    legend: 'material-symbols:military-tech-rounded'
}
</script>

<style scoped lang="scss">
.section-title {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: var(--padding-medium);
    line-height: 1.3;
    letter-spacing: -0.01em;
}

.section-text {
    font-size: clamp(1.125rem, 2vw, 1.25rem);
    line-height: 1.6;
    color: var(--text-color);
    margin-bottom: var(--padding-large);
    max-width: 65ch;

    &.titles-intro {
        margin-top: var(--padding-large);
    }
}

.difficulty-levels,
.achievement-titles {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    margin-bottom: var(--padding-large);
}

.difficulty-item,
.achievement-item {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    box-shadow: var(--box-shadow);
    border: 2px solid var(--surface-color-light);
    transition: transform 0.2s ease-in-out;

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
}

.difficulty-header,
.achievement-header {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    margin-bottom: var(--padding-small);
}

.difficulty-icon,
.achievement-icon {
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: var(--surface-color-light);
    color: var(--primary-color);

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
}

.difficulty-description,
.achievement-description {
    font-size: clamp(1rem, 2vw, 1.125rem);
    line-height: 1.6;
    color: var(--text-secondary);
    margin-left: calc(2.5rem + var(--padding-small));
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

    .section-text,
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
        
        &.easy { color: var(--high-contrast-success); }
        &.medium { color: var(--high-contrast-warning); }
        &.hard { color: var(--high-contrast-error); }

        &.novice { color: var(--high-contrast-bronze); }
        &.master { color: var(--high-contrast-silver); }
        &.legend { color: var(--high-contrast-gold); }
    }
}

@media screen and (min-width: 640px) {
    .difficulty-levels,
    .achievement-titles {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: var(--padding-medium);
    }
}
</style>
