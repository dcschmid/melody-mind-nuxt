<template>
    <Form @submit="(values) => handleLogin(values as LoginCredentials)"
          v-slot="{ errors }"
          class="auth-form"
          aria-labelledby="login-title">
        <h2 id="login-title">{{ $t('login.title') }}</h2>

        <div class="form-group">
            <label :for="'login-email'" class="form-label">{{ $t('login.emailLabel') }}</label>
            <div class="input-wrapper">
                <Icon name="material-symbols:mail-outline" class="input-icon" aria-hidden="true" />
                <Field :id="'login-email'" name="email" type="email"
                    :placeholder="$t('login.emailPlaceholder')" :rules="validators.email"
                    v-model="formState.email" autocomplete="email" aria-required="true"
                    :aria-invalid="errors.email ? 'true' : 'false'"
                    :aria-describedby="errors.email ? 'login-email-error' : ''" />
            </div>
            <ErrorMessage name="email">
                <template v-slot="{ message }">
                    <p class="error-message" :id="'login-email-error'" role="alert">{{ message }}</p>
                </template>
            </ErrorMessage>
        </div>

        <div class="form-group">
            <label :for="'login-password'" class="form-label">{{ $t('login.passwordLabel') }}</label>
            <div class="input-wrapper">
                <Icon name="material-symbols:lock-outline" class="input-icon" aria-hidden="true" />
                <Field :id="'login-password'" name="password" type="password"
                    :placeholder="$t('login.passwordPlaceholder')" :rules="validators.password"
                    v-model="formState.password" autocomplete="current-password" aria-required="true"
                    :aria-invalid="errors.password ? 'true' : 'false'"
                    :aria-describedby="errors.password ? 'login-password-error' : ''" />
            </div>
            <ErrorMessage name="password">
                <template v-slot="{ message }">
                    <p class="error-message" :id="'login-password-error'" role="alert">{{ message }}</p>
                </template>
            </ErrorMessage>
        </div>

        <button type="submit" class="submit-button" :aria-busy="formState.isSubmitting"
            :disabled="formState.isSubmitting">
            {{ $t('login.submitButton') }}
        </button>

        <div class="social-login-divider">
            <span>{{ $t('login.orContinueWith') }}</span>
        </div>

        <div class="social-login-buttons">
            <button type="button" @click="handleDiscordLogin" class="social-login-button discord">
                <Icon name="mdi:discord" size="24" aria-hidden="true" />
                <span>{{ $t('login.continueWithDiscord') }}</span>
            </button>

            <button type="button" @click="handleGithubLogin" class="social-login-button github">
                <Icon name="mdi:github" size="24" aria-hidden="true" />
                <span>{{ $t('login.continueWithGithub') }}</span>
            </button>
        </div>

        <div class="auth-links" role="navigation" aria-label="Additional authentication options">
            <a href="#" @click.prevent="$emit('switch-form', 'register')" class="link">
                <Icon name="material-symbols:person-add-outline" size="20" aria-hidden="true" />
                <span>{{ $t('login.noAccount') }}</span>
            </a>
        </div>

        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
            {{ $t(formState.errorMessage) }}
        </div>
    </Form>
</template>

<script setup lang="ts">
import { useAuthForm } from '~/composables/useAuthForm'
import { useAuth, type LoginCredentials } from '~/composables/useAuth'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { signInWithDiscord } from '~/lib/auth-client'
import { authClient } from '~/lib/auth-client'

const { formState, validators } = useAuthForm()
const { handleLogin } = useAuth()

const handleDiscordLogin = async () => {
    try {
        await signInWithDiscord()
    } catch (error) {
        formState.errorMessage = 'login.error.discordLoginFailed'
    }
}

const handleGithubLogin = async () => {
    try {
        await authClient.signIn.social({
            provider: "github"
        })
    } catch (error) {
        formState.errorMessage = 'login.error.githubLoginFailed'
    }
}

defineEmits<{
    'switch-form': [form: 'register']
}>()
</script>

<style lang="scss">
@use '@/assets/scss/components/_auth-forms.scss';

.social-login-divider {
    margin: 1.5rem 0;
    text-align: center;
    position: relative;

    &::before,
    &::after {
        content: '';
        position: absolute;
        top: 50%;
        width: calc(50% - 1rem);
        height: 1px;
        background-color: var(--border-color);
    }

    &::before {
        left: 0;
    }

    &::after {
        right: 0;
    }

    span {
        background-color: var(--background-color);
        padding: 0 0.5rem;
        color: var(--text-color-light);
        font-size: 0.9rem;
    }
}

.social-login-buttons {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.social-login-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    background-color: transparent;
    color: var(--text-color);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
        background-color: var(--hover-color);
    }

    &.discord {
        background-color: #5865F2;
        border-color: #5865F2;
        color: white;

        &:hover {
            background-color: #4752c4;
        }
    }

    &.github {
        background-color: #24292e;
        border-color: #24292e;
        color: white;

        &:hover {
            background-color: #1c2024;
        }
    }
}
</style>
