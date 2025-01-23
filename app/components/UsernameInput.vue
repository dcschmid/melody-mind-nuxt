<template>
    <div 
        class="username-input" 
        v-if="!hasUsername"
        :class="{ 'reduce-motion': prefersReducedMotion }"
    >
        <h2 id="username-title">{{ $t('username.title') }}</h2>
        <form 
            @submit.prevent="saveUsername" 
            class="username-form"
            aria-labelledby="username-title"
            novalidate
        >
            <div class="form-group">
                <label 
                    for="username-input"
                    class="username-label"
                >
                    {{ $t('username.label') }}
                </label>
                <div class="input-wrapper">
                    <input 
                        id="username-input"
                        ref="usernameInput"
                        type="text" 
                        v-model="username" 
                        :placeholder="$t('username.placeholder')"
                        :aria-describedby="validationMessage ? 'validation-message' : undefined"
                        :aria-invalid="!!validationMessage"
                        required
                        minlength="2"
                        maxlength="20"
                        autocomplete="username"
                        @input="validateUsername"
                        @blur="validateUsername"
                    >
                    <div 
                        v-if="validationMessage"
                        id="validation-message"
                        class="validation-message"
                        role="alert"
                    >
                        {{ validationMessage }}
                    </div>
                </div>
            </div>
            <button 
                type="submit" 
                class="save-button"
                :disabled="!isValid || isSubmitting"
                :aria-busy="isSubmitting"
            >
                <span>{{ $t('username.submit') }}</span>
                <Icon
                    name="material-symbols:arrow-forward-rounded"
                    class="button-icon"
                    size="24"
                    aria-hidden="true"
                />
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const emit = defineEmits(['usernameSet'])

const username = ref('')
const hasUsername = ref(false)
const validationMessage = ref('')
const isValid = ref(false)
const isSubmitting = ref(false)
const prefersReducedMotion = ref(false)
const usernameInput = ref<HTMLInputElement | null>(null)

onMounted(() => {
    // Check stored username
    const storedUsername = localStorage.getItem('username')
    if (storedUsername) {
        username.value = storedUsername
        hasUsername.value = true
        emit('usernameSet')
    } else {
        // Focus input if no stored username
        usernameInput.value?.focus()
    }

    // Check for reduced motion preference
    prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    // Listen for changes in motion preferences
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
        prefersReducedMotion.value = e.matches
    })
})

const validateUsername = () => {
    const value = username.value.trim()
    
    if (!value) {
        validationMessage.value = t('username.errors.required')
        isValid.value = false
        return
    }

    if (value.length < 2) {
        validationMessage.value = t('username.errors.tooShort')
        isValid.value = false
        return
    }

    if (value.length > 20) {
        validationMessage.value = t('username.errors.tooLong')
        isValid.value = false
        return
    }

    if (!/^[a-zA-Z0-9_-]+$/.test(value)) {
        validationMessage.value = t('username.errors.invalidChars')
        isValid.value = false
        return
    }

    validationMessage.value = ''
    isValid.value = true
}

const saveUsername = async () => {
    validateUsername()
    
    if (!isValid.value) {
        usernameInput.value?.focus()
        return
    }

    try {
        isSubmitting.value = true
        const trimmedUsername = username.value.trim()
        
        // Simulate a delay to show loading state
        if (!prefersReducedMotion.value) {
            await new Promise(resolve => setTimeout(resolve, 300))
        }
        
        localStorage.setItem('username', trimmedUsername)
        hasUsername.value = true
        emit('usernameSet')
        
        // Announce success to screen readers
        const announcement = new CustomEvent('announce', {
            detail: {
                message: t('username.success', { username: trimmedUsername }),
                priority: 'polite'
            }
        })
        document.dispatchEvent(announcement)
    } catch (error) {
        validationMessage.value = t('username.errors.saveFailed')
        console.error('Failed to save username:', error)
    } finally {
        isSubmitting.value = false
    }
}

