<template>
    <section class="intro" v-if="category">
        <h1>{{ category.headline }} {{ $t('category.selected') }}</h1>
        <p>{{ category.introSubline }}</p>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    category: {
        headline: string
        introSubline: string
    } | null
}>()
</script>

<style scoped lang="scss">
.intro {
    text-align: center;
    margin-bottom: clamp(var(--padding-medium), 5vw, var(--padding-large));

    h1 {
        font-size: var(--header-font-size);
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: var(--padding-medium);
    }

    p {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-secondary);
    }
}
</style>
