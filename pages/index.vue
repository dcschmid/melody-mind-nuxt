<template>
    <div class="landing-page">
        <div class="hero-section">
            <div class="container">
                <div class="language-picker-container">
                    <LanguagePicker />
                </div>
                <div class="content">
                    <div class="welcome-section">
                        <h1 class="title">{{ $t('welcome.title') }}</h1>
                        <p class="intro-text">{{ $t('intro') }}</p>

                        <div class="cta-section">
                            <NuxtLink to="/gamehome" class="primary-button">
                                {{ $t('welcome.start') }}
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import LanguagePicker from '~/components/LanguagePicker.vue';
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.landing-page {
    min-height: calc(100vh - var(--header-height));
    background: var(--background-color);
    overflow: hidden;
    position: relative;
    @include flex-center;
}

.language-picker-container {
    width: 100%;
    @include flex-center;
    margin-bottom: var(--padding-medium);
}

.hero-section {
    position: relative;
    width: 100%;
    @include flex-center;
    min-height: calc(100vh - var(--header-height));
}

.container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
}

.content {
    @include flex-center;
    width: 100%;
}

.welcome-section {
    text-align: center;
    width: 100%;
    margin: var(--padding-small);

    .title {
        font-size: var(--header-font-size);
        font-weight: bold;
        margin-bottom: var(--padding-large);
        line-height: 1.2;
        color: var(--text-color);
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
}

.cta-section {
    margin-top: var(--padding-large);
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

@include mobile {
    .hero-section {
        padding: var(--padding-small);
    }

    .welcome-section {
        padding: var(--padding-medium);
        margin: calc(var(--padding-small) / 2);
    }
}

@include tablet {
    .welcome-section {
        padding: var(--padding-medium);
    }
}
</style>
