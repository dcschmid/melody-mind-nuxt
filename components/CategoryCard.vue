<template>
    <div class="category-card" :class="{ 'not-playable': !isPlayable }" :aria-disabled="!isPlayable">
        <NuxtLink v-if="isPlayable" :to="categoryUrl" class="category-link"
            :aria-label="$t('gameHome.playCategory', { category: headline })">
            <div class="category-content">
                <div class="image-container">
                    <picture>
                        <source :srcset="`${imageUrl}?w=800 800w, ${imageUrl}?w=480 480w`"
                            :sizes="'(max-width: 768px) 480px, 800px'" />
                        <img :src="imageUrl" :alt="headline" loading="lazy" decoding="async" :width="480"
                            :height="270" />
                    </picture>
                </div>
                <div class="category-info">
                    <h2>{{ headline }}</h2>
                </div>
            </div>
        </NuxtLink>
        <div v-else class="category-content coming-soon"
            :aria-label="$t('gameHome.comingSoon', { category: headline })">
            <div class="image-container">
                <picture>
                    <source :srcset="`${imageUrl}?w=800 800w, ${imageUrl}?w=480 480w`"
                        :sizes="'(max-width: 768px) 480px, 800px'" />
                    <img :src="imageUrl" :alt="headline" loading="lazy" decoding="async" :width="480"
                        :height="270" />
                </picture>
                <div class="coming-soon-badge">
                    {{ $t('gameHome.comingSoonLabel') }}
                </div>
            </div>
            <div class="category-info">
                <h2>{{ headline }}</h2>
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
    isPlayable: {
        type: Boolean,
        default: true
    }
})
</script>

<style scoped lang="scss">
.category-card {
    position: relative;
    border-radius: var(--border-radius);
    overflow: hidden;
    background: var(--surface-color);
    border: 1px solid rgb(255 255 255 / 10%);
    backface-visibility: hidden;
    transform: translateZ(0);

    &:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--box-shadow-hover);

        .image-container img {
            transform: scale(1.1);
        }

        .category-info {
            transform: translateY(-5px);
        }
    }

    &.not-playable {
        opacity: 0.9;
        filter: grayscale(20%);
        pointer-events: none;
    }
}

.category-content {
    position: relative;
    height: 100%;
}

.image-container {
    position: relative;
    overflow: hidden;
    aspect-ratio: 16/9;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease-out;
    }
}

.category-info {
    padding: var(--padding-medium);
    transition: transform 0.3s ease-out;

    h2 {
        font-size: var(--subtitle-font-size);
        color: var(--text-color);
        margin: 0;
    }
}

.coming-soon-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
}
</style>
