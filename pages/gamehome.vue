<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <main class="gameHome" id="main-content">
            <section class="intro" v-motion-slide-top>
                <h1>{{ $t('gameHome.title') }}</h1>
            </section>

            <section class="search-section" v-motion-slide-visible>
                <SearchBar
                    id="category-search"
                    v-model="searchQuery"
                    :placeholder="$t('gameHome.searchPlaceholder')"
                />
            </section>

            <section class="categories-section" aria-label="Spielkategorien">
                <div class="categories-grid">
                    <CategoryCard
                        v-for="category in filteredCategories"
                        :key="category.slug"
                        :headline="category.headline"
                        :image-url="category.imageUrl"
                        :category-url="localePath(category.categoryUrl)"
                        :is-playable="category.isPlayable"
                    />
                </div>
            </section>
        </main>
    </NuxtLayout>
</template>

<script setup>
import { onMounted } from 'vue'

const { searchQuery, filteredCategories, loadCategories } = useCategories()
const { locale } = useI18n()
const localePath = useLocalePath()

onMounted(() => {
    loadCategories(locale.value)
})
</script>

<style scoped lang="scss">
.gameHome {
    width: 100%;
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        font-size: var(--header-font-size);
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
        font-weight: 700;
    }
}

.search-section {
    margin-bottom: var(--padding-large);
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
    gap: var(--padding-large);
    padding: var(--padding-small);
    will-change: transform;
    contain: content;

    @media (min-width: 640px) {
        grid-template-columns: repeat(2, 1fr);
    }

    @media (min-width: 1024px) {
        grid-template-columns: repeat(3, 1fr);
    }

    @media (prefers-reduced-motion: no-preference) {
        .category-card {
            animation: fadeIn 0.5s ease-out;
        }
    }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}

@media (max-width: 768px) {
    .gameHome {
        padding: var(--padding-small);
    }

    .categories-grid {
        gap: var(--padding-medium);
    }
}
</style>
