<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="false" :show-coins="false">
        <div role="main">
            <h1>{{ $t('welcome') }}</h1>

            <div>
                {{ $t('intro') }}
            </div>

            <form v-if="!isRegistering" @submit.prevent="handleLogin" class="auth-form" aria-labelledby="login-title">
                <h2 id="login-title">{{ $t('login.title') }}</h2>
                <div v-if="errorMessage" class="error-message" role="alert" aria-live="assertive">
                    {{ errorMessage }}
                </div>
                <div class="form-group">
                    <label for="login-method">{{ $t('login.methodLabel') }}</label>
                    <select id="login-method" v-model="loginMethod" class="form-control"
                        aria-describedby="login-method-description">
                        <option value="email">{{ $t('login.emailOption') }}</option>
                        <option value="username">{{ $t('login.usernameOption') }}</option>
                    </select>
                </div>
                <div class="form-group" v-if="loginMethod === 'email'">
                    <label for="email">{{ $t('login.emailLabel') }}</label>
                    <input type="email" id="email" v-model="email" aria-required="true" :aria-invalid="!!emailError">
                    <span v-if="emailError" class="error-message">{{ $t('errors.emailRequired') }}</span>
                </div>
                <div class="form-group" v-else>
                    <label for="username">{{ $t('login.usernameLabel') }}</label>
                    <input type="text" id="username" v-model="username" required :aria-invalid="!!usernameError">
                    <span v-if="usernameError" class="error-message">{{ $t('errors.usernameRequired') }}</span>
                </div>
                <div class="form-group">
                    <label for="password">{{ $t('login.passwordLabel') }}</label>
                    <input type="password" id="password" v-model="password" required :aria-invalid="!!passwordError">
                    <span v-if="passwordError" class="error-message">{{ $t('errors.passwordRequired') }}</span>
                </div>
                <button type="submit">{{ $t('login.submitButton') }}</button>
                <p>
                    <a href="#" @click.prevent="isRegistering = true">{{ $t('login.noAccount') }}</a>
                </p>
                <p>
                    <a href="#" @click.prevent="handleForgotPassword">{{ $t('login.forgotPassword') }}</a>
                </p>
            </form>

            <!-- Registrierungs Formular -->
            <form v-else @submit.prevent="handleRegister" class="auth-form">
                <h2>{{ $t('register.title') }}</h2>
                <div v-if="errorMessage" class="error-message" role="alert" aria-live="assertive">
                    {{ errorMessage }}
                </div>
                <div class="form-group">
                    <label for="name">{{ $t('register.nameLabel') }}</label>
                    <input type="text" id="name" v-model="name" required>
                </div>
                <div class="form-group">
                    <label for="reg-username">{{ $t('register.usernameLabel') }}</label>
                    <input type="text" id="reg-username" v-model="username" required>
                    <small>{{ $t('register.usernameLengthHint') }}</small>
                </div>
                <div class="form-group">
                    <label for="reg-email">{{ $t('register.emailLabel') }}</label>
                    <input type="email" id="reg-email" v-model="email" required>
                </div>
                <div class="form-group">
                    <label for="reg-password">{{ $t('register.passwordLabel') }}</label>
                    <input type="password" id="reg-password" v-model="password" required>
                </div>
                <button type="submit">{{ $t('register.submitButton') }}</button>
                <p>
                    <a href="#" @click.prevent="isRegistering = false">{{ $t('register.hasAccount') }}</a>
                </p>
            </form>
            <div>
                <h2 class="social-login-title">{{ $t('socialLogin.title') }}</h2>
                <div class="social-login-group">
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.social({ provider: 'github', callbackURL: '/gamehome' })">
                        <Icon name="line-md:github-loop" size="30" style="fill: #000;" /> GitHub
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.social({ provider: 'google', callbackURL: '/gamehome' })">
                        <Icon name="mage:google" size="30" style="fill: #000;" /> Google
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.social({ provider: 'discord', callbackURL: '/gamehome' })">
                        <Icon name="meteor-icons:discord" size="30" style="fill: #000;" /> Discord
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.social({ provider: 'twitch', callbackURL: '/gamehome' })">
                        <Icon name="mdi:twitch" size="30" style="fill: #000;" /> Twitch
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.social({ provider: 'twitter', callbackURL: '/gamehome' })">
                        <Icon name="prime:twitter" size="24" style="fill: #000;" /> Twitter
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.oauth2({ providerId: 'spotify', callbackURL: '/gamehome' })">
                        <Icon name="line-md:spotify" size="30" style="fill: #000;" />Spotify
                    </button>
                    <button v-if="!session?.data"
                        @click="() => authClient.signIn.oauth2({ providerId: 'yahoo', callbackURL: '/gamehome' })">
                        <Icon name="jam:yahoo" size="34" style="fill: #000;" /> Yahoo
                    </button>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authClient } from "../lib/auth-client";
