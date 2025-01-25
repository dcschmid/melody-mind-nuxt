<template>
    <article 
        class="category-card" 
        :class="{ 'not-playable': !isPlayable }"
        :aria-disabled="!isPlayable"
    >
        <NuxtLink 
            v-if="isPlayable" 
            :to="categoryUrl" 
            class="category-link"
            :aria-label="t('gameHome.playCategory', { category: headline })"
            :aria-describedby="`${cardId}-description`"
            @keydown.enter="$emit('select')" 
            @keydown.space.prevent="$emit('select')"
        >
            <div class="category-content">
                <div class="image-container">
                    <UnLazyImage 
                        :src="imageUrl" 
                        :alt="t('gameHome.categoryAlt', { category: headline })" 
                        loading="lazy"
                        class="category-image"
                        auto-sizes
                        :thumbhash="thumbHash"
                    />
                    
                    <h2 :id="`${cardId}-title`" class="category-title">
                        {{ headline }}
                    </h2>
                </div>
            </div>
        </NuxtLink>

        <div 
            v-else 
            class="category-content coming-soon" 
            :aria-label="t('gameHome.comingSoon', { category: headline })"
            :aria-describedby="`${cardId}-description`"
            role="article" 
            tabindex="0"
        >
            <div class="image-container">
                <UnLazyImage 
                    :src="imageUrl" 
                    :alt="t('gameHome.categoryAlt', { category: headline })" 
                    loading="lazy"
                    class="category-image"
                    auto-sizes
                    :thumbhash="thumbHash"
                />
                <h2 :id="`${cardId}-title`" class="category-title">
                </h2>

                <div 
                    class="coming-soon-badge" 
                    role="status"
                    aria-live="polite"
                >
                    {{ t('gameHome.comingSoonLabel') }}
                </div>
            </div>
        </div>
    </article>
</template>

<script setup lang="ts">
import { useThumbHash } from '~/composables/useThumbHash'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const { getThumbHash } = useThumbHash()

const props = defineProps({
    headline: {
        type: String,
        required: true
    },
    imageUrl: {
        type: String,
        required: true
    },
    categoryUrl: {
        type: String,
        required: true
    },
    introSubline: {
        type: String,
        required: true
    },
    isPlayable: {
        type: Boolean,
        default: true
    }
})

// ThumbHash für das Bild abrufen
const thumbHash = computed(() => getThumbHash(props.imageUrl))

// Generiere eine eindeutige ID für ARIA-Attribute
const cardId = computed(() => 
    `category-${props.headline.toLowerCase().replace(/\s+/g, '-')}`
)

defineEmits(['select'])
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.category-card {
    position: relative;
    width: 100%;
    cursor: pointer;
    transition: transform 0.3s ease;

    @include interactive-element;
    @include aspect-ratio(16, 9);

    &:not(.not-playable) {
        @media (hover: hover) {
            &:hover,
            &:focus-within {
                transform: scale(1.02);
                
                .category-content::after {
                    opacity: 1;
                }
                
                .category-description {
                    opacity: 1;
                }
            }
        }
    }

    &.not-playable {
        cursor: not-allowed;
    }
}

.category-link {
    display: block;
    height: 100%;
    text-decoration: none;
    color: inherit;
    outline: none;

    &:focus-visible {
        outline: 3px solid var(--focus-outline-color);
        outline-offset: 2px;
        border-radius: 8px;
    }
}

.category-content {
    @include fade-transition;
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
    background-color: var(--surface-color);

    &::after {
        @include overlay-layer;
        @include gradient-overlay;
        content: '';
        opacity: 0;
        transition: opacity 0.3s ease;
    }
}

.image-container {
    @include image-wrapper;
    
    .category-image {
        @include responsive-image;
        border-radius: 8px;
    }
}

.category-title {
    background: rgba(0, 0, 0, 0.7);

    @include flex-center;
    @include absolute-fill;
    font-size: var(--font-size-responsive-md);
    font-weight: 600;
    color: var(--text-on-primary);
    text-align: center;
    z-index: 2;
    height: 100%;
    width: 100%;
    margin: 0;
}

.coming-soon {
    cursor: not-allowed;
    
    .category-title {
        font-size: var(--font-size-responsive-md);
    }

    .category-description {
        opacity: 1;
        font-size: var(--font-size-responsive-sm);
    }
}

.coming-soon-badge {
    @include absolute-center;
    background: var(--primary-color);
    color: #000;
    padding: clamp(0.5rem, 1.5vw, 1rem) clamp(1rem, 2vw, 2rem);
    border-radius: var(--border-radius);
    font-weight: 700;
    font-size: clamp(0.875rem, 1.5vw, 1rem);
    z-index: 3;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

@media (prefers-reduced-motion: reduce) {
    .category-card,
    .category-content::after,
    .category-description {
        transition: none;
    }

    .category-card:hover {
        transform: none;
    }
}

@media (prefers-contrast: more) {
    .category-title {
        background: rgba(0, 0, 0, 0.9);
        color: var(--high-contrast-text);
    }

    .category-description {
        background: rgba(0, 0, 0, 0.95);
        color: var(--high-contrast-text);
    }

    .coming-soon-badge {
        background: var(--high-contrast-primary);
        color: var(--high-contrast-text);
        border: 2px solid var(--high-contrast-text);
    }

    .category-link:focus-visible {
        outline: 3px solid var(--high-contrast-focus);
    }
}

@media screen and (max-width: 640px) {
    .category-title {
        font-size: var(--font-size-responsive-md);
        padding: var(--padding-small);
    }

    .category-description {
        font-size: var(--font-size-responsive-sm);
        padding: var(--padding-small);
    }

    .coming-soon-badge {
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
    }
}
</style>
