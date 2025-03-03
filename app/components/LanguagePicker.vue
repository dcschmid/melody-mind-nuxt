<template>
  <div class="relative isolate">
    <!-- Hauptbutton mit modernem Tailwind v4 Design -->
    <button
      :id="buttonId"
      type="button"
      class="group flex min-h-[44px] w-auto items-center gap-3 rounded-lg bg-[rgba(var(--surface-color-rgb),0.9)] px-4 py-3 font-medium text-[rgb(var(--text-color-rgb))] shadow-sm hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:text-[rgb(var(--highlight-color-rgb))] hover:shadow-md focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-all motion-safe:duration-300 print:border-black print:bg-white print:text-black print:shadow-none"
      :aria-expanded="isOpen"
      aria-haspopup="listbox"
      :aria-controls="dropdownId"
      :aria-label="$t('accessibility.languageSelector')"
      @click="toggleDropdown"
      @keydown.down.prevent="openAndFocus"
      @keydown.up.prevent="openAndFocusLast"
      @keydown.esc="closeDropdown"
    >
      <span class="sr-only">{{ $t('accessibility.currentLanguage') }}</span>

      <!-- Aktuelle Sprachflagge mit verbessertem Kontrast und Größe für AAA-Konformität -->
      <span
        class="h-6 w-6 flex-shrink-0 overflow-hidden rounded-full border border-[rgba(255,255,255,0.2)] shadow-md group-hover:border-[rgba(var(--primary-light-color-rgb),0.3)] motion-safe:transition-all motion-safe:duration-300 print:border-black print:shadow-none"
      >
        <img
          :src="`/images/flags/${currentLocale}.svg`"
          :alt="`${currentLocaleName} flag`"
          class="h-full w-full object-cover"
          width="24"
          height="24"
          aria-hidden="true"
          loading="lazy"
        />
      </span>

      <!-- Aktuelle Sprache mit verbesserter Lesbarkeit -->
      <span class="text-base font-medium">{{ currentLocaleName }}</span>

      <!-- Dropdown-Pfeil mit verbesserter Animation und Kontrast -->
      <Icon
        name="material-symbols:keyboard-arrow-down-rounded"
        class="text-xl text-[rgba(var(--text-color-rgb),0.8)] group-hover:text-[rgb(var(--highlight-color-rgb))] motion-safe:transition-transform motion-safe:duration-300 motion-safe:ease-in-out print:text-black"
        :class="isOpen ? 'rotate-180 text-[rgb(var(--highlight-color-rgb))]' : ''"
        aria-hidden="true"
      />
    </button>

    <!-- Dropdown mit verbesserten Animationen, Schatten und Glaseffekt für WCAG AAA -->
    <div
      v-show="isOpen"
      :id="dropdownId"
      ref="dropdown"
      class="absolute top-[calc(100%+0.75rem)] left-0 mt-1 min-w-[220px] origin-top-left overflow-hidden rounded-lg border border-[rgba(var(--primary-light-color-rgb),0.2)] bg-[rgba(var(--surface-color-rgb),0.95)] py-3 shadow-md backdrop-blur-sm motion-safe:transform motion-safe:transition-all motion-safe:duration-300 print:border-black print:bg-white print:shadow-none"
      role="listbox"
      :aria-labelledby="buttonId"
      :aria-activedescendant="activeItemId"
      tabindex="-1"
      @blur="handleBlur"
      @keydown.esc="closeDropdown"
      @keydown.up.prevent="navigateUp"
      @keydown.down.prevent="navigateDown"
      @keydown.home.prevent="navigateToFirst"
      @keydown.end.prevent="navigateToLast"
    >
      <!-- Subtile Trennlinie im Dropdown mit verbessertem Kontrast -->
      <div
        class="mb-3 h-px w-full bg-gradient-to-r from-transparent via-[rgba(var(--primary-light-color-rgb),0.2)] to-transparent print:bg-black"
      />

      <!-- Verbesserte Sprachoptionen mit konsistenten Tailwind v4 Klassen -->
      <div class="max-h-[350px] overflow-y-auto overscroll-contain px-2">
        <template v-for="locale in availableLocales" :key="locale.code">
          <button
            :id="`language-option-${locale.code}`"
            class="my-1 flex min-h-[44px] w-full items-center gap-3 rounded-md px-4 py-3 text-left text-base text-[rgb(var(--text-color-rgb))] hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:text-[rgb(var(--highlight-color-rgb))] focus-visible:bg-[rgb(var(--surface-hover-color-rgb))] focus-visible:text-[rgb(var(--highlight-color-rgb))] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[rgb(var(--focus-color-rgb))] motion-safe:transition-colors motion-safe:duration-300 print:border print:border-black print:text-black"
            :class="{
              'bg-[rgba(var(--primary-color-rgb),0.1)] font-semibold':
                locale.code === currentLocale,
            }"
            role="option"
            :aria-selected="locale.code === currentLocale"
            @click="switchLanguage(locale.code)"
            @keydown.enter="switchLanguage(locale.code)"
            @keydown.space.prevent="switchLanguage(locale.code)"
          >
            <!-- Sprachflagge mit verbessertem Kontrast und Größe für AAA-Konformität -->
            <div
              class="h-6 w-6 flex-shrink-0 overflow-hidden rounded-full border border-[rgba(255,255,255,0.2)] shadow-md print:border-black print:shadow-none"
            >
              <img
                :src="`/images/flags/${locale.code}.svg`"
                :alt="`${locale.name} flag`"
                class="h-full w-full object-cover"
                width="24"
                height="24"
                aria-hidden="true"
                loading="lazy"
              />
            </div>

            <!-- Sprachname mit verbesserter Lesbarkeit -->
            <span class="flex-grow">{{ locale.name }}</span>

            <!-- Ausgewählte Sprache Indikator mit verbessertem Kontrast -->
            <Icon
              v-if="locale.code === currentLocale"
              name="material-symbols:check-circle"
              class="ml-auto text-lg text-[rgb(var(--highlight-color-rgb))] print:text-black"
              aria-hidden="true"
            />
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

