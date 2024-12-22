import { reactive, computed } from 'vue'
import type { ComputedRef } from 'vue'
import { useI18n } from 'vue-i18n'

/**
 * Interface for the authentication form state
 */
interface AuthFormState {
  email: string
  password: string
  name: string
  username: string
  isSubmitting: boolean
  isRegistering: boolean
  showForgotPassword: boolean
  errorMessage: string
}

/**
 * Type for form field validation functions
 * Returns true if valid, or an error message string if invalid
 */
type ValidationFunction = (value: unknown) => string | true

/**
 * Interface for form validators
 */
interface FormValidators {
  email: ValidationFunction
  password: ValidationFunction
  username: ValidationFunction
  name: ValidationFunction
}

/**
 * Interface for the auth form composable return type
 */
interface AuthFormComposable {
  formState: AuthFormState
  validators: FormValidators
  showLoginForm: ComputedRef<boolean>
  showRegisterForm: ComputedRef<boolean>
  showForgotPasswordForm: ComputedRef<boolean>
}

/**
 * Composable for managing authentication form state and validation
 * @returns {AuthFormComposable} Form state, validators, and computed view states
 */
export const useAuthForm = (): AuthFormComposable => {
  const { t } = useI18n()

  const formState = reactive<AuthFormState>({
    email: '',
    password: '',
    name: '',
    username: '',
    isSubmitting: false,
    isRegistering: false,
    showForgotPassword: false,
    errorMessage: ''
  })

  /**
   * Form field validators with specific validation rules
   */
  const validators: FormValidators = {
    /**
     * Validates email format
     * @param value - The email value to validate
     * @returns {string | true} True if valid, error message if invalid
     */
    email: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('login.error.required')
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return t('login.error.invalidEmail')
      return true
    },

    /**
     * Validates password requirements
     * @param value - The password value to validate
     * @returns {string | true} True if valid, error message if invalid
     */
    password: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('login.error.required')
      if (value.length < 8) return t('login.error.invalidPassword')
      return true
    },

    /**
     * Validates username requirements
     * @param value - The username value to validate
     * @returns {string | true} True if valid, error message if invalid
     */
    username: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('register.error.usernameRequired')
      if (value.length < 3) return t('register.error.usernameTooShort')
      if (value.length > 20) return t('register.error.usernameTooLong')
      if (!/^[a-zA-Z0-9_-]+$/.test(value)) return t('register.error.invalidUsername')
      return true
    },

    /**
     * Validates display name requirements
     * @param value - The name value to validate
     * @returns {string | true} True if valid, error message if invalid
     */
    name: (value: unknown): string | true => {
      if (!value || typeof value !== 'string') return t('register.error.nameRequired')
      if (value.length < 2) return t('register.error.nameTooShort')
      return true
    }
  }

  // Computed properties for form visibility
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
