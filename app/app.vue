<template>
  <div id="app" class="min-h-screen" role="application">
    <a href="#main-content" class="skip-to-content">{{ $t ? $t('common.skipToContent') : 'Skip to content' }}</a>
    <NuxtPage />
    <div id="main-content" tabindex="-1" class="outline-none"></div>
  </div>
</template>

<style>
/* Page transitions with support for reduced motion preferences */
/* Globale Fokusindikatoren für bessere Barrierefreiheit */
*:focus-visible {
  outline: 3px solid rgb(var(--focus-color-rgb, 59, 130, 246));
  outline-offset: 4px;
}

/* Skip-to-content Link für Tastaturnutzer */
.skip-to-content {
  position: absolute;
  top: -9999px;
  left: 50%;
  transform: translateX(-50%);
  background: rgb(var(--primary-color-rgb, 59, 130, 246));
  color: white;
  padding: 0.5rem 1rem;
  z-index: 9999;
  text-decoration: none;
  border-radius: 0 0 0.375rem 0.375rem;
  font-weight: 600;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.skip-to-content:focus-visible {
  top: 0;
  outline: 3px solid rgb(var(--focus-color-rgb, 59, 130, 246));
  outline-offset: 2px;
}

@media (prefers-reduced-motion: no-preference) {
  .page-enter-active,
  .page-leave-active {
    transition:
      opacity 0.5s ease,
      transform 0.5s ease;
  }

  .page-enter-from,
  .page-leave-to {
    opacity: 0;
    transform: translateX(50px);
  }

  .page-enter-to,
  .page-leave-from {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Reduced motion version - subtle fade only */
@media (prefers-reduced-motion: reduce) {
  .page-enter-active,
  .page-leave-active {
    transition: opacity 0.3s ease;
  }

  .page-enter-from,
  .page-leave-to {
    opacity: 0;
  }

  .page-enter-to,
  .page-leave-from {
    opacity: 1;
  }
}

/* High contrast mode support */
@media (prefers-contrast: more) {
  .page-enter-active,
  .page-leave-active,
  .page-enter-from,
  .page-leave-to,
  .page-enter-to,
  .page-leave-from {
    transition: none;
    transform: none;
    opacity: 1;
  }

  /* Erhöhter Kontrast für Fokusindikatoren */
  *:focus-visible {
    outline: 4px solid white !important;
    outline-offset: 4px !important;
    box-shadow: 0 0 0 2px black !important;
  }

  /* Bessere Lesbarkeit von Text */
  body {
    line-height: 1.8 !important;
  }

  /* Verbesserter Kontrast für Links */
  a:not([class]) {
    text-decoration: underline !important;
    text-decoration-thickness: 2px !important;
  }
}

/* Print-optimierte Darstellung */
@media print {
  .page-enter-active,
  .page-leave-active,
  .page-enter-from,
  .page-leave-to,
  .page-enter-to,
  .page-leave-from {
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }

  body {
    font-size: 12pt !important;
    line-height: 1.6 !important;
    color: black !important;
    background: white !important;
  }
}
</style>
