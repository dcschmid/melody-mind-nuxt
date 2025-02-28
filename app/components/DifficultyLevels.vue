<template>
  <section 
    id="difficulty-levels" 
    class="max-w-content mx-auto px-large py-large"
    :aria-labelledby="sectionTitleId"
    role="region"
  >
    <!-- Sektions-Überschrift -->
    <h2 
      :id="sectionTitleId" 
      class="text-center mb-large text-xl font-bold text-text leading-tight"
    >
      {{ t('gameRules.difficultyLevels.title') }}
    </h2>

    <!-- Einführungstext -->
    <p 
      class="text-md leading-relaxed text-text mb-large max-w-prose mx-auto text-center"
      :id="introTextId"
      aria-live="polite"
    >
      {{ t('gameRules.difficultyLevels.intro') }}
    </p>

    <!-- Schwierigkeitsstufen Grid -->
    <div 
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-medium mb-large" 
      role="list" 
      :aria-labelledby="introTextId"
    >
      <!-- Einzelne Schwierigkeitsstufe -->
      <div 
        v-for="level in difficultyLevels" 
        :key="level"
        role="listitem"
        class="bg-surface rounded-[--border-radius] p-medium shadow border-2 transition-all duration-normal focus-within:outline-focus focus-within:outline-offset-focus hover:-translate-y-2 hover:shadow-hover"
        :class="{
          'border-success': level === 'easy',
          'border-highlight': level === 'medium',
          'border-error': level === 'hard'
        }"
      >
        <!-- Schwierigkeitsstufen-Header -->
        <div class="flex items-center gap-small mb-medium">
          <span 
            class="flex items-center justify-center w-touch h-touch rounded-full bg-surface-light text-lg"
            :class="{
              'text-success': level === 'easy',
              'text-highlight': level === 'medium',
              'text-error': level === 'hard'
            }"
            aria-hidden="true"
          >
            <Icon :name="difficultyIcons[level]" />
          </span>
          
          <h3 
            :id="`${level}-title`" 
            class="text-lg font-semibold text-text mb-small leading-tight"
          >
            {{ t(`gameRules.difficultyLevels.levels.${level}.title`) }}
          </h3>
        </div>
        
        <!-- Beschreibung -->
        <p 
          class="text-sm text-text-secondary mb-medium leading-normal"
          :aria-labelledby="`${level}-title`"
        >
          {{ t(`gameRules.difficultyLevels.levels.${level}.description`) }}
        </p>
      </div>
    </div>

    <!-- Einführungstext für Titel -->
    <p 
      class="text-md leading-relaxed text-text my-large max-w-prose mx-auto text-center"
      :id="titlesIntroId"
      aria-live="polite"
    >
      {{ t('gameRules.difficultyLevels.titles.intro') }}
    </p>

    <!-- Erfolge/Titel Grid -->
    <div 
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-medium mb-large" 
      role="list" 
      :aria-labelledby="titlesIntroId"
    >
      <!-- Einzelner Titel -->
      <div 
        v-for="title in achievementTitles" 
        :key="title"
        role="listitem"
        class="bg-surface rounded-[--border-radius] p-medium shadow border-2 transition-all duration-normal focus-within:outline-focus focus-within:outline-offset-focus hover:-translate-y-2 hover:shadow-hover motion-reduce:hover:transform-none"
        :class="{
          'border-bronze': title === 'novice',
          'border-silver': title === 'master',
          'border-gold': title === 'legend'
        }"
      >
        <!-- Titel-Header -->
        <div class="flex items-center gap-small mb-medium">
          <span 
            class="flex items-center justify-center w-touch h-touch rounded-full bg-surface-light text-lg"
            :class="{
              'text-bronze': title === 'novice',
              'text-silver': title === 'master',
              'text-gold': title === 'legend'
            }"
            aria-hidden="true"
          >
            <Icon :name="achievementIcons[title]" />
          </span>
          
          <h3 
            :id="`${title}-title`" 
            class="text-lg font-semibold text-text mb-small leading-tight"
          >
            {{ t(`gameRules.difficultyLevels.titles.${title}.title`) }}
          </h3>
        </div>
        
        <!-- Beschreibung -->
        <p 
          class="text-sm text-text-secondary mb-medium leading-normal"
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
