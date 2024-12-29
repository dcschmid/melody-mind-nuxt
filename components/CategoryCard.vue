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
                            decoding="async" :width="480" :height="270" />
                    </picture>
                    <div class="category-title" aria-hidden="true">{{ headline }}</div>
                    <div class="category-description" aria-hidden="true">{{ introSubline }}</div>
                </div>
            </div>
        </NuxtLink>
        <div v-else class="category-content coming-soon" :aria-label="$t('gameHome.comingSoon', { category: headline })"
            role="article" tabindex="0">
            <div class="image-container">
                <picture>
                    <source :srcset="imageUrl" :sizes="'(max-width: 768px) 480px, 800px'" />
                    <img :src="imageUrl" :alt="$t('gameHome.categoryAlt', { category: headline })" loading="lazy"
                        decoding="async" :width="480" :height="270" />
                </picture>
                <div class="category-title" aria-hidden="true">{{ headline }}</div>
                <div class="category-description" aria-hidden="true">{{ introSubline }}</div>
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

<style scoped lang="scss">
.category-card {
    position: relative;
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    transition: transform 0.3s ease;

    &:not(.not-playable):hover {
        transform: scale(1.02);

        .category-content::after {
            opacity: 1;
        }
    }
}

.category-link {
    text-decoration: none;
    color: inherit;
    display: block;
    outline: none;

    &:focus {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    &:focus:not(:focus-visible) {
        outline: none;
    }

    &:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }
}

.category-content {
    position: relative;
    width: 100%;
    height: 100%;

    &:not(.coming-soon)::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.6));
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    &.coming-soon {
        cursor: not-allowed;

        &:focus {
            outline: 2px solid var(--color-primary);
            outline-offset: 2px;
        }
    }
}

.image-container {
    position: relative;
    width: 100%;
    height: 100%;
    aspect-ratio: 16/9;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: var(--border-radius-lg);
    }
}

.category-title {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
}

.category-description {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 1rem;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    opacity: 0;
    transition: opacity 0.3s ease;
    display: flex;
    align-items: center;
    text-align: center;
    font-size: 1rem;
    line-height: 1.5;
}

.coming-soon-badge {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-size: 1.2rem;
    font-weight: 600;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3),
        0 0 30px rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 10;
}
</style>
