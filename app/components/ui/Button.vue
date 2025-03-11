<template>
  <component
    :is="as"
    :class="
      button({
        variant,
        size,
        fullWidth,
        disabled,
        class: className,
      })
    "
    :disabled="disabled"
    :aria-disabled="disabled"
    :type="as === 'button' ? type : undefined"
    :data-testid="$attrs['data-testid'] || 'button'"
    v-bind="$attrs"
  >
    <!-- Für Icon-Buttons: Wenn kein Text, aber aria-label vorhanden ist -->
    <span v-if="hideLabel && $attrs['aria-label']" class="sr-only">{{ $attrs['aria-label'] }}</span>
    <slot />
  </component>
</template>

<script setup lang="ts">
import { tv } from 'tailwind-variants'

// Button Varianten mit tailwind-variants
const button = tv({
  base: [
    // Base styles
    'inline-flex items-center justify-center gap-2 text-base',
    // Base sizes and spacing
    'min-h-[44px] min-w-[44px] px-4 py-4 mb6',
    // Common styles
    'rounded-lg focus-visible:ring-3 focus-visible:ring-[rgb(var(--focus-color-rgb))] focus-visible:ring-offset-4 focus-visible:outline-hidden',
    // Transitions
    'motion-safe:transition-all motion-safe:duration-300 motion-reduce:transition-none',
    // Cursor
    'cursor-pointer',
  ],
  variants: {
    // Varianten
    variant: {
      primary: [
        'bg-[rgb(var(--primary-color-rgb))] text-[rgb(var(--text-on-primary-color-rgb))] shadow-sm',
        'hover:bg-[rgb(var(--primary-dark-color-rgb))] hover:shadow-md',
        'active:bg-[rgb(var(--primary-darker-color-rgb))]',
        'focus-visible:bg-[rgb(var(--primary-dark-color-rgb))]',
      ],
      secondary: [
        'border border-[rgb(var(--border-color-rgb))] bg-[rgb(var(--surface-color-rgb))] text-[rgb(var(--text-color-rgb))]',
        'hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:border-[rgb(var(--primary-light-color-rgb))]',
        'active:bg-[rgb(var(--surface-active-color-rgb))]',
        'focus-visible:bg-[rgb(var(--surface-hover-color-rgb))]',
      ],
      outline: [
        'border border-[rgb(var(--border-color-rgb))] bg-transparent text-[rgb(var(--text-color-rgb))]',
        'hover:bg-[rgb(var(--surface-light-color-rgb))] hover:border-[rgb(var(--primary-color-rgb))]',
        'active:bg-[rgb(var(--surface-hover-color-rgb))]',
        'focus-visible:bg-[rgb(var(--surface-light-color-rgb))]',
      ],
      icon: [
        'rounded-full bg-transparent p-2 text-[rgb(var(--text-color-rgb))]',
        'hover:bg-[rgb(var(--surface-hover-color-rgb))] hover:text-[rgb(var(--primary-color-rgb))]',
        'active:bg-[rgb(var(--surface-active-color-rgb))]',
        'focus-visible:bg-[rgb(var(--surface-hover-color-rgb))] focus-visible:text-[rgb(var(--primary-color-rgb))]',
      ],
      text: [
        'bg-transparent p-2 text-[rgb(var(--text-color-rgb))] underline-offset-4',
        'hover:bg-[rgb(var(--surface-light-color-rgb))] hover:underline',
        'active:bg-[rgb(var(--surface-hover-color-rgb))]',
        'focus-visible:bg-[rgb(var(--surface-light-color-rgb))] focus-visible:underline',
      ],
    },
    // Größen
    size: {
      sm: 'min-h-[36px] px-3 py-1.5 text-sm',
      md: '', // Default, keine zusätzlichen Klassen nötig
      lg: 'min-h-[52px] px-6 py-3 text-lg',
    },
    // Weitere Optionen
    fullWidth: {
      true: 'w-full',
    },
    // Status
    disabled: {
      true: 'pointer-events-none cursor-not-allowed opacity-70 aria-disabled:true',
    },
  },
  defaultVariants: {
    variant: 'primary',
    size: 'md',
    fullWidth: false,
    disabled: false,
  },
})

defineProps({
  variant: {
    type: String as () => 'primary' | 'secondary' | 'outline' | 'icon' | 'text',
    default: 'primary',
    validator: (value: string) =>
      ['primary', 'secondary', 'outline', 'icon', 'text'].includes(value),
  },
  size: {
    type: String as () => 'sm' | 'md' | 'lg',
    default: 'md',
    validator: (value: string) => ['sm', 'md', 'lg'].includes(value),
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
  className: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  hideLabel: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String as () => 'button' | 'submit' | 'reset',
    default: 'button',
    validator: (value: string) => ['button', 'submit', 'reset'].includes(value),
  },
  as: {
    type: String,
    default: 'button',
    validator: (value: string) => ['button', 'a', 'div', 'span'].includes(value),
  },
})
</script>

<style scoped>
/* High Contrast Mode for WCAG AAA */
@media (prefers-contrast: more) {
  :where(button, a) {
    border: 3px solid currentColor !important;
    background-color: black !important;
    color: white !important;
    text-decoration: underline !important;
    outline: 2px solid white !important;
    outline-offset: 3px !important;
  }

  :where(button, a):focus-visible {
    outline-width: 4px !important;
    outline-style: solid !important;
    outline-color: white !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5) !important;
  }
}

/* Print optimization */
@media print {
  :where(button, a) {
    border: 1px solid black !important;
    background-color: transparent !important;
    color: black !important;
    text-decoration: none !important;
    box-shadow: none !important;
  }
}
</style>
