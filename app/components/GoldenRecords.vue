<template>
    <RulesSection id="golden-lps">
        <template #title>{{ $t('gameRules.goldenRecords.title') }}</template>
        <p class="section-text" v-html="$t('gameRules.goldenRecords.intro', ['<span class=\'highlight\'>', '</span>'])"></p>

        <RulesList>
            <li>{{ $t('gameRules.goldenRecords.rewards.easy') }}</li>
            <li>{{ $t('gameRules.goldenRecords.rewards.medium') }}</li>
            <li>{{ $t('gameRules.goldenRecords.rewards.hard') }}</li>
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
