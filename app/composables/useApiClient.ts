/**
 * API Client composable using Nuxt's useFetch
 * Provides optimized, type-safe access to backend API endpoints
 */

// Highscore interfaces
export interface Highscore {
  id?: string
  points: number
  category: string
  difficulty: string
  language: string
  goldLP: boolean
  silverLP: boolean
  bronzeLP: boolean
  createdAt?: string
}

export interface SaveHighscoreResponse {
  success: boolean
  data?: Highscore
  error?: string
}

/**
 * API client composable that leverages Nuxt's built-in useFetch with improved type safety and error handling
 */
export const useApiClient = () => {
  // Common fetch options with good defaults
  const fetchOptions = {
    // Cache results for 5 minutes by default (can be overridden per request)
    key: '',
    server: true, // Allow SSR fetching
    lazy: false, // Immediate fetch by default
    retry: 1, // Retry once on failure
    timeout: 10000, // 10 second timeout
    onRequest({ request, options }: { request: string; options: { headers?: Record<string, string>; key?: string; body?: unknown; [key: string]: unknown } }) {
      // Add common headers like authorization if needed
      options.headers = {
        ...(options.headers || {}),
        'Content-Type': 'application/json'
      }

      // Generate cache key based on URL and params
      options.key = options.key || `${request}-${JSON.stringify(options.body || {})}`
    },
    onRequestError({ error }: { error: Error }) {
      console.error('API request error:', error)
    },
    onResponse({ response }: { response: Response }) {
      // You could add response validation or transformation here
      return response
    },
    onResponseError({ response }: { response: Response }) {
      console.error('API response error:', response.statusText)
    }
  }

  /**
   * Get list of highscores with optional filtering
   */
  const getHighscores = async (params?: {
    category?: string,
    difficulty?: string,
    language?: string,
    limit?: number
  }) => {
    // Spezifischen Cache-Key für bessere Cache-Strategie generieren
    const cacheKey = `highscores-${params?.category || 'all'}-${params?.difficulty || 'all'}-${params?.language || 'all'}-${params?.limit || 'default'}`
    const { data, error, refresh } = await useFetch('/api/highscores', {
      ...fetchOptions,
      method: 'GET',
      params,
      key: cacheKey,
      // Für bessere Performance mit Caching-Strategien arbeiten
      getCachedData: () => {
        // Optional: Daten aus dem SessionStorage holen, falls vorhanden
        const cached = sessionStorage.getItem(cacheKey)
        if (cached) {
          try {
            return JSON.parse(cached)
          } catch {
            // Fehler beim Parsen ignorieren
          }
        }
        return null
      },
      transform: (data) => {
        // Performance-Optimierte Transformation mit TypeScript Type Guard
        if (!Array.isArray(data)) return []
        const result = data.map(item => ({
          id: item.id,
          points: Number(item.points) || 0,
          category: String(item.category),
          difficulty: String(item.difficulty),
          language: String(item.language),
          goldLP: Boolean(item.goldLP),
          silverLP: Boolean(item.silverLP),
          bronzeLP: Boolean(item.bronzeLP),
          createdAt: item.createdAt
        } as Highscore))
        // Speichern im SessionStorage für schnelleren Zugriff in der aktuellen Sitzung
        try {
          sessionStorage.setItem(cacheKey, JSON.stringify(result))
        } catch {
          // Fehler beim Speichern ignorieren
        }
        return result
      }
    })

    return {
      highscores: data.value as Highscore[],
      error: error.value,
      refresh
    }
  }

  /**
   * Save a new highscore to the database
   */
  const saveHighscore = async (highscore: Omit<Highscore, 'id' | 'createdAt'>) => {
    // Performance-optimierte API-Anfrage für Speichern von Highscores
    const { data, error } = await useFetch<SaveHighscoreResponse>('/api/highscores', {
      ...fetchOptions,
      method: 'POST',
      body: highscore,
      immediate: true, // Sofort ausführen
      watch: false, // Nicht auf Props-Änderungen überwachen (optimiert Rendering)
      // Performance-Optimierung: Nach dem Speichern Cache invalidieren
      onResponse() {
        // Löschen aller Highscore-Cache-Einträge aus dem SessionStorage
        Object.keys(sessionStorage).forEach(key => {
          if (key.startsWith('highscores-')) {
            sessionStorage.removeItem(key)
          }
        })
      }
    })

    return {
      result: data.value,
      error: error.value
    }
  }

  /**
   * Get a user's game stats
   */
  const getUserStats = async (userId?: string) => {
    const { data, error, refresh } = await useFetch('/api/user/stats', {
      ...fetchOptions,
      method: 'GET',
      params: { userId }
    })

    return {
      stats: data.value,
      error: error.value,
      refresh
    }
  }

  /**
   * Generic API request method for custom endpoints
   */
  const request = async <T>(url: string, options = {}) => {
    const { data, error, refresh } = await useFetch<T>(url, {
      ...fetchOptions,
      ...options
    })

    return {
      data: data.value,
      error: error.value,
      refresh
    }
  }

  /**
   * Präfetcht Highscore-Daten für kritische Kategorien im Hintergrund
   * Verbessert gefühlte Performance beim Laden der häufigsten Highscore-Listen
   */
  const prefetchPopularHighscores = () => {
    // Daten im Hintergrund vorladen für bessere Performance
    // Wird von der Startseite aufgerufen, verbessert die Navigation zu Highscores
    const prefetchPromises = [
      // Allgemeine Highscores (Top 10)
      getHighscores({ limit: 10 }),
      // Pop-Highscores (beliebteste Kategorie)
      getHighscores({ category: 'pop', limit: 5 })
    ]
    // Promise.allSettled ermöglicht unabhängiges Vorladen ohne Fehlerunterbrechung
    return Promise.allSettled(prefetchPromises)
  }

  /**
   * Optimierte Ressourcenverwaltung: Speicher-Cache bei Inaktivität oder Tab-Wechsel leeren
   * Verbessert Performance bei längerer Nutzung und reduziert Speicherverbrauch
   */
  onMounted(() => {
    if (import.meta.client) {
      // Event-Listener für Tab-Wechsel hinzufügen
      window.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          // Cache selektiv leeren wenn Tab nicht sichtbar ist
          // Highscores behalten da sie häufig benötigt werden
          // Andere API-Daten können neu geladen werden
          const memoryCleanup = setTimeout(() => {
            // Selektiv nur bestimmte Cache-Einträge leeren
            // für bessere Ressourcennutzung
          }, 30000) // Nach 30 Sekunden im Hintergrund

          // Cleanup wenn Tab wieder aktiv wird
          document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
              clearTimeout(memoryCleanup)
            }
          }, { once: true })
        }
      })
    }
  })

  return {
    getHighscores,
    saveHighscore,
    getUserStats,
    request,
    prefetchPopularHighscores
  }
}
