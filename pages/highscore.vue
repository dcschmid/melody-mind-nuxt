<template>
    <NuxtLayout name="default" :show-header="true">
        <main class="highscore-page">
            <h1>{{ $t('highscore.title') }}</h1>

            <div v-if="loading">{{ $t('common.loading') }}</div>
            <div v-else-if="error">{{ error }}</div>
            <div v-else>
                <!-- Gesamt-Highscore -->
                <section class="highscore-section">
                    <h2 class="section-title">{{ $t('highscore.total') }}</h2>
                    <HighscoreTable :scores="highscoreStore.totalHighscores" :column-labels="{
                        rank: '#',
                        avatar: $t('highscore.avatar'),
                        name: $t('highscore.name'),
                        points: $t('highscore.points')
                    }" />
                </section>

                <!-- Kategorie-Highscores -->
                <template v-if="highscoreStore.categories.length > 0">
                    <section v-for="category in highscoreStore.categories" :key="category.slug" class="highscore-section">
                        <h2 class="section-title">{{ category.name }}</h2>
                        <HighscoreTable :scores="highscoreStore.categoryScores[category.slug]" />
                    </section>
                </template>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHighscoreStore } from '~/stores/highscore'

const { t } = useI18n()
const highscoreStore = useHighscoreStore()

const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    await highscoreStore.fetchHighscores()
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
})
</script>

<style lang="scss" scoped>
.highscore-page {
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.section-title {
    color: var(--primary-color);
    margin-bottom: var(--padding-small);
}

.highscore-section {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-small);
    margin-bottom: var(--padding-small);
    box-shadow: var(--shadow-elevation-medium);
}
</style>
