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

const { formState, validators } = useAuthForm()
const { handleLogin } = useAuth()

defineEmits<{
    'switch-form': [form: 'register']
}>()
</script>

<style lang="scss">
@use '@/assets/scss/components/_auth-forms.scss';
</style>
