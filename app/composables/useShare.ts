import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'

/**
 * Interface for share data parameters
 */
interface ShareData {
  totalPoints: number
  correctAnswers: number
  maxQuestions: number
}

/**
 * Interface for share configuration
 */
interface ShareConfig {
  currentCategoryData?: { name: string }
  category: string
  difficulty: string
}

/**
 * Interface for social media sharing URLs
 */
interface SocialUrls {
  twitter: () => string
  whatsapp: () => string
  telegram: () => string
  reddit: () => string
}

/**
 * Composable for handling social media sharing functionality
 *
 * @param currentCategoryData - Current category data including name
 * @param category - Category identifier
 * @param difficulty - Difficulty level
 * @returns Object containing sharing methods and state
 */
export const useShare = ({ currentCategoryData, category, difficulty }: ShareConfig) => {
    const { t } = useI18n()
    const isMobile = ref(false)
    const canShare = ref(false)

    // Computed properties for frequently used values
    const genreName = computed(() => currentCategoryData?.name || category)
    const difficultyText = computed(() => t(`game.gameOver.share.message.difficulty.${difficulty}`))
    const baseUrl = computed(() => window.location.href)
    const originUrl = computed(() => window.location.origin)
    const getHashtags = computed(() => ['MelodyMind', 'MusicQuiz', genreName.value].join(','))

    /**
     * Achievement thresholds for different medal levels
     */
    const THRESHOLDS = {
        PERFECT: 1,
        SILVER: 0.75,
        BRONZE: 0.5
    } as const

    /**
     * Memoized message parts for better performance
     * Pre-computes translation strings that are frequently used
     */
    const getMessageParts = computed(() => ({
        intro: (points: number) => t('game.gameOver.share.message.intro', { points }),
        genre: t('game.gameOver.share.message.genre', { genre: genreName.value }),
        perfect: t('game.gameOver.share.message.perfect', { difficulty: difficultyText.value }),
        silver: t('game.gameOver.share.message.silver', { difficulty: difficultyText.value }),
        bronze: t('game.gameOver.share.message.bronze', { difficulty: difficultyText.value }),
        stats: (correct: number, total: number) =>
            t('game.gameOver.share.message.stats', { correct, total }),
        challenge: t('game.gameOver.share.message.challenge', { url: originUrl.value })
    }))

    /**
     * Initialize mobile detection and share capability
     * Uses requestIdleCallback for non-critical initialization
     */
    onMounted(() => {
        const controller = new AbortController()

        requestIdleCallback(() => {
            if (!controller.signal.aborted) {
                isMobile.value = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)
                canShare.value = !!navigator.share
            }
        })

        return () => controller.abort()
    })

    /**
     * Generates the complete share message based on game results
     *
     * @param shareData - Object containing game results
     * @returns Formatted share message string
     */
    const getShareMessage = ({ totalPoints, correctAnswers, maxQuestions }: ShareData): string => {
        const parts = getMessageParts.value
        const messages = [
            parts.intro(totalPoints),
            parts.genre
        ]

        const ratio = correctAnswers / maxQuestions
        if (ratio === THRESHOLDS.PERFECT) {
            messages.push(parts.perfect)
        } else if (ratio >= THRESHOLDS.SILVER) {
            messages.push(parts.silver)
        } else if (ratio >= THRESHOLDS.BRONZE) {
            messages.push(parts.bronze)
        }

        messages.push(
            parts.stats(correctAnswers, maxQuestions),
            parts.challenge
        )

        return messages.join('\n\n')
    }

    /**
     * Shares content using the Web Share API if available
     *
     * @param shareData - Object containing game results
     */
    const shareViaAPI = async (shareData: ShareData): Promise<void> => {
        if (!canShare.value) return

        try {
            await navigator.share({
                title: getMessageParts.value.intro(shareData.totalPoints),
                text: getShareMessage(shareData),
                url: baseUrl.value
            })
        } catch (error) {
            console.error('Error sharing content:', error)
        }
    }

    /**
     * Creates sharing URLs for different social media platforms
     *
     * @param shareData - Object containing game results
     * @param platform - Social media platform identifier
     * @returns Formatted sharing URL
     */
    const createSocialShareUrl = (shareData: ShareData, platform: keyof SocialUrls): string => {
        const text = getShareMessage(shareData)
        const encodedText = encodeURIComponent(text)
        const encodedUrl = encodeURIComponent(baseUrl.value)
        const encodedHashtags = encodeURIComponent(getHashtags.value)

        const urls: SocialUrls = {
            twitter: () => `https://twitter.com/intent/tweet?text=${encodedText}&hashtags=${encodedHashtags}`,
            whatsapp: () => `whatsapp://send?text=${encodedText}`,
            telegram: () => `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`,
            reddit: () => `https://www.reddit.com/submit?url=${encodedUrl}&title=${encodedText}`
        }

        return urls[platform]()
    }

    /**
     * Handles sharing to specific social media platforms
     *
     * @param shareData - Object containing game results
     * @param platform - Social media platform identifier
     */
    const createSocialShare = (shareData: ShareData, platform: keyof SocialUrls): void => {
        const url = createSocialShareUrl(shareData, platform)
        if (platform === 'whatsapp' && isMobile.value) {
            window.location.href = url
        } else {
            window.open(url, '_blank')?.focus()
        }
    }

    // Return public API
    return {
        isMobile,
        canShare,
        shareViaAPI,
        shareToTwitter: (shareData: ShareData) => createSocialShare(shareData, 'twitter'),
        shareToWhatsApp: (shareData: ShareData) => createSocialShare(shareData, 'whatsapp'),
        shareToTelegram: (shareData: ShareData) => createSocialShare(shareData, 'telegram'),
        shareToReddit: (shareData: ShareData) => createSocialShare(shareData, 'reddit')
    }
}
