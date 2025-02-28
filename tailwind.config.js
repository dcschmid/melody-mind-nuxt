/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./app.vue",
    "./app/**/*.{vue,js,ts}",
  ],
  theme: {
    extend: {
      colors: {
        // Primärfarben mit RGB für Opacity Support
        'primary': {
          DEFAULT: 'rgb(var(--primary-color-rgb))',
          dark: 'var(--primary-color-dark)',
          light: 'var(--primary-color-light)',
        },
        
        // Sekundärfarben mit RGB
        'secondary': {
          DEFAULT: 'rgb(var(--secondary-color-rgb))',
          dark: 'var(--secondary-color-dark)',
          light: 'var(--secondary-color-light)',
        },
        
        // System Colors
        'highlight': 'var(--highlight-color)',
        'highlight-dark': 'var(--highlight-color-dark)',
        
        // Surface Colors optimiert für Opacity-Modifier
        'surface': {
          DEFAULT: 'rgb(var(--surface-color-rgb))',
          light: 'rgb(var(--surface-color-light-rgb))',
          hover: 'rgb(var(--surface-color-hover-rgb))',
        },
        
        // Text Colors mit RGB
        'text': {
          DEFAULT: 'rgb(var(--text-color-rgb))',
          secondary: 'var(--text-secondary)',
          dark: 'var(--text-color-dark)',
        },
        
        // Weitere Farben (ohne RGB, da selten mit Opacity verwendet)
        'error': {
          DEFAULT: 'var(--error-color)',
          dark: 'var(--error-color-dark)',
        },
        'success': {
          DEFAULT: 'var(--success-color)',
          dark: 'var(--success-color-dark)',
        },
        'gold': {
          DEFAULT: 'var(--color-gold)',
          dark: 'var(--color-gold-dark)',
        },
        'silver': 'var(--color-silver)',
        'bronze': 'var(--color-bronze)',
      },
      
      fontSize: {
        'base': 'var(--font-size-base)',
        'sm': 'var(--font-size-responsive-sm)',
        'md': 'var(--font-size-responsive-md)',
        'lg': 'var(--font-size-responsive-lg)',
        'xl': 'var(--font-size-responsive-xl)',
        '2xl': 'var(--font-size-responsive-2xl)',
        '3xl': 'var(--font-size-responsive-3xl)',
      },
      
      lineHeight: {
        'tight': 'var(--line-height-tight)',
        'normal': 'var(--line-height-normal)',
        'relaxed': 'var(--line-height-relaxed)',
      },
      
      fontWeight: {
        'normal': 'var(--font-weight-normal)',
        'medium': 'var(--font-weight-medium)',
        'semibold': 'var(--font-weight-semibold)',
        'bold': 'var(--font-weight-bold)',
      },
      
      fontFamily: {
        'sans': ['var(--font-family)'],
      },
      
      padding: {
        'small': 'var(--padding-small)',
        'medium': 'var(--padding-medium)',
        'large': 'var(--padding-large)',
      },
      
      gap: {
        'small': 'var(--padding-small)',
        'medium': 'var(--padding-medium)',
        'large': 'var(--padding-large)',
      },
      
      margin: {
        'small': 'var(--padding-small)',
        'medium': 'var(--padding-medium)',
        'large': 'var(--padding-large)',
      },
      
      borderRadius: {
        'DEFAULT': 'var(--border-radius)',
        'accessibility': '0.25rem',  // Mindestgröße für Touch-Ziel-Ränder
      },
      
      boxShadow: {
        'DEFAULT': 'var(--box-shadow)',
        'hover': 'var(--box-shadow-hover)',
        'glow-sm': '0 0 10px rgba(var(--primary-color-rgb, 0, 0, 0), 0.5)',
        'glow-md': '0 0 15px rgba(var(--primary-color-rgb, 0, 0, 0), 0.6)',
        'inner-top': 'inset 0 1px 2px 0 rgba(255, 255, 255, 0.1)',
        'focus': '0 0 0 4px rgba(var(--highlight-color-rgb), 0.8), 0 0 0 2px rgba(0, 0, 0, 0.6), 0 0 20px rgba(var(--highlight-color-rgb), 0.4)',
        'focus-contrast': '0 0 0 4px white, 0 0 0 6px black',
        'focus-subtle': '0 0 0 2px rgba(var(--highlight-color-rgb), 0.5)',
        'focus-glow': '0 0 15px 5px rgba(var(--highlight-color-rgb), 0.7)',
      },
      
      transitionProperty: {
        'DEFAULT': 'all',
      },
      
      transitionDuration: {
        'normal': 'var(--transition-speed)',
        'fast': '150ms',
        'slow': '500ms',
      },
      
      transitionTimingFunction: {
        'bounce': 'var(--transition-bounce)',
      },
      
      maxWidth: {
        'content': 'var(--content-width)',
        'prose': 'var(--max-line-length)',
      },
      
      height: {
        'header': 'var(--header-height)',
      },
      
      minHeight: {
        'touch': 'var(--min-touch-target)',
      },
      
      outlineWidth: {
        'focus': 'var(--focus-outline-width)',
      },
      
      outlineColor: {
        'focus': 'var(--focus-outline-color)',
      },
      
      outlineOffset: {
        'focus': 'var(--focus-outline-offset)',
      },
      
      blur: {
        'overlay': 'var(--blur-strength)',
      },
      
      opacity: {
        'disabled': 'var(--opacity-disabled)',
      },
      
      zIndex: {
        'menu': 'var(--z-index-menu)',
        'header': 'var(--z-index-header)',
        'overlay': 'var(--z-index-overlay)',
        'menu-content': '100', // für z-[calc(var(--z-index-menu)+1)]
        'foreground': '200',
        'top': '999',
        'above-overlay': 'calc(var(--z-index-overlay) + 10)',
      },
      
      containers: {
        'card': '400px',
        'section': '768px',
      },
      
      // Neue Animationen
      animation: {
        'gradient-slow': 'gradient-shift 15s ease infinite',
        'pulse-slow': 'pulse 8s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shine': 'shine 2s linear infinite',
        'pulse-focus': 'gentle-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gentle-pulse': 'gentle-pulse 2s infinite',
      },
      keyframes: {
        'gradient-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'shine': {
          'from': { backgroundPosition: '200% 0' },
          'to': { backgroundPosition: '-200% 0' },
        },
        'gentle-pulse': {
          '0%, 100%': { 
            boxShadow: '0 0 0 4px rgba(var(--highlight-color-rgb), 0.5)'
          },
          '50%': { 
            boxShadow: '0 0 0 6px rgba(var(--highlight-color-rgb), 0.8)' 
          },
        },
      },
      
      // Erweiterte Backdrop Filter
      backdropBlur: {
        'xs': '2px',
      },
      
      // Spezielle Scale-Werte für subtile Hover-Effekte
      scale: {
        '102': '1.02',
        '105': '1.05',
        '98': '0.98',
      },
      
      // Spezielle Aspect-Ratios
      aspectRatio: {
        'video': '16 / 9',
        'card': '4 / 3',
        'square': '1 / 1',
      },
      
      // Erweiterte Ring-Stile für Fokus-Indikatoren
      ringColor: {
        'focus': 'var(--focus-outline-color)',
        'contrast': 'white',
      },
      ringWidth: {
        '3': '3px',
        '4': '4px',
        '5': '5px',
      },
      ringOffsetWidth: {
        '3': '3px',
        '4': '4px',
        '5': '5px',
      },
    },
  },
  // Explizit den JIT-Modus aktivieren und Opacity-Plugins
  future: {
    hoverOnlyWhenSupported: true,
  },
  corePlugins: {
    backgroundOpacity: true,
    textOpacity: true,
    borderOpacity: true,
  },
  plugins: [
    // Optional: Plugin für Container-Queries hinzufügen
    // require('@tailwindcss/container-queries'),
  ],
  // Stelle sicher, dass JIT-Mode aktiviert ist (standardmäßig in Tailwind v3)
  mode: 'jit',
}
