<template>
  <header 
    role="banner" 
    class="fixed top-0 inset-x-0 h-header bg-surface/95 backdrop-blur-sm z-header border-b border-white/10"
  >
    <div class="container mx-auto px-medium h-full flex items-center justify-between">
      <!-- Logo/Branding -->
      <div class="flex items-center">
        <slot name="left" />
      </div>

      <!-- Navigation -->
      <nav :aria-label="navLabel" class="flex items-center">
        <slot name="right" />
      </nav>
    </div>
  </header>
  
  <!-- Spacer für den Header -->
  <div class="h-header" aria-hidden="true"></div>
</template>

<script setup lang="ts">
defineProps({
  navLabel: {
    type: String,
    default: 'Hauptnavigation'
  }
});
</script>