const { locale, locales } = useI18n()
const router = useRouter()
const route = useRoute()
const isOpen = ref(false)
const dropdown = ref<HTMLElement | null>(null)
const activeItemId = ref('')

// Eindeutige IDs für ARIA
const buttonId = `language-picker-${Math.random().toString(36).substring(2, 9)}`
const dropdownId = `language-dropdown-${Math.random().toString(36).substring(2, 9)}`

// Verfügbare Sprachen
const availableLocales = computed(() => {
  return locales.value.map((l) => {
    if (typeof l === 'string') {
      return { code: l, name: l }
    }
    return l
  })
})

// Aktuelle Sprache
const currentLocale = computed(() => locale.value)
const currentLocaleName = computed(() => {
  const current = availableLocales.value.find((l) => l.code === currentLocale.value)
  return current ? current.name : currentLocale.value
})

// Dropdown öffnen/schließen
function toggleDropdown() {
  isOpen.value = !isOpen.value

  if (isOpen.value) {
    // Focus auf das Dropdown setzen
    setTimeout(() => {
      dropdown.value?.focus()
    }, 10)
  }
}

// Dropdown öffnen und ersten Eintrag fokussieren
function openAndFocus() {
  if (!isOpen.value) {
    isOpen.value = true
    setTimeout(() => {
      navigateToFirst()
    }, 10)
  }
}

// Dropdown öffnen und letzten Eintrag fokussieren
function openAndFocusLast() {
  if (!isOpen.value) {
    isOpen.value = true
    setTimeout(() => {
      navigateToLast()
    }, 10)
  }
}

// Dropdown schließen
function closeDropdown() {
  isOpen.value = false
}

// Blur-Handling
function handleBlur(event: FocusEvent) {
  // Prüfen, ob der Fokus innerhalb des Dropdowns bleibt
  const currentTarget = event.currentTarget as Node
  if (currentTarget && !currentTarget.contains(event.relatedTarget as Node)) {
    closeDropdown()
  }
}

// Aktiven Eintrag setzen
function setActiveItem(localeCode: string) {
  activeItemId.value = `language-option-${localeCode}`
  document.getElementById(activeItemId.value)?.focus()
}

