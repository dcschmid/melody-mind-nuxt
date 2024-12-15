<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="rules-page">
            <article class="rules-container">
                <h1 class="main-title">{{ $t('gameRules.title') }}</h1>

                <section class="rules-section" aria-labelledby="overview">
                    <h2 id="overview" class="section-title">{{ $t('gameRules.overview.title') }}</h2>
                    <p class="section-text">{{ $t('gameRules.overview.text') }}</p>
                </section>

                <section class="rules-section" aria-labelledby="difficulty-levels">
                    <h2 id="difficulty-levels" class="section-title">
                        {{ $t('gameRules.difficultyLevels.title') }}
                    </h2>
                    <p class="section-text">{{ $t('gameRules.difficultyLevels.intro') }}</p>

                    <ul class="rules-list">
                        <li v-for="level in ['easy', 'medium', 'hard']" :key="level">
                            <strong>{{ $t(`gameRules.difficultyLevels.levels.${level}.title`) }}:</strong>
                            {{ $t(`gameRules.difficultyLevels.levels.${level}.description`) }}
                        </li>
                    </ul>

                    <p class="section-text">{{ $t('gameRules.difficultyLevels.titles.intro') }}</p>

                    <ul class="rules-list">
                        <li v-for="title in ['novice', 'master', 'legend']" :key="title">
                            <strong>{{ $t(`gameRules.difficultyLevels.titles.${title}.title`) }}:</strong>
                            {{ $t(`gameRules.difficultyLevels.titles.${title}.description`) }}
                        </li>
                    </ul>
                </section>

                <section class="rules-section" aria-labelledby="points-system">
                    <h2 id="points-system" class="section-title">
                        {{ $t('gameRules.pointSystem.title') }}
                    </h2>
                    <ul class="rules-list">
                        <li>{{ $t('gameRules.pointSystem.points.correct') }}</li>
                        <li>{{ $t('gameRules.pointSystem.points.wrong') }}</li>
                    </ul>
                </section>

                <section class="rules-section" aria-labelledby="golden-lps">
                    <h2 id="golden-lps" class="section-title">
                        {{ $t('gameRules.goldenRecords.title') }}
                    </h2>
                    <p class="section-text"
                        v-html="$t('gameRules.goldenRecords.intro', ['<span class=\'highlight\'>', '</span>'])"></p>
                    <ul class="rules-list">
                        <li>{{ $t('gameRules.goldenRecords.rewards.easy') }}</li>
                        <li>{{ $t('gameRules.goldenRecords.rewards.medium') }}</li>
                        <li>{{ $t('gameRules.goldenRecords.rewards.hard') }}</li>
                    </ul>
                </section>

                <section class="rules-section" aria-labelledby="rankings">
                    <h2 id="rankings" class="section-title">
                        {{ $t('gameRules.rankings.title') }}
                    </h2>
                    <p class="section-text">{{ $t('gameRules.rankings.description') }}</p>
                    <ul class="rules-list">
                        <li>{{ $t('gameRules.rankings.types.genre') }}</li>
                        <li>{{ $t('gameRules.rankings.types.overall') }}</li>
                    </ul>
                </section>

                <section class="rules-section" aria-labelledby="tips-tricks">
                    <h2 id="tips-tricks" class="section-title">
                        {{ $t('gameRules.tipsAndTricks.title') }}
                    </h2>
                    <ul class="rules-list">
                        <li>{{ $t('gameRules.tipsAndTricks.tips.startEasy') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.chooseStrengths') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.practice') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.accuracy') }}</li>
                    </ul>
                </section>
            </article>
        </main>
    </NuxtLayout>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})
</script>

<style lang="scss" scoped>
.rules-page {
    width: 100%;
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.rules-container {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: clamp(var(--padding-medium), 4vw, var(--padding-large));
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
}

.main-title {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
    margin-bottom: var(--padding-large);
}

.rules-section {
    margin-bottom: var(--padding-large);

    &:last-child {
        margin-bottom: 0;
    }
}

.section-title {
    font-size: calc(var(--header-font-size) * 0.8);
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
}

.section-text {
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    color: var(--text-secondary);
    margin-bottom: var(--padding-medium);
}

.rules-list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin-bottom: var(--padding-medium);

    li {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-secondary);
        margin-bottom: var(--padding-small);

        strong {
            color: var(--text-color);
            font-weight: 600;
        }
    }
}

.highlight {
    color: var(--highlight-color);
    font-weight: 600;
}

@media (max-width: 768px) {
    .rules-page {
        padding: var(--padding-small);
    }

    .rules-container {
        padding: var(--padding-medium);
    }

    .main-title {
        font-size: calc(var(--header-font-size) * 0.8);
    }

    .section-title {
        font-size: calc(var(--header-font-size) * 0.7);
    }

    .rules-list {
        padding-left: var(--padding-medium);
    }
}

// Accessibility Verbesserungen
:focus-visible {
    outline: var(--focus-outline-width) solid var(--focus-outline-color);
    outline-offset: var(--focus-outline-offset);
}

// Print Styles
@media print {
    .rules-container {
        box-shadow: none;
        border: 1px solid #000;
    }

    .main-title,
    .section-title {
        color: #000;
    }

    .section-text,
    .rules-list li {
        color: #333;
    }
}
</style>
