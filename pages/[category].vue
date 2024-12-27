<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <div class="categoryPage">
            <CategoryIntro :category="currentCategory || null" />

            <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                v-if="currentCategory">
                <CategoryCover :image-url="currentCategory.imageUrl" :headline="currentCategory.headline" />

                <p class="text">{{ currentCategory.text }}</p>

                <UsernameInput ref="usernameInput" v-if="!hasUsername" @username-set="onUsernameSet" />
                <CategoryDifficultySelector v-if="hasUsername" :categorySlug="currentCategory.slug" />
            </article>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
const route = useRoute()
const { locale } = useI18n()
const url = useRequestURL()

interface Category {
    slug: string
    headline: string
    introSubline: string
    imageUrl: string
    text: string
}

const categories = ref<Category[]>([])
const usernameInput = ref(null)
const hasUsername = ref(false)

const loadCategories = async () => {
    const cacheKey = `categories_${locale.value}`

    if (categories.value.length > 0) return

    const cached = sessionStorage.getItem(cacheKey)
    if (cached) {
        categories.value = JSON.parse(cached)
        return
    }

    try {
        const data = await import(`../json/${locale.value}_categories.json`)
        categories.value = data.default
        sessionStorage.setItem(cacheKey, JSON.stringify(data.default))
    } catch (error) {
        console.error('Fehler beim Laden der Kategorien:', error)
        categories.value = []
    }
}

const currentCategory = computed(() => {
    return categories.value.find(cat => cat.slug === route.params.category)
})

const jsonLd = computed(() => ({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: currentCategory.value?.headline,
    description: currentCategory.value?.introSubline,
    url: url.href,
    image: currentCategory.value?.imageUrl
}))

useHead(() => ({
    title: currentCategory.value
        ? `${currentCategory.value.headline} - Melody Mind`
        : 'Kategorien - Melody Mind',
    titleTemplate: (titleChunk) => {
        return titleChunk ? `${titleChunk} - Melody Mind` : 'Melody Mind';
    },
    meta: [
        {
            name: 'description',
            content: currentCategory.value?.introSubline || 'Entdecken Sie unsere Kategorien'
        },
        {
            name: 'robots',
            content: 'index, follow'
        },
        {
            name: 'og:title',
            content: currentCategory.value?.headline || 'Kategorien'
        },
        {
            name: 'og:description',
            content: currentCategory.value?.introSubline || 'Entdecken Sie unsere Kategorien'
        },
        {
            name: 'og:type',
            content: 'website'
        },
        {
            name: 'og:url',
            content: url.href
        }
    ],
    link: [
        {
            rel: 'canonical',
            href: url.href
        }
    ],
    script: [
        {
            type: 'application/ld+json',
            children: JSON.stringify(jsonLd.value)
        }
    ]
}))

const onUsernameSet = () => {
    hasUsername.value = true
}

onMounted(() => {
    const storedUsername = localStorage.getItem('username')
    if (storedUsername) {
        hasUsername.value = true
    }
    loadCategories()
})
</script>

<style scoped lang="scss">
.categoryPage {
    width: var(--content-width);
    margin: 1.5rem auto;
    padding: clamp(var(--padding-medium), 4vw, var(--padding-large));
    color: var(--text-color);
}

.category {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
    display: grid;
    gap: clamp(var(--padding-medium), 3vw, var(--padding-large));
    place-items: center;
    padding: clamp(var(--padding-medium), 3vw, var(--padding-large));
    transition: all var(--transition-speed);

    &:hover {
        box-shadow: var(--box-shadow-hover);
    }
}

.text {
    font-size: clamp(1.125rem, 2vw, var(--body-font-size));
    line-height: var(--line-height-body);
    max-width: min(90%, var(--max-line-length));
    margin: 0 auto;
    text-align: center;
    color: var(--text-secondary);
}

@media (width <=767px) {
    .text {
        font-size: clamp(1.125rem, 4vw, 1.25rem);
        padding: 0 var(--padding-small);
    }
}
</style>
