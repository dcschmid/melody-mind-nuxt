<template>
  <div class="relative isolate">
    <!-- Hauptbutton mit optimiertem Tailwind-Klassenaufbau -->
    <button
      type="button"
      :id="buttonId"
      class="group flex items-center gap-2 w-auto py-small px-medium 
             bg-surface/80 border border-white/10 
             text-text font-medium rounded-lg shadow-sm
             hover:bg-surface-hover hover:text-highlight
             focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-highlight focus-visible:ring-offset-2
             transition-all duration-normal"
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
      
      <!-- Aktuelle Sprachflagge -->
      <span class="flex-shrink-0 w-5 h-5 rounded overflow-hidden shadow-sm">
        <img 
          :src="`/images/flags/${currentLocale}.svg`" 
          :alt="`${currentLocaleName} flag`"
          class="w-full h-full object-cover"
          width="20"
          height="20"
          aria-hidden="true"
        />
      </span>
      
      <!-- Aktuelle Sprache -->
      <span>{{ currentLocaleName }}</span>
      
      <!-- Dropdown-Pfeil mit verbesserter Animation -->
      <Icon 
        name="material-symbols:keyboard-arrow-down-rounded" 
        class="text-lg text-text/70 transition-transform duration-300 ease-in-out motion-reduce:transition-none" 
        :class="isOpen ? 'rotate-180 text-highlight' : ''"
        aria-hidden="true"
      />
    </button>

    <!-- Dropdown mit verbesserten Animationen, Schatten und Glaseffekt -->
    <div
      v-show="isOpen"
      :id="dropdownId"
      ref="dropdown"
      class="absolute left-0 top-[calc(100%+0.5rem)] z-menu-content 
             min-w-[200px] py-2 mt-1 overflow-hidden
             bg-surface/95 border border-white/10 rounded-lg
             shadow-xl backdrop-blur-sm backdrop-saturate-150
             transform origin-top-left transition-all duration-200
             motion-reduce:transform-none motion-reduce:transition-none"
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
      <!-- Subtile Trennlinie im Dropdown -->
      <div class="h-px w-full bg-gradient-to-r from-transparent via-white/10 to-transparent mb-2"></div>
      
      <!-- Verbesserte Sprachoptionen mit konsistenten Tailwind-Klassen -->
      <div class="max-h-[300px] overflow-y-auto overscroll-contain px-1">
        <template v-for="locale in availableLocales" :key="locale.code">
          <button
            :id="`language-option-${locale.code}`"
            class="flex items-center w-full gap-3 px-3 py-2 my-0.5
                   text-left text-text text-base
                   rounded-md transition-colors duration-200 
                   hover:bg-surface-hover hover:text-highlight
                   focus:outline-none focus-visible:bg-surface-hover focus-visible:text-highlight focus-visible:ring-2 
                   focus-visible:ring-inset focus-visible:ring-highlight/70"
            :class="{ 
              'bg-primary/10 font-semibold': locale.code === currentLocale
            }"
            role="option"
            :aria-selected="locale.code === currentLocale"
            @click="switchLanguage(locale.code)"
            @keydown.enter="switchLanguage(locale.code)"
            @keydown.space.prevent="switchLanguage(locale.code)"
          >
            <!-- Sprachflagge -->
            <div class="flex-shrink-0 w-5 h-5 rounded overflow-hidden shadow-sm">
              <img 
                :src="`/images/flags/${locale.code}.svg`" 
                :alt="`${locale.name} flag`" 
                class="w-full h-full object-cover"
                width="20"
                height="20"
                aria-hidden="true"
              />
            </div>
            
            <!-- Auswahlindikator -->
            <div class="flex-shrink-0 w-5 flex items-center justify-center">
              <Icon 
                v-if="locale.code === currentLocale" 
                name="material-symbols:check-small-rounded" 
                class="text-highlight text-lg"
                aria-hidden="true"
              />
            </div>
            
            <!-- Sprachname -->
            <span>{{ locale.name }}</span>
            
            <!-- Screen reader text -->
            <span v-if="locale.code === currentLocale" class="sr-only">
              {{ $t('accessibility.currentlySelected') }}
            </span>
          </button>
        </template>
      </div>
    </div>

    <!-- Optimiertes Klick-Outside-Element -->
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-0 bg-transparent" 
      @click="closeDropdown" 
      aria-hidden="true"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter, useRoute } from 'vue-router';

