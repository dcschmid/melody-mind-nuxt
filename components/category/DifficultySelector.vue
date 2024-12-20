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
}

.buttonHeadline {
    font-size: var(--header-font-size);
    font-weight: 700;
    color: var(--text-color);
}

.buttonGroup {
    display: flex;
    gap: clamp(var(--padding-small), 2vw, var(--padding-medium));
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    max-width: min(100%, 900px);
    margin: 0 auto;
    padding: var(--padding-medium) 0;

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
        flex: 1;
        min-width: clamp(200px, 25%, 300px);
        justify-content: center;

        &:hover {
            background: var(--button-hover-color);
            transform: translateY(-2px);
        }

        &:active {
            transform: translateY(0);
        }
    }
}

@media (width <=767px) {
    .buttonGroup {
        flex-direction: column;
        padding: var(--padding-small) 0;
        max-width: 350px;

        .button {
            width: 100%;
            min-width: 100%;
            padding: var(--padding-medium) var(--padding-medium);
        }
    }
}
</style>
