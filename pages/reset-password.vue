<template>
  <div class="reset-password">
    <h2>Passwort zurücksetzen</h2>
    <form @submit.prevent="handleResetPassword" v-if="token">
      <div class="form-group">
        <input
          type="password"
          v-model="newPassword"
          placeholder="Neues Passwort"
          required
        >
      </div>
      <button type="submit">Passwort ändern</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authClient } from '../lib/auth-client'

const route = useRoute()
const router = useRouter()
const token = route.query.token
const newPassword = ref('')

const handleResetPassword = async () => {
  try {
    const { error } = await authClient.resetPassword({
      newPassword: newPassword.value,
    })
    if (error) throw error
    alert('Passwort wurde erfolgreich geändert')
    router.push('/')
  } catch (error) {
    console.error('Reset password error:', error)
    alert('Fehler beim Zurücksetzen des Passworts')
  }
}
</script> 
