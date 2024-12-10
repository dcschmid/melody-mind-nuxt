<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <div class="categoryPage">
            <section class="intro" v-if="currentCategory">
                <h1>{{ currentCategory.headline }} {{ $t('category.selected') }}</h1>
                <p>{{ currentCategory.introSubline }}</p>
            </section>

            <article class="category" :data-category="currentCategory?.slug" aria-labelledby="difficulty-heading"
                v-if="currentCategory" v-motion :initial="{ opacity: 0, y: 100 }" :enter="{ opacity: 1, y: 0 }">
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
                            :to="localePath(`/${currentCategory.slug}/${difficulty}`)" class="button"
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
    try {
        const data = await import(`../json/${locale.value}_categories.json`)
        categories.value = data.default
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
    max-width: var(--max-line-length);
    margin: 0 auto;
    padding: var(--padding-medium);
    animation: fadeIn 0.8s ease-out;
}

.intro {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        margin-bottom: var(--padding-small);
    }
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

.category {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    align-items: center;
    width: 100%;
    padding: var(--padding-large);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: transform 0.3s ease-in-out;

    &:hover {
        transform: translateY(-5px);
    }
}

.cover {
    position: relative;
    margin: 0 auto;
}

.coverImage {
    width: 100%;
    max-width: 280px;
    height: auto;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: transform var(--transition-speed) ease-in-out,
        box-shadow var(--transition-speed) ease-in-out;

    &:hover {
        transform: scale(1.08);
        box-shadow: 0 15px 30px rgb(0 0 0 / 40%);
    }
}

.text {
    max-width: 700px;
    margin: 0 auto;
    font-family: var(--font-family);
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    hyphens: auto;
    color: var(--text-color);
    text-align: center;
    letter-spacing: var(--spacing-text);
}

.difficultySection {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);
    align-items: center;
    width: 100%;
}

.buttonHeadline {
    font-family: var(--font-family);
    font-size: var(--header-font-size);
    font-weight: 700;
    line-height: var(--line-height-body);
    color: var(--text-color);
    text-align: center;
}

.buttonGroup {
    display: flex;
    flex-wrap: wrap;
    gap: var(--padding-medium);
    justify-content: center;
    padding: calc(var(--padding-small) / 2);

    .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: var(--padding-small) var(--padding-medium);
        color: var(--button-text-color);
        background-color: var(--highlight-color);
        border-radius: var(--border-radius);
        text-decoration: none;
        transition: background-color var(--transition-speed);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        transform: translateZ(0);
        will-change: transform;

        &::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
        }

        &:hover {
            transform: translateY(-2px) translateZ(0);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);

            &::before {
                width: 300px;
                height: 300px;
            }
        }

        &:active {
            transform: translateY(1px);
        }
    }
}

@media (width <=768px) {
    .category {
        padding: var(--padding-medium);
    }

    .coverImage {
        max-width: 200px;
    }
}

@media (width <=480px) {
    .buttonGroup {
        flex-direction: column;
        width: 100%;
        max-width: 300px;
    }

    .coverImage {
        max-width: 150px;
    }

    .buttonHeadline {
        font-size: calc(var(--header-font-size) * 0.8);
    }
}
</style>
