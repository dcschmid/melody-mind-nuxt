<template>
    <RulesSection id="golden-lps">
        <template #title><span class="records-title">{{ $t('gameRules.goldenRecords.title') }}</span></template>
        <p class="section-text record-text" v-html="$t('gameRules.goldenRecords.intro', ['<span class=\'highlight\'>', '</span>'])"></p>

        <RulesList>
            <li><span class="record-description">{{ $t('gameRules.goldenRecords.rewards.easy') }}</span></li>
            <li><span class="record-description">{{ $t('gameRules.goldenRecords.rewards.medium') }}</span></li>
            <li><span class="record-description">{{ $t('gameRules.goldenRecords.rewards.hard') }}</span></li>
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

.records-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: 700;
    text-align: center;
    margin-bottom: var(--padding-large);
}

.record-text {
    font-size: var(--font-size-responsive-md);
    font-weight: 600;
}

.record-description {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
}

.record-info {
    font-size: var(--font-size-base);
}
</style>
