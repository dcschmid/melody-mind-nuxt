<template>
    <div class="layout">
        <a href="#main-content" class="skip-link">{{ $t('navigation.skipToMain') }}</a>

        <header v-if="showHeader" role="banner">
            <LanguagePicker />

            <nav v-if="showMenu" aria-label="Hauptnavigation">
                <button class="menu-button" :class="{ 'is-active': isMenuOpen }"
                    :aria-label="isMenuOpen ? $t('navigation.closeMenu') : $t('navigation.openMenu')"
                    :aria-expanded="isMenuOpen" aria-controls="menu" @click="toggleMenu">
                    <span class="menu-button-line"></span>
                </button>
            </nav>
        </header>

        <div id="menu" class="menu" :class="{ 'is-open': isMenuOpen }" @keydown.esc="closeMenu" tabindex="-1"
            role="dialog" aria-modal="true" :aria-label="$t('navigation.mainMenu')">
            <button class="close-button" :aria-label="$t('navigation.closeMenu')" @click="closeMenu">
                <Icon name="material-symbols:close" size="36" />
            </button>

            <div class="menu-content">
                <NuxtLink :to="localePath('gamehome')" class="menu-item">
                    <Icon name="material-symbols:home-outline" size="36" />
                    <span>{{ $t('navigation.home') }}</span>
                </NuxtLink>
                <NuxtLink :to="localePath('gamerules')" class="menu-item">
                    <Icon name="fluent:question-32-filled" size="36" />
                    <span>{{ $t('navigation.rules') }}</span>
                </NuxtLink>
                <NuxtLink :to="localePath('highscores')" class="menu-item">
                    <Icon name="material-symbols:trophy-outline" size="36" />
                    <span>{{ $t('navigation.highscores') }}</span>
                </NuxtLink>
                <NuxtLink :to="localePath('profile')" class="menu-item">
                    <Icon name="lucide:user-round" size="36" />
                    <span>{{ $t('navigation.profile') }}</span>
                </NuxtLink>
                <button v-if="session.data" @click="handleSignOut" class="menu-item">
                    <Icon name="ic:baseline-logout" size="36" />
                    <span>{{ $t('navigation.signOut') }}</span>
                </button>
            </div>
        </div>

        <slot />
    </div>
</template>

<script setup lang="ts">
import { authClient } from "../lib/auth-client"
const localePath = useLocalePath()
const session = authClient.useSession()
const router = useRouter()

const { showHeader, showMenu, showCoins } = defineProps({
    showHeader: { type: Boolean, default: false },
    showMenu: { type: Boolean, default: false },
    showCoins: { type: Boolean, default: false }
})

const isMenuOpen = ref(false)
const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
    document.body.style.overflow = isMenuOpen.value ? 'hidden' : ''
}

const route = useRoute()
watch(() => route.path, () => {
    isMenuOpen.value = false
    document.body.style.overflow = ''
})

onUnmounted(() => {
    document.body.style.overflow = ''
})

const handleSignOut = async () => {
    await authClient.signOut()
    isMenuOpen.value = false
    document.body.style.overflow = ''
    router.push('/')
}

const pointsDisplay = ref<any>(null)

// Expose pointsDisplay ref
defineExpose({
    pointsDisplay
})

// Add keyboard navigation detection
onMounted(() => {
    function handleFirstTab(e: KeyboardEvent) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-user');
            window.removeEventListener('keydown', handleFirstTab);
        }
    }
    window.addEventListener('keydown', handleFirstTab);

    // Cleanup
    onUnmounted(() => {
        window.removeEventListener('keydown', handleFirstTab);
    });
});

const closeMenu = () => {
    isMenuOpen.value = false
    document.body.style.overflow = ''
}

// Keyboard Event Listener
onMounted(() => {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isMenuOpen.value) {
            closeMenu()
        }
    })
})

onUnmounted(() => {
    document.removeEventListener('keydown', closeMenu)
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
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: var(--z-index-menu);
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: var(--header-height);

    &.is-open {
        opacity: 1;
        visibility: visible;
    }

    .menu-content {
        width: min(90%, 500px);
        display: flex;
        flex-direction: column;
        gap: var(--padding-large);
        padding: calc(var(--padding-large) * 2);
    }

    .menu-item {
        display: flex;
        align-items: center;
        gap: var(--padding-medium);
        padding: var(--padding-large);
        font-size: 1.5rem;
        font-weight: 500;
        color: var(--text-color);
        background: var(--surface-color);
        border-radius: var(--border-radius);
        transition: all 0.3s var(--transition-bounce);
        text-decoration: none;
        border: 1px solid transparent;

        .icon {
            font-size: 2rem;
            width: 40px;
            height: 40px;
            color: var(--highlight-color);
        }

        span {
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        &:hover,
        &:focus-visible {
            background: var(--secondary-color);
            transform: translateX(8px);
            border-color: var(--highlight-color);

            .icon {
                transform: scale(1.1);
            }
        }

        &:focus-visible {
            outline: none;
            border-color: var(--highlight-color);
            box-shadow: 0 0 0 2px var(--highlight-color);
        }
    }
}

@media (max-width: 768px) {
    .menu {
        .menu-content {
            width: 100%;
            padding: calc(var(--header-height) + var(--padding-medium)) var(--padding-medium);
        }

        .menu-item {
            padding: var(--padding-medium);
            font-size: 1.25rem;
        }
    }
}

.close-button {
    position: absolute;
    top: var(--padding-medium);
    right: var(--padding-medium);
    width: 48px;
    height: 48px;
    border: none;
    background: transparent;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: var(--text-color);
    cursor: pointer;
    transition: all 0.3s var(--transition-bounce);
    z-index: calc(var(--z-index-menu) + 1);

    .icon {
        transition: all 0.3s var(--transition-bounce);
    }

    &:hover,
    &:focus-visible {
        .icon {
            color: transparent;
            transform: rotate(180deg) scale(1.1);
        }
    }

    &:focus-visible {
        outline: none;
        box-shadow: 0 0 0 2px var(--highlight-color);
    }
}

// Verbesserte Animation für das Menü
.menu {
    &.is-open {
        .menu-content {
            transform: translateY(0);
            opacity: 1;
        }
    }

    .menu-content {
        transform: translateY(30px);
        opacity: 0;
        transition: all 0.4s var(--transition-bounce);
    }
}
</style>
