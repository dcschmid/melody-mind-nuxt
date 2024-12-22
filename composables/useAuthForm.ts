import { reactive, computed } from 'vue'
import { useI18n } from 'vue-i18n'

export const useAuthForm = () => {
  const { t } = useI18n()

  const formState = reactive({
    email: '',
    password: '',
    name: '',
    username: '',
    isSubmitting: false,
    isRegistering: false,
    showForgotPassword: false,
    errorMessage: ''
  })

  const validators = {
    email: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('login.error.required')
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return t('login.error.invalidEmail')
      return true
    },
    password: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('login.error.required')
      if (value.length < 8) return t('login.error.invalidPassword')
      return true
    },
    username: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('register.error.usernameRequired')
      if (value.length < 3) return t('register.error.usernameTooShort')
      if (value.length > 20) return t('register.error.usernameTooLong')
      if (!/^[a-zA-Z0-9_-]+$/.test(value)) return t('register.error.invalidUsername')
      return true
    },
    name: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('register.error.nameRequired')
      if (value.length < 2) return t('register.error.nameTooShort')
      return true
    }
  }

  const showLoginForm = computed(() => !formState.isRegistering && !formState.showForgotPassword)
  const showRegisterForm = computed(() => formState.isRegistering && !formState.showForgotPassword)
  const showForgotPasswordForm = computed(() => formState.showForgotPassword)

  return {
    formState,
    validators,
    showLoginForm,
    showRegisterForm,
    showForgotPasswordForm
  }
}
