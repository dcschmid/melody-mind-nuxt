<template>
    <section 
        v-if="category" 
        class="intro" 
        :aria-labelledby="headlineId"
        role="region"
    >
        <h1 :id="headlineId" class="headline category-title">
            <span class="category-name">{{ category.headline }}</span>
            <span class="selected-text">{{ t('category.selected') }}</span>
        </h1>
        
        <p 
            class="description category-description" 
            :id="descriptionId"
            aria-live="polite"
        >
            {{ category.introSubline }}
        </p>

        <div 
            v-if="category.description" 
            class="extended-description"
            :aria-labelledby="descriptionId"
        >
            <p>{{ category.description }}</p>
        </div>
    </section>
</template>

<script setup lang="ts">
interface Category {
    headline: string
    introSubline: string
    description?: string
}

const props = defineProps<{
    category: Category | null
}>()

const { t } = useI18n()

const headlineId = computed(() => 
    props.category ? `category-${props.category.headline.toLowerCase().replace(/\s+/g, '-')}-title` : ''
)

const descriptionId = computed(() => 
    props.category ? `category-${props.category.headline.toLowerCase().replace(/\s+/g, '-')}-desc` : ''
)
</script>

<style scoped lang="scss">
.intro {
    text-align: center;
    max-width: 800px;
    margin: 0 auto clamp(var(--padding-medium), 5vw, var(--padding-large));
    padding: 0 var(--padding-medium);
}

.category-title {
    font-size: var(--font-size-responsive-2xl);
    font-weight: 700;
    text-align: center;
    color: var(--primary-color);
    margin-bottom: var(--padding-medium);
    line-height: 1.3;
    letter-spacing: -0.01em;

    .category-name {
        display: inline-block;
        margin-right: 0.25em;
    }

    .selected-text {
        color: var(--text-color);
        font-weight: 600;
    }

    @media (prefers-reduced-motion: no-preference) {
        .category-name {
            transition: color 0.2s ease-in-out;
        }
    }

    @media (hover: hover) {
        &:hover .category-name {
            color: var(--primary-color-dark);
        }
    }
}

.category-description {
    font-size: var(--font-size-responsive-md);
    line-height: 1.6;
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
    max-width: 65ch;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    padding: 0 var(--padding-small);
}

.extended-description {
    font-size: var(--font-size-responsive-sm);
    line-height: 1.6;
    color: var(--text-secondary);
    margin-top: var(--padding-medium);
    text-align: center;
    padding: 0 var(--padding-small);
    
    p {
        max-width: 65ch;
        margin-left: auto;
        margin-right: auto;
    }
}

@media screen and (max-width: 640px) {
    .intro {
        padding: 0 var(--padding-small);
    }

    .category-title {
        font-size: var(--font-size-responsive-xl);
        padding: 0 var(--padding-small);
        
        .category-name,
        .selected-text {
            display: block;
            margin: 0;
        }
        
        .selected-text {
            margin-top: 0.5rem;
            font-size: 0.9em;
        }
    }

    .category-description {
        font-size: var(--font-size-responsive-sm);
    }
}

@media (prefers-contrast: more) {
    .category-title {
        color: var(--high-contrast-primary);
        
        .selected-text {
            color: var(--high-contrast-text);
        }
    }

    .category-description {
        color: var(--high-contrast-text);
    }

    .extended-description {
        color: var(--high-contrast-text);
    }
}
</style>
