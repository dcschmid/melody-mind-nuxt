import { useAuthForm } from './useAuthForm'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { authClient } from "../lib/auth-client"

/**
 * Interface for basic login credentials
 * @interface LoginCredentials
 */
export interface LoginCredentials {
  /** User's email address */
  email: string
  /** User's password */
  password: string
}

/**
 * Interface for registration credentials, extends login credentials
 * @interface RegisterCredentials
 * @extends {LoginCredentials}
 */
export interface RegisterCredentials extends LoginCredentials {
  /** User's display name */
  name: string
  /** User's unique username */
  username: string
}

/**
 * Composable for handling authentication operations
 * @returns Authentication methods for login, registration, and password recovery
 */
export const useAuth = () => {
  const { formState } = useAuthForm()
  const router = useRouter()
  const { t } = useI18n()

  /**
   * Sets an error message and logs the error
   * @param {string} key - The key for the error message translation
   * @param {any} error - The error object to log
   */
  const setError = (key: string, error: any) => {
    console.error(`${key} error:`, error)
    formState.errorMessage = `errors.${key}Failed`
  }

  /**
   * Handles user login
   * @param {LoginCredentials} credentials - The user's login credentials
   * @throws Will throw an error if login fails
   */
  const handleLogin = async ({ email, password }: LoginCredentials) => {
    try {
      formState.isSubmitting = true
      formState.errorMessage = ''

      await authClient.signIn.email({ email, password })
      await router.push('/gamehome')
    } catch (error: any) {
      setError('login', error)
    } finally {
      formState.isSubmitting = false
    }
  }

  /**
   * Handles user registration
   * @param {RegisterCredentials} credentials - The user's registration information
   * @throws Will throw an error if registration fails
   */
  const handleRegister = async ({ email, password, name, username }: RegisterCredentials) => {
    try {
      formState.isSubmitting = true
      formState.errorMessage = ''

      const { error } = await authClient.signUp.email({
        email,
        password,
        name,
        username
      })

      if (error) throw error

      // After successful registration, sign in automatically
      await authClient.signIn.email({ email, password })
      await router.push('/gamehome')
    } catch (error: any) {
      setError('registration', error)
    } finally {
      formState.isSubmitting = false
    }
  }


  return {
    handleLogin,
    handleRegister
  }
}
