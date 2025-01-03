<template>
    <div class="search-wrapper">
        <div class="search-input-container">
            <Icon name="ic:baseline-search" size="24" class="search-icon" aria-hidden="true" />
            <input 
                :id="id"
                :value="modelValue"
                type="search"
                class="filterInput"
                :placeholder="placeholder"
                :aria-label="placeholder"
                @input="$emit('update:modelValue', $event.target.value);$emit('input', $event)"
            />
        </div>
    </div>
</template>

<script setup>
defineProps({
    id: {
        type: String,
        default: 'search-input'
    },
    modelValue: {
        type: String,
        required: true
    },
    placeholder: {
        type: String,
        required: true
    }
})

defineEmits(['update:modelValue', 'input'])
</script>

<style scoped lang="scss">
.search-wrapper {
    max-width: min(600px, 90%);
    margin: 0 auto;
}

.search-input-container {
    position: relative;
    display: flex;
    align-items: center;

    .search-icon {
        position: absolute;
        left: var(--padding-medium);
        color: var(--text-secondary);
    }
}

.filterInput {
    width: 100%;
    padding: var(--padding-medium) var(--padding-medium) var(--padding-medium) calc(var(--padding-medium) * 3);
    font-size: var(--body-font-size);
    color: var(--text-color);
    background: var(--surface-color);
    border: 2px solid var(--secondary-color);
    border-radius: var(--border-radius);
    transition: all 0.3s var(--transition-bounce);

    &:focus {
        outline: none;
        border-color: var(--highlight-color);
        box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.2);
        transform: scale(1.01);
    }

    &::placeholder {
        color: var(--text-secondary);
    }
}
</style>
