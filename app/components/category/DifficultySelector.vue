<template>
    <div class="difficultySection">
        <div class="game-modes">
            <h2 id="difficulty-heading" class="difficulty-title buttonHeadline">
                {{ $t('category.difficulty.title') }}
            </h2>
            <div class="mode-selector">
                <button 
                    class="mode-button" 
                    :class="{ active: !isMultiplayer }"
                    @click="isMultiplayer = false"
                    :aria-label="$t('category.mode.singleplayer')"
                >
                    <Icon name="mdi:account" size="24" />
                    {{ $t('category.mode.singleplayer') }}
                </button>
                <button 
                    class="mode-button" 
                    :class="{ active: isMultiplayer }"
                    @click="isMultiplayer = true"
                    :aria-label="$t('category.mode.multiplayer')"
                >
                    <Icon name="mdi:account-group" size="24" />
                    {{ $t('category.mode.multiplayer') }}
                </button>
            </div>
        </div>

        <div class="buttonGroup" role="group" aria-label="Schwierigkeitsgrade">
            <NuxtLink 
                v-for="difficulty in ['easy', 'medium', 'hard']" 
                :key="difficulty"
                :to="getDifficultyPath(difficulty)" 
                class="difficulty-button button"
                :aria-label="$t(`category.difficulty.${difficulty}.label`)"
            >
                <Icon name="mdi:play-outline" size="36" />
                {{ $t(`category.difficulty.${difficulty}`) }}
            </NuxtLink>
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    categorySlug: string
}>()

const localePath = useLocalePath()
const isMultiplayer = ref(false)

const getDifficultyPath = (difficulty: string) => {
    const basePath = isMultiplayer.value ? '/multiplayer/game-' : '/game-'
    return localePath(`${basePath}${props.categorySlug}/${difficulty}`)
}</script>

<style scoped lang="scss">
@use '@/assets/scss/mixins' as *;

.difficultySection {
    @include grid-center;
    width: 100%;
    margin-bottom: var(--padding-large);
}

.game-modes {
    @include grid-center;
    gap: var(--padding-medium);
    margin-bottom: var(--padding-large);
}

.difficulty-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
}

.mode-selector {
    display: flex;
    gap: var(--padding-small);
    justify-content: center;
    flex-wrap: wrap;
}

.mode-button {
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    padding: var(--padding-small) var(--padding-medium);
    border: 2px solid var(--primary-color);
    border-radius: var(--border-radius);
    background: transparent;
    color: var(--text-color);
    font-size: var(--font-size-responsive-md);
    cursor: pointer;
    transition: all var(--transition-speed) var(--transition-bounce);

    &:hover {
        background: var(--primary-color);
        color: var(--button-text-color);
    }

    &.active {
        background: var(--primary-color);
        color: var(--button-text-color);
    }
}

.buttonGroup {
    @include flex-container;
    flex-wrap: wrap;
    gap: var(--padding-small);

    .difficulty-button {
        @include button-primary;
        min-height: var(--min-touch-target);
        flex: 1;
        max-width: var(--max-button-width, 200px);
        text-decoration: none;
        font-size: var(--font-size-responsive-md);
        font-weight: var(--font-weight-semibold);
    }
}
</style>
