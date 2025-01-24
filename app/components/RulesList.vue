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
    padding-left: clamp(1.5rem, 5vw, 2rem);
    margin-bottom: var(--padding-medium);
    max-width: 70ch; /* Optimale Lesebreite */
    font-size: var(--font-size-base);
    line-height: 1.6;

    ::v-deep(li) {
        position: relative;
        font-size: var(--font-size-base);
        margin-bottom: var(--padding-small);
        padding-left: 0.5rem;

        /* Verbesserte Marker-Sichtbarkeit */
        &::marker {
            color: var(--text-color);
            font-size: 1.2em;
        }

        /* Fallback für ältere Browser */
        &::before {
            content: "•";
            position: absolute;
            left: -1rem;
            color: var(--text-color);
            font-size: 1.2em;
        }

        strong {
            color: var(--text-color);
            font-weight: 600;
        }

        /* Links innerhalb der Liste */
        a {
            color: var(--link-color);
            text-decoration: underline;
            text-underline-offset: 0.2em;
            transition: color 0.2s ease;

            &:hover,
            &:focus {
                color: var(--link-hover-color);
                text-decoration-thickness: 0.125em;
            }

            &:focus-visible {
                outline: 3px solid var(--focus-ring-color);
                outline-offset: 2px;
                border-radius: 2px;
            }
        }
    }
}

/* High Contrast Mode */
@media (prefers-contrast: more) {
    .rules-list {
        ::v-deep(li) {
            color: var(--text-high-contrast);
            
            &::marker,
            &::before {
                color: currentColor;
            }

            strong {
                color: var(--text-high-contrast);
                font-weight: 700;
            }

            a {
                color: var(--link-high-contrast);
                text-decoration-thickness: 0.125em;

                &:hover,
                &:focus {
                    color: var(--link-hover-high-contrast);
                    text-decoration-thickness: 0.2em;
                }
            }
        }
    }
}

/* Reduzierte Bewegung */
@media (prefers-reduced-motion: reduce) {
    .rules-list {
        ::v-deep(li) {
            a {
                transition: none;
            }
        }
    }
}

/* Mobile Anpassungen */
@media (max-width: 768px) {
    .rules-list {
        padding-left: clamp(1.25rem, 4vw, 1.5rem);

        ::v-deep(li) {
            font-size: 1rem;
            margin-bottom: 0.75rem;
        }
    }
}

/* Unterstützung für Hover auf Touch-Geräten */
@media (hover: hover) {
    .rules-list {
        ::v-deep(li) {
            a:hover {
                text-decoration-thickness: 0.125em;
            }
        }
    }
}

/* Druckoptimierung */
@media print {
    .rules-list {
        padding-left: 1.5rem;

        ::v-deep(li) {
            color: #000;
            page-break-inside: avoid;

            a {
                color: #000;
                text-decoration: underline;
            }
        }
    }
}
</style>
