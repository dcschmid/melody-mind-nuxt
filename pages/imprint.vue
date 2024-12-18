<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true" :show-coins="false">
        <main class="legal-page">
            <article class="legal-container">
                <h1 class="main-title">{{ $t('legal.imprint.title') }}</h1>

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
definePageMeta({
    layout: 'default'
})
</script>

<style lang="scss" scoped>
.legal-page {
    width: 100%;
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-medium);
}

.legal-container {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: clamp(var(--padding-medium), 4vw, var(--padding-large));
    box-shadow: var(--box-shadow);
    border: 1px solid rgb(255 255 255 / 10%);
}

.main-title {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
    margin-bottom: var(--padding-large);
}

.legal-section {
    margin-bottom: var(--padding-large);

    &:last-child {
        margin-bottom: 0;
    }
}

.section-title {
    font-size: calc(var(--header-font-size) * 0.8);
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
}

.content-block {
    color: var(--text-secondary);
    line-height: var(--line-height-body);

    p {
        margin-bottom: var(--padding-small);
    }

    a {
        color: var(--highlight-color);
        text-decoration: none;
        transition: opacity 0.3s ease;

        &:hover {
            opacity: 0.8;
        }
    }
}

@media (max-width: 768px) {
    .legal-page {
        padding: var(--padding-small);
    }

    .legal-container {
        padding: var(--padding-medium);
    }

    .main-title {
        font-size: calc(var(--header-font-size) * 0.8);
    }

    .section-title {
        font-size: calc(var(--header-font-size) * 0.7);
    }
}
</style>
