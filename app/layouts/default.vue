<template>
    <div class="layout">
        <SkipLink />

        <header v-if="showHeader" role="banner">
            <LanguagePicker v-if="showMenu" />

            <nav v-if="showMenu" :aria-label="t('navigation.mainNavLabel')">
                <button class="menu-button" :class="{ 'is-active': isMenuOpen }"
                    :aria-label="isMenuOpen ? t('accessibility.closeMenu') : t('navigation.openMenu')"
                    :aria-expanded="isMenuOpen" aria-controls="menu" @click="toggleMenu" aria-haspopup="true">
                    <span class="menu-button-line"></span>
                </button>
            </nav>
        </header>

        <div id="menu" v-if="showMenu" class="menu" :class="{ 'is-open': isMenuOpen }" @keydown.esc="closeMenu"
            tabindex="-1" role="dialog" aria-modal="true" :aria-label="t('navigation.mainMenu')" ref="menuRef">
            <button class="close-button" :aria-label="t('accessibility.closeMenu')" @click="closeMenu"
                ref="closeButtonRef">
                <Icon name="material-symbols:close" size="48" />
            </button>

            <div class="menu-content">
                <!-- Hauptnavigation -->
                <div class="menu-section">
                    <NuxtLink :to="localePath('gamehome')" class="menu-item">
                        <Icon name="material-symbols:home-outline" size="36" />
                        <span>{{ t('navigation.home') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('knowledge-overview')" class="menu-item">
                        <Icon name="material-symbols:library-music" size="36" />
                        <span>{{ t('navigation.knowledge') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('gamerules')" class="menu-item">
                        <Icon name="fluent:question-32-filled" size="36" />
                        <span>{{ t('navigation.rules') }}</span>
                    </NuxtLink>
                </div>

                <!-- Spenden-Bereich -->
                <div class="menu-section">
                    <h2 class="section-title">{{ t('navigation.support') }}</h2>
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
                    <h2 class="section-title">{{ t('navigation.legal') }}</h2>
                    <NuxtLink :to="localePath('imprint')" class="menu-item">
                        <Icon name="material-symbols:info-outline" size="36" />
                        <span>{{ t('navigation.imprint') }}</span>
                    </NuxtLink>
                    <NuxtLink :to="localePath('privacy')" class="menu-item">
                        <Icon name="material-symbols:privacy-tip-outline" size="36" />
                        <span>{{ t('navigation.privacy') }}</span>
                    </NuxtLink>
                </div>
            </div>
        </div>

        <main id="main-content" role="main">
            <slot />
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLocalePath } from '#i18n'
import { useFocusTrap } from '@vueuse/integrations/useFocusTrap'

const { t } = useI18n();
const localePath = useLocalePath();

const { showHeader, showMenu } = defineProps({
    showHeader: { type: Boolean, default: false },
    showMenu: { type: Boolean, default: false },
})

const isMenuOpen = ref(false);
const menuRef = ref<HTMLElement | null>(null);
const closeButtonRef = ref<HTMLElement | null>(null);

const { activate, deactivate } = useFocusTrap(menuRef, {
    immediate: false,
    escapeDeactivates: true,
    allowOutsideClick: true,
    fallbackFocus: () => closeButtonRef.value as HTMLElement,
});

function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value;
    if (isMenuOpen.value) {
        nextTick(() => {
            activate();
            closeButtonRef.value?.focus();
        });
    } else {
        deactivate();
    }
}

function closeMenu() {
    isMenuOpen.value = false;
    deactivate();
}

// Cleanup
onUnmounted(() => {
    deactivate();
});
</script>

<style scoped lang="scss">
.layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

header {
    position: flex;
    width: 100%;
    height: var(--header-height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: var(--z-index-header);
    margin: 0 auto;

    nav {
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        gap: var(--padding-small);
        align-items: center;
        justify-content: space-between;

        @media (width >= 768px) {
            flex-wrap: nowrap;
            gap: var(--padding-medium);
        }
    }
}

.menu-button {
    position: relative;
    width: var(--min-touch-target);
    height: var(--min-touch-target);
    background: transparent;
    border: 2px solid transparent;
    cursor: pointer;
    padding: 12px;
    z-index: calc(var(--z-index-menu) + 1);
    border-radius: var(--border-radius);

    &:focus-visible {
        border-color: var(--focus-outline-color);
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
        box-shadow: 0 0 0 4px rgba(0, 247, 255, 0.4);
    }

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
    display: grid;
    place-items: center;
    background-color: var(--overlay-background);
    backdrop-filter: blur(var(--blur-strength));
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s var(--transition-bounce);

    .menu-content {
        width: min(90%, 400px);
        display: flex;
        flex-direction: column;
        gap: var(--padding-medium);
        padding: var(--padding-large);
        transform: translateY(30px);
        transition: transform 0.4s var(--transition-bounce);
    }

    &.is-open {
        opacity: 1;
        visibility: visible;

        .menu-content {
            transform: translateY(0);
        }
    }

    a,
    button {
        @include button-base;
        position: relative;
        display: flex;
        align-items: center;
        gap: var(--padding-medium);
        width: 100%;
        padding: var(--padding-medium);
        font-size: var(--button-font-size);
        color: var(--text-color);
        background: var(--surface-color);
        border-radius: var(--border-radius);
        transition: all 0.3s var(--transition-bounce);

        .icon {
            color: var(--highlight-color);
            transition: color 0.3s ease;
        }

        &:hover,
        &:focus-visible {
            background: var(--secondary-color);
            transform: scale(1.03);

            .icon {
                color: var(--text-color);
            }
        }
    }
}

.hamburger {
    @include button-icon;
    position: relative;
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
    padding: 1rem var(--padding-medium);
    min-height: 60px; // Vergrößerter Touch-Bereich
    font-size: 1.25rem; // Größere Schrift
    letter-spacing: 0.12px;
    word-spacing: 0.16em;
    font-weight: 500;
    color: var(--text-color);
    transition: all 0.3s var(--transition-bounce);
    text-decoration: none;
    border: 2px solid transparent;
    border-radius: var(--border-radius);

    .icon {
        color: var(--text-color);
        opacity: 0.9;
        transition: all 0.3s var(--transition-bounce);
        flex-shrink: 0;
    }

    &:hover,
    &:focus-visible {
        transform: translateX(8px);
        background-color: var(--surface-color-light);
        border-color: var(--highlight-color);

        .icon {
            color: var(--highlight-color);
            transform: scale(1.1);
            opacity: 1;
        }
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
        box-shadow: 0 0 0 4px rgba(0, 247, 255, 0.4);
    }
}

.close-button {
    position: absolute;
    top: var(--padding-medium);
    right: var(--padding-medium);
    padding: var(--padding-small);
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid transparent;
    background: var(--surface-color);
    color: var(--text-color);
    cursor: pointer;
    z-index: calc(var(--z-index-menu) + 1);
    border-radius: var(--border-radius);
    transition: all 0.3s var(--transition-bounce);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);

    .icon {
        width: 80px;
        height: 80px;
        color: currentColor;
    }

    &:hover,
    &:focus-visible {
        color: var(--highlight-color);
        transform: rotate(90deg);
        background: var(--surface-color-light);
        border-color: var(--highlight-color);
    }

    &:focus-visible {
        outline: none;
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

main {
    flex: 1;
    margin: 0 auto;
    font-size: var(--body-font-size);
    line-height: 1.6;
    color: var(--text-color);

    @media (width >= 768px) {
        max-width: var(--max-line-length);
        width: 100%;
    }
}
</style>
