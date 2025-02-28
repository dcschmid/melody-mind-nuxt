<template>
  <Button 
    variant="icon"
    :class="[
      'group relative w-touch h-touch flex flex-col justify-center items-center rounded p-2 transition-colors duration-normal',
      isActive ? 'bg-surface-hover' : 'bg-surface hover:bg-surface-hover',
      'border border-white/10'
    ]"
    v-bind="$attrs"
  >
    <!-- Visuell versteckter Text für Screenreader -->
    <span class="sr-only">{{ isActive ? closeLabel : openLabel }}</span>
    
    <!-- Hamburger-Linien -->
    <span 
      aria-hidden="true"
      class="block w-6 h-0.5 transition-all duration-normal origin-center"
      :class="[
        isActive ? 'rotate-45 translate-y-1.5 bg-highlight' : 'bg-text group-hover:bg-highlight mb-1.5'
      ]"
    ></span>
    <span 
      aria-hidden="true"
      class="block w-6 h-0.5 transition-all duration-normal"
      :class="[
        isActive ? 'opacity-0 scale-x-0' : 'bg-text group-hover:bg-highlight'
      ]"
    ></span>
    <span 
      aria-hidden="true"
      class="block w-6 h-0.5 transition-all duration-normal origin-center"
      :class="[
        isActive ? '-rotate-45 -translate-y-1.5 bg-highlight' : 'bg-text group-hover:bg-highlight mt-1.5'
      ]"
    ></span>
  </Button>
</template>

<script setup lang="ts">
import Button from './Button.vue';

defineProps({
  isActive: {
    type: Boolean,
    default: false
  },
  openLabel: {
    type: String,
    default: 'Menü öffnen'
  },
  closeLabel: {
    type: String,
    default: 'Menü schließen'
  }
});
</script>
