<template>
  <div class="cover-wrapper" :aria-labelledby="headlineId">
    <h2 :id="headlineId" class="visually-hidden">{{ headline }}</h2>
    <div class="cover" role="img" :aria-label="imageAltText">
      <UnLazyImage 
        v-if="imageUrl" 
        class="coverImage" 
        :src="imageUrl" 
        :alt="imageAltText"
        width="280" 
        height="280" 
        loading="lazy"
        :thumbhash="thumbHash"
        auto-sizes
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
import { useThumbHash } from '~/composables/useThumbHash'
import { useI18n } from 'vue-i18n'

const { getThumbHash } = useThumbHash()
const { t } = useI18n()

const props = defineProps<{
  imageUrl: string
  headline: string
}>()

// ThumbHash für das Bild abrufen
const thumbHash = computed(() => props.imageUrl ? getThumbHash(props.imageUrl) : undefined)

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
  transition: all var(--transition-speed) var(--transition-bounce);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--box-shadow-hover);
  }

  &:focus-within {
    outline: var(--focus-outline-width) solid var(--focus-outline-color);
    outline-offset: var(--focus-outline-offset);
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
  font-size: var(--font-size-responsive-md);
  font-weight: var(--font-weight-medium);
  padding: var(--padding-medium);
  text-align: center;
  line-height: var(--line-height-normal);
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
