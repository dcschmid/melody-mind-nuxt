<template>
  <div class="cover" role="img" :aria-label="imageAltText">
    <img v-if="imageUrl" class="coverImage" :src="imageUrl" :alt="headline" width="280" height="280" loading="lazy"
      decoding="async" />
    <div v-else class="fallbackImage">{{ $t('category.noImage') }}</div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  imageUrl: string
  headline: string
}>()

const imageAltText = computed(() => `${props.headline} ${useI18n().t('category.image.alt')}`)
</script>

<style scoped lang="scss">
.cover {
  position: relative;
  width: 100%;
  max-width: clamp(280px, 35vw, 400px);
  aspect-ratio: 1;
  margin: 0 auto;
}

.coverImage {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.fallbackImage {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-color);
  border-radius: var(--border-radius);
  color: var(--text-secondary);
}
</style> 
