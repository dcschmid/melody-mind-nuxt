<template>
    <NuxtLayout name="default" :show-header="true">
        <main class="highscore-page">
            <h1>{{ $t('highscore.title') }}</h1>

            <div v-if="isLoading">{{ $t('common.loading') }}</div>
            <div v-else>
                <!-- Gesamt-Highscore -->
                <section class="highscore-section">
                    <h2 class="section-title">{{ $t('highscore.total') }}</h2>
                    <HighscoreTable :scores="totalHighscores" :user-id="session?.data?.user?.id" :column-labels="{
                        rank: '#',
                        avatar: $t('highscore.avatar'),
                        name: $t('highscore.name'),
                        points: $t('highscore.points')
                    }" />
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
// Core imports and setup
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'
import { useHead, useSeoMeta } from '@unhead/vue'
import { useRequestURL } from '#app'

/**
 * Authentication session management using authClient
 */
const session = authClient.useSession()
const { locale } = useI18n()

/**
 * Type definitions for score and category data
 */
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

/**
 * Reactive state management
 */
const totalHighscores = ref<Score[]>([])        // Stores overall highscores
const categories = ref<Category[]>([])          // Stores available categories
const categoryScores = ref<Record<string, any[]>>({})  // Stores scores per category
const isLoading = ref<boolean>(true)           // Loading state indicator

const currentUserRank = ref<number | null>(null)      // Current user's rank
const currentUserScore = ref<Score | null>(null)      // Current user's score

/**
 * Finds and sets the current user's rank in the highscore list
 */
const findCurrentUserRank = () => {
    const userId = session.value?.data?.user?.id
    if (!userId || !totalHighscores.value) return

    const userIndex = totalHighscores.value.findIndex(score => score.user_id === userId)
    if (userIndex !== -1) {
        currentUserRank.value = userIndex + 1
        currentUserScore.value = totalHighscores.value[userIndex]
    }
}

/**
 * Caching implementation for API requests
 * Caches responses for 1 minute to reduce API load
 */
const cache = new Map<string, { data: any, timestamp: number }>()
const CACHE_DURATION = 60000 // 1 minute cache duration

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

/**
 * Loads categories and total highscores in parallel
 */
const loadCategories = async () => {
    try {
        const [categoriesResponse, totalScores] = await Promise.all([
            fetchWithCache(`/api/user/categories?language=${locale.value}`),
            fetchWithCache(`/api/highscore/total/list?language=${locale.value}`)
        ])

        categories.value = categoriesResponse.categories
        totalHighscores.value = totalScores.scores

        await loadCategoryHighscores(categoriesResponse.categories)
    } catch (error) {
        console.error('Error loading data:', error)
    } finally {
        isLoading.value = false
    }
}

/**
 * Loads highscores for each category in parallel
 */
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

/**
 * Initialize data on component mount
 */
onMounted(async () => {
    await loadCategories()
    findCurrentUserRank()
})

/**
 * SEO configuration
 */
useSeoMeta({
    title: 'Highscores - Melody Mind',
    ogTitle: 'Highscores - Melody Mind',
    description: 'Discover the top players in our music quiz. Compare your score with others and climb the rankings.',
    ogDescription: 'Compare your score with other players and climb the rankings.',
})

/**
 * Dynamic canonical URL and additional head tags
 */
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
        { name: 'keywords', content: 'Melody Mind, Highscore, Rankings, Leaderboard, Music Knowledge, Quiz Points' }
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
