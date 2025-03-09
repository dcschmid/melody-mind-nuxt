import { useDebounce } from '@vueuse/core'
import { computed, ref } from 'vue'

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

  const preloadImages = (categoryData: Category[]) => {
    if (typeof window !== 'undefined') {
      categoryData.slice(0, 4).forEach((category) => {
        const img = new Image()
        // Verwende den Originalpfad ohne Query-Parameter
        img.src = category.imageUrl
      })
    }
  }

  const loadCategories = async (locale: string) => {
    try {
      const { default: data } = await import(`../json/${locale}_categories.json`)

      // Bildpfade für jede Kategorie präparieren
      const processedData = data.map((category: Category) => ({
        ...category,
        // Stellen sicher, dass der Bildpfad korrekt formatiert ist
        imageUrl: category.imageUrl.startsWith('/')
          ? category.imageUrl // Bereits ein absoluter Pfad
          : `/${category.imageUrl}` // Konvertiere zu absolutem Pfad
      }))

      categories.value = processedData
      preloadImages(processedData)
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
