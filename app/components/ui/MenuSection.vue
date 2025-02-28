<template>
  <section 
    :aria-labelledby="headingId" 
    class="bg-gradient-to-br from-surface/90 to-surface-light/90 backdrop-blur-sm p-6 rounded-xl border border-white/5 shadow-lg transition-all hover:shadow-xl group"
  >
    <h2 
      v-if="title" 
      :id="headingId" 
      class="flex items-center gap-2 mb-4 relative"
    >
      <!-- Accent line -->
      <span class="inline-block w-1.5 h-6 bg-gradient-to-b from-primary to-primary-light rounded-full mr-1 shadow-glow-sm"></span>
      
      <span class="text-white font-bold uppercase text-sm tracking-wider">
        {{ title }}
      </span>
      
      <!-- Subtle line -->
      <span class="flex-grow h-px bg-gradient-to-r from-white/20 to-transparent ml-2"></span>
    </h2>
    
    <div 
      class="space-y-2.5 transition-all"
      :role="list ? 'list' : undefined"
      :aria-label="listLabel || title"
    >
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  // Indicates if the section contains a list
  list: {
    type: Boolean,
    default: true
  },
  // Optional custom label for the list
  listLabel: {
    type: String,
    default: ''
  }
});

// Generate a unique ID for the heading
const headingId = computed(() => {
  return props.title ? `section-heading-${props.title.toLowerCase().replace(/\s+/g, '-')}` : '';
});
</script>

<style scoped>
.shadow-glow-sm {
  box-shadow: 0 0 10px rgba(var(--primary-color-rgb), 0.5);
}
</style>
