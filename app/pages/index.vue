<template>
    <NuxtLayout :show-header="false" :show-menu="false">
        <div class="landing-page">
            <div class="welcome-section">
                <div class="language-picker-container">
                    <LanguagePicker />
                </div>
                <h1 class="title">{{ $t('welcome.title') }}</h1>
                <p class="intro-text">{{ $t('intro') }}</p>
                <NuxtLink to="/gamehome" class="primary-button">
                    {{ $t('welcome.start') }}
                </NuxtLink>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

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
});
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.landing-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    background: var(--background-color);
    overflow: hidden;
    position: relative;
}

.welcome-section {
    text-align: center;
    max-width: 800px;
    width: 100%;
}

.language-picker-container {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}

.title {
    font-size: var(--header-font-size);
    font-weight: bold;
    margin-bottom: var(--padding-large);
    line-height: 1.2;
    color: var(--primary-color);
}

.intro-text {
    font-size: var(--body-font-size);
    line-height: var(--line-height-body);
    color: var(--text-secondary);
    margin-bottom: var(--padding-large);
    max-width: var(--max-line-length);
    margin-left: auto;
    margin-right: auto;
}

.primary-button {
    display: inline-block;
    padding: var(--padding-small) var(--padding-medium);
    font-size: var(--button-font-size);
    font-weight: 600;
    color: var(--button-text-color);
    background: var(--primary-color);
    border-radius: var(--border-radius);
    text-decoration: none;
    transition: all var(--transition-speed) ease;
    border: none;
    cursor: pointer;
    box-shadow: var(--box-shadow);

    &:hover {
        background: var(--button-hover-color);
        box-shadow: var(--box-shadow-hover);
        transform: translateY(-2px);
    }

    &:active {
        transform: translateY(0);
    }
}
</style>
