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
    @include grid-center;
    width: 100%;
    padding: 0 var(--padding-medium);
    margin-bottom:  var(--padding-large)
}

.buttonHeadline {
    @include heading-style;
    text-align: center;
}

.buttonGroup {
    @include flex-container;
    flex-wrap: wrap;
    gap: var(--padding-small);

    .button {
        @include button-primary;
        min-height: var(--min-touch-target);
        flex: 1;
        max-width: 200px;
        text-decoration: none;
    }
}
</style>
