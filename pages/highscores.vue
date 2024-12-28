<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <h1 class="title">{{ t('highscores.title') }}</h1>

        <section class="search-section" role="search">
            <SearchBar id="category-search" v-model="searchQuery" :placeholder="t('highscores.searchPlaceholder')" />
        </section>

        <div class="categories-list">
            <div v-for="category in filteredCategories" :key="category" class="category-card">
                <div class="category-header">
                    <h2 class="category-title">{{ category }}</h2>
                    <select v-model="selectedDifficulties[category]" class="difficulty-select"
                        @change="() => fetchHighscores(category)">
                        <option value="easy">{{ t('difficulty.easy') }}</option>
                        <option value="medium">{{ t('difficulty.medium') }}</option>
                        <option value="hard">{{ t('difficulty.hard') }}</option>
                    </select>
                </div>

                <div class="scores-table">
                    <table v-if="groupedHighscores[category]?.length">
                        <thead>
                            <tr>
                                <th class="rank-cell">{{ t('highscores.rank') }}</th>
                                <th class="player-cell">{{ t('highscores.player') }}</th>
                                <th class="points-cell">{{ t('highscores.points') }}</th>
                                <th class="lps-cell">{{ t('highscores.lps') }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(score, index) in sortedScores(category)" :key="index">
                                <td class="rank-cell" data-th="Rank">
                                    <span v-if="index < 3" class="medal">
                                        {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
                                    </span>
                                    #{{ index + 1 }}
                                </td>
                                <td class="player-cell" data-th="Player">{{ score.username }}</td>
                                <td class="points-cell" data-th="Points">{{ score.points }}</td>
                                <td class="lps-cell" data-th="LPs">
                                    <template v-if="score.goldLp || score.silverLp || score.bronzeLp">
                                        <Icon v-if="score.goldLp" name="material-symbols:album" size="32"
                                            class="gold" />
                                        <Icon v-if="score.silverLp" name="material-symbols:album" size="32"
                                            class="silver" />
                                        <Icon v-if="score.bronzeLp" name="material-symbols:album" size="32"
                                            class="bronze" />
                                    </template>
                                    <span v-else>-</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else-if="loading" class="loading">
                        {{ t('highscores.loading') }}
                    </div>
                    <div v-else class="no-scores">
                        {{ t('highscores.noScores') }}
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import SearchBar from '@/components/SearchBar.vue'

const { locale, t } = useI18n()
const highscores = ref([])
const searchQuery = ref('')
const selectedDifficulties = ref({})
const loading = ref(true)

// Fetch highscores
const fetchHighscores = async (category) => {
    try {
        loading.value = true
        const currentLocale = locale.value || 'de'

        const response = await $fetch('/api/highscores', {
            method: 'GET',
            params: {
                language: currentLocale
            }
        })


        if (Array.isArray(response)) {
            highscores.value = response

            // Initialize difficulties for new categories
            const categories = [...new Set(response.map(score => score.category))]

            categories.forEach(category => {
                if (!selectedDifficulties.value[category]) {
                    selectedDifficulties.value[category] = 'easy'
                }
            })

        } else {
            highscores.value = []
        }
    } catch (error) {
        highscores.value = []
    } finally {
        loading.value = false
    }
}

// Group highscores by category and filter by difficulty
const groupedHighscores = computed(() => {
    if (!Array.isArray(highscores.value) || highscores.value.length === 0) {
        return {}
    }

    const result = {}

    // Group by category first
    highscores.value.forEach(score => {
        const { category, difficulty } = score
        if (!result[category]) {
            result[category] = []
        }

        // Only add scores that match the selected difficulty
        const selectedDifficulty = selectedDifficulties.value[category]
        if (difficulty === selectedDifficulty) {
            result[category].push({ ...score })
        }
    })

    // Sort by rank (should already be sorted from API)
    Object.keys(result).forEach(category => {
        result[category].sort((a, b) => a.rank - b.rank)
    })

    return result
})

// Filter categories based on search query
const filteredCategories = computed(() => {
    const categories = Object.keys(groupedHighscores.value)
    if (!searchQuery.value.trim()) return categories

    const query = searchQuery.value.toLowerCase().trim()
    return categories.filter(category =>
        category.toLowerCase().includes(query)
    )
})

// Sort scores by rank
const sortedScores = (category) => {
    return groupedHighscores.value[category]
}

// Get medal icon
const getMedalIcon = (index) => {
    if (index === 0) return 'emoji:1st_place_medal'
    if (index === 1) return 'emoji:2nd_place_medal'
    if (index === 2) return 'emoji:3rd_place_medal'
}

// Watch for language changes
watch(locale, () => {
    fetchHighscores()
})

// Initial fetch
onMounted(() => {
    fetchHighscores()
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;


.title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-top: 5rem;
    margin-bottom: var(--padding-small);
    text-align: center;
    color: var(--primary-color);
}

.search-section {
    width: 100%;
    max-width: 500px;
    margin-bottom: var(--padding-small);
}

.categories-list {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-medium);
}

.category-card {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    width: 100%;
    max-width: 600px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--padding-medium);
    padding-bottom: var(--padding-small);
    border-bottom: 1px solid var(--border-color);

    .category-title {
        color: var(--primary-color);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
        display: block;
    }

    .difficulty-select {
        padding: 0.5rem 2rem 0.5rem 1rem;
        font-size: 0.9rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        background-color: var(--background-secondary);
        color: var(--text-color);
        cursor: pointer;

        &:focus {
            outline: none;
            border-color: var(--primary-color);
        }
    }
}

.scores-table {
    @media (max-width: 768px) {
        table, thead, tbody, tr, td {
            display: block;
        }

        thead {
            display: none;
        }

        tr {
            background: var(--background-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
            padding: 0.5rem;
        }

        td {
            position: relative;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border-color-light);
            display: flex;
            align-items: center;

            &:last-child {
                border-bottom: none;
            }

            &::before {
                content: attr(data-th);
                font-weight: bold;
                color: var(--text-secondary);
                width: 80px;
                flex-shrink: 0;
                text-align: left;
            }

            &.rank-cell, 
            &.points-cell, 
            &.lps-cell {
                justify-content: space-between;
            }

            &.player-cell {
                justify-content: space-between;
            }
        }
    }

    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: var(--background-secondary);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        overflow: hidden;

        tr {
            border-bottom: 1px solid var(--border-color-light);
            &:last-child {
                border-bottom: none;
            }
        }

        td, th {
            padding: 1rem;
            text-align: right;
        }

        td.player-cell,
        th:nth-child(2) {
            text-align: left;
        }
    }

    .medal {
        font-size: 1.25rem;
        margin-right: 0.5rem;
    }

    .points-cell {
        font-weight: 700;
        color: var(--primary-color);
    }

    .lps-cell {
        .gold {
            color: #FFD700;
            filter: drop-shadow(0 0 2px rgba(255, 215, 0, 0.5));
        }

        .silver {
            color: #C0C0C0;
            filter: drop-shadow(0 0 2px rgba(192, 192, 192, 0.5));
        }

        .bronze {
            color: #CD7F32;
            filter: drop-shadow(0 0 2px rgba(205, 127, 50, 0.5));
        }
    }
}

@include mobile {
    .highscores {
        padding: var(--padding-small);
    }

    .categories-list {
        gap: var(--padding-small);
    }

    .category-card {
        padding: var(--padding-small);

        .category-header {
            padding: var(--padding-small);

            .category-title {
                font-size: 1.125rem;
            }

            .difficulty-select {
                padding: 0.375rem 1.5rem 0.375rem 0.75rem;
                font-size: 0.875rem;
            }
        }

        .scores-table {
            table {

                th,
                td {
                    padding: 0.75rem;
                    font-size: 0.875rem;
                }
            }
        }
    }
}

@include tablet {
    .categories-list {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1200px) {
    .categories-list {
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>
