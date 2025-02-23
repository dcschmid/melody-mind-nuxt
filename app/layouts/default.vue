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
            <div class="menu-content">
                <button class="close-button" @click="closeMenu" :aria-label="t('accessibility.closeMenu')" ref="closeButtonRef">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path fill="#fff" d="m3.5 2.086l4.5 4.5l4.5-4.5L13.914 3.5L9.414 8l4.5 4.5l-1.414 1.414l-4.5-4.5l-4.5 4.5L2.086 12.5l4.5-4.5l-4.5-4.5z"/></svg>
                </button>
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
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: var(--overlay-background);
    backdrop-filter: var(--overlay-blur);
    opacity: 0;
    visibility: hidden;
    transition: var(--menu-transition);
    z-index: var(--z-index-menu);
    overflow-y: auto;

    .menu-content {
        position: relative;
        width: 100%;
        margin: var(--header-height) auto;
        display: flex;
        flex-direction: column;
        gap: var(--padding-large);
        padding: var(--padding-large);
        background: var(--surface-color);
        border-radius: var(--border-radius);
        border: 1px solid rgb(255 255 255 / 10%);
        box-shadow: var(--box-shadow);
        transform: translateY(-30px) scale(0.95);
        transition: transform 0.4s var(--transition-bounce);
        max-height: calc(100vh - var(--header-height) - var(--padding-large));
        overflow-y: auto;

        /* Scrollbar Styling */
        &::-webkit-scrollbar {
            width: 8px;
        }

        &::-webkit-scrollbar-track {
            background: var(--surface-color-light);
            border-radius: 4px;
        }

        &::-webkit-scrollbar-thumb {
            background: var(--secondary-color);
            border-radius: 4px;

            &:hover {
                background: var(--secondary-color-light);
            }
        }

        /* Close Button neu positioniert */
        .close-button {
            position: absolute;
            top: var(--padding-medium);
            right: var(--padding-medium);
            width: var(--min-touch-target);
            height: var(--min-touch-target);
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--surface-color-light);
            color: var(--text-color);
            border: 1px solid transparent;
            border-radius: 50%;
            cursor: pointer;
            transition: var(--menu-transition);
            box-shadow: var(--box-shadow);
            z-index: calc(var(--z-index-menu) + 1);
            text-align: center;

            svg {
                color: var(--text-color);
                position: absolute;
                width: 32px;
                height: 32px;
            }

            &:hover,
            &:focus-visible {
                color: var(--highlight-color);
                transform: rotate(90deg) scale(1.1);
                background: var(--surface-color-hover);
                border-color: var(--highlight-color);
                box-shadow: var(--box-shadow-hover);
            }

            &:focus-visible {
                outline: var(--focus-outline-width) solid var(--focus-outline-color);
                outline-offset: var(--focus-outline-offset);
            }
        }
    }

    &.is-open {
        opacity: 1;
        visibility: visible;

        .menu-content {
            transform: translateY(0) scale(1);
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
    gap: var(--padding-small);
    background: var(--surface-color-light);
    padding: var(--padding-medium);
    border-radius: var(--border-radius);

    &:not(:last-child) {
        border-bottom: 1px solid rgb(255 255 255 / 10%);
    }
}

.section-title {
    color: var(--text-secondary);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: var(--spacing-text);
    margin-bottom: var(--padding-small);
}

.menu-item {
    display: flex;
    align-items: center;
    gap: var(--padding-medium);
    padding: var(--padding-small) var(--padding-medium);
    min-height: var(--min-touch-target);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-medium);
    color: var(--text-color);
    background: var(--surface-color);
    transition: var(--menu-transition);
    text-decoration: none;
    border: 1px solid transparent;
    border-radius: var(--border-radius);

    .icon {
        color: var(--primary-color);
        transition: var(--menu-transition);
        flex-shrink: 0;
    }

    &:hover,
    &:focus-visible {
        transform: translateX(8px);
        background: var(--surface-color-hover);
        border-color: var(--primary-color);
        box-shadow: var(--box-shadow);

        .icon {
            color: var(--highlight-color);
            transform: scale(1.1);
        }
    }

    &:focus-visible {
        outline: var(--focus-outline-width) solid var(--focus-outline-color);
        outline-offset: var(--focus-outline-offset);
    }
}

@media (max-width: 768px) {
    .menu {
        padding: 0;
        
        .menu-content {
            width: 100%;
            height: 100vh;
            margin: 0;
            max-height: none;
            border-radius: 0;
            padding: calc(var(--header-height) + var(--padding-medium)) var(--padding-medium) var(--padding-medium);
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
