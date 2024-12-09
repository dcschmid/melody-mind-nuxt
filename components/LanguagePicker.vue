<script setup>
const { locale, locales, setLocale, t } = useI18n()
const isOpen = ref(false)

const availableLocales = computed(() => {
    return locales.value.filter(i => i.code !== locale.value)
})

const getFlagEmoji = (countryCode) => {
    const code = countryCode.toUpperCase() === 'EN' ? 'GB' : countryCode.toUpperCase()
    const codePoints = code
        .split('')
        .map(char => 127397 + char.charCodeAt());
    return String.fromCodePoint(...codePoints);
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
        <div class="current-language" @click="isOpen = !isOpen">
            <span class="flag">{{ getFlagEmoji(locale.substring(0, 2)) }}</span>
            <span class="language-name">{{ t(`languages.${locale}`) }}</span>
            <span class="dropdown-arrow" :class="{ 'open': isOpen }">▼</span>
        </div>
        <div v-show="isOpen" class="language-options">
            <a v-for="loc in availableLocales" :key="loc.code" href="#" class="language-option"
                @click.prevent="handleLocaleChange(loc.code)">
                <span class="flag">{{ getFlagEmoji(loc.code.substring(0, 2)) }}</span>
                <span class="language-name">{{ t(`languages.${loc.code}`) }}</span>
            </a>
        </div>
    </div>
</template>

<style scoped>
.language-picker {
    position: relative;
    display: inline-block;
    margin: 1rem;
}

.current-language {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: var(--background-color);
    border: 2px solid var(--highlight-color);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 120px;
}

.dropdown-arrow {
    margin-left: auto;
    font-size: 0.8rem;
    transition: transform 0.3s ease;
}

.dropdown-arrow.open {
    transform: rotate(180deg);
}

.current-language:hover {
    background-color: var(--highlight-color);
    color: var(--button-text-color);
}

.language-options {
    position: absolute;
    top: calc(100% + 5px);
    left: 0;
    z-index: 1000;
    width: 100%;
    background-color: var(--background-color);
    border: 2px solid var(--highlight-color);
    border-radius: var(--border-radius);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.language-option {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    color: var(--text-color);
    text-decoration: none;
    transition: all 0.3s ease;
}

.language-option:not(:last-child) {
    border-bottom: 1px solid var(--highlight-color);
}

.language-option:hover {
    background-color: var(--highlight-color);
    color: var(--button-text-color);
}

.flag {
    font-size: 1.2rem;
}

.language-name {
    font-size: 0.9rem;
}
</style>
