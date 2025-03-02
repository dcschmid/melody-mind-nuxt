<template>
  <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
    <main class="mx-auto w-full max-w-[75rem] p-4 md:p-8 print:print-friendly motion-reduce:transition-none">
      <article class="space-y-8">
        <h1 class="mb-8 text-center text-2xl font-bold leading-[1.4] text-[var(--color-primary)] md:text-3xl">
          {{ $t('legal.imprint.title') }}
        </h1>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.information.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.information.operator') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.information.address') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.information.country') }}
            </p>
          </div>
        </section>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.contact.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.contact.emailLabel') }}:
              {{ $t('legal.imprint.contact.emailAddress') }}
            </p>
          </div>
        </section>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.responsible.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.information.operator') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.information.address') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.information.country') }}
            </p>
          </div>
        </section>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.disputeResolution.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.disputeResolution.text') }}:
              <a
                :href="$t('legal.imprint.disputeResolution.link')"
                target="_blank"
                rel="noopener noreferrer"
                class="rounded text-[var(--color-primary)] underline-offset-2 transition-colors duration-300 hover:text-[var(--primary-color-dark)] hover:underline focus-visible:outline focus-visible:outline-offset-2 focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] motion-reduce:transition-none"
                aria-label="Link zur Streitschlichtungsplattform der Europäischen Kommission (öffnet in neuem Tab)"
              >
                {{ $t('legal.imprint.disputeResolution.link') }}
              </a>
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.disputeResolution.additional') }}
            </p>
          </div>
        </section>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.jurisdiction.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.jurisdiction.text') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.jurisdiction.applicableLaw') }}
            </p>
            <p class="mb-2">
              {{ $t('legal.imprint.jurisdiction.jurisdiction') }}
            </p>
          </div>
        </section>

        <section
          class="mb-8 rounded-lg bg-[var(--color-surface)] p-4 shadow transition-all duration-300 last:mb-0 md:p-8 motion-reduce:transition-none"
        >
          <h2 class="mb-4 text-xl font-semibold leading-[1.4] text-[var(--color-primary)] md:text-2xl">
            {{ $t('legal.imprint.lawReference.title') }}
          </h2>
          <div class="text-base leading-[1.6] text-[#f0f0f0]">
            <p class="mb-2">
              {{ $t('legal.imprint.lawReference.text') }}
            </p>
          </div>
        </section>
      </article>
    </main>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useSeoMeta } from '#imports'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// SEO Meta Tags
useSeoMeta({
  title: computed(() => t('legal.imprint.meta.title')),
  description: computed(() => t('legal.imprint.meta.description')),
  ogTitle: computed(() => t('legal.imprint.meta.title')),
  ogDescription: computed(() => t('legal.imprint.meta.description')),
  ogType: 'website',
  robots: 'noindex, follow', // Legal pages should not be indexed
})
</script>

<!-- Tailwind CSS classes are used directly in the template -->
<style>
/* Print-specific styles that can't be easily handled with Tailwind classes */
@media print {
  h1 {
    font-size: 24px !important;
    color: black !important;
  }
  h2 {
    font-size: 20px !important;
    color: black !important;
  }
  p {
    font-size: 14px !important;
    color: black !important;
  }
  main,
  article,
  section {
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    background: none !important;
  }
  section {
    page-break-inside: avoid;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1em !important;
  }
  a {
    text-decoration: underline !important;
    color: #000 !important;
  }
}

/* Unterstützung für hohen Kontrast */
@media (prefers-contrast: more) {
  h1,
  h2 {
    text-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
  }

  a {
    text-decoration: underline !important;
    font-weight: 700 !important;
  }
}

/* Unterstützung für reduzierten Bewegungsmodus */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
</style>
