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
.username-input {
    text-align: center;
    margin: 2rem auto;
    max-width: 400px;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    backdrop-filter: blur(10px);

    h2 {
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        color: white;
    }
}

.username-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;

    input {
        padding: 0.75rem 1rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 1rem;

        &:focus {
            outline: none;
            border-color: var(--primary-color);
        }

        &::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
    }

    .save-button {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        
        svg {
            transition: transform 0.3s ease;
        }

        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

            svg {
                transform: translateX(4px);
            }
        }

        &:active {
            transform: translateY(0);
        }
    }
}
</style>
