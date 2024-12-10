<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <article class="rulesContainer">
            <h1 class="mainTitle">{{ $t('gameRules.title') }}</h1>

            <section aria-labelledby="overview">
                <h2 id="overview" class="sectionTitle">{{ $t('gameRules.overview.title') }}</h2>
                <p class="text">{{ $t('gameRules.overview.text') }}</p>
            </section>

            <section aria-labelledby="difficulty-levels">
                <h2 id="difficulty-levels" class="sectionTitle">{{ $t('gameRules.difficultyLevels.title') }}</h2>

                <p class="text">{{ $t('gameRules.difficultyLevels.intro') }}</p>

                <ul class="list">
                    <li>
                        {{ $t('gameRules.difficultyLevels.levels.easy.title') }}:
                        {{ $t('gameRules.difficultyLevels.levels.easy.description') }}
                    </li>
                    <li>
                        {{ $t('gameRules.difficultyLevels.levels.medium.title') }}:
                        {{ $t('gameRules.difficultyLevels.levels.medium.description') }}
                    </li>
                    <li>
                        {{ $t('gameRules.difficultyLevels.levels.hard.title') }}:
                        {{ $t('gameRules.difficultyLevels.levels.hard.description') }}
                    </li>
                </ul>

                <p class="text">{{ $t('gameRules.difficultyLevels.titles.intro') }}</p>

                <ul class="list">
                    <li>
                        {{ $t('gameRules.difficultyLevels.titles.novice.title') }}:
                        {{ $t('gameRules.difficultyLevels.titles.novice.description') }}
                    </li>
                    <li>
                        {{ $t('gameRules.difficultyLevels.titles.master.title') }}:
                        {{ $t('gameRules.difficultyLevels.titles.master.description') }}
                    </li>
                    <li>
                        {{ $t('gameRules.difficultyLevels.titles.legend.title') }}:
                        {{ $t('gameRules.difficultyLevels.titles.legend.description') }}
                    </li>
                </ul>
            </section>

            <section aria-labelledby="points-system">
                <h2 class="sectionTitle" id="points-system">{{ $t('gameRules.pointSystem.title') }}</h2>

                <ul class="list">
                    <li>{{ $t('gameRules.pointSystem.points.correct') }}</li>
                    <li>{{ $t('gameRules.pointSystem.points.wrong') }}</li>
                </ul>
            </section>

            <section aria-labelledby="golden-lps">
                <h2 class="sectionTitle" id="golden-lps">{{ $t('gameRules.goldenRecords.title') }}</h2>

                <p class="text">{{ $t('gameRules.goldenRecords.intro', ['<span class="golden-lp">', '</span>']) }}</p>

                <ul class="list">
                    <li>{{ $t('gameRules.goldenRecords.rewards.easy') }}</li>
                    <li>{{ $t('gameRules.goldenRecords.rewards.medium') }}</li>
                    <li>{{ $t('gameRules.goldenRecords.rewards.hard') }}</li>
                </ul>
            </section>

            <section aria-labelledby="rankings">
                <h2 class="sectionTitle" id="rankings">{{ $t('gameRules.rankings.title') }}</h2>

                <p class="text">{{ $t('gameRules.rankings.description') }}</p>

                <ul class="list">
                    <li>{{ $t('gameRules.rankings.types.genre') }}</li>
                    <li>{{ $t('gameRules.rankings.types.overall') }}</li>
                </ul>
            </section>

            <section aria-labelledby="tips-tricks">
                <h2 class="sectionTitle" id="tips-tricks">{{ $t('gameRules.tipsAndTricks.title') }}</h2>

                <ul class="list">
                    <li>{{ $t('gameRules.tipsAndTricks.tips.startEasy') }}</li>
                    <li>{{ $t('gameRules.tipsAndTricks.tips.chooseStrengths') }}</li>
                    <li>{{ $t('gameRules.tipsAndTricks.tips.practice') }}</li>
                    <li>{{ $t('gameRules.tipsAndTricks.tips.accuracy') }}</li>
                </ul>
            </section>
        </article>
    </NuxtLayout>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})
</script>

<style lang="scss" scoped>
.rulesContainer {
    padding: var(--padding-large);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);

    @media (max-width: 768px) {
        padding: var(--padding-medium);
    }
}

.mainTitle {
    margin-bottom: var(--padding-large);
    font-family: var(--font-family);
    font-size: var(--header-font-size);
    font-weight: 900;
    line-height: var(--line-height-body);
    color: var(--text-color);
    text-align: center;

    @media (max-width: 768px) {
        font-size: calc(var(--header-font-size) * 0.8);
    }
}

.sectionTitle {
    margin: var(--padding-medium) 0;
    font-family: var(--font-family);
    font-size: calc(var(--header-font-size) * 0.8);
    font-weight: 700;
    line-height: var(--line-height-body);
    color: var(--text-color);

    @media (max-width: 768px) {
        font-size: calc(var(--header-font-size) * 0.7);
    }
}

.text {
    margin-bottom: var(--padding-medium);
    font-family: var(--font-family);
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    color: var(--text-color);
    letter-spacing: var(--spacing-text);

    strong {
        font-weight: 600;
    }
}

.list {
    margin-bottom: var(--padding-medium);
    padding-left: var(--padding-large);
    list-style-type: disc;

    li {
        margin-bottom: var(--padding-small);
        font-family: var(--font-family);
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-color);

        strong {
            font-weight: 600;
        }
    }

    @media (max-width: 768px) {
        padding-left: var(--padding-medium);
    }
}

.highlight {
    font-weight: 600;
    color: var(--highlight-color);
}

// Focus Styles
:focus-visible {
    outline: var(--focus-outline-width) solid var(--focus-outline-color);
    outline-offset: var(--focus-outline-offset);
}

// High Contrast Mode Support
@media (forced-colors: active) {
    .rulesContainer {
        border: 2px solid CanvasText;
    }

    .highlight,
    .list li strong {
        border-bottom: 1px solid CurrentColor;
    }
}

// Reduced Motion
@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
    }
}

// Print Styles
@media print {
    .rulesContainer {
        border: 1px solid #000;
        box-shadow: none;
    }

    .mainTitle,
    .sectionTitle {
        color: #000;
    }

    .list {
        page-break-inside: avoid;
    }
}

// Better Touch Targets
@media (hover: none) and (pointer: coarse) {
    .list li {
        padding: calc(var(--padding-small) / 2) 0;
    }
}
</style>
