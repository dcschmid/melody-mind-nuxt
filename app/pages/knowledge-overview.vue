<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <div class="gameHome" id="main-content">
            <section class="intro">
                <h1 tabindex="-1" class="page-title">{{ $t('knowledge.title') }}</h1>
                <p class="intro-text overview-text" v-if="$t('knowledge.description')">{{ $t('knowledge.description') }}</p>
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
                        :intro-subline="item.description"
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
import { ref, computed, unref } from 'vue'
import { useRouter } from 'vue-router'
import { useRequestURL } from '#imports'
import { useAsyncData, queryContent } from '#imports'

const searchQuery = ref('')
const router = useRouter()
const { locale, t } = useI18n()
const localePath = useLocalePath()
const url = useRequestURL()

// SEO Meta Tags
const metaTitle = computed(() => t('knowledge.meta.title'))
const metaDescription = computed(() => t('knowledge.meta.description'))

useSeoMeta({
    title: metaTitle,
    description: metaDescription,
    ogTitle: metaTitle,
    ogDescription: metaDescription,
    ogType: 'website',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1',
    twitterCard: 'summary_large_image',
    ogUrl: url.href
})

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

// JSON-LD
const jsonLdData = computed(() => ({
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: unref(metaTitle),
    description: unref(metaDescription),
    url: url.href,
    mainEntity: {
        '@type': 'ItemList',
        itemListElement: (knowledgeItems.value || []).map((item, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            item: {
                '@type': 'Article',
                name: item.title,
                description: item.description,
                url: localePath(`/knowledge/${item._file.split('/')[1]}/${item._file.split('/').pop().replace('.md', '')}`)
            }
        }))
    }
}))

useJsonld(() => unref(jsonLdData))

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
    max-width: var(--content-width);
    padding: var(--padding-medium);
}

.page-title {
    font-size: var(--font-size-responsive-3xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
    margin-bottom: var(--padding-large);
    color: var(--primary-color);
    line-height: var(--line-height-tight);
}

.overview-text {
    font-size: var(--font-size-responsive-md);
    line-height: var(--line-height-relaxed);
    text-align: center;
    color: var(--text-secondary);
    max-width: var(--max-line-length);
    margin: 0 auto var(--padding-large);
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--padding-large);
    padding: var(--padding-medium);

    @media (width >= 640px) {
        grid-template-columns: repeat(2, 1fr);
    }

    @media (width >= 1024px) {
        grid-template-columns: repeat(3, 1fr);
    }

    @media (width <= 768px) {
        gap: var(--padding-medium);
        padding: var(--padding-small);
    }
}

.category-card {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    overflow: hidden;
    transition: all var(--transition-speed) var(--transition-bounce);
    box-shadow: var(--box-shadow);

    &:hover {
        transform: translateY(-2px);
        box-shadow: var(--box-shadow-hover);
    }

    &:focus-within {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }
}

.category-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.category-description {
    font-size: var(--font-size-base);
    color: var(--text-secondary);
    line-height: var(--line-height-normal);
}

@media (prefers-reduced-motion: reduce) {
    .category-card {
        transition: none;
        transform: none;

        &:hover {
            transform: none;
        }
    }
}

@media (prefers-reduced-motion: no-preference) {
    .category-card {
        animation: fadeIn var(--transition-speed) var(--transition-bounce);
    }
}

.visually-hidden {
    @include sr-only;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(var(--padding-medium));
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
