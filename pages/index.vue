<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="false">
        <main class="login-page" id="main-content">
            <div class="content-wrapper">
                <section class="welcome-section" v-motion-slide-top>
                    <h1>{{ $t('welcome') }}</h1>
                    <p class="intro-text">{{ $t('intro') }}</p>
                </section>

                <section class="auth-section" v-motion-slide-visible>
                    <!-- Login Form -->
                    <Form v-if="!formState.isRegistering && !formState.showForgotPassword" @submit="handleLogin" class="auth-form"
                        aria-labelledby="login-title">
                        <h2 id="login-title">{{ $t('login.title') }}</h2>

                        <div class="form-group">
                            <label for="login-method">{{ $t('login.methodLabel') }}</label>
                            <div class="select-wrapper">
                                <Field name="loginMethod" as="select" v-model="formState.loginMethod" class="form-control">
                                    <option value="email">{{ $t('login.emailOption') }}</option>
                                    <option value="username">{{ $t('login.usernameOption') }}</option>
                                </Field>
                                <Icon name="material-symbols:keyboard-arrow-down-rounded" size="24"
                                    class="select-icon" />
                            </div>
                        </div>

                        <div class="form-group" v-if="formState.loginMethod === 'email'">
                            <label for="email">{{ $t('login.emailLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:mail-outline" size="24" class="input-icon" />
                                <Field name="email" type="email" :rules="validators.email" v-model="formState.email"
                                    :placeholder="$t('login.emailPlaceholder')" />
                            </div>
                            <ErrorMessage name="email" class="error-message" />
                        </div>

                        <div class="form-group" v-else>
                            <label for="username">{{ $t('login.usernameLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:person-outline" size="24" class="input-icon" />
                                <Field name="username" type="text" :rules="validators.username" v-model="formState.username"
                                    :placeholder="$t('login.usernamePlaceholder')" />
                            </div>
                            <ErrorMessage name="username" class="error-message" />
                        </div>

                        <div class="form-group">
                            <label for="password">{{ $t('login.passwordLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:lock-outline" size="24" class="input-icon" />
                                <Field name="password" type="password" :rules="validators.password" v-model="formState.password"
                                    :placeholder="$t('login.passwordPlaceholder')" />
                            </div>
                            <ErrorMessage name="password" class="error-message" />
                        </div>

                        <button type="submit" class="submit-button">
                            {{ $t('login.submitButton') }}
                        </button>

                        <div class="auth-links">
                            <a href="#" @click.prevent="formState.isRegistering = true" class="link">
                                {{ $t('login.noAccount') }}
                            </a>
                            <a href="#" @click.prevent="formState.showForgotPassword = true" class="link">
                                {{ $t('login.forgotPassword') }}
                            </a>
                        </div>
                    </Form>

                    <!-- Register Form -->
                    <Form v-else-if="formState.isRegistering && !formState.showForgotPassword" @submit="handleRegister" class="auth-form"
                        aria-labelledby="register-title">
                        <h2 id="register-title">{{ $t('register.title') }}</h2>

                        <div class="form-group">
                            <label for="name">{{ $t('register.nameLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:person-outline" size="24" class="input-icon" />
                                <Field name="name" type="text" :rules="validators.name" v-model="formState.name"
                                    :placeholder="$t('register.namePlaceholder')" />
                            </div>
                            <ErrorMessage name="name" class="error-message" />
                        </div>

                        <div class="form-group">
                            <label for="reg-username">{{ $t('register.usernameLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:alternate-email" size="24" class="input-icon" />
                                <Field name="username" type="text" :rules="validators.username" v-model="formState.username"
                                    :placeholder="$t('register.usernamePlaceholder')" />
                            </div>
                            <ErrorMessage name="username" class="error-message" />
                            <small>{{ $t('register.usernameLengthHint') }}</small>
                        </div>

                        <div class="form-group">
                            <label for="reg-email">{{ $t('register.emailLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:mail-outline" size="24" class="input-icon" />
                                <Field name="email" type="email" :rules="validators.email" v-model="formState.email"
                                    :placeholder="$t('register.emailPlaceholder')" />
                            </div>
                            <ErrorMessage name="email" class="error-message" />
                        </div>

                        <div class="form-group">
                            <label for="reg-password">{{ $t('register.passwordLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:lock-outline" size="24" class="input-icon" />
                                <Field name="password" type="password" :rules="validators.password" v-model="formState.password"
                                    :placeholder="$t('register.passwordPlaceholder')" />
                            </div>
                            <ErrorMessage name="password" class="error-message" />
                        </div>

                        <button type="submit" class="submit-button">
                            {{ $t('register.submitButton') }}
                        </button>

                        <div class="auth-links">
                            <a href="#" @click.prevent="formState.isRegistering = false" class="link">
                                {{ $t('register.hasAccount') }}
                            </a>
                        </div>
                    </Form>

                    <!-- Forgot Password Form -->
                    <Form v-else-if="formState.showForgotPassword" @submit="handleForgotPassword" class="auth-form"
                        aria-labelledby="forgot-password-title">
                        <h2 id="forgot-password-title">{{ $t('forgotPassword.title') }}</h2>

                        <div class="form-group">
                            <label for="reset-email">{{ $t('forgotPassword.emailLabel') }}</label>
                            <div class="input-wrapper">
                                <Icon name="material-symbols:mail-outline" size="24" class="input-icon" />
                                <Field name="email" type="email" :rules="validators.email" v-model="formState.email"
                                    :placeholder="$t('forgotPassword.emailPlaceholder')" />
                            </div>
                            <ErrorMessage name="email" class="error-message" />
                        </div>

                        <button type="submit" class="submit-button">
                            {{ $t('forgotPassword.submitButton') }}
                        </button>

                        <div class="auth-links">
                            <a href="#" @click.prevent="formState.showForgotPassword = false; formState.isRegistering = false" class="link">
                                {{ $t('forgotPassword.backToLogin') }}
                            </a>
                        </div>
                    </Form>
                </section>
            </div>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { authClient } from "../lib/auth-client";
import { useRouter } from 'vue-router';

const { t } = useI18n()
const session = authClient.useSession()
const router = useRouter();

// Typen für die Formulardaten definieren
interface LoginCredentials {
  email?: string;
  username?: string;
  password: string;
}

interface RegisterData extends LoginCredentials {
  name: string;
  email: string;
  username: string;
}

// Formularstatus in einem reaktiven Objekt zusammenfassen
const formState = reactive({
  isRegistering: false,
  showForgotPassword: false,
  loginMethod: 'email' as 'email' | 'username',
  errorMessage: '',
})

const validators = {
    email: (value: string) => {
        if (!value) return t('errors.emailRequired')
        return /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value) || t('errors.invalidEmail')
    },
    username: (value: string) => {
        if (!value) return t('errors.usernameRequired')
        return value.length >= 3 || t('errors.usernameTooShort')
    },
    password: (value: string) => {
        if (!value) return t('errors.passwordRequired')
        return value.length >= 6 || t('errors.passwordTooShort')
    },
    name: (value: string) => {
        if (!value) return t('errors.nameRequired')
        return value.length >= 2 || t('errors.nameTooShort')
    }
}

const handleLogin = async () => {
    try {
        const credentials = formState.loginMethod === 'email'
            ? { email: formState.email, password: formState.password }
            : { username: formState.username, password: formState.password }

        const result = await authClient.signIn[formState.loginMethod](credentials)
        if (result.error) throw result.error

        router.push('/gamehome')
    } catch (error) {
        console.error('Login error:', error)
        formState.errorMessage = 'errors.loginFailed'
    }
}

const handleRegister = async () => {
    try {
        const registrationData = {
            email: formState.email,
            password: formState.password,
            name: formState.name,
            username: formState.username
        }

        const { error } = await authClient.signUp.email(registrationData)
        if (error) throw error

        formState.isRegistering = false
        alert(t('register.successMessage'))
    } catch (error) {
        console.error('Registration error:', error)
        formState.errorMessage = 'errors.registrationFailed'
    }
}

const handleForgotPassword = async () => {
    try {
        const { error } = await authClient.forgetPassword({
            email: formState.email,
            redirectTo: `${window.location.origin}/reset-password`
        })

        if (error) throw error
        alert(t('forgotPassword.successMessage'))
        formState.showForgotPassword = false
    } catch (error) {
        console.error('Password reset error:', error)
        formState.errorMessage = 'errors.passwordResetFailed'
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

.welcome-section {
    text-align: center;
    margin-bottom: var(--padding-large);

    h1 {
        font-size: var(--header-font-size);
        color: var(--text-color);
        margin-bottom: var(--padding-medium);
    }

    .intro-text {
        font-size: var(--body-font-size);
        color: var(--text-secondary);
        line-height: 1.6;
    }
}

.auth-form {
    background: var(--surface-color);
    padding: var(--padding-large);
    border-radius: var(--border-radius);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);

    h2 {
        font-size: 1.5rem;
        color: var(--text-color);
        margin-bottom: var(--padding-large);
        text-align: center;
    }
}

.form-group {
    margin-bottom: var(--padding-medium);

    label {
        display: block;
        margin-bottom: var(--padding-small);
        color: var(--text-color);
        font-weight: 500;
    }

    small {
        display: block;
        margin-top: 0.5rem;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
}

.input-wrapper {
    position: relative;

    .input-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        pointer-events: none;
    }
}

.select-wrapper {
    position: relative;
    width: 100%;

    select {
        appearance: none;
        width: 100%;
        padding: 1rem 3rem;
        background: var(--surface-color);
        border: 1px solid var(--secondary-color);
        border-radius: var(--border-radius);
        color: var(--text-color);
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s var(--transition-bounce);

        &:hover {
            border-color: var(--highlight-color);
            background: var(--secondary-color);
        }

        &:focus {
            outline: none;
            border-color: var(--highlight-color);
            box-shadow: 0 0 0 2px rgba(var(--highlight-color-rgb), 0.2);
        }

        option {
            background: var(--surface-color);
            color: var(--text-color);
            padding: 1rem;
        }
    }

    .select-icon {
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: var(--highlight-color);
        pointer-events: none;
        transition: transform 0.3s var(--transition-bounce);
    }

    &:hover .select-icon {
        transform: translateY(-50%) translateY(-2px);
        color: var(--highlight-color);
    }
}

// Verbesserte Animation für das Dropdown
@keyframes slideDown {
    0% {
        opacity: 0;
        transform: translateY(-10px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

select[size] {
    animation: slideDown 0.3s var(--transition-bounce);
}

// Dark mode Anpassungen
@media (prefers-color-scheme: dark) {
    .select-wrapper {
        select {
            option {
                background: var(--surface-color);
            }
        }
    }
}

// Mobile Optimierungen
@media (max-width: 768px) {
    .select-wrapper {
        select {
            padding: 0.875rem 2.5rem;
            font-size: 0.9rem;
        }
    }
}

input,
select {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    background: var(--background-color);
    border: 1px solid var(--secondary-color);
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: 1rem;
    transition: all 0.3s var(--transition-bounce);

    &::placeholder {
        color: var(--text-secondary);
    }

    &:focus {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.1);
    }

    &[aria-invalid="true"] {
        border-color: var(--error-color);
    }
}

.submit-button {
    width: 100%;
    padding: 1rem;
    background: var(--highlight-color);
    color: var(--button-text-color);
    border: none;
    border-radius: var(--border-radius);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s var(--transition-bounce);

    &:hover {
        background: var(--button-hover-color);
        transform: translateY(-2px);
    }

    &:active {
        transform: translateY(0);
    }
}

.auth-links {
    margin-top: var(--padding-medium);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;

    .link {
        color: var(--highlight-color);
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;

        &:hover {
            color: var(--button-hover-color);
            text-decoration: underline;
        }
    }
}

.error-message {
    background: var(--error-color);
    color: white;
    padding: var(--padding-small) var(--padding-medium);
    border-radius: var(--border-radius);
    margin-bottom: var(--padding-medium);
    font-size: 0.9rem;
    font-weight: 500;
}

@media (max-width: 768px) {
    .login-page {
        padding: var(--padding-medium);
    }

    .auth-form {
        padding: var(--padding-medium);
    }

    .welcome-section {
        margin-bottom: var(--padding-medium);
    }
}
</style>
