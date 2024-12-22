<template>
    <NuxtLayout name="default" :show-header="false" :show-menu="false">
        <main class="login-page" id="main-content">
            <div class="content-wrapper">
                <section class="welcome-section" aria-labelledby="welcome-title">
                    <LanguagePicker />
                    <h1 id="welcome-title">{{ $t('welcome.title') }}</h1>
                    <p class="intro-text">{{ $t('intro') }}</p>
                </section>

                <div class="auth-container" role="region" aria-label="Authentication forms">
                    <!-- Login Form -->
                    <Form v-if="showLoginForm" @submit="handleLogin" v-slot="{ errors, submitForm }" class="auth-form"
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

                        <div class="auth-links" role="navigation" aria-label="Additional authentication options">
                            <a href="#" @click.prevent="formState.isRegistering = true" class="link"
                                aria-label="Create new account">
                                <Icon name="material-symbols:person-add-outline" size="20" aria-hidden="true" />
                                <span>{{ $t('login.noAccount') }}</span>
                            </a>
                            <a href="#" @click.prevent="formState.showForgotPassword = true" class="link"
                                aria-label="Reset forgotten password">
                                <Icon name="material-symbols:key-outline" size="20" aria-hidden="true" />
                                <span>{{ $t('login.forgotPassword') }}</span>
                            </a>
                        </div>

                        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
                            {{ $t(formState.errorMessage) }}
                        </div>
                    </Form>

                    <!-- Register Form -->
                    <Form v-else-if="showRegisterForm" @submit="handleRegister" v-slot="{ errors, submitForm }"
                        class="auth-form" aria-labelledby="register-title">
                        <h2 id="register-title">{{ $t('register.title') }}</h2>

                        <div class="form-group">
                            <label :for="'register-name'" class="form-label">{{ $t('register.nameLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:person-outline" class="input-icon" aria-hidden="true" />
                                <Field :id="'register-name'" name="name" type="text"
                                    :placeholder="$t('register.namePlaceholder')" :rules="validators.name"
                                    v-model="formState.name" autocomplete="name" aria-required="true"
                                    :aria-invalid="errors.name ? 'true' : 'false'"
                                    :aria-describedby="errors.name ? 'register-name-error' : ''" />
                            </div>
                            <ErrorMessage name="name">
                                <template v-slot="{ message }">
                                    <p class="error-message" :id="'register-name-error'" role="alert">{{ message }}</p>
                                </template>
                            </ErrorMessage>
                        </div>

                        <div class="form-group">
                            <label :for="'register-username'" class="form-label">{{ $t('register.usernameLabel')
                                }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:alternate-email" class="input-icon" aria-hidden="true" />
                                <Field :id="'register-username'" name="username" type="text"
                                    :placeholder="$t('register.usernamePlaceholder')" :rules="validators.username"
                                    v-model="formState.username" autocomplete="username" aria-required="true"
                                    :aria-invalid="errors.username ? 'true' : 'false'"
                                    :aria-describedby="errors.username ? 'register-username-error' : ''" />
                            </div>
                            <ErrorMessage name="username">
                                <template v-slot="{ message }">
                                    <p class="error-message" :id="'register-username-error'" role="alert">{{ message }}
                                    </p>
                                </template>
                            </ErrorMessage>
                            <small>{{ $t('register.usernameLengthHint') }}</small>
                        </div>

                        <div class="form-group">
                            <label :for="'register-email'" class="form-label">{{ $t('register.emailLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:mail-outline" class="input-icon" aria-hidden="true" />
                                <Field :id="'register-email'" name="email" type="email"
                                    :placeholder="$t('register.emailPlaceholder')" :rules="validators.email"
                                    v-model="formState.email" autocomplete="email" aria-required="true"
                                    :aria-invalid="errors.email ? 'true' : 'false'"
                                    :aria-describedby="errors.email ? 'register-email-error' : ''" />
                            </div>
                            <ErrorMessage name="email">
                                <template v-slot="{ message }">
                                    <p class="error-message" :id="'register-email-error'" role="alert">{{ message }}</p>
                                </template>
                            </ErrorMessage>
                        </div>

                        <div class="form-group">
                            <label :for="'register-password'" class="form-label">{{ $t('register.passwordLabel')
                                }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:lock-outline" class="input-icon" aria-hidden="true" />
                                <Field :id="'register-password'" name="password" type="password"
                                    :placeholder="$t('register.passwordPlaceholder')" :rules="validators.password"
                                    v-model="formState.password" autocomplete="new-password" aria-required="true"
                                    :aria-invalid="errors.password ? 'true' : 'false'"
                                    :aria-describedby="errors.password ? 'register-password-error' : ''" />
                            </div>
                            <ErrorMessage name="password">
                                <template v-slot="{ message }">
                                    <p class="error-message" :id="'register-password-error'" role="alert">{{ message }}
                                    </p>
                                </template>
                            </ErrorMessage>
                        </div>

                        <button type="submit" class="submit-button" :aria-busy="formState.isSubmitting"
                            :disabled="formState.isSubmitting">
                            {{ $t('register.submitButton') }}
                        </button>

                        <div class="auth-links" role="navigation" aria-label="Additional authentication options">
                            <a href="#" @click.prevent="formState.isRegistering = false" class="link"
                                aria-label="Back to login">
                                <Icon name="material-symbols:person-add-outline" size="20" aria-hidden="true" />
                                <span>{{ $t('register.hasAccount') }}</span>
                            </a>
                        </div>

                        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
                            {{ $t(formState.errorMessage) }}
                        </div>
                    </Form>

                    <!-- Forgot Password Form -->
                    <Form v-else-if="showForgotPasswordForm" @submit="handleForgotPassword"
                        v-slot="{ errors, submitForm }" class="auth-form" aria-labelledby="forgot-password-title">
                        <h2 id="forgot-password-title">{{ $t('forgotPassword.title') }}</h2>

                        <div class="form-group">
                            <label :for="'forgot-password-email'" class="form-label">{{ $t('forgotPassword.emailLabel')
                                }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:mail-outline" class="input-icon" aria-hidden="true" />
                                <Field :id="'forgot-password-email'" name="email" type="email"
                                    :placeholder="$t('forgotPassword.emailPlaceholder')" :rules="validators.email"
                                    v-model="formState.email" autocomplete="email" aria-required="true"
                                    :aria-invalid="errors.email ? 'true' : 'false'"
                                    :aria-describedby="errors.email ? 'forgot-password-email-error' : ''" />
                            </div>
                            <ErrorMessage name="email">
                                <template v-slot="{ message }">
                                    <p class="error-message" :id="'forgot-password-email-error'" role="alert">{{ message
                                        }}
                                    </p>
                                </template>
                            </ErrorMessage>
                        </div>

                        <button type="submit" class="submit-button" :aria-busy="formState.isSubmitting"
                            :disabled="formState.isSubmitting">
                            {{ $t('forgotPassword.submitButton') }}
                        </button>

                        <div class="auth-links" role="navigation" aria-label="Additional authentication options">
                            <a href="#"
                                @click.prevent="formState.showForgotPassword = false; formState.isRegistering = false"
                                class="link" aria-label="Back to login">
                                <Icon name="material-symbols:key-outline" size="20" aria-hidden="true" />
                                <span>{{ $t('forgotPassword.backToLogin') }}</span>
                            </a>
                        </div>

                        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
                            {{ $t(formState.errorMessage) }}
                        </div>
                    </Form>
                </div>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { useAuthForm } from '~/composables/useAuthForm'
import { useAuth } from '~/composables/useAuth'
import { useSeo } from '~/composables/useSeo'
import { Form, Field, ErrorMessage } from 'vee-validate'

const { formState, validators, showLoginForm, showRegisterForm, showForgotPasswordForm } = useAuthForm()
const { handleLogin, handleRegister, handleForgotPassword } = useAuth()
const { setupSeo } = useSeo()

setupSeo({
  pageName: 'home',
  type: 'website',
  imageUrl: '/images/melody-mind-social.jpg' // Assuming you have a social sharing image
})
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

.welcome-section {
    text-align: center;
    margin-bottom: var(--padding-large);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-medium);

    h1 {
        font-size: var(--header-font-size);
        color: var(--text-color);
        margin: 0;
    }

    .intro-text {
        font-size: var(--body-font-size);
        color: var(--text-secondary);
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
}

.auth-form {
    width: 100%;
    padding: var(--padding-large);
    background: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    margin-bottom: var(--padding-large);

    h2 {
        font-size: 1.5rem;
        color: var(--text-color);
        margin-bottom: var(--padding-large);
        text-align: center;
    }
}

.form-group {
    margin-bottom: var(--padding-medium);
}

.form-label {
    display: block;
    margin-bottom: var(--padding-small);
    color: var(--text-color);
    font-weight: 500;
    font-size: 1rem;
}

.input-wrapper {
    position: relative;
    margin-bottom: 0.25rem;

    .input-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        pointer-events: none;
    }
}

input,
select {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    background: var(--background-color);
    border: 2px solid var(--secondary-color);
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: 1rem;
    transition: all 0.2s ease;

    &::placeholder {
        color: var(--text-secondary);
        opacity: 0.8;
    }

    &:focus {
        outline: none;
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
    }

    &[aria-invalid="true"] {
        border-color: var(--error-color);

        &:focus {
            box-shadow: 0 0 0 3px rgba(var(--error-color-rgb), 0.2);
        }
    }
}

.submit-button {
    width: 100%;
    padding: 12px 24px;
    margin-top: 1.5rem;
    background: var(--primary-color);
    color: var(--text-on-primary);
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    position: relative;
    overflow: hidden;

    &::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.3s ease-out, height 0.3s ease-out;
    }

    &:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);

        &::before {
            width: 300px;
            height: 300px;
        }
    }

    &:active {
        transform: translateY(1px);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    &:disabled {
        background: var(--disabled-color, #cccccc);
        cursor: not-allowed;
        transform: none;
        box-shadow: none;

        &::before {
            display: none;
        }
    }
}

.auth-links {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;

    .link {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-color);
        text-decoration: none;
        padding: 8px 12px;
        border-radius: 6px;
        transition: all 0.2s ease;

        &:hover {
            background: var(--hover-bg, rgba(0, 0, 0, 0.05));
            color: var(--primary-color);
            transform: translateX(4px);
        }

        .icon {
            opacity: 0.8;
        }

        span {
            font-size: 0.95rem;
        }
    }
}

.form-error {
    margin-top: var(--padding-medium);
    padding: 1rem;
    background: var(--error-color-light);
    border: 1px solid var(--error-color-border);
    border-radius: var(--border-radius);
    color: var(--error-color);
    font-weight: 500;
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

@media (max-width: 768px) {
    .login-page {
        padding: var(--padding-medium);
    }

    .welcome-section {
        margin-bottom: var(--padding-medium);
    }

    .auth-form {
        padding: var(--padding-medium);
    }
}
</style>
