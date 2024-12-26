<template>
    <NuxtLayout name="default" :show-header="true">
        <main class="highscore-page">
            <h1>{{ $t('highscore.title') }}</h1>

            <div v-if="loading">{{ $t('common.loading') }}</div>
            <div v-else-if="error">{{ $t('common.error') }}</div>
            <div v-else>
                <!-- Total Highscores -->
                <section class="highscore-section">
                    <h2>{{ $t('highscore.total') }}</h2>
                    <HighscoreTable 
                      :scores="totalHighscores"
                      :column-labels="{
                        rank: '#',
                        name: $t('highscore.name'),
                        score: $t('highscore.score')
                      }"
                    />
                </section>

                <!-- Category Highscores -->
                <template v-if="categories.length > 0">
                    <section 
                      v-for="category in categories" 
                      :key="category.slug" 
                      class="highscore-section"
                    >
                      <h2>{{ category.name }}</h2>
                      <HighscoreTable 
                        :scores="categoryScores[category.slug]"
                        :column-labels="{
                          rank: '#',
                          name: $t('highscore.name'),
                          score: $t('highscore.score')
                        }"
                      />
                    </section>
                </template>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const loading = ref(true)
const error = ref(null)
const totalHighscores = ref([])
const categoryScores = ref({})
const categories = ref([])

async function fetchHighscores() {
  try {
    const [categoriesRes, scoresRes] = await Promise.all([
      fetch('/api/categories').then(r => r.json()),
      fetch('/api/highscore/total').then(r => r.json())
    ])

    categories.value = categoriesRes.categories
    totalHighscores.value = scoresRes.scores

    // Fetch category scores
    const categoryPromises = categories.value.map(async category => {
      const res = await fetch(`/api/highscore/category/${category.slug}`)
      const data = await res.json()
      categoryScores.value[category.slug] = data.scores
    })

    await Promise.all(categoryPromises)
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHighscores()
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