// Generiere eindeutige IDs für ARIA-Attribute
const uniqueId = Math.floor(Math.random() * 10000);
const buttonId = `language-selector-${uniqueId}`;
const dropdownId = `language-dropdown-${uniqueId}`;

// Dropdown-Status
const isOpen = ref(false);
const dropdown = ref(null);
const activeItemId = ref('');

// I18n und Router Setup
const { locale, locales, setLocale } = useI18n();
const router = useRouter();
const route = useRoute();

// Aktueller Locale und verfügbare Locales
const currentLocale = computed(() => locale.value);
const availableLocales = computed(() => locales.value);
const currentLocaleName = computed(() => {
  const found = availableLocales.value.find(l => l.code === currentLocale.value);
  return found ? found.name : '';
});

// Dropdown öffnen/schließen
function toggleDropdown() {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    setActiveItem(currentLocale.value);
    // Den Fokus erst beim nächsten Tick auf das Dropdown setzen
    setTimeout(() => {
      dropdown.value?.focus();
    }, 10);
  }
}

// Dropdown öffnen und ersten Eintrag fokussieren
function openAndFocus() {
  if (!isOpen.value) {
    isOpen.value = true;
    setTimeout(() => {
      navigateToFirst();
    }, 10);
  }
}

// Dropdown öffnen und letzten Eintrag fokussieren
function openAndFocusLast() {
  if (!isOpen.value) {
    isOpen.value = true;
    setTimeout(() => {
      navigateToLast();
    }, 10);
  }
}

// Dropdown schließen
function closeDropdown() {
  isOpen.value = false;
}

// Blur-Handling
function handleBlur(event) {
  // Nur schließen, wenn der Fokus nicht innerhalb des Dropdowns oder Button bleibt
  if (!event.currentTarget.contains(event.relatedTarget)) {
    closeDropdown();
  }
}

// Aktiven Eintrag setzen
function setActiveItem(localeCode) {
  activeItemId.value = `language-option-${localeCode}`;
  // Element fokussieren
  document.getElementById(activeItemId.value)?.focus();
}

// Keyboard-Navigation: Nach oben
function navigateUp() {
  const options = [...availableLocales.value];
  const currentIndex = options.findIndex(l => l.code === activeItemId.value.replace('language-option-', ''));
  const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
  setActiveItem(options[prevIndex].code);
}

// Keyboard-Navigation: Nach unten
function navigateDown() {
  const options = [...availableLocales.value];
  const currentIndex = options.findIndex(l => l.code === activeItemId.value.replace('language-option-', ''));
  const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
  setActiveItem(options[nextIndex].code);
}

// Zum ersten Element navigieren
function navigateToFirst() {
  setActiveItem(availableLocales.value[0].code);
}

// Zum letzten Element navigieren
function navigateToLast() {
  setActiveItem(availableLocales.value[availableLocales.value.length - 1].code);
}

// Sprache wechseln
async function switchLanguage(localeCode) {
  if (localeCode === currentLocale.value) {
    closeDropdown();
    return;
  }
  
  try {
    // Locale ändern
    await setLocale(localeCode);
    
    // URL-Pfad entsprechend anpassen
    const { fullPath } = route;
    const newPath = fullPath.replace(`/${currentLocale.value}/`, `/${localeCode}/`);
    
    // Nur navigieren, wenn sich der Pfad geändert hat
    if (newPath !== fullPath) {
      await router.push(newPath);
    }
    
    closeDropdown();
  } catch (error) {
    console.error('Failed to switch language:', error);
  }
}

// Keyboard-Event-Listener für bessere Zugänglichkeit
function handleKeydown(event) {
  if (!isOpen.value) return;
  
  // Tab oder Escape schließt das Dropdown
  if (event.key === 'Tab' || event.key === 'Escape') {
    closeDropdown();
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style>
/* 
* Dieses Stylesheet ist absichtlich leer, da alle Stile
* direkt über Tailwind-Klassen implementiert werden.
* Für globale Utilities nutzen wir die assets/css/tailwind.css.
*/
</style>
