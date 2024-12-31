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
        background: var(--highlight-color);
        color: var(--button-text-color);
        padding: var(--padding-medium) var(--padding-large);
        border-radius: var(--border-radius);
        font-size: var(--button-font-size);
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: var(--padding-small);
        min-height: var(--min-touch-target);
        transition: all var(--transition-speed);
        box-shadow: var(--box-shadow);
        justify-content: center;
        text-align: center;
        flex: 1;
        min-width: 200px;
        max-width: 300px;

        &:hover {
            background: var(--button-hover-color);
            transform: translateY(-2px);
        }

        &:active {
            transform: translateY(0);
        }
    }
}
</style>
