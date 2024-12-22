<template>
    <Form @submit="(values: any) => handleForgotPassword({ email: values.email })" 
          v-slot="{ errors }" 
          class="auth-form" 
          aria-labelledby="forgot-password-title">
        <h2 id="forgot-password-title">{{ $t('forgotPassword.title') }}</h2>

        <div class="form-group">
            <label :for="'forgot-password-email'" class="form-label">{{ $t('forgotPassword.emailLabel') }}</label>
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
                    <p class="error-message" :id="'forgot-password-email-error'" role="alert">{{ message }}</p>
                </template>
            </ErrorMessage>
        </div>

        <button type="submit" class="submit-button" :aria-busy="formState.isSubmitting"
            :disabled="formState.isSubmitting">
            {{ $t('forgotPassword.submitButton') }}
        </button>

        <div class="auth-links">
            <a href="#" @click.prevent="$emit('switch-form', 'login')" class="link">
                <Icon name="material-symbols:key-outline" size="20" aria-hidden="true" />
                <span>{{ $t('forgotPassword.backToLogin') }}</span>
            </a>
        </div>

        <div v-if="formState.errorMessage" class="form-error" role="alert" aria-live="polite">
            {{ $t(formState.errorMessage) }}
        </div>
    </Form>
</template>

<script setup lang="ts">
import { useAuthForm } from '~/composables/useAuthForm'
import { useAuth } from '~/composables/useAuth'
import { Form, Field, ErrorMessage } from 'vee-validate'

const { formState, validators } = useAuthForm()
const { handleForgotPassword } = useAuth()

defineEmits<{
    'switch-form': [form: 'login']
}>()
</script>

<style lang="scss">
@import '@/assets/scss/components/_auth-forms.scss';
</style>
