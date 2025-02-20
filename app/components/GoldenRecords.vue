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

<style scoped lang="scss">
.section-text {
    margin-bottom: var(--padding-medium);
    line-height: var(--line-height-relaxed);
    max-width: var(--max-line-length);
    margin-left: auto;
    margin-right: auto;
}

.records-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
    margin-bottom: var(--padding-large);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.record-text {
    font-size: var(--font-size-responsive-md);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);

    .highlight {
        color: var(--primary-color);
    }
}

.record-description {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    line-height: var(--line-height-normal);
    transition: color var(--transition-speed) var(--transition-bounce);

    &:hover {
        color: var(--text-color);
    }
}

.record-info {
    font-size: var(--font-size-base);
    line-height: var(--line-height-normal);
    color: var(--text-color);
}

@media (prefers-reduced-motion: reduce) {
    .record-description {
        transition: none;
    }
}
</style>
