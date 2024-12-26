<template>
    <div class="landing-page">
        <div class="container">
            <div class="content">
                <div class="welcome-section">
                    <h1>{{ $t('landing.title') }}</h1>
                    <p>{{ $t('landing.description') }}</p>
                    <div class="cta-buttons">
                        <NuxtLink to="/categories" class="button primary">
                            {{ $t('landing.startPlaying') }}
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
.landing-page {
    min-height: calc(100vh - var(--header-height));
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: var(--background-gradient);

    .container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }

    .content {
        display: flex;
        justify-content: center;
        gap: 4rem;
        padding: 2rem;
    }

    .welcome-section {
        text-align: center;
        max-width: 600px;

        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            color: var(--text-secondary);
        }
    }

    .cta-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;

        .button {
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
        }
    }
}

@media (max-width: 768px) {
    .landing-page {
        .content {
            flex-direction: column;
            gap: 2rem;
        }

        .welcome-section {
            h1 {
                font-size: 2rem;
            }

            p {
                font-size: 1rem;
            }
        }
    }
}
</style>
