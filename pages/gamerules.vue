<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="rules-page">
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
                            <strong>{{ $t('gameRules.difficultyLevels.levels.easy.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.levels.easy.description') }}
                        </li>
                        <li>
                            <strong>{{ $t('gameRules.difficultyLevels.levels.medium.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.levels.medium.description') }}
                        </li>
                        <li>
                            <strong>{{ $t('gameRules.difficultyLevels.levels.hard.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.levels.hard.description') }}
                        </li>
                    </ul>

                    <p class="text">{{ $t('gameRules.difficultyLevels.titles.intro') }}</p>

                    <ul class="list">
                        <li>
                            <strong>{{ $t('gameRules.difficultyLevels.titles.novice.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.titles.novice.description') }}
                        </li>
                        <li>
                            <strong>{{ $t('gameRules.difficultyLevels.titles.master.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.titles.master.description') }}
                        </li>
                        <li>
                            <strong>{{ $t('gameRules.difficultyLevels.titles.legend.title') }}</strong>: {{
                                $t('gameRules.difficultyLevels.titles.legend.description') }}
                        </li>
                    </ul>
                </section>

                <section aria-labelledby="points-system">
                    <h2 class="sectionTitle" id="points-system">{{ $t('gameRules.pointsSystem.title') }}</h2>

                    <ul class="list">
                        <li>{{ $t('gameRules.pointsSystem.rules.0') }}</li>
                        <li>{{ $t('gameRules.pointsSystem.rules.1') }}</li>
                    </ul>
                </section>

                <section aria-labelledby="golden-lps">
                    <h2 class="sectionTitle" id="golden-lps">{{ $t('gameRules.goldenRecords.title') }}</h2>

                    <p class="text">{{ $t('gameRules.goldenRecords.intro') }}</p>

                    <ul class="list">
                        <li><strong>{{ $t('gameRules.goldenRecords.rewards.easy') }}</strong></li>
                        <li><strong>{{ $t('gameRules.goldenRecords.rewards.medium') }}</strong></li>
                        <li><strong>{{ $t('gameRules.goldenRecords.rewards.hard') }}</strong></li>
                    </ul>
                </section>

                <section aria-labelledby="rankings">
                    <h2 class="sectionTitle" id="rankings">{{ $t('gameRules.rankings.title') }}</h2>

                    <p class="text">{{ $t('gameRules.rankings.text') }}</p>

                    <ul class="list">
                        <li>{{ $t('gameRules.rankings.lists.0') }}</li>
                        <li>{{ $t('gameRules.rankings.lists.1') }}</li>
                    </ul>
                </section>

                <section aria-labelledby="tips-tricks">
                    <h2 class="sectionTitle" id="tips-tricks">{{ $t('gameRules.tipsAndTricks.title') }}</h2>

                    <ul class="list">
                        <li>{{ $t('gameRules.tipsAndTricks.tips.0') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.1') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.2') }}</li>
                        <li>{{ $t('gameRules.tipsAndTricks.tips.3') }}</li>
                    </ul>
                </section>
            </article>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
definePageMeta({})
</script>

<style lang="scss" scoped>
.rules-page {
    width: 100%;
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.rulesContainer {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: clamp(var(--padding-medium), 4vw, var(--padding-large));
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
}

.mainTitle {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
    margin-bottom: var(--padding-large);
}

.list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin-bottom: var(--padding-medium);

    &[role="list"] {
        list-style: none;
    }

    li {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-secondary);
        margin-bottom: var(--padding-small);

        &:last-child {
            margin-bottom: 0;
        }

        strong {
            color: var(--text-color);
            font-weight: 600;
        }
    }
}

%shared-text-styles {
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    color: var(--text-secondary);
}

.text {
    @extend %shared-text-styles;
    margin-bottom: var(--padding-medium);
}

.sectionTitle {
    font-size: calc(var(--header-font-size) * 0.8);
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
}

@media (max-width: 768px) {
    .rules-page {
        padding: var(--padding-small);
    }

    .rulesContainer {
        padding: var(--padding-medium);
    }

    .mainTitle,
    .sectionTitle {
        font-size: calc(var(--header-font-size) * 0.8);
    }

    .list {
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
    .rules-page {
        max-width: none;
    }

    .rulesContainer {
        box-shadow: none;
        border: 1px solid #000;
        padding: 2cm;
    }

    .mainTitle,
    .sectionTitle,
    .list li strong {
        color: #000;
    }

    .text,
    .list li {
        color: #333;
    }

    section {
        break-inside: avoid;
    }
}
</style>
