<template>
    <div class="points-display">
        <div class="points-container">
            <span class="points" :class="{ 'points-update': isAnimating }">
                {{ formattedPoints }}
            </span>
            <span class="points-label">Punkte</span>
        </div>
        <transition name="bonus">
            <div v-if="showBonus" class="bonus-indicator">
                +{{ latestBonus }}
            </div>
        </transition>
    </div>
</template>

<script setup lang="ts">
const points = ref(0)
const isAnimating = ref(false)
const showBonus = ref(false)
const latestBonus = ref(0)

const formattedPoints = computed(() => {
    return points.value.toLocaleString()
})

const updatePoints = (newPoints: number) => {
    latestBonus.value = newPoints
    showBonus.value = true
    isAnimating.value = true

    points.value += newPoints

    setTimeout(() => {
        showBonus.value = false
        isAnimating.value = false
    }, 2000)
}

// Explizit die updatePoints-Methode exponieren
defineExpose({
    updatePoints
})
</script>

<style lang="scss" scoped>
.points-display {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--padding-small);
    padding: var(--padding-small);
}

.points-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.points {
    font-size: var(--header-font-size);
    font-weight: bold;
    color: var(--text-color);
    transition: transform 0.3s ease;

    &.points-update {
        transform: scale(1.2);
        color: var(--highlight-color);
    }
}

.points-label {
    font-size: var(--body-font-size);
    color: var(--text-color);
}

.bonus-indicator {
    position: absolute;
    top: -20px;
    right: 0;
    color: #FFD700;
    font-weight: bold;
    font-size: var(--body-font-size);
}

.bonus-enter-active,
.bonus-leave-active {
    transition: all 0.5s ease;
}

.bonus-enter-from {
    opacity: 0;
    transform: translateY(20px);
}

.bonus-leave-to {
    opacity: 0;
    transform: translateY(-20px);
}
</style> 
