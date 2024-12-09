<template>
    <div>
        <h1>Welcome to the homepage</h1>
        <AppAlert>
            This is an auto-imported component
        </AppAlert>

        <form v-if="!isRegistering" @submit.prevent="handleLogin" class="auth-form">
            <h2>Anmelden</h2>
            <div class="form-group">
                <select v-model="loginMethod" class="form-control">
                    <option value="email">Mit E-Mail anmelden</option>
                    <option value="username">Mit Benutzername anmelden</option>
                </select>
            </div>
            <div class="form-group" v-if="loginMethod === 'email'">
                <input type="email" v-model="email" placeholder="E-Mail" required>
            </div>
            <div class="form-group" v-else>
                <input type="text" v-model="username" placeholder="Benutzername" required>
            </div>
            <div class="form-group">
                <input type="password" v-model="password" placeholder="Passwort" required>
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
                <button v-if="!session?.data" @click="() => authClient.signIn.social({ provider: 'github' })">
                    Continue with GitHub
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.social({ provider: 'google' })">
                    Continue with Google
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.social({ provider: 'discord' })">
                    Continue with Discord
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.social({ provider: 'twitch' })">
                    Continue with Twitch
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.social({ provider: 'twitter' })">
                    Continue with Twitter
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.oauth2({ providerId: 'spotify' })">
                    Mit Spotify fortfahren
                </button>
                <button v-if="!session?.data" @click="() => authClient.signIn.oauth2({ providerId: 'yahoo' })">
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

const session = authClient.useSession()
const isRegistering = ref(false)
const loginMethod = ref('email')
const email = ref('')
const password = ref('')
const name = ref('')
const username = ref('')

const handleLogin = async () => {
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
    } catch (error) {
        console.error('Login error:', error)
        alert('Login fehlgeschlagen')
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
        alert('Registrierung fehlgeschlagen')
    }
}

const handleForgotPassword = async () => {
    try {
        const { data, error } = await authClient.forgetPassword({
            email: email.value,
            redirectTo: '/reset-password'
        })
        if (error) throw error
        alert('Überprüfen Sie Ihre E-Mail für weitere Anweisungen')
    } catch (error) {
        console.error('Password reset error:', error)
        alert('Passwort-Reset fehlgeschlagen')
    }
}
</script>

<style scoped>
.auth-form {
    max-width: var(--max-line-length);
    margin: 0 auto;
    padding: var(--padding-large);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
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
    min-height: var(--min-touch-target);
    padding: var(--padding-small);
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
</style>