// Expose the hasUsername state
defineExpose({
    hasUsername
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.username-input {
    @include font-smoothing;
    @include container(400px);
    @include glass-morphism;
    @include content-width(400px);
    text-align: center;
    margin: 2rem auto;
    padding: 2rem;
    border-radius: 1rem;
    color: var(--text-color);

    h2 {
        margin-bottom: 1.5rem;
        font-size: max(1.5rem, 24px);
        font-weight: 700;
        line-height: 1.3;
        letter-spacing: 0.01em;
    }
}

.username-form {
    @include flex-column;
    gap: 1.5rem;
}

.form-group {
    text-align: left;
}

.username-label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: max(1.125rem, 18px);
    font-weight: 500;
    color: var(--text-color);
}

.input-wrapper {
    position: relative;
}

input {
    @include input-base;
    @include input-placeholder;
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: max(1.125rem, 18px);
    line-height: 1.5;
    border: 2px solid var(--border-color);
    border-radius: 0.5rem;
    background-color: var(--surface-color);
    color: var(--text-color);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;

    &:hover:not(:disabled) {
        border-color: var(--border-hover-color);
    }

    &:focus {
        outline: none;
        border-color: var(--focus-color);
        box-shadow: 0 0 0 3px var(--focus-ring-color);
    }

    &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    &[aria-invalid="true"] {
        border-color: var(--error-color);
        
        &:focus {
            box-shadow: 0 0 0 3px var(--error-ring-color);
        }
    }

    .reduce-motion & {
        transition: none;
    }
}

.validation-message {
    position: absolute;
    top: 100%;
    left: 0;
    margin-top: 0.25rem;
    font-size: max(0.875rem, 14px);
    color: var(--error-color);
    font-weight: 500;
}

.save-button {
    @include button-primary;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem 1.5rem;
    font-size: max(1.125rem, 18px);
    font-weight: 600;
    line-height: 1.5;
    border-radius: 0.5rem;
    
    &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    &[aria-busy="true"] {
        position: relative;
        
        .button-icon {
            animation: spin 1s linear infinite;
        }
    }

    .reduce-motion & {
        transition: none;

        &[aria-busy="true"] .button-icon {
            animation: none;
        }
    }
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

/* High contrast mode */
@media (forced-colors: active) {
    .username-input {
        border: 2px solid CanvasText;
    }

    input {
        border: 2px solid CanvasText;
        
        &:focus {
            outline: 2px solid Highlight;
            outline-offset: 2px;
        }
    }

    .save-button {
        border: 2px solid ButtonText;
        
        &:disabled {
            opacity: 1;
            color: GrayText;
            border-color: GrayText;
        }
    }
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    .username-input {
        background-color: color-mix(in srgb, var(--surface-color) 85%, #000);
    }

    input {
        background-color: color-mix(in srgb, var(--surface-color) 90%, #000);
    }
}

/* Print mode */
@media print {
    .username-input {
        background: none;
        border: 1px solid #000;
        margin: 1rem 0;
        padding: 1rem;
    }

    input {
        border: 1px solid #000;
        background: none;
    }

    .save-button {
        display: none;
    }
}

/* Mobile optimizations */
@media (max-width: 768px) {
    .username-input {
        margin: 1rem auto;
        padding: 1.5rem;

        h2 {
            font-size: max(1.25rem, 20px);
        }
    }

    .username-label {
        font-size: max(1rem, 16px);
    }

    input {
        font-size: max(1rem, 16px);
        padding: 0.625rem 0.875rem;
    }

    .save-button {
        font-size: max(1rem, 16px);
        padding: 0.625rem 1.25rem;
    }
}

/* Increased contrast mode */
@media screen and (prefers-contrast: more) {
    .username-input {
        border: 2px solid currentColor;
    }

    input {
        border-width: 2px;
    }

    .username-label {
        font-weight: 600;
    }

    .validation-message {
        font-weight: 600;
    }
}
</style>
