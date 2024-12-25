<template>
    <Form @submit="(values) => handleRegister(values as RegisterCredentials)" 
          v-slot="{ errors }" 
          class="auth-form" 
          aria-labelledby="register-title">
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
            <label :for="'register-username'" class="form-label">{{ $t('register.usernameLabel') }}</label>
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
                    <p class="error-message" :id="'register-username-error'" role="alert">{{ message }}</p>
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
            <label :for="'register-password'" class="form-label">{{ $t('register.passwordLabel') }}</label>
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
                    <p class="error-message" :id="'register-password-error'" role="alert">{{ message }}</p>
                </template>
            </ErrorMessage>
        </div>

        <button type="submit" class="submit-button" :aria-busy="formState.isSubmitting"
            :disabled="formState.isSubmitting">
            {{ $t('register.submitButton') }}
        </button>

        <div class="auth-links">
            <a href="#" @click.prevent="$emit('switch-form', 'login')" class="link">
                <Icon name="material-symbols:login" size="20" aria-hidden="true" />
                <span>{{ $t('register.hasAccount') }}</span>
            </a>
        </div>

        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
            {{ $t(formState.errorMessage) }}
        </div>
    </Form>
</template>

<script setup lang="ts">
import { useAuthForm } from '~/composables/useAuthForm'
import { useAuth, type RegisterCredentials } from '~/composables/useAuth'
import { Form, Field, ErrorMessage } from 'vee-validate'

const { formState, validators } = useAuthForm()
const { handleRegister } = useAuth()

defineEmits<{
    'switch-form': [form: 'login']
}>()
</script>

<style lang="scss">
@use '@/assets/scss/components/_auth-forms.scss';
</style>
