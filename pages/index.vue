<template>
    <div role="main">
        <h1>Willkommen</h1>
        <AppAlert>This is an auto-imported component
        </AppAlert>

        <form v-if="!isRegistering" @submit.prevent="handleLogin" class="auth-form" aria-labelledby="login-title">
            <h2 id="login-title">Anmelden</h2>
            <div v-if="errorMessage" class="error-message" role="alert" aria-live="assertive">
                {{ errorMessage }}
            </div>
            <div class="form-group">
                <label for="login-method">Anmeldemethode wählen</label>
                <select id="login-method" v-model="loginMethod" class="form-control"
                    aria-describedby="login-method-description">
                    <option value="email">Mit E-Mail anmelden</option>
                    <option value="username">Mit Benutzername anmelden</option>
                </select>
            </div>
            <div class="form-group" v-if="loginMethod === 'email'">
                <label for="email">E-Mail Adresse</label>
                <input type="email" id="email" v-model="email" aria-required="true" :aria-invalid="!!emailError">
                <span v-if="emailError" class="error-message">{{ emailError }}</span>
            </div>
            <div class="form-group" v-else>
                <label for="username">Benutzername</label>
                <input type="text" id="username" v-model="username" placeholder="Benutzername" required :aria-invalid="!!usernameError">
                <span v-if="usernameError" class="error-message">{{ usernameError }}</span>
            </div>
            <div class="form-group">
                <label for="password">Passwort</label>
                <input type="password" id="password" v-model="password" placeholder="Passwort" required :aria-invalid="!!passwordError">
                <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
            </div>
            <button type="submit">Anmelden</button>
            <p>
                <a href="#" @click.prevent="isRegistering = true">Noch kein Konto? Registrieren</a>
            </p>
            <p>
                <a href="#" @click.prevent="handleForgotPassword">Passwort vergessen?</a>
            </p>
        </form>

        <!-- Registrierungs Formular -->
        <form v-else @submit.prevent="handleRegister" class="auth-form">
            <h2>Registrieren</h2>
            <div v-if="errorMessage" class="error-message" role="alert" aria-live="assertive">
                {{ errorMessage }}
            </div>
            <div class="form-group">
                <input type="text" v-model="name" placeholder="Name" required>
            </div>
            <div class="form-group">
                <input type="text" v-model="username" placeholder="Benutzername" required>
                <small>Mindestens 3 Zeichen, maximal 20 Zeichen</small>
            </div>
            <div class="form-group">
                <input type="email" v-model="email" placeholder="E-Mail" required>
            </div>
            <div class="form-group">
                <input type="password" v-model="password" placeholder="Passwort" required>
            </div>
            <button type="submit">Registrieren</button>
            <p>
                <a href="#" @click.prevent="isRegistering = false">Bereits registriert? Anmelden</a>
            </p>
        </form>
        <div>
            <div class="social-login-group">
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.social({ provider: 'github', callbackURL: '/gamehome' })">
                    Continue with GitHub
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.social({ provider: 'google', callbackURL: '/gamehome' })">
                    Continue with Google
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.social({ provider: 'discord', callbackURL: '/gamehome' })">
                    Continue with Discord
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.social({ provider: 'twitch', callbackURL: '/gamehome' })">
                    Continue with Twitch
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.social({ provider: 'twitter', callbackURL: '/gamehome' })">
                    Continue with Twitter
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.oauth2({ providerId: 'spotify', callbackURL: '/gamehome' })">
                    Mit Spotify fortfahren
                </button>
                <button v-if="!session?.data"
                    @click="() => authClient.signIn.oauth2({ providerId: 'yahoo', callbackURL: '/gamehome' })">
                    Mit Yahoo fortfahren
                </button>
            </div>
            <div>
                <pre>{{ session.data }}</pre>
                <button v-if="session.data" @click="authClient.signOut()">
                    Sign out
                </button>
            </div>
        </div>
    </div>
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
    emailError.value = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.'
    isValid = false
  }
  if (!password.value) {
    passwordError.value = 'Bitte geben Sie ein Passwort ein.'
    isValid = false
  }
  if (loginMethod.value === 'username' && !username.value) {
    usernameError.value = 'Bitte geben Sie einen Benutzernamen ein.'
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
    errorMessage.value = 'Login fehlgeschlagen. Bitte überprüfen Sie Ihre Eingaben.'
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
    errorMessage.value = 'Registrierung fehlgeschlagen. Bitte überprüfen Sie Ihre Eingaben.'
  }
}

const handleForgotPassword = async () => {
  try {
    const { data, error } = await authClient.forgetPassword({
      email: email.value,
      redirectTo: '/reset-password'
    })
    if (error) throw error
    errorMessage.value = 'Überprüfen Sie Ihre E-Mail für weitere Anweisungen.'
  } catch (error) {
    console.error('Password reset error:', error)
    errorMessage.value = 'Passwort-Reset fehlgeschlagen. Bitte versuchen Sie es erneut.'
  }
}
</script>

<style scoped>
.auth-form {
    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: var(--background-color);
    color: var(--text-color);
}

h2 {
    font-size: var(--header-font-size);
    margin-bottom: var(--padding-medium);
    color: var(--text-color);
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
    width: 100%;
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
</style>
