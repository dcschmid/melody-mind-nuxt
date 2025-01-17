<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <div class="gameHome" id="main-content">
            <section class="intro">
                <h1 tabindex="-1">{{ $t('knowledge.title') }}</h1>
                <p class="intro-text" v-if="$t('knowledge.description')">{{ $t('knowledge.description') }}</p>
            </section>

            <section class="search-section" role="search">
                <SearchBar id="knowledge-search" v-model="searchQuery" :placeholder="$t('gameHome.searchPlaceholder')" />
            </section>

            <section class="categories-section" role="region" aria-labelledby="categories-heading">
                <h2 id="categories-heading" class="visually-hidden">{{ $t('knowledge.overview') }}</h2>
                <div class="categories-grid" role="list">
                    <CategoryCard 
                        v-for="item in filteredKnowledgeItems" 
                        :key="item._path"
                        :headline="item.title"
                        :image-url="item.image"
                        :category-url="localePath(`/knowledge/${item._file.split('/')[1]}/${item._file.split('/').pop().replace('.md', '')}`)"
                        :description="item.description"
                        :is-playable="true"
                        class="category-card"
                        role="listitem"
                        @select="navigateToKnowledge(item)"
                    />
                </div>
            </section>
        </div>
    </NuxtLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRequestURL } from '#imports'
import { useAsyncData, queryContent } from '#imports'

const searchQuery = ref('')
const router = useRouter()
const { locale, t } = useI18n()
const localePath = useLocalePath()
const url = useRequestURL()

// Fetch knowledge articles using Nuxt Content
const { data: knowledgeItems } = await useAsyncData(
    'knowledge',
    () => queryContent('knowledge', locale.value).find()
)

const filteredKnowledgeItems = computed(() => {
    if (!searchQuery.value || !knowledgeItems.value) return knowledgeItems.value || []
    const query = searchQuery.value.toLowerCase()
    return knowledgeItems.value.filter(item => 
        item.title?.toLowerCase().includes(query) || 
        item.description?.toLowerCase().includes(query)
    )
})

useSeoMeta({
    title: computed(() => t('knowledge.title')),
    ogTitle: computed(() => t('knowledge.title')),
    description: computed(() => t('knowledge.description')),
    ogDescription: computed(() => t('knowledge.description')),
    ogType: 'website',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1',
    twitterCard: 'summary_large_image',
    ogUrl: computed(() => url.href)
})

const navigateToKnowledge = (item) => {
    const lang = item._file.split('/')[1]
    const filename = item._file.split('/').pop().replace('.md', '')
    const path = `/knowledge/${lang}/${filename}`
    router.push(localePath(path))
}
</script>

<style scoped lang="scss">
.gameHome {
    width: 100%;
    margin: 0 auto;
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        font-size: var(--header-font-size);
        color: var(--primary-color);
        margin-bottom: var(--padding-medium);
        font-weight: 700;
    }
}

.search-section {
    margin-bottom: var(--padding-large);
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    padding: var(--padding-medium);

    @media (min-width: 640px) {
        grid-template-columns: repeat(2, 1fr);
    }

    @media (min-width: 1024px) {
        grid-template-columns: repeat(3, 1fr);
    }

    @media (max-width: 768px) {
        gap: var(--padding-medium);
        padding: var(--padding-small);
    }

    @media (prefers-reduced-motion: reduce) {
        * {
            transition: none !important;
        }
    }
}

.category-card {
    background: var(--card-background);
    border-radius: var(--border-radius);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: var(--shadow-small);

    &:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-medium);
    }

    &:focus-within {
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }
}

@media (prefers-reduced-motion: no-preference) {
    .category-card {
        animation: fadeIn 0.5s ease-out;
    }
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
