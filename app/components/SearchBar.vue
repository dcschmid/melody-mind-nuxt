<template>
  <div class="relative mx-auto max-w-[var(--content-width)]" role="search" data-testid="search-bar" aria-labelledby="search-heading">
    <h2 id="search-heading" class="sr-only">
      {{ label || placeholder }}
    </h2>
    <label :for="id" class="sr-only">{{ label || placeholder }}</label>

    <div class="relative flex items-center">
      <Icon
        name="ic:baseline-search"
        size="24"
        class="pointer-events-none absolute left-3 text-[rgb(var(--text-secondary-color-rgb))] dark:text-[rgb(var(--text-secondary-dark-color-rgb,255,255,255))]"
        aria-hidden="true"
        focusable="false"
        data-testid="search-icon"
      />

      <input
        :id="id"
        ref="searchInput"
        :value="modelValue"
        type="search"
        class="w-full rounded-lg border-2 border-[rgb(var(--surface-light-color-rgb))] bg-[rgb(var(--surface-color-rgb))] px-4 py-3 pl-10 text-base leading-normal text-[rgb(var(--text-color-rgb))] placeholder:text-[rgb(var(--text-secondary-color-rgb))] placeholder:opacity-70 hover:border-[rgb(var(--primary-color-rgb))] focus-visible:border-[rgb(var(--focus-color-rgb))] focus-visible:outline-[3px] focus-visible:outline-[rgb(var(--focus-color-rgb))] focus-visible:outline-offset-2 motion-safe:transition-all motion-safe:duration-300 print:border-black print:bg-white print:text-black print:placeholder:text-gray-500 dark:bg-[rgb(var(--surface-dark-color-rgb,18,18,18))] dark:text-[rgb(var(--text-dark-color-rgb,255,255,255))] dark:border-[rgb(var(--surface-light-dark-color-rgb,48,48,48))]"
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
        class="absolute right-2 flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border-2 border-transparent bg-transparent text-[rgb(var(--text-secondary-color-rgb))] hover:bg-[rgb(var(--surface-light-color-rgb))] hover:text-[rgb(var(--text-color-rgb))] hover:scale-110 focus-visible:bg-[rgb(var(--surface-light-color-rgb))] focus-visible:text-[rgb(var(--text-color-rgb))] focus-visible:outline-[3px] focus-visible:outline-offset-4 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-all motion-safe:duration-300 print:text-black dark:hover:bg-[rgb(var(--surface-light-dark-color-rgb,48,48,48))] dark:text-[rgb(var(--text-secondary-dark-color-rgb,170,170,170))]"
        data-testid="clear-search"
        :aria-label="$t('common.clearSearch')"
        @click="clearSearch"
      >
        <Icon name="ic:baseline-close" size="20" aria-hidden="true" focusable="false" />
      </button>
    </div>

    <!-- Suggestions List -->
    <div
      v-if="showSuggestions && suggestions && suggestions.length > 0"
      :id="listboxId"
      class="absolute top-full right-0 left-0 z-50 mt-1 rounded-lg border-2 border-[rgb(var(--surface-light-color-rgb))] bg-[rgb(var(--surface-color-rgb))] py-1 shadow-lg print:hidden dark:bg-[rgb(var(--surface-dark-color-rgb,18,18,18))] dark:border-[rgb(var(--surface-light-dark-color-rgb,48,48,48))]"
      data-testid="search-suggestions"
      role="listbox"
      :aria-label="$t('common.searchSuggestions')"
    >
      <div
        v-for="(suggestion, index) in suggestions"
        :id="`${id}-suggestion-${suggestion.id || index}`"
        :key="suggestion.id || index"
        class="cursor-pointer px-4 py-3 text-[rgb(var(--text-color-rgb))] hover:bg-[rgb(var(--surface-light-color-rgb))] hover:text-[rgb(var(--highlight-color-rgb))] motion-safe:transition-all motion-safe:duration-200 dark:text-[rgb(var(--text-dark-color-rgb,255,255,255))] dark:hover:bg-[rgb(var(--surface-light-dark-color-rgb,48,48,48))]"
        :class="{ 'bg-[rgb(var(--surface-light-color-rgb))] font-semibold text-[rgb(var(--highlight-color-rgb))] dark:bg-[rgb(var(--surface-light-dark-color-rgb,48,48,48))]': index === activeIndex }"
        role="option"
        :aria-selected="index === activeIndex"
        @mousedown.prevent="selectSuggestion(suggestion)"
        @mouseover="activeIndex = index"
      >
        {{ suggestion.text }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface Props {
  /** ID für das Sucheingabefeld, wird für die Zugänglichkeit benötigt */
  id: string
  /** Der aktuelle Wert des Suchfelds (v-model) */
  modelValue: string
  /** Platzhaltertext, der angezeigt wird, wenn das Suchfeld leer ist */
  placeholder: string
  /** Optionales Label für das Suchfeld (für Screenreader) */
  label?: string
  /** Optionale ID eines Elements, das das Suchfeld beschreibt (für aria-describedby) */
  describedBy?: string
  /** Array von Vorschlägen, die angezeigt werden sollen */
  suggestions?: Array<{ id: string; text: string }>
}

const props = withDefaults(defineProps<Props>(), {
  id: 'search-input',
  suggestions: () => [],
  describedBy: undefined,
  label: undefined,
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

const activeDescendant = computed(() => {
  if (activeIndex.value >= 0 && props.suggestions.length > activeIndex.value) {
    const suggestion = props.suggestions[activeIndex.value]
    return `${props.id}-suggestion-${suggestion && suggestion.id ? suggestion.id : activeIndex.value}`
  }
  return undefined
})

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
      if (activeIndex.value >= 0 && activeIndex.value < props.suggestions.length) {
        const suggestion = props.suggestions[activeIndex.value]
        if (
          suggestion &&
          typeof suggestion === 'object' &&
          'id' in suggestion &&
          'text' in suggestion
        ) {
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

<style scoped>
/* High Contrast Mode */
@media (prefers-contrast: more) {
  input[type='search'] {
    border: 4px solid black !important;
    background-color: white !important;
    color: black !important;
    outline: 4px solid black !important;
    outline-offset: 6px !important;
    font-weight: 600 !important;
  }

  input[type='search']:focus-visible {
    outline: 4px solid black !important;
    outline-offset: 4px !important;
    border-color: black !important;
    text-decoration: underline !important;
    text-decoration-thickness: 2px !important;
  }

  button:focus-visible {
    outline: 4px solid black !important;
    outline-offset: 4px !important;
    background-color: white !important;
    color: black !important;
    text-decoration: underline !important;
    text-decoration-thickness: 2px !important;
  }

  div[role='listbox'] {
    border: 4px solid black !important;
    background-color: white !important;
    box-shadow: none !important;
    margin-top: 8px !important;
  }

  div[role='option'] {
    border-bottom: 2px solid rgba(0, 0, 0, 0.5) !important;
    color: black !important;
    padding: 0.75rem 1rem !important;
    font-weight: 600 !important;
  }

  div[role='option']:hover,
  div[role='option'][aria-selected='true'] {
    background-color: black !important;
    color: white !important;
    outline: 2px solid white !important;
  }
}

/* Print mode */
@media print {
  div[role='search'] {
    max-width: 100% !important;
    margin: 1rem 0 !important;
  }

  input[type='search'] {
    border: 1px solid black !important;
    background-color: white !important;
    color: black !important;
    box-shadow: none !important;
  }

  button {
    display: none !important;
  }
}

/* Mobile Anpassungen */
@media (max-width: 768px) {
  input[type='search'] {
    font-size: 1rem !important;
    padding: 0.625rem 0.875rem !important;
    padding-left: 2.5rem !important;
    min-height: 3rem !important; /* Verbesserte Touch-Ziel-Größe */
  }

  div[role='listbox'] {
    margin-top: 0.25rem !important;
  }

  div[role='option'] {
    padding: 0.75rem 1rem !important;
    min-height: 3rem !important; /* Verbesserte Touch-Ziel-Größe */
  }
}

/* Dark Mode Anpassungen */
@media (prefers-color-scheme: dark) {
  /* Styles werden über Tailwind-Klassen mit dark: Präfix gesteuert */
}
</style>
