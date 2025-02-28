<template>
  <article 
    class="relative w-full transition-transform duration-normal rounded-[--border-radius] overflow-hidden group/card"
    :class="{ 'opacity-disabled cursor-not-allowed': !isPlayable, 'cursor-pointer': isPlayable }"
    :aria-disabled="!isPlayable"
  >
    <!-- Spielbare Kategorie mit Link -->
    <NuxtLink 
      v-if="isPlayable" 
      :to="categoryUrl" 
      class="block h-full text-inherit no-underline outline-none focus-visible:outline-none group/link"
      :aria-label="t('gameHome.playCategory', { category: headline })"
      :aria-describedby="`${cardId}-description`"
      @keydown.enter="$emit('select')" 
      @keydown.space.prevent="$emit('select')"
    >
      <!-- Das eigentliche Kartencontainer -->
      <div class="relative w-full h-full aspect-video rounded-[--border-radius] overflow-hidden bg-surface shadow transition-all duration-normal">
        <!-- Karten-Inhalt mit Bild und Titel -->
        <div class="w-full h-full">
          <UnLazyImage 
            :src="imageUrl" 
            :alt="t('gameHome.categoryAlt', { category: headline })" 
            loading="lazy"
            class="w-full h-full object-cover rounded-[--border-radius]"
            auto-sizes
            :thumbhash="thumbHash"
          />
          
          <h2 
            :id="`${cardId}-title`" 
            class="absolute inset-0 flex items-center justify-center m-0 text-md font-semibold text-text text-center leading-tight z-overlay w-full h-full bg-black/70 backdrop-blur-xs
                   group-focus-visible/link:bg-black/80 group-focus-visible/link:text-highlight"
          >
            {{ headline }}
          </h2>
        </div>
        
        <!-- Hover-Effekt-Überlagerung -->
        <div 
          class="absolute inset-0 bg-gradient-to-t from-primary/30 to-secondary/20 opacity-0 group-hover/link:opacity-100 transition-all duration-normal"
          aria-hidden="true"
        ></div>
      </div>
      
      <!-- Überlagerungen für Fokus-Zustand mit Tailwind -->
      <div class="absolute inset-0 z-10 pointer-events-none">
        <!-- Äußerer Fokus-Ring -->
        <div 
          class="absolute -inset-[2px] rounded-[calc(var(--border-radius)+2px)] border-4 border-transparent transition-all duration-normal
                 group-focus-visible/link:border-highlight motion-reduce:group-focus-visible/link:border-highlight"
        ></div>
        
        <!-- Innerer Schatten für Tiefeneffekt -->
        <div 
          class="absolute inset-0 rounded-[--border-radius] opacity-0 transition-all duration-normal
                 group-focus-visible/link:opacity-100 shadow-[0_0_20px_rgba(0,247,255,0.7)]"
        ></div>
        
        <!-- Eck-Akzente für zusätzliches visuelles Feedback -->
        <div class="absolute top-0 left-0 w-4 h-4 opacity-0 group-focus-visible/link:opacity-100 transition-all duration-normal">
          <div class="absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 border-highlight rounded-tl-lg"></div>
        </div>
        <div class="absolute top-0 right-0 w-4 h-4 opacity-0 group-focus-visible/link:opacity-100 transition-all duration-normal">
          <div class="absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 border-highlight rounded-tr-lg"></div>
        </div>
        <div class="absolute bottom-0 left-0 w-4 h-4 opacity-0 group-focus-visible/link:opacity-100 transition-all duration-normal">
          <div class="absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 border-highlight rounded-bl-lg"></div>
        </div>
        <div class="absolute bottom-0 right-0 w-4 h-4 opacity-0 group-focus-visible/link:opacity-100 transition-all duration-normal">
          <div class="absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 border-highlight rounded-br-lg"></div>
        </div>
      </div>
    </NuxtLink>

    <!-- Coming-Soon-Version mit ähnlichem Tailwind-Ansatz -->
    <div 
      v-else 
      class="relative w-full h-full aspect-video rounded-[--border-radius] overflow-hidden bg-surface shadow focus-visible:outline-highlight focus-visible:outline-4 focus-visible:outline-offset-4"
      :aria-label="t('gameHome.comingSoon', { category: headline })"
      :aria-describedby="`${cardId}-description`"
      role="article" 
      tabindex="0"
    >
      <div class="w-full h-full">
        <UnLazyImage 
          :src="imageUrl" 
          :alt="t('gameHome.categoryAlt', { category: headline })" 
          loading="lazy"
          class="w-full h-full object-cover rounded-[--border-radius]"
          auto-sizes
          :thumbhash="thumbHash"
        />
        
        <h2 
          :id="`${cardId}-title`" 
          class="absolute inset-0 flex items-center justify-center m-0 text-md md:text-xl font-semibold text-text text-center leading-tight z-overlay w-full h-full bg-black/70 backdrop-blur-xs"
        >
          {{ headline }}
        </h2>

        <!-- Coming Soon Badge -->
        <div 
          class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-primary text-white font-bold text-md px-medium py-small rounded-[--border-radius] shadow z-overlay"
          role="status"
          aria-live="polite"
        >
          {{ t('gameHome.comingSoonLabel') }}
        </div>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { useThumbHash } from '~/composables/useThumbHash'
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

const { t } = useI18n()
const { getThumbHash } = useThumbHash()

const props = defineProps({
  headline: {
    type: String,
    required: true
  },
  imageUrl: {
    type: String,
    required: true
  },
  categoryUrl: {
    type: String,
    required: true
  },
  introSubline: {
    type: String,
    required: true
  },
  isPlayable: {
    type: Boolean,
    default: true
  }
})

// ThumbHash für das Bild abrufen
const thumbHash = computed(() => props.imageUrl ? getThumbHash(props.imageUrl) : '')

// Generiere eine eindeutige ID für ARIA-Attribute
const cardId = computed(() => 
  `category-${props.headline.toLowerCase().replace(/\s+/g, '-')}`
)

defineEmits(['select'])
</script>

<style lang="scss" scoped>
/* Minimales CSS für das, was nicht in Tailwind abbildbar ist */
.opacity-disabled {
  opacity: var(--opacity-disabled);
}

/* Hoher Kontrast-Modus über CSS für WCAG AAA */
@media (prefers-contrast: more) {
  .group-focus-visible\/link\:border-highlight {
    border-color: white !important;
    outline: 2px solid black;
  }
  
  div[role="status"] {
    @apply bg-primary-dark text-white border-2 border-white;
  }
}

/* Diese Klasse fügt zusätzlich eine Animation hinzu für Bewegungstolerantere Nutzer */
@media (prefers-reduced-motion: no-preference) {
  .group-focus-visible\/link\:border-highlight {
    animation: focus-pulse 2s infinite alternate;
  }
  
  @keyframes focus-pulse {
    from { box-shadow: 0 0 0 0 rgba(var(--highlight-color-rgb), 0.4); }
    to { box-shadow: 0 0 0 8px rgba(var(--highlight-color-rgb), 0.7); }
  }
}
</style>
