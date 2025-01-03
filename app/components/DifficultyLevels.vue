<template>
    <RulesSection id="difficulty-levels">
        <template #title>{{ $t('gameRules.difficultyLevels.title') }}</template>
        <p class="section-text">{{ $t('gameRules.difficultyLevels.intro') }}</p>

        <RulesList>
            <li v-for="level in ['easy', 'medium', 'hard']" :key="level">
                <strong>{{ $t(`gameRules.difficultyLevels.levels.${level}.title`) }}:</strong>
                {{ $t(`gameRules.difficultyLevels.levels.${level}.description`) }}
            </li>
        </RulesList>

        <p class="section-text">{{ $t('gameRules.difficultyLevels.titles.intro') }}</p>

        <RulesList>
            <li v-for="title in ['novice', 'master', 'legend']" :key="title">
                <strong>{{ $t(`gameRules.difficultyLevels.titles.${title}.title`) }}:</strong>
                {{ $t(`gameRules.difficultyLevels.titles.${title}.description`) }}
            </li>
        </RulesList>
    </RulesSection>
</template>

<script setup>
// No specific script needed for now
</script>

<style scoped>
.section-text {
    margin-bottom: var(--padding-medium);
}
</style>
