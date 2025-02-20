<template>
    <section 
        class="rules-section" 
        :aria-labelledby="id"
        :class="{ 'has-background': background }"
    >
        <h2 
            :id="id" 
            class="section-title"
            :class="{ 'centered': centered }"
        >
            <slot name="title"></slot>
        </h2>
        <div 
            class="section-content"
            :class="{ 'centered': centered }"
        >
            <slot></slot>
        </div>
    </section>
</template>

<script setup lang="ts">
interface Props {
    id: string
    background?: boolean
    centered?: boolean
}

defineProps<Props>()
</script>

<style lang="scss" scoped>
.rules-section {
    margin-bottom: var(--padding-large);
    max-width: var(--max-line-length);
    width: 100%;

    &:last-child {
        margin-bottom: 0;
    }

    &.has-background {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: var(--padding-medium);
        box-shadow: var(--box-shadow);
    }
}

.section-title {
    font-size: var(--font-size-responsive-xl);
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-tight);
    color: var(--text-color);
    margin-bottom: var(--padding-large);

    &.centered {
        text-align: center;
    }
}

.section-content {
    font-size: var(--font-size-responsive-sm);
    line-height: var(--line-height-relaxed);
    color: var(--text-color);

    &.centered {
        text-align: center;
    }

    /* Links innerhalb des Inhalts */
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

    /* Hervorgehobener Text */
    strong,
    em {
        color: var(--text-color);
        font-weight: var(--font-weight-semibold);
    }
}

/* High Contrast Mode */
@media (prefers-contrast: more) {
    .rules-section {
        &.has-background {
            border: 2px solid var(--border-high-contrast);
            box-shadow: none;
        }
    }

    .section-title {
        color: var(--text-high-contrast);
    }

    .section-content {
        color: var(--text-high-contrast);

        a {
            color: var(--link-high-contrast);
            text-decoration-thickness: 0.125em;

            &:hover,
            &:focus {
                color: var(--link-hover-high-contrast);
                text-decoration-thickness: 0.2em;
            }
        }

        strong,
        em {
            color: var(--text-high-contrast);
            font-weight: 700;
        }
    }
}

/* Reduzierte Bewegung */
@media (prefers-reduced-motion: reduce) {
    .section-content {
        a {
            transition: none;
        }
    }
}

/* Mobile Anpassungen */
@media (max-width: 768px) {
    .rules-section {
        &.has-background {
            padding: var(--padding-small);
        }
    }

    .section-title {
        font-size: var(--font-size-responsive-md);
        margin-bottom: var(--padding-small);
    }

    .section-content {
        font-size: var(--font-size-base);
    }
}

/* Unterstützung für Hover auf Touch-Geräten */
@media (hover: hover) {
    .section-content {
        a:hover {
            text-decoration-thickness: 0.125em;
        }
    }
}

/* Druckoptimierung */
@media print {
    .rules-section {
        margin: var(--padding-medium) 0;
        page-break-inside: avoid;

        &.has-background {
            background: none;
            border: 1px solid var(--button-text-color);
            padding: var(--padding-medium);
            box-shadow: none;
        }
    }

    .section-title,
    .section-content {
        color: var(--button-text-color);
    }

    .section-content {
        a {
            color: var(--button-text-color);
            text-decoration: underline;
        }
    }
}
</style>
