import { useDebounce } from '@vueuse/core'
import { ref, computed } from 'vue'

interface Category {
  headline: string
  imageUrl: string
  categoryUrl: string
  isPlayable: boolean
  slug: string
}

export const useCategories = () => {
  const categories = ref<Category[]>([])
  const searchQuery = ref('')
  const debouncedSearch = useDebounce(searchQuery, 300)

  const filteredCategories = computed(() => {
    let result = categories.value

    if (debouncedSearch.value) {
      const query = debouncedSearch.value.toLowerCase()
      result = result.filter((category) => category.headline.toLowerCase().includes(query))
    }

    // Sort playable categories first
    return result.sort((a, b) => {
      if (a.isPlayable === b.isPlayable) return 0
      return a.isPlayable ? -1 : 1
    })
  })

  const preloadImages = (categoryData: any[]) => {
    if (typeof window !== 'undefined') {
      categoryData.slice(0, 4).forEach((category) => {
        const img = new Image()
        img.src = `${category.imageUrl}?w=480`
        img.importance = 'high'
      })
    }
  }

  const loadCategories = async (locale: string) => {
    try {
      const { default: data } = await import(`../json/${locale}_categories.json`)
      categories.value = data
      preloadImages(data)
    } catch (error) {
      console.error('Fehler beim Laden der Kategorien:', error)
      categories.value = []
    }
  }

  return {
    categories,
    searchQuery,
    filteredCategories,
    loadCategories,
  }
}
