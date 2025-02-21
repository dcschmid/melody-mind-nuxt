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
const thumbHash = computed(() => props.imageUrl ? getThumbHash(props.imageUrl) : '')

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
    transition: transform var(--transition-speed) var(--transition-bounce);

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
            }
        }
    }

    &.not-playable {
        cursor: not-allowed;
        opacity: var(--opacity-disabled);
    }
}

.category-link {
    display: block;
    height: 100%;
    text-decoration: none;
    color: inherit;
    outline: none;

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
        border-radius: var(--border-radius);
    }
}

.category-content {
    @include fade-transition;
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: var(--border-radius);
    overflow: hidden;
    background-color: var(--surface-color);
    box-shadow: var(--box-shadow);

    &::after {
        @include overlay-layer;
        @include gradient-overlay;
        content: '';
        opacity: 0;
        transition: opacity var(--transition-speed) var(--transition-bounce);
    }
}

.image-container {
    @include image-wrapper;
    
    .category-image {
        @include responsive-image;
        border-radius: var(--border-radius);
    }
}

.category-title {
    background: var(--overlay-background);
    @include flex-center;
    @include absolute-fill;
    font-size: var(--font-size-responsive-sm);
    font-weight: var(--font-weight-semibold);
    color: var(--text-color);
    text-align: center;
    z-index: var(--z-index-overlay);
    height: 100%;
    width: 100%;
    margin: 0;
    line-height: var(--line-height-tight);
}

.coming-soon {
    cursor: not-allowed;
    
    .category-title {
        font-size: var(--font-size-responsive-md);
    }
}

.coming-soon-badge {
    @include absolute-center;
    background: var(--primary-color);
    color: var(--button-text-color);
    padding: clamp(var(--padding-small), 1.5vw, var(--padding-medium));
    border-radius: var(--border-radius);
    font-weight: var(--font-weight-bold);
    font-size: var(--font-size-responsive-sm);
    z-index: var(--z-index-overlay);
    box-shadow: var(--box-shadow);
}

@media (prefers-reduced-motion: reduce) {
    .category-card,
    .category-content::after {
        transition: none;
    }

    .category-card:hover {
        transform: none;
    }
}

@media (prefers-contrast: more) {
    .category-title {
        background: var(--overlay-background);
        color: var(--text-color);
    }

    .coming-soon-badge {
        background: var(--primary-color-dark);
        color: var(--button-text-color);
        border: 2px solid var(--text-color);
    }

    .category-link:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }
}

@media screen and (max-width: 640px) {
    .category-title {
        font-size: var(--font-size-responsive-md);
        padding: var(--padding-small);
    }

    .coming-soon-badge {
        font-size: var(--font-size-responsive-sm);
        padding: var(--padding-small) var(--padding-medium);
    }
}
</style>
