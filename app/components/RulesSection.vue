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
    margin-bottom: clamp(2rem, 5vw, 3rem);
    max-width: 70ch; /* Optimale Lesebreite */
    width: 100%;

    &:last-child {
        margin-bottom: 0;
    }

    &.has-background {
        background-color: var(--surface-color);
        border-radius: var(--border-radius);
        padding: clamp(1.5rem, 4vw, 2rem);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
}

.section-title {
    font-size: clamp(1.5rem, 2vw + 1rem, 2rem);
    font-weight: 700;
    line-height: 1.3;
    color: var(--text-color);
    margin-bottom: clamp(1rem, 3vw, 1.5rem);

    &.centered {
        text-align: center;
    }
}

.section-content {
    font-size: clamp(1rem, 1vw + 0.75rem, 1.125rem);
    line-height: 1.6;
    color: var(--text-color);

    &.centered {
        text-align: center;
    }

    /* Links innerhalb des Inhalts */
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

    /* Hervorgehobener Text */
    strong,
    em {
        color: var(--text-color);
        font-weight: 600;
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
            padding: 1.25rem;
        }
    }

    .section-title {
        font-size: clamp(1.25rem, 4vw, 1.5rem);
        margin-bottom: 1rem;
    }

    .section-content {
        font-size: 1rem;
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
        margin: 1rem 0;
        page-break-inside: avoid;

        &.has-background {
            background: none;
            border: 1px solid #000;
            padding: 1rem;
            box-shadow: none;
        }
    }

    .section-title,
    .section-content {
        color: #000;
    }

    .section-content {
        a {
            color: #000;
            text-decoration: underline;
        }
    }
}
</style>
