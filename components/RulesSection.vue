<template>
    <section class="rules-section" :aria-labelledby="id">
        <h2 :id="id" class="section-title">
            <slot name="title"></slot>
        </h2>
        <slot></slot>
    </section>
</template>

<script setup>
defineProps({
    id: {
        type: String,
        required: true
    }
})
</script>

<style lang="scss" scoped>
.rules-section {
    margin-bottom: var(--padding-large);

    &:last-child {
        margin-bottom: 0;
    }
}

.section-title {
    font-size: calc(var(--header-font-size) * 0.8);
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
}

@media (max-width: 768px) {
    .section-title {
        font-size: calc(var(--header-font-size) * 0.7);
    }
}
</style>
