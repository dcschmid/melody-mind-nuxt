<template>
  <button 
    :class="[
      'btn',
      variant === 'primary' ? 'btn-primary' : '',
      variant === 'secondary' ? 'btn-secondary' : '',
      variant === 'icon' ? 'btn-icon' : '',
      fullWidth ? 'w-full' : '',
      className
    ]"
    :disabled="disabled"
    :aria-disabled="disabled"
    :type="type"
    v-bind="$attrs"
  >
    <!-- Für Icon-Buttons: Wenn kein Text, aber aria-label vorhanden ist -->
    <span v-if="hideLabel && $attrs['aria-label']" class="sr-only">{{ $attrs['aria-label'] }}</span>
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'icon'].includes(value)
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  hideLabel: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'button',
    validator: (value: string) => ['button', 'submit', 'reset'].includes(value)
  }
})
</script>
