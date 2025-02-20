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

    // Mapping von Sprachcodes zu Ländercodes für Flaggen
    const languageToCountry: { [key: string]: string } = {
        'EN': 'GB', // Englisch -> Großbritannien
        'DA': 'DK', // Dänisch -> Dänemark
        'SV': 'SE', // Schwedisch -> Schweden
        'PT': 'PT', // Portugiesisch -> Portugal
        'NL': 'NL', // Niederländisch -> Niederlande
        'FI': 'FI'  // Finnisch -> Finnland
    }

    const code = languageToCountry[cacheKey] || cacheKey
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
    gap: var(--padding-small);
    padding: var(--padding-small) var(--padding-medium);
    background-color: var(--surface-color);
    border: 2px solid transparent;
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    cursor: pointer;
    min-width: var(--min-touch-target);
    transition: all var(--transition-speed) var(--transition-bounce);

    &:hover {
        background-color: var(--secondary-color);
        border-color: var(--highlight-color);
        color: var(--text-color);

        .dropdown-arrow {
            color: var(--highlight-color);
        }
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }
}

.dropdown-arrow {
    margin-left: auto;
    transition: transform var(--transition-speed) var(--transition-bounce);
    color: var(--text-secondary);

    &.is-open {
        transform: rotate(180deg);
        color: var(--highlight-color);
    }
}

.language-options {
    position: absolute;
    top: calc(100% + var(--padding-small));
    left: 0;
    width: 100%;
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    border: 2px solid var(--surface-color-light);
    overflow: hidden;
    box-shadow: var(--box-shadow);

    .language-option {
        display: flex;
        align-items: center;
        gap: var(--padding-small);
        width: 100%;
        padding: var(--padding-small) var(--padding-medium);
        border: none;
        background: transparent;
        color: var(--text-color);
        font-size: var(--font-size-base);
        line-height: var(--line-height-normal);
        text-align: left;
        cursor: pointer;
        transition: all var(--transition-speed) var(--transition-bounce);

        &:hover {
            background-color: var(--surface-color-light);
            color: var(--text-color);
        }

        &:focus-visible {
            outline: none;
            background-color: var(--surface-color-light);
            color: var(--text-color);
            box-shadow: inset 0 0 0 var(--focus-outline-width) var(--focus-outline-color);
        }

        &:not(:last-child) {
            border-bottom: 1px solid var(--surface-color-light);
        }

        &[aria-selected="true"] {
            background-color: var(--surface-color-light);
            color: var(--primary-color);
            font-weight: var(--font-weight-semibold);
        }
    }
}

.flag {
    font-size: var(--font-size-responsive-md);
    line-height: var(--line-height-tight);
}

.language-name {
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
}

/* Screen reader only class */
.sr-only {
    @include sr-only;
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
        min-width: var(--min-touch-target);
        padding: var(--padding-small);
    }

    .language-name {
        font-size: var(--font-size-responsive-sm);
    }

    .language-option {
        padding: var(--padding-small);
    }
}

/* Unterstützung für Hover auf Touch-Geräten */
@media (hover: hover) {
    .current-language:hover,
    .language-option:hover {
        background-color: var(--surface-color-hover);
        color: var(--text-color);
    }
}
</style>
