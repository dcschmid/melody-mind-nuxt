<template>
    <div class="difficultySection">
        <h2 id="difficulty-heading" class="buttonHeadline">
            {{ $t('category.difficulty.title') }}
        </h2>
        <div class="buttonGroup" role="group" aria-label="Schwierigkeitsgrade">
            <NuxtLink v-for="difficulty in ['easy', 'medium', 'hard']" :key="difficulty"
                :to="getDifficultyPath(difficulty)" class="button"
                :aria-label="$t(`category.difficulty.${difficulty}.label`)">
                <Icon name="mdi:play-outline" size="36" /> {{ $t(`category.difficulty.${difficulty}`) }}
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    categorySlug: string
}>()

const localePath = useLocalePath()

const getDifficultyPath = (difficulty: string) => {
    return localePath(`/game-${props.categorySlug}/${difficulty}`)
}
</script>

<style scoped lang="scss">
@use '@/assets/scss/mixins' as *;

.difficultySection {
    display: grid;
    gap: var(--padding-medium);
    place-items: center;
    width: 100%;
    padding: 0 var(--padding-medium);
}

.buttonHeadline {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
    text-align: center;
}

.buttonGroup {
    display: flex;
    flex-wrap: wrap;
    gap: var(--padding-medium);
    width: 100%;
    margin: 0 auto;
    justify-content: center;

    .button {
        @include button-primary;
        min-height: var(--min-touch-target);
        gap: var(--padding-small);
        flex: 1;
        max-width: 200px;
    }
}
</style>
