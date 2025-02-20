<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="legal-page">
            <article class="legal-container">
                <h1 class="page-title">{{ $t('legal.imprint.title') }}</h1>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.information.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.imprint.information.operator') }}</p>
                        <p>{{ $t('legal.imprint.information.address') }}</p>
                        <p>{{ $t('legal.imprint.information.country') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.contact.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.imprint.contact.emailLabel') }}: {{ $t('legal.imprint.contact.emailAddress') }}
                        </p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.responsible.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.imprint.information.operator') }}</p>
                        <p>{{ $t('legal.imprint.information.address') }}</p>
                        <p>{{ $t('legal.imprint.information.country') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.disputeResolution.title') }}</h2>
                    <div class="content-block">
                        <p>
                            {{ $t('legal.imprint.disputeResolution.text') }}:
                            <a :href="$t('legal.imprint.disputeResolution.link')" target="_blank"
                                rel="noopener noreferrer">
                                {{ $t('legal.imprint.disputeResolution.link') }}
                            </a>
                        </p>
                        <p>{{ $t('legal.imprint.disputeResolution.additional') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.jurisdiction.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.imprint.jurisdiction.text') }}</p>
                        <p>{{ $t('legal.imprint.jurisdiction.applicableLaw') }}</p>
                        <p>{{ $t('legal.imprint.jurisdiction.jurisdiction') }}</p>
                    </div>
                </section>

                <section class="legal-section">
                    <h2 class="section-title">{{ $t('legal.imprint.lawReference.title') }}</h2>
                    <div class="content-block">
                        <p>{{ $t('legal.imprint.lawReference.text') }}</p>
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
    title: computed(() => t('legal.imprint.meta.title')),
    description: computed(() => t('legal.imprint.meta.description')),
    ogTitle: computed(() => t('legal.imprint.meta.title')),
    ogDescription: computed(() => t('legal.imprint.meta.description')),
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

.page-title {
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

.content-block {
    font-size: var(--font-size-base);
    line-height: var(--line-height-relaxed);
    margin-bottom: var(--padding-medium);
    color: var(--text-secondary);

    p {
        margin-bottom: var(--padding-small);
    }

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

@media (prefers-reduced-motion: reduce) {
    .content-block a {
        transition: none;
    }
}

@media (width <= 768px) {
    .legal-page {
        padding: var(--padding-small);
    }

    .page-title {
        font-size: var(--font-size-responsive-xl);
        margin-bottom: var(--padding-medium);
    }

    .section-title {
        font-size: var(--font-size-responsive-lg);
    }

    .content-block {
        font-size: var(--font-size-responsive-sm);
    }

    .legal-section {
        padding: var(--padding-small);
    }
}
</style>
