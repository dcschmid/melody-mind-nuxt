import { useDebounce } from "@vueuse/core";
import { ref, computed } from "vue";

interface Category {
  headline: string;
  imageUrl: string;
  categoryUrl: string;
  isPlayable: boolean;
  slug: string;
}

export const useCategories = () => {
  const categories = ref<Category[]>([]);
  const searchQuery = ref("");
  const debouncedSearch = useDebounce(searchQuery, 300);

  const filteredCategories = computed(() => {
    if (!debouncedSearch.value) return categories.value;

    const query = debouncedSearch.value.toLowerCase();
    return categories.value.filter((category) => category.headline.toLowerCase().includes(query));
  });

  const preloadImages = (categoryData: any[]) => {
    if (typeof window !== "undefined") {
      categoryData.slice(0, 4).forEach((category) => {
        const img = new Image();
        img.src = `${category.imageUrl}?w=480`;
        img.importance = "high";
      });
    }
  };

  const loadCategories = async (locale: string) => {
    const cacheKey = `categories_${locale}`;

    if (typeof window !== "undefined") {
      try {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
          const { data, timestamp } = JSON.parse(cached);
          if (Date.now() - timestamp < 24 * 60 * 60 * 1000) {
            categories.value = data;
            preloadImages(data);
            return;
          }
        }
      } catch (error) {
        console.error("Cache-Fehler:", error);
      }
    }

    try {
      const { default: data } = await import(`../json/${locale}_categories.json`);
      categories.value = data;
      if (typeof window !== "undefined") {
        localStorage.setItem(
          cacheKey,
          JSON.stringify({
            data,
            timestamp: Date.now(),
          })
        );
        preloadImages(data);
      }
    } catch (error) {
      console.error("Fehler beim Laden der Kategorien:", error);
      categories.value = [];
    }
  };

  return {
    categories,
    searchQuery,
    filteredCategories,
    loadCategories,
  };
};
