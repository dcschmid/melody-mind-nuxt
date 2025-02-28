<template>
  <RulesSection id="golden-lps">
    <template #title>
      <span class="text-xl font-bold text-text leading-tight text-center block mb-large">
        {{ $t('gameRules.goldenRecords.title') }}
      </span>
    </template>
    
    <!-- Einführungstext mit hervorgehobenen Elementen -->
    <p 
      class="text-md leading-relaxed text-text mb-medium max-w-prose mx-auto" 
      v-html="$t('gameRules.goldenRecords.intro', ['<span class=\'text-primary font-semibold transition-colors duration-normal\'>', '</span>'])"
      aria-live="polite"
    ></p>

    <!-- Auflistung der Belohnungen mit verbesserten Zugänglichkeitsattributen -->
    <RulesList
      :title="$t('gameRules.goldenRecords.rewardsListTitle')"
      class="mb-large"
    >
      <li 
        v-for="(difficulty, index) in ['easy', 'medium', 'hard']" 
        :key="difficulty"
        class="mb-small last:mb-0 group"
      >
        <span 
          class="text-base text-text-secondary leading-normal transition-colors duration-normal group-hover:text-text group-focus-within:text-text motion-reduce:transition-none"
          :aria-label="$t(`gameRules.goldenRecords.rewards.${difficulty}AccessibleLabel`)"
        >
          {{ $t(`gameRules.goldenRecords.rewards.${difficulty}`) }}
        </span>
        
        <!-- Badge für den Schwierigkeitsgrad -->
        <span 
          class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
          :class="{
            'bg-success/20 text-success': difficulty === 'easy',
            'bg-highlight/20 text-highlight': difficulty === 'medium',
            'bg-error/20 text-error': difficulty === 'hard'
          }"
          aria-hidden="true"
        >
          {{ $t(`gameRules.difficultyLevels.levels.${difficulty}.title`) }}
        </span>
      </li>
    </RulesList>
    
    <!-- Zusätzlicher Abschlusshinweis mit besserer Erkennbarkeit -->
    <div 
      class="p-medium rounded-lg bg-surface/60 backdrop-blur-xs border border-primary/20 max-w-prose mx-auto text-center"
      role="note"
      aria-label="Wichtiger Hinweis"
    >
      <p class="text-base text-text leading-relaxed mb-0">
        <Icon name="material-symbols:info-outline" class="inline-block mr-1 text-primary" aria-hidden="true" />
        {{ $t('gameRules.goldenRecords.note') }}
      </p>
    </div>
  </RulesSection>
</template>

<script setup>
// Keine spezielle Logik erforderlich
</script>

<style lang="scss" scoped>
/* Unterstützung für hohen Kontrast-Modus */
@media (prefers-contrast: more) {
  .text-primary {
    @apply text-white bg-primary px-1 py-0.5 rounded-sm;
  }
  
  [role="note"] {
    @apply border-2 border-white bg-surface;
  }
  
  .group:hover span,
  .group:focus-within span {
    @apply text-white;
  }
}
</style>
