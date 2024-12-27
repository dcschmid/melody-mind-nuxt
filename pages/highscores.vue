<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">

        <div class="highscores-container">
            <h1>{{ t('highscores.title') }}</h1>

            <div class="controls">
                <!-- Search Input -->
                <div class="search-input">
                    <input v-model="searchQuery" type="text" :placeholder="t('highscores.searchPlaceholder')" />
                </div>
            </div>

            <ClientOnly>
                <!-- Highscores by Category -->
                <div class="categories-grid">
                    <div v-for="category in filteredCategories" :key="category" class="category-card">
                        <h2>{{ category }}</h2>
                        <div class="scores-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>{{ t('highscores.rank') }}</th>
                                        <th>{{ t('highscores.player') }}</th>
                                        <th>{{ t('highscores.difficulty') }}</th>
                                        <th>{{ t('highscores.points') }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(score, index) in groupedHighscores[category]" :key="index"
                                        :class="{ 'gold': index === 0, 'silver': index === 1, 'bronze': index === 2 }">
                                        <td data-label="Rang">{{ index + 1 }}</td>
                                        <td data-label="Spieler">{{ score.username }}</td>
                                        <td data-label="Schwierigkeit">{{ t(`difficulty.${score.difficulty}`) }}</td>
                                        <td data-label="Punkte">{{ score.points }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- No Results Message -->
                <div v-if="filteredCategories.length === 0" class="no-results">
                    {{ t('highscores.noResults') }}
                </div>

                <template #fallback>
                    <div class="loading-state">
                        {{ t('common.loading') }}
                    </div>
                </template>
            </ClientOnly>
        </div>

    </NuxtLayout>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const searchQuery = ref('')
const { locale, t } = useI18n()

// Verwende useLazyAsyncData für bessere SSR-Performance
const { data: highscores, refresh } = useLazyAsyncData(
    `highscores-${locale.value}`,
    async () => {
        try {
            const response = await $fetch('/api/highscores', {
                params: {
                    language: locale.value
                }
            })
            return response || []
        } catch (error) {
            console.error('Error fetching highscores:', error)
            return []
        }
    },
    {
        immediate: true,
        server: true,
        default: () => []
    }
)

// Aktualisiere die Daten wenn sich die Sprache ändert
watch(locale, () => {
    refresh()
})

const groupedHighscores = computed(() => {
    const groups = {}
    const scores = unref(highscores) || []
    
    scores.forEach(score => {
        if (!groups[score.category]) {
            groups[score.category] = []
        }
        groups[score.category].push(score)
    })
    return groups
})

const filteredCategories = computed(() => {
    if (!searchQuery.value.trim()) return Object.keys(groupedHighscores.value)

    const query = searchQuery.value.toLowerCase()
    return Object.keys(groupedHighscores.value).filter(category =>
        category.toLowerCase().includes(query)
    )
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.highscores-container {
    padding: var(--padding-large);
    max-width: 1200px;
    margin: 0 auto;
    color: var(--text-color);

    h1 {
        @include heading-1;
        text-align: center;
        margin-bottom: var(--padding-large);
        color: var(--primary-color);
    }
}

.controls {
    margin-bottom: var(--padding-large);
    
    .search-input {
        max-width: 400px;
        margin: 0 auto;

        input {
            width: 100%;
            padding: var(--padding-small);
            background-color: var(--surface-color);
            border: 2px solid var(--secondary-color);
            border-radius: var(--border-radius);
            color: var(--text-color);
            font-size: var(--body-font-size);

            &:focus {
                outline: none;
                border-color: var(--highlight-color);
            }
        }
    }
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--padding-large);
}

.category-card {
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-medium);
    box-shadow: var(--box-shadow);

    h2 {
        color: var(--highlight-color);
        font-size: 1.5rem;
        margin-bottom: var(--padding-medium);
        text-align: center;
    }
}

.scores-table {
    table {
        width: 100%;
        border-collapse: collapse;
        background: var(--background-color);
        border-radius: var(--border-radius);
        overflow: hidden;

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--surface-color);
        }

        th {
            background-color: var(--surface-color);
            color: var(--text-secondary);
            font-weight: 600;
            white-space: nowrap;
        }

        tr {
            transition: background-color 0.2s;

            &:hover {
                background-color: var(--surface-color);
            }

            &.gold td:first-child {
                color: #ffd700;
                font-weight: bold;
            }

            &.silver td:first-child {
                color: #c0c0c0;
                font-weight: bold;
            }

            &.bronze td:first-child {
                color: #cd7f32;
                font-weight: bold;
            }
        }

        // Responsive Anpassungen
        @include mobile {
            th {
                display: none; // Header ausblenden auf Mobil
            }

            tr {
                display: block;
                margin-bottom: 1rem;
                border: 1px solid var(--surface-color);
                border-radius: var(--border-radius);
                background-color: var(--surface-color);

                td {
                    display: block;
                    padding: 8px 12px;
                    text-align: right;
                    border: none;

                    &:before {
                        content: attr(data-label);
                        float: left;
                        font-weight: bold;
                        color: var(--text-secondary);
                    }

                    &:not(:last-child) {
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    }
                }
            }
        }
    }
}

.no-results {
    text-align: center;
    color: var(--text-secondary);
    padding: var(--padding-large);
}

.loading-state {
    text-align: center;
    padding: var(--padding-large);
}
</style>