import { useRouter } from 'vue-router';

const session = authClient.useSession()
const isRegistering = ref(false)
const loginMethod = ref('email')
const email = ref('')
const password = ref('')
const name = ref('')
const username = ref('')
const router = useRouter();
const errorMessage = ref('')
const emailError = ref('')
const passwordError = ref('')
const usernameError = ref('')

const validateForm = () => {
    let isValid = true
    emailError.value = ''
    passwordError.value = ''
    usernameError.value = ''

    if (loginMethod.value === 'email' && !email.value) {
        emailError.value = 'errors.emailRequired'
        isValid = false
    }
    if (!password.value) {
        passwordError.value = 'errors.passwordRequired'
        isValid = false
    }
    if (loginMethod.value === 'username' && !username.value) {
        usernameError.value = 'errors.usernameRequired'
        isValid = false
    }
    return isValid
}

const handleLogin = async () => {
    if (!validateForm()) return

    try {
        let result;
        if (loginMethod.value === 'email') {
            result = await authClient.signIn.email({
                email: email.value,
                password: password.value
            })
        } else {
            result = await authClient.signIn.username({
                username: username.value,
                password: password.value
            })
        }

        if (result.error) throw result.error

        router.push('/gamehome')
    } catch (error) {
        console.error('Login error:', error)
        errorMessage.value = 'errors.loginFailed'
    }
}

const handleRegister = async () => {
    try {
        const { data, error } = await authClient.signUp.email({
            email: email.value,
            password: password.value,
            name: name.value,
            username: username.value
        })
        if (error) throw error
        isRegistering.value = false
    } catch (error) {
        console.error('Registration error:', error)
        errorMessage.value = 'errors.registrationFailed'
    }
}

const handleForgotPassword = async () => {
    try {
        const { data, error } = await authClient.forgetPassword({
            email: email.value,
            redirectTo: '/reset-password'
        })
        if (error) throw error
        errorMessage.value = 'errors.passwordResetSuccess'
    } catch (error) {
        console.error('Password reset error:', error)
        errorMessage.value = 'errors.passwordResetFailed'
    }
}
</script>

<style scoped>
.auth-form {
    margin: 2rem auto;
    padding: 2rem;
    background-color: var(--background-color);
    color: var(--text-color);
}

h2 {
    font-size: var(--header-font-size);
    margin-bottom: var(--padding-medium);
    color: var(--text-color);
    text-align: center;
}

.social-login-title {
    text-align: center;
    margin-bottom: var(--padding-medium);
}

.form-group {
    margin-bottom: var(--padding-medium);
}

.form-control,
input,
select {
    width: 100%;
    min-height: 44px;
    padding: 0.5rem 1rem;
    font-size: var(--body-font-size);
    color: var(--text-color);
    background-color: var(--background-color);
    border: 2px solid var(--highlight-color);
    border-radius: var(--border-radius);
    transition: border-color var(--transition-speed);
}

.form-control:focus,
input:focus,
select:focus {
    outline: none;
    border-color: var(--button-hover-color);
}

button[type="submit"] {
    width: 100%;
    min-height: var(--min-touch-target);
    padding: var(--padding-small) var(--padding-medium);
    font-size: var(--button-font-size);
    color: var(--button-text-color);
    background-color: var(--highlight-color);
    border: none;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: background-color var(--transition-speed);
}

button[type="submit"]:hover {
    background-color: var(--button-hover-color);
}

a {
    display: inline-block;
    margin-top: var(--padding-small);
    color: var(--highlight-color);
    text-decoration: none;
    transition: color var(--transition-speed);
}

a:hover {
    color: var(--button-hover-color);
}

small {
    display: block;
    margin-top: 0.5rem;
    color: var(--text-color);
    opacity: 0.8;
}

/* Social Login Buttons */
button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 300px;
    margin: var(--padding-small) 0;
    min-height: var(--min-touch-target);
    padding: var(--padding-small) var(--padding-medium);
    font-size: var(--button-font-size);
    color: var(--button-text-color);
    background-color: var(--highlight-color);
    border: none;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: background-color var(--transition-speed);
}

button:hover {
    background-color: var(--button-hover-color);
}

.social-login-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--padding-small);
    margin-top: var(--padding-medium);
}

.error-message {
    color: var(--error-color);
    background-color: var(--error-bg);
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
    font-weight: bold;
}

input:focus,
select:focus,
button:focus {
    outline: 3px solid var(--highlight-color);
    outline-offset: 2px;
}

@media (min-width: 768px) {
    .social-login-group {
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
    }

    button {
        flex: 0 0 calc(50% - var(--padding-small));
        margin: var(--padding-small);
    }
}
</style>
