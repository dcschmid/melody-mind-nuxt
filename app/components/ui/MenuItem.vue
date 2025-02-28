<template>
  <component
    :is="to ? NuxtLink : tag"
    :to="to"
    :href="href"
    :target="external ? '_blank' : undefined"
    :rel="external ? 'noopener noreferrer' : undefined"
    :aria-label="ariaLabel"
    :role="role || (list ? 'listitem' : undefined)"
    class="menu-item-modern group"
  >
    <!-- Icon Container mit Hintergrundeffekt -->
    <div v-if="icon" class="relative flex-shrink-0">
      <!-- Subtiler Hintergrund-Kreis -->
      <div class="absolute inset-0 rounded-full bg-primary/10 transform scale-0 group-hover:scale-110 transition-all duration-300 -z-10"></div>
      
      <Icon 
        :name="icon" 
        size="28" 
        class="text-primary group-hover:text-highlight transition-all duration-300 relative z-10"
        aria-hidden="true"
      />
    </div>
    
    <!-- Text mit eigener Transition -->
    <div class="flex-grow transition-all duration-300">
      <slot />
    </div>
    
    <!-- Pfeil-Icon rechts, wird bei Hover sichtbar -->
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 20 20" 
      fill="currentColor" 
      class="w-5 h-5 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300 text-highlight"
      aria-hidden="true"
    >
      <path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
    </svg>
    
    <!-- Für externe Links: Screen Reader Text -->
    <span v-if="external" class="sr-only">{{ externalLinkText }}</span>
  </component>
</template>

<script setup lang="ts">
import { NuxtLink } from '#components';
  
const props = defineProps({
  icon: {
    type: String,
    default: ''
  },
  to: {
    type: [String, Object],
    default: null
  },
  href: {
    type: String,
    default: null
  },
  external: {
    type: Boolean,
    default: false
  },
  tag: {
    type: String,
    default: 'a'
  },
  list: {
    type: Boolean,
    default: true
  },
  role: {
    type: String,
    default: ''
  },
  ariaLabel: {
    type: String,
    default: ''
  },
  externalLinkText: {
    type: String,
    default: '(öffnet in neuem Tab)'
  }
});
</script>

<style lang="scss" scoped>
.menu-item-modern {
  @apply flex items-center gap-4 py-3 px-4 rounded-lg bg-surface/60 backdrop-blur-sm text-text;
  @apply font-medium w-full no-underline border border-white/5 transition-all duration-300;
  @apply relative overflow-hidden min-h-[56px];
  
  /* Hover/Focus Styles */
  @apply hover:bg-surface-hover hover:border-primary-light hover:pl-5 hover:pr-3;
  @apply focus-visible:outline focus-visible:outline-focus focus-visible:outline-offset-focus;
  
  /* Shine Effect */
  &::before {
    content: '';
    @apply absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0;
    @apply translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000;
  }
  
  /* Ensure visual focus indication meets AAA standards */
  &:focus:not(:focus-visible) {
    outline: none;
  }
  
  /* Shadow Effect */
  @apply shadow-sm hover:shadow-md;
}
</style>
