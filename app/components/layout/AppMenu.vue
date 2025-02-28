<template>
  <div 
    id="menu" 
    class="fixed inset-0 w-full h-full backdrop-blur-overlay z-menu overflow-y-auto transition-all duration-normal ease-in-out bg-gradient-to-b from-black/80 to-black/90"
    :class="[
      isOpen ? 'opacity-100 visible' : 'opacity-0 invisible pointer-events-none',
      reducedMotion ? 'motion-reduce' : ''
    ]" 
    @keydown.esc="$emit('close')"
    tabindex="-1" 
    role="dialog" 
    aria-modal="true" 
    :aria-label="menuLabel" 
    ref="menuRef"
  >
    <!-- Animierter Hintergrund -->
    <div class="absolute inset-0 bg-gradient-to-tr from-primary/10 to-secondary/10 animate-gradient-slow"></div>
    
    <!-- Menü Container mit Glaseffekt -->
    <div 
      class="relative w-full max-w-3xl mx-auto my-[calc(var(--header-height)+1rem)] p-large shadow-2xl overflow-y-auto transform transition-all duration-normal"
      :class="[
        isOpen ? 'translate-y-0 scale-100 opacity-100' : 'translate-y-[-20px] scale-95 opacity-0',
        'backdrop-blur-md bg-black/40 border border-white/10 rounded-xl'
      ]"
    >
      <!-- Shine effect -->
      <div class="absolute inset-0 overflow-hidden rounded-xl pointer-events-none">
        <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
        <div class="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-transparent via-white/20 to-transparent"></div>
      </div>
    
      <!-- Verbesserter Close Button -->
      <button 
        class="absolute top-4 right-4 flex items-center justify-center w-12 h-12 bg-black/30 hover:bg-surface-hover text-white hover:text-highlight rounded-full shadow-lg border border-white/10 transition-all duration-normal"
        @click="$emit('close')" 
        :aria-label="closeLabel" 
        ref="closeButtonRef"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="fill-current">
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
        <span class="sr-only">{{ closeLabel }}</span>
      </button>
      
      <!-- Menü Inhalt mit verbesserten Abständen -->
      <div class="mt-8 space-y-8">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { useFocusTrap } from '@vueuse/integrations/useFocusTrap';
import { usePreferredReducedMotion } from '@vueuse/core';
import Button from '../ui/Button.vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  menuLabel: {
    type: String,
    default: 'Menü'
  },
  closeLabel: {
    type: String,
    default: 'Menü schließen'
  }
});

const emits = defineEmits(['close']);
const menuRef = ref<HTMLElement | null>(null);
const closeButtonRef = ref<HTMLElement | null>(null);
const reducedMotion = usePreferredReducedMotion();

const { activate, deactivate } = useFocusTrap(menuRef, {
  immediate: false,
  escapeDeactivates: true,
  allowOutsideClick: true,
  fallbackFocus: () => closeButtonRef.value as HTMLElement,
});

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    // Prevent scrolling of the background when menu is open
    document.body.classList.add('overflow-hidden');
    activate();
    setTimeout(() => {
      closeButtonRef.value?.focus();
    }, 50);
  } else {
    document.body.classList.remove('overflow-hidden');
    deactivate();
  }
});

onMounted(() => {
  if (props.isOpen) {
    document.body.classList.add('overflow-hidden');
    activate();
  }
});

onUnmounted(() => {
  document.body.classList.remove('overflow-hidden');
  deactivate();
});
</script>

<style scoped>
.motion-reduce {
  transition: none !important;
}
.motion-reduce * {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient-slow {
  animation: gradient-shift 15s ease infinite;
  background-size: 200% 200%;
}
</style>
