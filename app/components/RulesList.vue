<template>
    <ul 
        class="rules-list"
        role="list"
        :aria-label="title || $t('common.rulesList')"
    >
        <slot></slot>
    </ul>
</template>

<script setup lang="ts">
interface Props {
    title?: string
}

defineProps<Props>()
</script>

<style lang="scss" scoped>
.rules-list {
    list-style-type: disc;
    padding-left: var(--padding-large);
    margin-bottom: var(--padding-medium);
    max-width: var(--max-line-length);
    font-size: var(--font-size-base);
    line-height: var(--line-height-relaxed);

    ::v-deep(li) {
        position: relative;
        font-size: var(--font-size-base);
        margin-bottom: var(--padding-small);
        padding-left: calc(var(--padding-small) / 2);

        &::marker {
            color: var(--text-color);
            font-size: var(--font-size-responsive-md);
        }

        &::before {
            content: "•";
            position: absolute;
            left: calc(-1 * var(--padding-medium));
            color: var(--text-color);
            font-size: var(--font-size-responsive-md);
        }

        strong {
            color: var(--text-color);
            font-weight: var(--font-weight-semibold);
        }

        a {
            color: var(--primary-color);
            text-decoration: underline;
            text-underline-offset: var(--spacing-text);
            transition: color var(--transition-speed) var(--transition-bounce);

            &:hover,
            &:focus {
                color: var(--primary-color-dark);
                text-decoration-thickness: 0.125em;
            }

            &:focus-visible {
                outline: var(--focus-outline-width) solid var(--focus-outline-color);
                outline-offset: var(--focus-outline-offset);
                border-radius: var(--border-radius);
            }
        }
    }
}

@media (prefers-contrast: more) {
    .rules-list {
        ::v-deep(li) {
            color: var(--text-color);
            
            &::marker,
            &::before {
                color: currentColor;
            }

            strong {
                color: var(--text-color);
                font-weight: var(--font-weight-bold);
            }

            a {
                color: var(--primary-color-dark);
                text-decoration-thickness: 0.125em;

                &:hover,
                &:focus {
                    color: var(--primary-color);
                    text-decoration-thickness: 0.2em;
                }
            }
        }
    }
}

@media (prefers-reduced-motion: reduce) {
    .rules-list {
        ::v-deep(li) {
            a {
                transition: none;
            }
        }
    }
}

@media (max-width: 768px) {
    .rules-list {
        padding-left: var(--padding-medium);

        ::v-deep(li) {
            font-size: var(--font-size-base);
            margin-bottom: var(--padding-small);
        }
    }
}

@media print {
    .rules-list {
        padding-left: var(--padding-medium);

        ::v-deep(li) {
            color: var(--button-text-color);
            page-break-inside: avoid;

            a {
                color: var(--button-text-color);
                text-decoration: underline;
            }
        }
    }
}
</style>
