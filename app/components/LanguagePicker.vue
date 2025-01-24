<template>
    <div 
        class="language-picker"
        role="navigation"
        aria-label="Language selection"
    >
        <button 
            class="current-language"
            @click="isOpen = !isOpen"
            :aria-expanded="isOpen"
            :aria-controls="dropdownId"
            aria-haspopup="listbox"
        >
            <span class="flag" aria-hidden="true">{{ (locale && locale.length >= 2) ? getFlagEmoji(locale.substring(0, 2)) : '' }}</span>
            <span class="language-name">{{ t(`languages.${locale}`) }}</span>
            <Icon
                name="material-symbols:keyboard-arrow-down-rounded"
                size="24"
                class="dropdown-arrow"
                :class="{ 'is-open': isOpen }"
                aria-hidden="true"
            />
            <span class="sr-only">{{ isOpen ? t('common.closeLanguageMenu') : t('common.openLanguageMenu') }}</span>
        </button>

        <div 
            v-show="isOpen" 
            class="language-options"
            :id="dropdownId"
            role="listbox"
            :aria-label="t('common.selectLanguage')"
            tabindex="-1"
        >
            <button
                v-for="loc in availableLocales"
                :key="loc.code"
                class="language-option"
                @click="handleLocaleChange(loc.code)"
                role="option"
                :aria-selected="loc.code === locale"
            >
                <span class="flag" aria-hidden="true">{{ (loc?.code && loc.code.length >= 2) ? getFlagEmoji(loc.code.substring(0, 2)) : '' }}</span>
                <span class="language-name">{{ t(`languages.${loc.code}`) }}</span>
                <span class="sr-only">{{ t('common.selectLanguageLabel', { language: t(`languages.${loc.code}`) }) }}</span>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale, locales, setLocale, t } = useI18n()
const isOpen = ref(false)
const dropdownId = 'language-dropdown'

const availableLocales = computed(() => {
    return locales.value.filter(i => i.code !== locale.value)
})

const flagEmojiCache = new Map()

const getFlagEmoji = (countryCode: string): string => {
    const cacheKey = countryCode.toUpperCase()
    if (flagEmojiCache.has(cacheKey)) {
        return flagEmojiCache.get(cacheKey)
    }

    const code = cacheKey === 'EN' ? 'GB' : cacheKey
    const codePoints = code
        .split('')
        .map(char => 127397 + char.charCodeAt())
    const emoji = String.fromCodePoint(...codePoints)
    flagEmojiCache.set(cacheKey, emoji)
    return emoji
}

const handleLocaleChange = async (localeCode: string) => {
    await setLocale(localeCode)
    isOpen.value = false
    announceLanguageChange(localeCode)
}

const announceLanguageChange = (newLocale: string) => {
    const message = t('common.languageChanged', { language: t(`languages.${newLocale}`) })
    const announcement = document.createElement('div')
    announcement.setAttribute('role', 'status')
    announcement.setAttribute('aria-live', 'polite')
    announcement.classList.add('sr-only')
    announcement.textContent = message
    document.body.appendChild(announcement)
    setTimeout(() => announcement.remove(), 1000)
}

const closeDropdown = (e: MouseEvent) => {
    if (!e.target || !(e.target as HTMLElement).closest('.language-picker')) {
        isOpen.value = false
    }
}

// Tastaturnavigation
const handleKeyDown = (e: KeyboardEvent) => {
    if (!isOpen.value) return
    
    const options = document.querySelectorAll('.language-option')
    const currentIndex = Array.from(options).findIndex(option => option === document.activeElement)
    
    switch (e.key) {
        case 'Escape':
            isOpen.value = false
            break
        case 'ArrowDown':
            e.preventDefault()
            if (currentIndex < options.length - 1) {
                (options[currentIndex + 1] as HTMLElement).focus()
            }
            break
        case 'ArrowUp':
            e.preventDefault()
            if (currentIndex > 0) {
                (options[currentIndex - 1] as HTMLElement).focus()
            }
            break
        case 'Home':
            e.preventDefault()
            ;(options[0] as HTMLElement).focus()
            break
        case 'End':
            e.preventDefault()
            ;(options[options.length - 1] as HTMLElement).focus()
            break
    }
}

onMounted(() => {
    document.addEventListener('click', (e) => closeDropdown(e))
    document.addEventListener('keydown', (e) => handleKeyDown(e))
})

onUnmounted(() => {
    document.removeEventListener('click', closeDropdown)
    document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped lang="scss">
@use '@/assets/scss/mixins' as *;

.language-picker {
    position: relative;
    z-index: var(--z-index-header);
}

.current-language {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background-color: var(--surface-color);
    border: 2px solid transparent;
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: var(--font-size-base);
    font-weight: 500;
    line-height: 1.5;
    cursor: pointer;
    min-width: 140px;
    transition: all 0.2s ease;

    &:hover {
        background-color: var(--secondary-color);
        border-color: var(--highlight-color);
        color: var(--text-hover);

        .dropdown-arrow {
            color: var(--highlight-color);
        }
    }

    &:focus-visible {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 3px var(--focus-ring-color);
    }
}

.dropdown-arrow {
    margin-left: auto;
    transition: transform 0.2s ease;
    color: var(--text-secondary);

    &.is-open {
        transform: rotate(180deg);
        color: var(--highlight-color);
    }
}

.language-options {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    width: 100%;
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    border: 2px solid var(--secondary-color);
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    .language-option {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem 1rem;
        border: none;
        background: transparent;
        color: var(--text-color);
        font-size: var(--font-size-base);
        line-height: 1.5;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
            background-color: var(--secondary-color);
            color: var(--text-hover);
        }

        &:focus-visible {
            outline: none;
            background-color: var(--secondary-color);
            color: var(--text-hover);
            box-shadow: inset 0 0 0 3px var(--focus-ring-color);
        }

        &:not(:last-child) {
            border-bottom: 1px solid var(--border-color);
        }

        &[aria-selected="true"] {
            background-color: var(--secondary-color);
            color: var(--highlight-color);
            font-weight: 600;
        }
    }
}

.flag {
    font-size: 1.2rem;
    line-height: 1;
}

.language-name {
    font-size: var(--font-size-base);
    font-weight: 500;
}

/* Screen reader only class */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Reduzierte Bewegung */
@media (prefers-reduced-motion: reduce) {
    .current-language,
    .language-option,
    .dropdown-arrow {
        transition: none;
    }
}

/* High Contrast Mode */
@media (prefers-contrast: more) {
    .current-language,
    .language-options {
        border-width: 3px;
    }

    .language-option {
        border-bottom-width: 2px;
    }
}

/* Mobile Anpassungen */
@media (max-width: 768px) {
    .current-language {
        min-width: 120px;
        padding: 0.5rem 0.75rem;
    }

    .language-name {
        font-size: 0.9rem;
    }

    .language-option {
        padding: 0.5rem 0.75rem;
    }
}

/* Unterstützung für Hover auf Touch-Geräten */
@media (hover: hover) {
    .current-language:hover,
    .language-option:hover {
        background-color: var(--secondary-color);
        color: var(--text-hover);
    }
}
</style>
