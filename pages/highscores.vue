<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="highscores" id="main-content">
            <h1 class="title">{{ t('highscores.title') }}</h1>

            <section class="search-section" role="search">
                <SearchBar 
                    id="category-search" 
                    v-model="searchQuery" 
                    :placeholder="t('highscores.searchPlaceholder')" 
                />
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
                                    <td class="rank-cell">
                                        <div class="rank-display">
                                            <span v-if="index < 3" class="medal">
                                                {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
                                            </span>
                                            <span class="rank-number">{{ index + 1 }}</span>
                                        </div>
                                    </td>
                                    <td class="player-cell">{{ score.username }}</td>
                                    <td class="points-cell">{{ score.points }}</td>
                                    <td class="lps-cell">
                                        <div class="lp-display">
                                            <Icon name="material-symbols:album" class="lp-icon" />
                                            <span>{{ score.lps }}</span>
                                        </div>
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
        </main>
    </NuxtLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useFetch } from '#app'
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
        console.log('Frontend: Fetching highscores for language:', currentLocale)

        const response = await $fetch('/api/highscores', {
            method: 'GET',
            params: {
                language: currentLocale
            }
        })

        console.log('Frontend: Raw API response:', response)

        if (Array.isArray(response)) {
            highscores.value = response

            // Initialize difficulties for new categories
            const categories = [...new Set(response.map(score => score.category))]
            console.log('Frontend: Found categories:', categories)

            categories.forEach(category => {
                if (!selectedDifficulties.value[category]) {
                    selectedDifficulties.value[category] = 'easy'
                }
            })

            console.log('Frontend: Current difficulties:', selectedDifficulties.value)
        } else {
            console.error('Frontend: Invalid API response format:', response)
            highscores.value = []
        }
    } catch (error) {
        console.error('Frontend: Error fetching highscores:', error)
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
    console.log('Frontend: Language changed, fetching new data')
    fetchHighscores()
})

// Initial fetch
onMounted(() => {
    console.log('Frontend: Component mounted, fetching initial data')
    fetchHighscores()
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.highscores {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: var(--padding-medium);
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    align-items: center;
}

.title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--padding-small);
    text-align: center;
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
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
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
    width: 100%;
    
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: var(--padding-medium);
        background: var(--surface-color);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

        th, td {
            padding: 1.25rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: var(--background-secondary);
        }

        td {
            font-size: 1rem;
            color: var(--text-color);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr {
            transition: all 0.2s ease;

            &:hover {
                background: var(--background-secondary);
                transform: translateY(-1px);
            }
        }

        .rank-cell {
            width: 100px;
        }

        .player-cell {
            width: 40%;
            font-weight: 500;
        }

        .points-cell, .lps-cell {
            width: 120px;
            text-align: center;
        }

        .rank-display {
            display: flex;
            align-items: center;
            gap: 0.75rem;

            .medal {
                font-size: 1.5rem;
                line-height: 1;
            }

            .rank-number {
                font-weight: 600;
                min-width: 24px;
                color: var(--text-secondary);
            }
        }

        .lp-display {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.25rem 0.75rem;
            background: var(--background-secondary);
            border-radius: var(--border-radius);

            .lp-icon {
                color: var(--primary-color);
                font-size: 1.25rem;
            }
        }

        .points-cell {
            font-weight: 700;
            color: var(--primary-color);
            font-size: 1.125rem;
        }
    }
}

.medal-icon {
    font-size: 1.2em;
    margin-left: var(--padding-small);
}

.lp-icon {
    margin-right: var(--padding-small);
    font-size: 1.2em;
}

.rank-display {
    display: flex;
    align-items: center;
    gap: 0.25rem;
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
                th, td {
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
