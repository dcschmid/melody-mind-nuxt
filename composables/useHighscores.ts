interface Category {
    slug: string;
    name: string;
}

export function useHighscores() {
    const categoryScoresCache = new Map()

    const loadCategoryHighscores = async (categories: Category[], locale: string) => {
        try {
            const promises = categories.map(category => {
                const cacheKey = `${category.slug}-${locale}`

                if (categoryScoresCache.has(cacheKey)) {
                    return Promise.resolve({
                        slug: category.slug,
                        scores: categoryScoresCache.get(cacheKey)
                    })
                }

                return fetch(`/api/highscore/category/list?category=${category.slug}&language=${locale}`)
                    .then(res => res.json())
                    .then(data => {
                        categoryScoresCache.set(cacheKey, data.scores)
                        return { slug: category.slug, scores: data.scores }
                    })
            })

            return await Promise.all(promises)
        } catch (error) {
            console.error('Fehler beim Laden der Kategorie-Highscores:', error)
            throw error
        }
    }

    const loadTotalHighscores = async (locale: string) => {
        try {
            const response = await fetch(`/api/highscore/total/list?language=${locale}`)
            return await response.json()
        } catch (error) {
            console.error('Error loading total highscores:', error)
            throw error
        }
    }

    return {
        loadCategoryHighscores,
        loadTotalHighscores
    }
}
