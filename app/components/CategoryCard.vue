<template>
    <div class="category-card" :class="{ 'not-playable': !isPlayable }" :aria-disabled="!isPlayable" role="article">
        <NuxtLink v-if="isPlayable" :to="categoryUrl" class="category-link"
            :aria-label="$t('gameHome.playCategory', { category: headline })" tabindex="0"
            @keydown.enter="$emit('select')" @keydown.space.prevent="$emit('select')">
            <div class="category-content">
                <div class="image-container">
                    <picture>
                        <source :srcset="imageUrl" :sizes="'(max-width: 768px) 480px, 800px'" />
                        <img :src="imageUrl" :alt="$t('gameHome.categoryAlt', { category: headline })" loading="lazy"
                            decoding="async" />
                    </picture>
                    <div class="category-title">{{ headline }}</div>
                    <div class="category-description">{{ introSubline }}</div>
                </div>
            </div>
        </NuxtLink>
        <div v-else class="category-content coming-soon" :aria-label="$t('gameHome.comingSoon', { category: headline })"
            role="article" tabindex="0">
            <div class="image-container">
                <picture>
                    <source :srcset="imageUrl" :sizes="'(max-width: 768px) 480px, 800px'" />
                    <img :src="imageUrl" :alt="$t('gameHome.categoryAlt', { category: headline })" loading="lazy"
                        decoding="async" />
                </picture>
                <div class="category-title">{{ headline }}</div>
                <div class="category-description">{{ introSubline }}</div>
                <div class="coming-soon-badge" role="status">
                    {{ $t('gameHome.comingSoonLabel') }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
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

defineEmits(['select'])
</script>

<style lang="scss" scoped>
@use '@/assets/scss/mixins' as *;

.category-card {
    & {
        position: relative;
        width: 100%;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    @include interactive-element;
    @include aspect-ratio(16, 9);

    @include hover-focus-active {
        transform: scale(1.02);
    }
}

.category-link {
    display: block;
    height: 100%;
    text-decoration: none;
    color: inherit;
}

.category-content {
    @include fade-transition;
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;

    &:not(.coming-soon)::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.6));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
}

.category-content::after {
    @include overlay-layer;
    @include gradient-overlay;
    content: '';
    opacity: 0;
    transition: opacity 0.3s ease;
}

.image-container {
    @include image-wrapper;
    
    img {
        @include responsive-image;
        border-radius: 8px;
    }
}

.image-container img {
    @include responsive-image;
    border-radius: 8px;
}

.category-title {
    @include flex-center;
    @include absolute-fill;
    @include overlay-background(0.5);
    font-size: 1.25rem;
    font-weight: bold;
    @include property-transition(background-color);
    padding: 1rem;
    text-align: center;
}

.category-description {
    @include absolute-fill;
    @include overlay-background(0.8);
    top: auto; // Override absolute-fill für bottom-only
    padding: 1rem;
    text-align: center;
    opacity: 0;
    @include property-transition(opacity);
    pointer-events: none;
}

.coming-soon {
    cursor: not-allowed;
    
    .category-title {
        background: rgba(0, 0, 0, 0.7);
        font-size: 1.2rem;
    }
}

.coming-soon-badge {
    @include absolute-center;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: bold;
}

.category-content.coming-soon {
    cursor: not-allowed;
    height: 100%;
    
    .image-container {
        height: 100%;
    }
    
    .category-title {
        @include flex-center;
        @include absolute-fill;
        @include overlay-background(0.7);
        font-size: 1.2rem;
    }

    .category-description {
        @include absolute-fill;
        @include overlay-background(0.8);
        top: auto;
        padding: 1rem;
        text-align: center;
    }
}
</style>
