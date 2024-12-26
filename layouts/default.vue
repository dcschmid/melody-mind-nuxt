<template>
    <div class="layout">
        <a href="#main-content" class="skip-link">{{ $t('accessibility.skipToMain') }}</a>

        <header v-if="showHeader" role="banner">
            <LanguagePicker />

            <nav v-if="showMenu" :aria-label="$t('navigation.mainNavLabel')">
                <button class="menu-button" :class="{ 'is-active': isMenuOpen }"
                    :aria-label="isMenuOpen ? $t('accessibility.closeMenu') : $t('navigation.openMenu')"
                    :aria-expanded="isMenuOpen" aria-controls="menu" @click="toggleMenu">
                    <span class="menu-button-line"></span>
                </button>
            </nav>
        </header>

        <div id="menu" class="menu" :class="{ 'is-open': isMenuOpen }" @keydown.esc="closeMenu" tabindex="-1"
            role="dialog" aria-modal="true" :aria-label="$t('navigation.mainMenu')" ref="menuRef">
            <button class="close-button" :aria-label="$t('accessibility.closeMenu')" @click="closeMenu"
                ref="closeButtonRef">
                <Icon name="material-symbols:close" size="48" />
            </button>

            <div class="menu-content">
                <!-- Hauptnavigation -->
                <div class="menu-section">
                    <NuxtLink :to="localePath('gamehome')" class="menu-item">
                        <Icon name="material-symbols:home-outline" size="36" />
                        <span>{{ $t('navigation.home') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('gamerules')" class="menu-item">
                        <Icon name="fluent:question-32-filled" size="36" />
                        <span>{{ $t('navigation.rules') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('highscore')" class="menu-item">
                        <Icon name="material-symbols:trophy-outline" size="36" />
                        <span>{{ $t('navigation.leaderboard') }}</span>
                    </NuxtLink>
                </div>

                <!-- Spenden-Bereich -->
                <div class="menu-section">
                    <h2 class="section-title">{{ $t('navigation.support') }}</h2>
                    <a href="https://www.paypal.me/dcschmid" target="_blank" rel="noopener" class="menu-item">
                        <Icon name="logos:paypal" size="36" />
                        <span>PayPal</span>
                    </a>
                    <a href="https://www.buymeacoffee.com/dcschmid" target="_blank" rel="noopener" class="menu-item">
                        <Icon name="simple-icons:buymeacoffee" size="36" />
                        <span>Buy me a coffee</span>
                    </a>
                </div>

                <!-- Rechtliches -->
                <div class="menu-section">
                    <h2 class="section-title">{{ $t('navigation.legal') }}</h2>
                    <NuxtLink :to="localePath('imprint')" class="menu-item">
                        <Icon name="material-symbols:info-outline" size="36" />
                        <span>{{ $t('navigation.imprint') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('privacy')" class="menu-item">
                        <Icon name="material-symbols:privacy-tip-outline" size="36" />
                        <span>{{ $t('navigation.privacy') }}</span>
                    </NuxtLink>
                </div>
            </div>
        </div>

        <slot />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLocalePath } from '#i18n'
import { useFocusTrap } from '@vueuse/integrations/useFocusTrap'

const props = defineProps({
    showHeader: {
        type: Boolean,
        default: true
    },
    showMenu: {
        type: Boolean,
        default: true
    }
})

const { t } = useI18n()
const localePath = useLocalePath()

const isMenuOpen = ref(false)
const menuRef = ref<HTMLElement | null>(null)
const closeButtonRef = ref<HTMLElement | null>(null)

const { activate, deactivate } = useFocusTrap(menuRef)

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
    if (isMenuOpen.value) {
        activate()
        nextTick(() => {
            closeButtonRef.value?.focus()
        })
    } else {
        deactivate()
    }
}

const closeMenu = () => {
    isMenuOpen.value = false
    deactivate()
}

// Cleanup
onUnmounted(() => {
    deactivate()
})
</script>

<style scoped lang="scss">
.layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    padding: 0 var(--padding-medium);
    background-color: var(--surface-color);
    backdrop-filter: blur(var(--blur-strength));
    border-bottom: 1px solid rgb(255 255 255 / 10%);
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: var(--z-index-header);
}

.menu-button {
    position: relative;
    width: 48px;
    height: 48px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 12px;
    z-index: calc(var(--z-index-menu) + 1);

    .menu-button-line {
        position: relative;
        display: block;
        width: 100%;
        height: 2px;
        background: var(--text-color);
        transition: all 0.3s ease;

        &::before,
        &::after {
            content: '';
            position: absolute;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--text-color);
            transition: all 0.3s ease;
        }

        &::before {
            top: -8px;
        }

        &::after {
            bottom: -8px;
        }
    }

    &.is-active {
        .menu-button-line {
            background: transparent;

            &::before {
                top: 0;
                transform: rotate(45deg);
                background: var(--highlight-color);
            }

            &::after {
                bottom: 0;
                transform: rotate(-45deg);
                background: var(--highlight-color);
            }
        }
    }

    &:hover {

        .menu-button-line,
        .menu-button-line::before,
        .menu-button-line::after {
            background: var(--highlight-color);
        }
    }
}

.menu {
    position: fixed;
    inset: 0;
    background-color: var(--overlay-background);
    backdrop-filter: blur(var(--blur-strength));
    z-index: var(--z-index-menu);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: var(--header-height);
    overflow-y: auto;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;

    &.is-open {
        opacity: 1;
        visibility: visible;

        .menu-content {
            transform: translateY(0);
            opacity: 1;
        }
    }

    .menu-content {
        position: relative;
        width: min(90%, 400px);
        margin-bottom: var(--padding-large);
        display: flex;
        flex-direction: column;
        gap: var(--padding-large);
        padding: var(--padding-large);
        transform: translateY(30px);
        opacity: 0;
        transition: all 0.4s var(--transition-bounce);

        // Scrollbar Styling
        scrollbar-width: thin;
        scrollbar-color: var(--highlight-color) transparent;

        &::-webkit-scrollbar {
            width: 6px;
        }

        &::-webkit-scrollbar-track {
            background: transparent;
        }

        &::-webkit-scrollbar-thumb {
            background-color: var(--highlight-color);
            border-radius: 3px;
        }
    }
}

.menu-section {
    display: flex;
    flex-direction: column;
    gap: var(--padding-medium);

    &:not(:last-child) {
        padding-bottom: var(--padding-large);
        border-bottom: 1px solid rgb(255 255 255 / 10%);
    }
}

.section-title {
    color: var(--text-color);
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    opacity: 0.7;
    padding-left: var(--padding-medium);
}

.menu-item {
    display: flex;
    align-items: center;
    gap: var(--padding-medium);
    padding: var(--padding-medium);
    font-size: 1.125rem;
    color: var(--text-color);
    background: var(--surface-color);
    border-radius: var(--border-radius);
    transition: all 0.3s var(--transition-bounce);
    text-decoration: none;
    border: 1px solid transparent;

    .icon {
        color: var(--text-color);
        opacity: 0.8;
        transition: all 0.3s var(--transition-bounce);
    }

    &:hover,
    &:focus-visible {
        background: var(--secondary-color);
        transform: translateX(8px);
        border-color: var(--highlight-color);

        .icon {
            color: var(--highlight-color);
            transform: scale(1.1);
        }
    }
}

.close-button {
    position: absolute;
    top: var(--padding-medium);
    right: var(--padding-medium);
    padding: 0;
    max-width: 60px;
    max-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: var(--surface-color);
    color: var(--text-color);
    cursor: pointer;
    z-index: calc(var(--z-index-menu) + 1);
    border-radius: var(--border-radius);
    transition: all 0.3s var(--transition-bounce);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    .icon {
        display: block;
        width: 24px;
        height: 24px;
    }

    &:hover,
    &:focus-visible {
        color: var(--highlight-color);
        transform: rotate(90deg);
        background: var(--secondary-color);
    }
}

@media (max-width: 768px) {
    .menu {
        .menu-content {
            width: 100%;
            height: calc(100vh - var(--header-height));
            max-height: none;
            padding: var(--padding-medium);
        }

        .menu-item {
            padding: var(--padding-medium);
        }
    }
}
</style>