// Keyboard-Navigation: Nach oben
function navigateUp() {
  const currentIndex = availableLocales.value.findIndex(
    (l) => l.code === activeItemId.value.replace('language-option-', '')
  )
  if (currentIndex === -1) {
    // Falls kein aktives Element gefunden wird, zum ersten Element navigieren
    setActiveItem(availableLocales.value[0]?.code || '')
    return
  }
  const prevIndex = currentIndex > 0 ? currentIndex - 1 : availableLocales.value.length - 1
  setActiveItem(availableLocales.value[prevIndex]?.code || '')
}

// Keyboard-Navigation: Nach unten
function navigateDown() {
  const currentIndex = availableLocales.value.findIndex(
    (l) => l.code === activeItemId.value.replace('language-option-', '')
  )
  if (currentIndex === -1) {
    // Falls kein aktives Element gefunden wird, zum ersten Element navigieren
    setActiveItem(availableLocales.value[0]?.code || '')
    return
  }
  const nextIndex = currentIndex < availableLocales.value.length - 1 ? currentIndex + 1 : 0
  setActiveItem(availableLocales.value[nextIndex]?.code || '')
}

// Zum ersten Element navigieren
function navigateToFirst() {
  setActiveItem(availableLocales.value[0]?.code || '')
}

// Zum letzten Element navigieren
function navigateToLast() {
  setActiveItem(availableLocales.value[availableLocales.value.length - 1]?.code || '')
}

// Sprache wechseln
function switchLanguage(localeCode: string) {
  if (localeCode === currentLocale.value) {
    closeDropdown()
    return
  }

  // Prüfen, ob der Sprachcode gültig ist
  if (availableLocales.value.some((l) => l.code === localeCode)) {
    // Sprache wechseln
    locale.value = localeCode as typeof locale.value

    // Dropdown schließen
    closeDropdown()

    // Speichern der Sprachpräferenz
    try {
      localStorage.setItem('user-locale', localeCode)
    } catch (e) {
      console.error('Could not save locale preference', e)
    }

    // Auf die lokalisierte URL weiterleiten mit Hard Reload
    const { fullPath } = route
    const newPath = fullPath.replace(/^\/[^\/]+/, `/${localeCode}`)

    // Nur navigieren, wenn sich der Pfad tatsächlich geändert hat
    if (newPath !== fullPath) {
      // Hard Reload durchführen, indem wir window.location verwenden
      window.location.href = newPath
    } else {
      // Wenn sich der Pfad nicht geändert hat, trotzdem Hard Reload für die aktuelle Seite
      window.location.reload()
    }
  } else {
    console.error(`Invalid locale code: ${localeCode}`)
  }
}

// Keyboard-Event-Listener für bessere Zugänglichkeit
function handleKeydown(event: KeyboardEvent) {
  if (!isOpen.value) return

  // Dropdown schließen bei Escape oder Tab außerhalb
  if (
    event.key === 'Escape' ||
    (event.key === 'Tab' && !dropdown.value?.contains(event.target as Node))
  ) {
    closeDropdown()
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style lang="scss" scoped>
/* Verbesserte Zugänglichkeit für hohen Kontrast */
@media (prefers-contrast: more) {
  button[aria-haspopup='listbox'] {
    border: 3px solid white !important;
    background-color: black !important;
    color: white !important;
    outline: 2px solid white !important;
    outline-offset: 3px !important;
  }

  div[role='listbox'] {
    border: 3px solid white !important;
    background-color: black !important;
    color: white !important;
  }

  button[role='option'] {
    border: 2px solid rgba(255, 255, 255, 0.7) !important;
    margin: 4px 0 !important;
    border-radius: 6px !important;
  }

  button[role='option'][aria-selected='true'] {
    background-color: rgba(255, 255, 255, 0.3) !important;
    font-weight: bold !important;
  }

  button[role='option']:hover,
  button[role='option']:focus-visible {
    background-color: white !important;
    color: black !important;
  }
}

/* Druckoptimierung */
@media print {
  button[aria-haspopup='listbox'] {
    border: 1px solid black !important;
    background-color: white !important;
    color: black !important;
    box-shadow: none !important;
  }

  div[role='listbox'] {
    display: none !important;
  }
}
</style>
