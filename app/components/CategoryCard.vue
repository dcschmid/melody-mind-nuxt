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

<style scoped lang="scss">
.category-card {
    position: relative;
    width: 100%;
    aspect-ratio: 16/9;
    transition: transform 0.3s ease;
    cursor: pointer;

    &:hover {
        transform: scale(1.02);
        
        .category-content::after {
            opacity: 1;
        }
        
        .category-title {
            background: rgba(0, 0, 0, 0.8);
        }
        
        .category-description {
            opacity: 1;
        }
    }
}

.category-link {
    display: block;
    height: 100%;
    text-decoration: none;
    color: inherit;
}

.category-content {
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

.image-container {
    position: relative;
    width: 100%;
    height: 100%;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 8px;
    }
}

.category-title {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
    padding: 1rem;
    text-align: center;
}

.category-description {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    text-align: center;
    opacity: 0;
    transition: opacity 0.3s ease;
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
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: bold;
}
</style>
