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
  }

.category-title {
    font-size: var(--font-size-responsive-2xl);
    font-weight: var(--font-weight-bold);
    text-align: center;
    color: var(--primary-color);
    margin-bottom: var(--padding-medium);
    line-height: var(--line-height-tight);
    letter-spacing: var(--spacing-text);

    .category-name {
        display: inline-block;
        margin-right: 0.25em;
    }

    .selected-text {
        color: var(--text-color);
        font-weight: var(--font-weight-semibold);
    }

    @media (prefers-reduced-motion: no-preference) {
        .category-name {
            transition: color var(--transition-speed) var(--transition-bounce);
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
    line-height: var(--line-height-relaxed);
    color: var(--text-color);
    margin-bottom: var(--padding-medium);
    max-width: var(--max-line-length);
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}

.extended-description {
    font-size: var(--font-size-responsive-sm);
    line-height: var(--line-height-relaxed);
    color: var(--text-secondary);
    margin-top: var(--padding-medium);
    text-align: center;
    
    p {
        max-width: var(--max-line-length);
        margin-left: auto;
        margin-right: auto;
    }
}

@media screen and (max-width: 640px) {
    .category-title {
        font-size: var(--font-size-responsive-xl);
        
        .category-name,
        .selected-text {
            display: block;
            margin: 0;
        }
        
        .selected-text {
            margin-top: var(--padding-small);
            font-size: 0.9em;
        }
    }

    .category-description {
        font-size: var(--font-size-responsive-sm);
    }
}

@media (prefers-contrast: more) {
    .category-title {
        color: var(--primary-color-dark);
        
        .selected-text {
            color: var(--text-color);
        }
    }

    .category-description,
    .extended-description {
        color: var(--text-color);
    }
}
</style>
