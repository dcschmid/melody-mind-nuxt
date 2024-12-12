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
    margin: 1.5rem auto;
    padding: clamp(var(--padding-medium), 4vw, var(--padding-large));
    color: var(--text-color);
}

.intro {
    text-align: center;
    margin-bottom: clamp(var(--padding-medium), 5vw, var(--padding-large));

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
    gap: clamp(var(--padding-medium), 3vw, var(--padding-large));
    place-items: center;
    padding: clamp(var(--padding-medium), 3vw, var(--padding-large));
    transition: all var(--transition-speed);

    &:hover {
        box-shadow: var(--box-shadow-hover);
    }
}

.cover {
    position: relative;
    width: 100%;
    max-width: clamp(280px, 35vw, 400px);
    aspect-ratio: 1;
    margin: 0 auto;
}

.coverImage {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}

.text {
    font-size: clamp(1.125rem, 2vw, var(--body-font-size));
    line-height: var(--line-height-body);
    max-width: min(90%, var(--max-line-length));
    margin: 0 auto;
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
    gap: clamp(var(--padding-small), 2vw, var(--padding-medium));
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    max-width: min(100%, 900px);
    margin: 0 auto;
    padding: var(--padding-medium) 0;

    .button {
        background: var(--highlight-color);
        color: var(--button-text-color);
        padding: var(--padding-medium) var(--padding-large);
        border-radius: var(--border-radius);
        font-size: var(--button-font-size);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: var(--padding-small);
        min-height: var(--min-touch-target);
        transition: all var(--transition-speed);
        box-shadow: var(--box-shadow);
        flex: 1;
        min-width: clamp(200px, 25%, 300px);
        justify-content: center;

        &:hover {
            background: var(--button-hover-color);
            transform: translateY(-2px);
        }

        &:active {
            transform: translateY(0);
        }
    }
}

@media (width <= 767px) {
    .buttonGroup {
        flex-direction: column;
        padding: var(--padding-small) 0;
        max-width: 350px;

        .button {
            width: 100%;
            min-width: 100%;
            padding: var(--padding-medium) var(--padding-medium);
        }
    }

    .text {
        font-size: clamp(1.125rem, 4vw, 1.25rem);
        padding: 0 var(--padding-small);
    }
}
</style>
