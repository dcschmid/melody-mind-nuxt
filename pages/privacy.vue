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
definePageMeta({
    layout: 'default'
})
</script>

<style lang="scss" scoped>
.legal-page {
    width: 100%;
    margin: 0 auto;
}

.main-title {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--primary-color);
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

.subsection-title {
    font-size: calc(var(--header-font-size) * 0.6);
    font-weight: 600;
    color: var(--text-color);
    margin: var(--padding-medium) 0 var(--padding-small);
}

.content-block {
    color: var(--text-secondary);
    line-height: var(--line-height-body);

    p {
        margin-bottom: var(--padding-small);
    }
}

.privacy-list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin: var(--padding-small) 0;

    li {
        margin-bottom: var(--padding-small);
    }
}

@media (max-width: 768px) {

    .main-title {
        font-size: calc(var(--header-font-size) * 0.8);
    }

    .section-title {
        font-size: calc(var(--header-font-size) * 0.7);
    }

    .subsection-title {
        font-size: calc(var(--header-font-size) * 0.5);
    }
}
</style>
