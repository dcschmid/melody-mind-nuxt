<template>
    <NuxtLayout name="default" :show-header="true">
        <main class="highscore-page">
            <h1>{{ $t('highscore.title') }}</h1>

            <!-- Gesamt-Highscore -->
            <section class="highscore-section">
                <h2 class="section-title">{{ $t('highscore.total') }}</h2>
                <div class="highscore-table">
                    <div class="table-header">
                        <span class="rank">#</span>
                        <span class="name">{{ $t('highscore.name') }}</span>
                        <span class="score">{{ $t('highscore.points') }}</span>
                    </div>
                    <div class="table-body">
                        <div v-for="(score, index) in totalHighscores" :key="score.id" class="table-row"
                            :class="{ 'current-user': score.user_id === session?.user?.id }">
                            <span class="rank">{{ index + 1 }}</span>
                            <span class="name">{{ score.name }}</span>
                            <span class="score">{{ score.score?.toLocaleString() }}</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Kategorie-Highscores -->
            <template v-if="categories.length > 0">
                <section v-for="category in categories" :key="category.slug" class="highscore-section">
                    <h2 class="section-title">{{ category.name }}</h2>
                    <div class="highscore-table">
                        <div class="table-header">
                            <span class="rank">#</span>
                            <span class="name">{{ $t('highscore.name') }}</span>
                            <span class="score">{{ $t('highscore.points') }}</span>
                        </div>
                        <div class="table-body">
                            <div v-for="(score, index) in categoryScores[category.slug]" :key="score.id"
                                class="table-row" :class="{ 'current-user': score.user_id === session?.user?.id }">
                                <span class="rank">{{ index + 1 }}</span>
                                <span class="name">{{ score.name }}</span>
                                <span class="score">{{ score.score?.toLocaleString() }}</span>
                            </div>
                        </div>
                    </div>
                </section>
            </template>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'

const session = authClient.useSession()
const { locale } = useI18n()

const totalHighscores = ref([])
const categories = ref([])
const categoryScores = ref({})

// Lade alle verfügbaren Kategorien
const loadCategories = async () => {
    try {
        const response = await fetch(`/api/user/categories?language=${locale.value}`)
        const data = await response.json()
        categories.value = data.categories

        // Lade die Highscores für jede Kategorie
        for (const category of data.categories) {
            await loadCategoryHighscores(category)
        }
    } catch (error) {
        console.error('Error loading categories:', error)
    }
}

// Lade Gesamt-Highscores
const loadTotalHighscores = async () => {
    try {
        const response = await fetch(`/api/highscore/total/list?language=${locale.value}`)
        const data = await response.json()
        totalHighscores.value = data.scores
    } catch (error) {
        console.error('Error loading total highscores:', error)
    }
}

// Lade Kategorie-Highscores
const loadCategoryHighscores = async (category) => {
    try {
        const response = await fetch(`/api/highscore/category/list?category=${category.slug}&language=${locale.value}`)
        const data = await response.json()
        categoryScores.value[category.slug] = data.scores
    } catch (error) {
        console.error(`Error loading highscores for category ${category.slug}:`, error)
    }
}

onMounted(async () => {
    await Promise.all([
        loadTotalHighscores(),
        loadCategories()
    ])
})
</script>

<style lang="scss" scoped>
.highscore-page {
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-large);
}

.section-title {
    color: var(--primary-color);
    margin-bottom: var(--padding-medium);
    font-size: 1.5rem;
}

.highscore-section {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-large);
    margin-bottom: var(--padding-large);
    box-shadow: var(--shadow-elevation-medium);
}

.highscore-table {
    width: 100%;

    .table-header {
        display: grid;
        grid-template-columns: 80px 1fr 120px;
        padding: var(--padding-small);
        background: rgba(255, 255, 255, 0.05);
        border-radius: var(--border-radius);
        font-weight: bold;
        margin-bottom: var(--padding-small);
    }

    .table-row {
        display: grid;
        grid-template-columns: 80px 1fr 120px;
        padding: var(--padding-small);
        border-radius: var(--border-radius);

        &:hover {
            background: rgba(255, 255, 255, 0.05);
        }

        &.current-user {
            background: var(--primary-color-transparent);
        }
    }

    .rank {
        text-align: center;
    }

    .score {
        text-align: right;
    }
}
</style>
