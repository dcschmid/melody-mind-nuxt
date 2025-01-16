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

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.search-wrapper {
    @include container(600px);
    max-width: min(600px, 90%);
    margin: 0 auto;
}

.search-input {
    @include input-base;
    @include scale-transition;
    padding-left: 2.5rem;

    &:focus {
        transform: scale(1.01);
    }
}

.search-icon {
    @include absolute-center;
    left: var(--padding-medium);
    transform: translateY(-50%);
    color: var(--text-secondary);
}

.search-input-container {
    @include font-smoothing;
    @include z-index('above');
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
    @include input-base;
    @include focus-ring;
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
        @include text-truncate;
        color: var(--text-secondary);
    }
}
</style>
