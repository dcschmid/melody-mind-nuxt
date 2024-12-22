<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main class="login-page" id="main-content">
            <div class="content-wrapper">
                <AuthWelcomeSection />

                <Transition name="form-switch" mode="out-in">
                    <AuthLoginForm v-if="showLoginForm" @switch-form="handleFormSwitch" />
                    <AuthRegisterForm v-else-if="showRegisterForm" @switch-form="handleFormSwitch" />
                    <AuthForgotPasswordForm v-else-if="showForgotPasswordForm" @switch-form="handleFormSwitch" />
                </Transition>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { useAuthForm } from '~/composables/useAuthForm'
import { useSeo } from '~/composables/useSeo'

const { formState } = useAuthForm()
const { setupSeo } = useSeo()

setupSeo({
    pageName: 'login',
    customTitle: 'MelodyMind - Login',
    customDescription: 'Logge dich ein oder registriere dich bei MelodyMind, dem interaktiven Musikquiz.',
    customKeywords: 'musik quiz, musikquiz, musik spiel, musik rätsel, online quiz, musikwissen test, melodymind, musik trivia',
    noIndex: false
})

const showLoginForm = computed(() => !formState.isRegistering && !formState.showForgotPassword)
const showRegisterForm = computed(() => formState.isRegistering)
const showForgotPasswordForm = computed(() => formState.showForgotPassword)

const handleFormSwitch = (form: 'login' | 'register' | 'forgot-password') => {
    if (form === 'register') {
        formState.isRegistering = true
        formState.showForgotPassword = false
    } else if (form === 'login') {
        formState.isRegistering = false
        formState.showForgotPassword = false
    } else if (form === 'forgot-password') {
        formState.showForgotPassword = true
    }
}
</script>

<style scoped lang="scss">
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--padding-large);
    background: var(--background-color);
}

.content-wrapper {
    width: 100%;
    max-width: 480px;
    margin: 0 auto;
}

.auth-container {
    width: 100%;
    padding: var(--padding-large);
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    margin-bottom: var(--padding-large);
}

:root {
    --color-primary: #0056b3;
    --color-primary-dark: #004085;
    --color-primary-rgb: 0, 86, 179;
    --error-color: #dc3545;
    --error-color-rgb: 220, 53, 69;
    --error-color-light: rgba(220, 53, 69, 0.1);
    --error-color-border: rgba(220, 53, 69, 0.2);
}

.form-switch-enter-active,
.form-switch-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.form-switch-enter-from,
.form-switch-leave-to {
    opacity: 0;
    transform: translateX(20px);
}

.form-switch-enter-to,
.form-switch-leave-from {
    opacity: 1;
    transform: translateX(0);
}

@media (max-width: 768px) {
    .login-page {
        padding: var(--padding-medium);
    }

    .content-wrapper {
        margin-bottom: var(--padding-medium);
    }

    .auth-container {
        padding: var(--padding-medium);
    }
}
</style>
