<template>
    <NuxtLayout name="default" :show-header="true">
        <main class="highscore-page">
            <h1>{{ $t('highscore.title') }}</h1>

            <div v-if="isLoading">Laden...</div>
            <div v-else>
                <!-- Gesamt-Highscore -->
                <section class="highscore-section">
                    <h2 class="section-title">{{ $t('highscore.total') }}</h2>
                    <HighscoreTable :scores="totalHighscores" :user-id="session?.data?.user?.id" />
                </section>

                <!-- Kategorie-Highscores -->
                <template v-if="categories.length > 0">
                    <section v-for="category in categories" :key="category.slug" class="highscore-section">
                        <h2 class="section-title">{{ category.name }}</h2>
                        <HighscoreTable :scores="categoryScores[category.slug]" :user-id="session?.data?.user?.id" />
                    </section>
                </template>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'
import { useHead, useSeoMeta } from '@unhead/vue'
import { useRequestURL } from '#app'

const session = authClient.useSession()
const { locale } = useI18n()

interface Score {
    id: string;
    name: string;
    score: number;
    avatar_url?: string;
    user_id: string;
}

interface Category {
    slug: string;
    name: string;
}

const totalHighscores = ref<Score[]>([])
const categories = ref<Category[]>([])
const categoryScores = ref<Record<string, any[]>>({})
const isLoading = ref<boolean>(true)

const currentUserRank = ref<number | null>(null)
const currentUserScore = ref<Score | null>(null)

const findCurrentUserRank = () => {
    const userId = session.value?.data?.user?.id
    if (!userId || !totalHighscores.value) return

    const userIndex = totalHighscores.value.findIndex(score => score.user_id === userId)
    if (userIndex !== -1) {
        currentUserRank.value = userIndex + 1
        currentUserScore.value = totalHighscores.value[userIndex]
    }
}

// Caching-Strategie implementieren
const cache = new Map<string, { data: any, timestamp: number }>()
const CACHE_DURATION = 60000 // 1 Minute Cache

const fetchWithCache = async (url: string) => {
    const cached = cache.get(url)
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        return cached.data
    }

    const response = await fetch(url)
    const data = await response.json()
    cache.set(url, { data, timestamp: Date.now() })
    return data
}

// Parallele Verarbeitung der Highscores
const loadCategories = async () => {
    try {
        const [categoriesResponse, totalScores] = await Promise.all([
            fetchWithCache(`/api/user/categories?language=${locale.value}`),
            fetchWithCache(`/api/highscore/total/list?language=${locale.value}`)
        ])

        categories.value = categoriesResponse.categories
        totalHighscores.value = totalScores.scores

        // Lade Kategorie-Highscores parallel
        await loadCategoryHighscores(categoriesResponse.categories)
    } catch (error) {
        console.error('Error loading data:', error)
    } finally {
        isLoading.value = false
    }
}

// Optimierte Kategorie-Highscores-Ladung
const loadCategoryHighscores = async (categories: Category[]) => {
    const promises = categories.map(category =>
        fetchWithCache(`/api/highscore/category/list?category=${category.slug}&language=${locale.value}`)
            .then(data => ({ slug: category.slug, scores: data.scores }))
    )

    const results = await Promise.all(promises)
    results.forEach(result => {
        categoryScores.value[result.slug] = result.scores
    })
}

onMounted(async () => {
    await loadCategories()
    findCurrentUserRank()
})

// SEO Meta Tags
useSeoMeta({
    title: 'Highscores - Melody Mind',
    ogTitle: 'Highscores - Melody Mind',
    description: 'Entdecke die besten Spieler in unserem Musik-Quiz. Vergleiche deine Punktzahl mit anderen und steige in der Rangliste auf.',
    ogDescription: 'Vergleiche deine Punktzahl mit anderen Spielern und steige in der Rangliste auf.',
})

// Dynamische kanonische URL
const url = useRequestURL()

useHead({
    titleTemplate: (titleChunk) => {
        return titleChunk ? `${titleChunk} - Melody Mind` : 'Melody Mind';
    },
    link: [
        {
            rel: 'canonical',
            href: url.href
        }
    ],
    meta: [
        { name: 'robots', content: 'index, follow' },
        { name: 'keywords', content: 'Melody Mind, Highscore, Rangliste, Bestenliste, Musikwissen, Quiz Punkte' }
    ]
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
