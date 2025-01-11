<template>
    <NuxtPage />
</template>

<style>
.page-enter-active,
.page-leave-active {
    transition: opacity 1s ease, transform 1s ease;
}

.page-enter-from,
.page-leave-to {
    opacity: 0;
    transform: translateX(200px);
}

.page-enter-to,
.page-leave-from {
    opacity: 1;
    transform: translateX(0);
}
</style>
