<template>
    <div class="username-input" v-if="!hasUsername">
        <h2>{{ $t('username.title') }}</h2>
        <form @submit.prevent="saveUsername" class="username-form">
            <input 
                type="text" 
                v-model="username" 
                :placeholder="$t('username.placeholder')"
                required
                minlength="2"
                maxlength="20"
            >
            <button type="submit" class="save-button">
                <span>{{ $t('username.submit') }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14"></path>
                    <path d="m12 5 7 7-7 7"></path>
                </svg>
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
const emit = defineEmits(['usernameSet'])
const username = ref('')
const hasUsername = ref(false)

onMounted(() => {
    const storedUsername = localStorage.getItem('username')
    if (storedUsername) {
        username.value = storedUsername
        hasUsername.value = true
        emit('usernameSet')
    }
})

const saveUsername = () => {
    if (username.value.trim()) {
        localStorage.setItem('username', username.value.trim())
        hasUsername.value = true
        emit('usernameSet')
    }
}

// Expose the hasUsername state
defineExpose({
    hasUsername
})
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.input-container {
    @include surface-card;
    @include responsive-container;
}

.username-input {
    @include font-smoothing;
    @include container(400px);
    @include glass-morphism;
    @include content-width(400px);
    @include input-base;
    text-align: center;
    margin: 2rem auto;
    padding: 2rem;
    border-radius: 1rem;

    h2 {
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        color: white;
    }
}

.username-form {
    @include flex-column;

    input {
        @include input-base;
        @include input-placeholder;
        @include border-focus;
        padding: 0.75rem 1rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        @include glass-morphism;
    }

    .save-button {
        @include button-primary;
        gap: 0.5rem;
    }
}
</style>
