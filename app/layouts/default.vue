<template>
  <div class="min-h-screen flex flex-col bg-background">
    <SkipLink />

    <!-- Header mit ausgelagerten Komponenten -->
    <AppHeader v-if="showHeader" :navLabel="t('navigation.mainNavLabel')">
      <template #left>
        <LanguagePicker v-if="showMenu" />
      </template>
      
      <template #right>
        <HamburgerButton 
          v-if="showMenu"
          :isActive="isMenuOpen"
          :aria-label="isMenuOpen ? t('accessibility.closeMenu') : t('navigation.openMenu')"
          :aria-expanded="isMenuOpen" 
          aria-controls="menu" 
          aria-haspopup="true"
          @click="toggleMenu" 
        />
      </template>
    </AppHeader>

    <!-- Menü mit moderneren Komponenten -->
    <AppMenu 
      v-if="showMenu"
      :is-open="isMenuOpen"
      :menu-label="t('navigation.mainMenu')"
      :close-label="t('accessibility.closeMenu')"
      @close="closeMenu"
      ref="menuRef"
    >
      <!-- Hauptnavigation -->
      <MenuSection>
        <MenuItem 
          :to="localePath('gamehome')"
          icon="material-symbols:home-outline"
        >
          {{ t('navigation.home') }}
        </MenuItem>
        
        <MenuItem 
          :to="localePath('knowledge-overview')"
          icon="material-symbols:library-music"
        >
          {{ t('navigation.knowledge') }}
        </MenuItem>
        
        <MenuItem 
          :to="localePath('gamerules')"
          icon="fluent:question-32-filled"
        >
          {{ t('navigation.rules') }}
        </MenuItem>
      </MenuSection>

      <!-- Spenden-Bereich mit modernem Design -->
      <MenuSection :title="t('navigation.support')">
        <MenuItem 
          href="https://www.paypal.me/dcschmid"
          icon="logos:paypal"
          external
        >
          PayPal
        </MenuItem>
        
        <MenuItem 
          href="https://www.buymeacoffee.com/dcschmid"
          icon="simple-icons:buymeacoffee"
          external
        >
          Buy me a coffee
        </MenuItem>
      </MenuSection>

      <!-- Rechtliches mit verbesserter Darstellung -->
      <MenuSection :title="t('navigation.legal')">
        <MenuItem 
          :to="localePath('imprint')"
          icon="material-symbols:info-outline"
        >
          {{ t('navigation.imprint') }}
        </MenuItem>
        
        <MenuItem 
          :to="localePath('privacy')"
          icon="material-symbols:privacy-tip-outline"
        >
          {{ t('navigation.privacy') }}
        </MenuItem>
      </MenuSection>
    </AppMenu>

    <!-- Main Content -->
    <main id="main-content" role="main" class="flex-1 mx-auto text-text leading-relaxed max-w-prose w-full px-medium py-large">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLocalePath } from '#i18n'
// Korrekte Importpfade für Komponenten aus dem components-Verzeichnis
import HamburgerButton from '~/components/ui/HamburgerButton.vue'
import MenuItem from '~/components/ui/MenuItem.vue'
import MenuSection from '~/components/ui/MenuSection.vue'
import AppHeader from '~/components/layout/AppHeader.vue'
import AppMenu from '~/components/layout/AppMenu.vue'

const { t } = useI18n();
const localePath = useLocalePath();

const { showHeader, showMenu } = defineProps({
  showHeader: { type: Boolean, default: false },
  showMenu: { type: Boolean, default: false },
})

const isMenuOpen = ref(false);
const menuRef = ref(null);

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value;
}

function closeMenu() {
  isMenuOpen.value = false;
}
</script>
