<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="true">
    <div class="min-h-screen bg-[var(--color-surface)] p-4 text-white md:p-8">
      <div v-if="currentCategory" class="mx-auto max-w-4xl">
        <header class="mb-8 text-center">
          <h1 class="mb-4 text-3xl font-bold">
            {{ t('cover_quiz.title', { genre: currentCategory.headline }) }}
          </h1>
          <p class="text-gray-300">
            {{ t('cover_quiz.description') }}
          </p>
        </header>

        <CoverQuiz 
          v-if="!gameCompleted" 
          :category="$route.params.category as string" 
          @restart="handleRestart" 
        />

        <div v-else class="text-center">
          <h2 class="mb-4 text-2xl font-bold">{{ t('game.completed') }}</h2>
          <button
            @click="handleRestart"
            class="rounded-lg bg-[var(--color-primary)] px-6 py-3 font-medium text-white hover:bg-[var(--color-primary-dark)]"
          >
            {{ t('game.play_again') }}
          </button>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHead } from '#imports'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import CoverQuiz from '~/components/game/CoverQuiz.vue'

const { t, locale } = useI18n()
const route = useRoute()
const categories = ref<any[]>([])
const gameCompleted = ref(false)

const currentCategory = computed(() => {
  return categories.value.find((cat) => cat.slug === route.params.category)
})

// Type for category data
interface Category {
  slug: string
  headline: string
  text: string
}

const loadCategories = async () => {
  const cacheKey = `categories_${locale.value}`
  const cached = sessionStorage.getItem(cacheKey)
  
  if (cached) {
    categories.value = JSON.parse(cached)
    return
  }

  try {
    const data = await import(`~/json/${locale.value}_categories.json`)
    categories.value = data.default
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

const handleRestart = () => {
  gameCompleted.value = false
}

onMounted(() => {
  loadCategories()
})

useHead({
  title: computed(() => 
    currentCategory.value 
      ? `${t('cover_quiz.title', { genre: currentCategory.value.headline })} - Melody Mind` 
      : 'Cover Quiz - Melody Mind'
  ),
})
</script>
