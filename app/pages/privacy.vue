<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="legal-page">
            <article class="legal-container">
                <h1 class="main-title">{{ $t('legal.privacy.title') }}</h1>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.overview.title') }}</h2>
                    <div class="content-block">
                        <h3 class="subsection-title">{{ $t('legal.privacy.overview.general.title') }}</h3>
                        <p>{{ $t('legal.privacy.overview.general.text') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.dataCollection.title') }}</h2>
                    <div class="content-block">
                        <h3 class="subsection-title">{{ $t('legal.privacy.dataCollection.cookies.title') }}</h3>
                        <p>{{ $t('legal.privacy.dataCollection.cookies.text') }}</p>

                        <h3 class="subsection-title">{{ $t('legal.privacy.dataCollection.analytics.title') }}</h3>
                        <p>{{ $t('legal.privacy.dataCollection.analytics.text') }}</p>

                        <h3 class="subsection-title">{{ $t('legal.privacy.dataCollection.serverLogs.title') }}</h3>
                        <p>{{ $t('legal.privacy.dataCollection.serverLogs.text') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.gameData.title') }}</h2>
                    <div class="content-block">
                        <h3 class="subsection-title">{{ $t('legal.privacy.gameData.progress.title') }}</h3>
                        <p>{{ $t('legal.privacy.gameData.progress.intro') }}</p>
                        <ul class="privacy-list">
                            <li>{{ $t('legal.privacy.gameData.progress.list.scores') }}</li>
                            <li>{{ $t('legal.privacy.gameData.progress.list.awards') }}</li>
                            <li>{{ $t('legal.privacy.gameData.progress.list.rankings') }}</li>
                        </ul>
                        <p>{{ $t('legal.privacy.gameData.progress.purpose') }}</p>

                        <h3 class="subsection-title">{{ $t('legal.privacy.gameData.localStorage.title') }}</h3>
                        <p>{{ $t('legal.privacy.gameData.localStorage.intro') }}</p>
                        <ul class="privacy-list">
                            <li>{{ $t('legal.privacy.gameData.localStorage.list.categories') }}</li>
                            <li>{{ $t('legal.privacy.gameData.localStorage.list.settings') }}</li>
                            <li>{{ $t('legal.privacy.gameData.localStorage.list.language') }}</li>
                        </ul>
                        <p>{{ $t('legal.privacy.gameData.localStorage.storage') }}</p>

                        <h3 class="subsection-title">{{ $t('legal.privacy.gameData.session.title') }}</h3>
                        <p>{{ $t('legal.privacy.gameData.session.intro') }}</p>
                        <ul class="privacy-list">
                            <li>{{ $t('legal.privacy.gameData.session.list.auth') }}</li>
                            <li>{{ $t('legal.privacy.gameData.session.list.progress') }}</li>
                            <li>{{ $t('legal.privacy.gameData.session.list.settings') }}</li>
                        </ul>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.rights.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.privacy.rights.intro') }}</p>
                        <ul class="privacy-list">
                            <li>{{ $t('legal.privacy.rights.list.information') }}</li>
                            <li>{{ $t('legal.privacy.rights.list.correction') }}</li>
                            <li>{{ $t('legal.privacy.rights.list.restriction') }}</li>
                            <li>{{ $t('legal.privacy.rights.list.objection') }}</li>
                            <li>{{ $t('legal.privacy.rights.list.portability') }}</li>
                        </ul>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.deletion.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.privacy.deletion.intro') }}</p>
                        <ul class="privacy-list">
                            <li>{{ $t('legal.privacy.deletion.list.highscores') }}</li>
                            <li>{{ $t('legal.privacy.deletion.list.results') }}</li>
                            <li>{{ $t('legal.privacy.deletion.list.account') }}</li>
                        </ul>
                        <p>{{ $t('legal.privacy.deletion.local') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.privacy.contact.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.privacy.contact.text') }}</p>
                        <p>{{ $t('legal.privacy.contact.emailLabel') }}: {{ $t('legal.privacy.contact.emailAddress') }}
                        </p>
                    </div>
                </section>
            </article>
        </main>
    </NuxtLayout>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useSeoMeta } from '#imports'

const { t } = useI18n()

// SEO Meta Tags
useSeoMeta({
    title: computed(() => t('legal.privacy.meta.title')),
    description: computed(() => t('legal.privacy.meta.description')),
    ogTitle: computed(() => t('legal.privacy.meta.title')),
    ogDescription: computed(() => t('legal.privacy.meta.description')),
    ogType: 'website',
    robots: 'noindex, follow' // Legal pages should not be indexed
})
</script>

<style lang="scss" scoped>
.legal-page {
    width: 100%;
    margin: 0 auto;
    max-width: var(--content-width);
    padding: var(--padding-medium);
}

.main-title {
    font-size: var(--font-size-responsive-2xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
    margin-bottom: var(--padding-large);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.legal-section {
    margin-bottom: var(--padding-large);
    background: var(--surface-color);
    padding: var(--padding-medium);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);

    &:last-child {
        margin-bottom: 0;
    }
}

.section-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--padding-medium);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.subsection-title {
    font-size: var(--font-size-responsive-lg);
    font-weight: var(--font-weight-semibold);
    margin: var(--padding-medium) 0 var(--padding-small);
    color: var(--text-color);
    line-height: var(--line-height-tight);
}

.content-block {
    font-size: var(--font-size-base);
    line-height: var(--line-height-relaxed);
    color: var(--text-secondary);
    margin-bottom: var(--padding-medium);

    a {
        color: var(--primary-color);
        text-decoration: none;
        transition: all var(--transition-speed) var(--transition-bounce);

        &:hover {
            color: var(--primary-color-dark);
            text-decoration: underline;
        }

        &:focus-visible {
            outline: var(--focus-outline-width) solid var(--focus-outline-color);
            outline-offset: var(--focus-outline-offset);
            border-radius: var(--border-radius);
        }
    }
}

.privacy-list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin: var(--padding-small) 0;
    color: var(--text-secondary);

    li {
        margin-bottom: var(--padding-small);
        line-height: var(--line-height-normal);
    }
}

@media (prefers-reduced-motion: reduce) {
    .content-block a {
        transition: none;
    }
}

@media (width <= 768px) {
    .legal-page {
        padding: var(--padding-small);
    }

    .main-title {
        font-size: var(--font-size-responsive-xl);
    }

    .section-title {
        font-size: var(--font-size-responsive-lg);
    }

    .subsection-title {
        font-size: var(--font-size-responsive-md);
    }

    .content-block,
    .privacy-list {
        font-size: var(--font-size-responsive-sm);
    }

    .legal-section {
        padding: var(--padding-small);
    }
}
</style>
