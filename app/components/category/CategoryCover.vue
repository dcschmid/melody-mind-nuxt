<template>
  <div class="cover-wrapper" :aria-labelledby="headlineId">
    <h2 :id="headlineId" class="visually-hidden">{{ headline }}</h2>
    <div class="cover" role="img" :aria-label="imageAltText">
      <img 
        v-if="imageUrl" 
        class="coverImage" 
        :src="imageUrl" 
        :alt="imageAltText"
        width="280" 
        height="280" 
        loading="lazy"
        decoding="async" 
      />
      <div 
        v-else 
        class="fallbackImage" 
        role="img" 
        :aria-label="t('category.noImage')"
      >
        {{ t('category.noImage') }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  imageUrl: string
  headline: string
}>()

const { t } = useI18n()
const headlineId = computed(() => `category-${props.headline.toLowerCase().replace(/\s+/g, '-')}`)
const imageAltText = computed(() => t('category.image.altText', { 
  category: props.headline 
}))
</script>

<style scoped lang="scss">
.cover-wrapper {
  position: relative;
  width: 100%;
  max-width: clamp(280px, 35vw, 400px);
  margin: 0 auto;
}

.cover {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--box-shadow);
  transition: transform 0.2s ease-in-out;

  &:hover {
    transform: translateY(-2px);
  }

  &:focus-within {
    outline: 3px solid var(--focus-outline-color);
    outline-offset: 2px;
  }
}

.coverImage {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius);
  background-color: var(--surface-color);
}

.fallbackImage {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-color);
  border-radius: var(--border-radius);
  color: var(--text-color);
  font-size: clamp(1rem, 1.5vw, 1.25rem);
  font-weight: 500;
  padding: var(--padding-medium);
  text-align: center;
  line-height: 1.5;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
