<template>
    <NuxtLayout :show-header="false" :show-menu="false">
        <div class="landing-page">
            <div class="welcome-section">
                <div class="language-picker-container">
                    <LanguagePicker />
                </div>
                <h1 class="title page-title">{{ $t('welcome.title') }}</h1>
                <p class="intro-text page-text">{{ $t('intro') }}</p>
                <NuxtLinkLocale to="/gamehome" class="primary-button action-button">
                    {{ $t('welcome.start') }}
                </NuxtLinkLocale>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useRequestURL } from '#imports'

const { t } = useI18n()
const url = useRequestURL()

// SEO Meta Tags
useSeoMeta({
    title: computed(() => t('welcome.title')),
    description: computed(() => t('welcome.seo.description')),
    ogTitle: computed(() => t('welcome.title')),
    ogDescription: computed(() => t('welcome.seo.description')),
    ogType: 'website',
    robots: 'index, follow',
    viewport: 'width=device-width, initial-scale=1',
    twitterCard: 'summary_large_image',
    ogUrl: computed(() => url.href)
});

// JSON-LD
useJsonld({
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: computed(() => t('welcome.title')).value,
    description: computed(() => t('welcome.seo.description')).value,
    url: url.href,
    potentialAction: {
        '@type': 'SearchAction',
        'target': {
            '@type': 'EntryPoint',
            'urlTemplate': `${url.origin}/search?q={search_term_string}`
        },
        'query': 'required name=search_term_string'
    }
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.landing-page {
    @include full-page;
    background: var(--background-color);
    overflow: hidden;
    position: relative;
}

.welcome-section {
    @include center-content;
    width: 100%;
}

.language-picker-container {
    display: flex;
    justify-content: center;
    margin-bottom: var(--padding-large);
}

.page-title {
    font-size: var(--font-size-responsive-2xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
    color: var(--primary-color);
    line-height: var(--line-height-tight);
    margin-bottom: var(--padding-medium);
}

.page-text {
    font-size: var(--font-size-responsive-md);
    line-height: var(--line-height-relaxed);
    color: var(--text-secondary);
    margin-bottom: var(--padding-large);
    max-width: var(--max-line-length);
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}

.action-button {
    @include button-primary;
    display: inline-block;
    min-height: var(--min-touch-target);
    padding: var(--padding-medium) var(--padding-large);
    font-size: var(--font-size-responsive-sm);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color-dark);
    background: var(--primary-color);
    border-radius: var(--border-radius);
    text-decoration: none;
    transition: all var(--transition-speed) var(--transition-bounce);
    border: none;
    cursor: pointer;
    box-shadow: var(--box-shadow);

    &:hover {
        background: var(--primary-color-dark);
        box-shadow: var(--box-shadow-hover);
        transform: translateY(-2px);
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }

    &:active {
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    .action-button {
        transition: none;
        transform: none;

        &:hover,
        &:active {
            transform: none;
        }
    }
}

@media (width <= 768px) {
    .page-title {
        font-size: var(--font-size-responsive-xl);
    }

    .page-text {
        font-size: var(--font-size-responsive-sm);
    }

    .action-button {
        width: 100%;
        text-align: center;
        padding: var(--padding-small) var(--padding-medium);
    }
}
</style>
