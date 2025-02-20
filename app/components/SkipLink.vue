<template>
  <a href="#main-content" 
     class="skip-link" 
     @focus="onFocus" 
     @blur="onBlur"
     @click.prevent="handleSkip"
     @keydown.enter="handleSkip"
     role="link"
     :aria-hidden="!isVisible">
    {{ t('accessibility.skipToMain') }}
  </a>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const { t } = useI18n()
const isVisible = ref(false)

const onFocus = () => isVisible.value = true
const onBlur = () => isVisible.value = false

const handleSkip = (event: Event) => {
  event.preventDefault()
  const mainContent = document.getElementById('main-content')
  
  if (mainContent) {
    // Stelle sicher, dass das Element fokussierbar ist
    if (!mainContent.hasAttribute('tabindex')) {
      mainContent.setAttribute('tabindex', '-1')
    }
    
    // Scrolle zum Element
    mainContent.scrollIntoView({ behavior: 'smooth', block: 'start' })
    
    // Setze den Fokus
    mainContent.focus({ preventScroll: true })
    
    // Optional: Entferne tabindex nach dem Fokussieren
    setTimeout(() => {
      mainContent.removeAttribute('tabindex')
    }, 100)
  }
}
</script>

<style scoped lang="scss">
.skip-link {
  position: fixed;
  top: var(--padding-large);
  left: -9999px;
  z-index: var(--z-index-skip-link, 9999);
  min-width: 200px;
  min-height: 44px;
  padding: var(--padding-large) var(--padding-xlarge);
  background-color: var(--surface-color);
  color: var(--text-color);
  text-decoration: none;
  font-size: var(--font-size-responsive-md);
  font-weight: var(--font-weight-bold);
  line-height: 1.5;
  border: 3px solid var(--highlight-color);
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s var(--transition-bounce);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;

  // Verbesserter Fokus-Zustand
  &:focus {
    left: 50%;
    transform: translateX(-50%);
    outline: 3px solid var(--focus-outline-color, var(--highlight-color));
    outline-offset: 4px;
    background-color: var(--highlight-color);
    color: var(--surface-color);
    text-decoration: underline;
  }

  // Hover-Zustand
  &:hover {
    background-color: var(--highlight-color);
    color: var(--surface-color);
    text-decoration: underline;
    cursor: pointer;
  }

  // Active-Zustand
  &:active {
    transform: translateX(-50%) translateY(2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  // High Contrast Mode Unterstützung
  @media (forced-colors: active) {
    border: 3px solid CanvasText;
    &:focus {
      outline: 3px solid ButtonText;
    }
  }

  // Reduced Motion
  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
}
</style>
