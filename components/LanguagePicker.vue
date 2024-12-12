<script setup>
const { locale, locales, setLocale, t } = useI18n()
const isOpen = ref(false)

const availableLocales = computed(() => {
    return locales.value.filter(i => i.code !== locale.value)
})

const flagEmojiCache = new Map()

const getFlagEmoji = (countryCode) => {
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

const handleLocaleChange = async (localeCode) => {
    await setLocale(localeCode)
    isOpen.value = false
}

// Dropdown schließen wenn außerhalb geklickt wird
const closeDropdown = (e) => {
    if (!e.target.closest('.language-picker')) {
        isOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
    document.removeEventListener('click', closeDropdown)
})
</script>

<template>
    <div class="language-picker">
        <button class="current-language" @click="isOpen = !isOpen" :aria-expanded="isOpen">
            <span class="flag">{{ getFlagEmoji(locale.substring(0, 2)) }}</span>
            <span class="language-name">{{ t(`languages.${locale}`) }}</span>
            <Icon
                name="material-symbols:keyboard-arrow-down-rounded"
                size="24"
                class="dropdown-arrow"
                :class="{ 'is-open': isOpen }"
            />
        </button>

        <div v-show="isOpen" class="language-options">
            <button
                v-for="loc in availableLocales"
                :key="loc.code"
                class="language-option"
                @click="handleLocaleChange(loc.code)"
            >
                <span class="flag">{{ getFlagEmoji(loc.code.substring(0, 2)) }}</span>
                <span class="language-name">{{ t(`languages.${loc.code}`) }}</span>
            </button>
        </div>
    </div>
</template>

<style scoped lang="scss">
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
    border: 1px solid transparent;
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s var(--transition-bounce);
    min-width: 140px;

    &:hover {
        background-color: var(--secondary-color);
        border-color: var(--highlight-color);

        .dropdown-arrow {
            color: var(--highlight-color);
        }
    }

    &:focus-visible {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 2px var(--highlight-color);
    }
}

.dropdown-arrow {
    margin-left: auto;
    transition: all 0.3s var(--transition-bounce);
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
    border: 1px solid var(--secondary-color);
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    animation: slideDown 0.3s var(--transition-bounce);

    .language-option {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem 1rem;
        border: none;
        background: transparent;
        color: var(--text-color);
        font-size: 1rem;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s var(--transition-bounce);

        &:hover {
            background-color: var(--secondary-color);
            color: var(--highlight-color);
        }

        &:focus-visible {
            outline: none;
            background-color: var(--secondary-color);
            color: var(--highlight-color);
        }

        &:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
    }
}

.flag {
    font-size: 1.2rem;
    line-height: 1;
}

.language-name {
    font-weight: 500;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 768px) {
    .current-language {
        min-width: 120px;
        padding: 0.5rem 0.75rem;
    }

    .language-name {
        font-size: 0.9rem;
    }
}
</style>
