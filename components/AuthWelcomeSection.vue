<template>
    <section class="welcome-section" aria-labelledby="welcome-title">
        <div class="language-picker-wrapper">
            <LanguagePicker />
        </div>
        <h1 id="welcome-title">{{ $t('welcome.title') }}</h1>
        <p class="intro-text">{{ $t('intro') }}</p>
    </section>
</template>

<style lang="scss" scoped>
.welcome-section {
    text-align: center;
    padding: 2rem;
}

.language-picker-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}

.intro-text {
    margin-top: 1rem;
    font-size: 1.1rem;
    line-height: 1.6;
}
</style>
