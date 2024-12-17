<template>
    <ul class="rules-list">
        <slot></slot>
    </ul>
</template>

<style lang="scss" scoped>
.rules-list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin-bottom: var(--padding-medium);

    ::v-deep(li) {
        font-size: var(--body-font-size);
        line-height: var(--line-height-body);
        color: var(--text-secondary);
        margin-bottom: var(--padding-small);

        strong {
            color: var(--text-color);
            font-weight: 600;
        }
    }
}

@media (max-width: 768px) {
    .rules-list {
        padding-left: var(--padding-medium);
    }
}
</style>
