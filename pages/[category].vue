<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <div class="categoryPage">
            <section class="intro" v-if="currentCategory">
                <h1>{{ currentCategory.headline }} {{ $t('category.selected') }}</h1>
                <p>{{ currentCategory.introSubline }}</p>
            </section>

            <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                v-if="currentCategory">
                <div class="cover" role="img" :aria-label="currentCategory.headline + ' ' + $t('category.image.alt')">
                    <img v-if="currentCategory.imageUrl" class="coverImage" :src="currentCategory.imageUrl"
                        :alt="currentCategory.headline" width="280" height="280" loading="lazy" decoding="async" />
                    <div v-else class="fallbackImage">{{ $t('category.noImage') }}</div>
                </div>

                <p class="text">{{ currentCategory.text }}</p>

                <div class="difficultySection">
                    <h2 id="difficulty-heading" class="buttonHeadline">
                        {{ $t('category.difficulty.heading') }}
                    </h2>
                    <div class="buttonGroup" role="group" aria-label="Schwierigkeitsgrade">
                        <NuxtLink v-for="difficulty in ['easy', 'medium', 'hard']" :key="difficulty"
                            :to="localePath(`/game-${currentCategory.slug}/${difficulty}`)" class="button"
                            :aria-label="$t(`category.difficulty.${difficulty}.label`)">
                            <Icon name="mdi:play-outline" size="36" /> {{ $t(`category.difficulty.${difficulty}`) }}
                        </NuxtLink>
                    </div>
                </div>
            </article>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
definePageMeta({
    middleware: 'auth'
})

const route = useRoute()
const { locale } = useI18n()
const localePath = useLocalePath()

interface Category {
    slug: string
    headline: string
    introSubline: string
    imageUrl: string
    text: string
}

const categories = ref<Category[]>([])

// Kategorien laden
const loadCategories = async () => {
    const cacheKey = `categories_${locale.value}`

    // Prüfe erst den Runtime Cache
    if (categories.value.length > 0) return

    // Dann den SessionStorage
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

// Aktuelle Kategorie finden
const currentCategory = computed(() => {
    return categories.value.find(cat => cat.slug === route.params.category)
})

useHead(() => ({
    title: currentCategory.value ? `${currentCategory.value.headline} - Ihre Website` : 'Kategorien',
    meta: [
        {
            name: 'description',
            content: currentCategory.value?.introSubline || ''
        }
    ]
}))

onMounted(() => {
    loadCategories()
})
</script>

<style scoped lang="scss">
.categoryPage {
    width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-large);
    color: var(--text-color);
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        font-size: var(--header-font-size);
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
    }

    p {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-secondary);
    }
}

.category {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
    display: grid;
    gap: var(--padding-large);
    place-items: center;
    padding: var(--padding-large);
    transition: all var(--transition-speed);

    &:hover {
        box-shadow: var(--box-shadow-hover);
    }
}

.cover {
    position: relative;
    width: 100%;
    max-width: 500px;
    aspect-ratio: 1;
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--box-shadow);
    transition: transform var(--transition-speed);

    &:hover {
        transform: scale(1.05);
    }
}

.coverImage {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: filter var(--transition-speed);

    &:hover {
        filter: brightness(1.1);
    }
}

.text {
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    max-width: var(--max-line-length);
    text-align: center;
    color: var(--text-secondary);
}

.difficultySection {
    display: grid;
    gap: var(--padding-medium);
    place-items: center;
    width: 100%;
}

.buttonHeadline {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
}

.buttonGroup {
    display: flex;
    gap: var(--padding-medium);
    justify-content: center;

    .button {
        background: var(--highlight-color);
        color: var(--button-text-color);
        padding: var(--padding-small) var(--padding-large);
        border-radius: var(--border-radius);
        font-size: var(--button-font-size);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: var(--padding-small);
        min-height: var(--min-touch-target);
        transition: all var(--transition-speed);
        box-shadow: var(--box-shadow);

        &:hover {
            background: var(--button-hover-color);
            transform: scale(1.05);
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
        }
    }
}

@media (width <= 767px) {
    .buttonGroup {
        flex-direction: column;
        width: 100%;
        max-width: 300px;
    }

    .text {
        padding: 0 var(--padding-small);
    }
}
</style>
