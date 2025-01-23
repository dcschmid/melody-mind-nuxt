<template>
    <div 
        class="search-wrapper"
        role="search"
    >
        <label 
            :for="id" 
            class="sr-only"
        >{{ label || placeholder }}</label>
        
        <div class="search-input-container">
            <Icon 
                name="ic:baseline-search" 
                size="24" 
                class="search-icon" 
                aria-hidden="true"
                focusable="false"
            />
            
            <input 
                :id="id"
                ref="searchInput"
                :value="modelValue"
                type="search"
                class="search-input"
                :placeholder="placeholder"
                :aria-label="label || placeholder"
                :aria-describedby="describedBy"
                :aria-expanded="showSuggestions"
                :aria-activedescendant="activeDescendant"
                :aria-controls="listboxId"
                role="combobox"
                autocomplete="off"
                @input="handleInput"
                @keydown="handleKeyDown"
                @focus="handleFocus"
                @blur="handleBlur"
            />

            <button 
                v-if="modelValue"
                type="button"
                class="clear-button"
                :aria-label="$t('common.clearSearch')"
                @click="clearSearch"
            >
                <Icon 
                    name="ic:baseline-close" 
                    size="20"
                    aria-hidden="true"
                    focusable="false"
                />
            </button>
        </div>

        <!-- Suchvorschläge -->
        <div 
            v-if="showSuggestions && suggestions.length > 0"
            :id="listboxId"
            class="suggestions-list"
            role="listbox"
            :aria-label="$t('common.searchSuggestions')"
        >
            <div
                v-for="(suggestion, index) in suggestions"
                :key="suggestion.id"
                :id="'suggestion-' + index"
                class="suggestion-item"
                role="option"
                :aria-selected="index === activeIndex"
                :class="{ 'is-active': index === activeIndex }"
                @click="selectSuggestion(suggestion)"
                @mouseenter="activeIndex = index"
            >
                {{ suggestion.text }}
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
    id: string
    modelValue: string
    placeholder: string
    label?: string
    describedBy?: string
    suggestions?: Array<{ id: string; text: string }>
}

const props = withDefaults(defineProps<Props>(), {
    id: 'search-input',
    suggestions: () => [],
    describedBy: undefined,
    label: undefined
})

const emit = defineEmits<{
    (e: 'update:modelValue', value: string): void
    (e: 'input', event: Event): void
    (e: 'select', suggestion: { id: string; text: string }): void
}>()

const searchInput = ref<HTMLInputElement | null>(null)
const showSuggestions = ref(false)
const activeIndex = ref(-1)
const listboxId = `${props.id}-listbox`

const activeDescendant = computed(() => 
    activeIndex.value >= 0 ? `suggestion-${activeIndex.value}` : undefined
)

const handleInput = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', target.value)
    emit('input', event)
    showSuggestions.value = true
    activeIndex.value = -1
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (!showSuggestions.value || !props.suggestions.length) return

    switch (event.key) {
        case 'ArrowDown':
            event.preventDefault()
            activeIndex.value = Math.min(activeIndex.value + 1, props.suggestions.length - 1)
            break
        case 'ArrowUp':
            event.preventDefault()
            activeIndex.value = Math.max(activeIndex.value - 1, -1)
            break
        case 'Enter':
            if (activeIndex.value >= 0) {
                const suggestion = props.suggestions[activeIndex.value]
                if (suggestion) {
                    event.preventDefault()
                    selectSuggestion(suggestion)
                }
            }
            break
        case 'Escape':
            showSuggestions.value = false
            activeIndex.value = -1
            break
        case 'Tab':
            showSuggestions.value = false
            break
    }
}

const handleFocus = () => {
    if (props.modelValue && props.suggestions.length) {
        showSuggestions.value = true
    }
}

const handleBlur = () => {
    // Verzögerung um Click-Events zu ermöglichen
    setTimeout(() => {
        showSuggestions.value = false
        activeIndex.value = -1
    }, 200)
}

const selectSuggestion = (suggestion: { id: string; text: string }) => {
    emit('update:modelValue', suggestion.text)
    emit('select', suggestion)
    showSuggestions.value = false
    activeIndex.value = -1
    searchInput.value?.focus()
}

const clearSearch = () => {
    emit('update:modelValue', '')
    searchInput.value?.focus()
    showSuggestions.value = false
    activeIndex.value = -1
}
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.search-wrapper {
    position: relative;
    max-width: min(600px, 90%);
    margin: 0 auto;
}

.search-input-container {
    position: relative;
    display: flex;
    align-items: center;
}

.search-icon {
    position: absolute;
    left: 1rem;
    color: var(--text-secondary);
    pointer-events: none;
}

.search-input {
    width: 100%;
    padding: 0.875rem 2.5rem;
    font-size: clamp(1rem, 1vw + 0.75rem, 1.125rem);
    line-height: 1.5;
    color: var(--text-color);
    background: var(--surface-color);
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    transition: all 0.2s ease;

    &::placeholder {
        color: var(--text-secondary);
        opacity: 0.8;
    }

    &:hover {
        border-color: var(--border-hover-color);
    }

    &:focus {
        outline: none;
        border-color: var(--focus-ring-color);
        box-shadow: 0 0 0 3px var(--focus-ring-color);
    }
}

.clear-button {
    position: absolute;
    right: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    color: var(--text-secondary);
    background: transparent;
    border: 2px solid transparent;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
        color: var(--text-color);
        background: var(--surface-hover-color);
    }

    &:focus-visible {
        outline: none;
        border-color: var(--focus-ring-color);
        box-shadow: 0 0 0 2px var(--focus-ring-color);
        color: var(--text-color);
        background: var(--surface-hover-color);
    }

    /* High Contrast Mode */
    @media (prefers-contrast: more) {
        &:focus-visible {
            outline: 3px solid var(--focus-ring-color);
            outline-offset: 2px;
            box-shadow: none;
        }
    }

    /* Reduzierte Bewegung */
    @media (prefers-reduced-motion: reduce) {
        transition: none;
    }
}

.suggestions-list {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 0.5rem;
    padding: 0.5rem 0;
    background: var(--surface-color);
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 100;
}

.suggestion-item {
    padding: 0.75rem 1rem;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover,
    &.is-active {
        background: var(--surface-hover-color);
    }
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

/* High Contrast Mode */
@media (prefers-contrast: more) {
    .search-input {
        border-width: 3px;
    }

    .suggestions-list {
        border-width: 3px;
        box-shadow: none;
    }

    .suggestion-item {
        &:hover,
        &.is-active {
            background: var(--surface-high-contrast);
            outline: 2px solid var(--focus-ring-color);
        }
    }
}

/* Reduzierte Bewegung */
@media (prefers-reduced-motion: reduce) {
    .search-input,
    .clear-button,
    .suggestion-item {
        transition: none;
    }
}

/* Mobile Anpassungen */
@media (max-width: 768px) {
    .search-input {
        font-size: 1rem;
        padding: 0.75rem 2.25rem;
    }

    .suggestions-list {
        margin-top: 0.25rem;
    }

    .suggestion-item {
        padding: 0.625rem 0.875rem;
    }
}

/* Unterstützung für Hover auf Touch-Geräten */
@media (hover: hover) {
    .search-input:hover {
        border-color: var(--border-hover-color);
    }

    .clear-button:hover {
        background: var(--surface-hover-color);
    }

    .suggestion-item:hover {
        background: var(--surface-hover-color);
    }
}
</style>
