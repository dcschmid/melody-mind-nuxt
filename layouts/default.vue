<template>
    <div>
        <a href="#main-content" class="skip-link">{{ $t('navigation.skipToMain') }}</a>

        <header v-if="showHeader" role="banner">
            <ShowPoints v-if="showCoins" ref="pointsDisplay" />
            <template v-if="showMenu">
                <LanguagePicker />

                <nav aria-label="Hauptnavigation">
                    <div class="slot left">
                        <button class="hamburger icon-button" :aria-label="$t('navigation.openMenu')"
                            :aria-expanded="isMenuOpen" aria-controls="menu" @click="toggleMenu">
                            <Icon name="ic:baseline-menu" size="36" aria-hidden="true" />
                            <span class="sr-only">{{ $t('navigation.openMenu') }}</span>
                        </button>
                        <div id="menu" class="menu" :class="{ 'is-open': isMenuOpen }">
                            <button class="close-button" :aria-label="$t('navigation.closeMenu')" @click="toggleMenu">
                                <Icon name="zondicons:close-solid" size="48" aria-hidden="true" />
                            </button>
                            <NuxtLink :to="localePath('gamehome')">
                                <Icon name="material-symbols:home-outline" size="36" aria-hidden="true" />
                                {{ $t('navigation.home') }}
                            </NuxtLink>
                            <NuxtLink :to="localePath('gamerules')">
                                <Icon name="fluent:question-32-filled" size="36" aria-hidden="true" />
                                {{ $t('navigation.rules') }}
                            </NuxtLink>
                            <NuxtLink :to="localePath('highscores')">
                                <Icon name="material-symbols:trophy-outline" size="36" aria-hidden="true" />
                                {{ $t('navigation.highscores') }}
                            </NuxtLink>
                            <NuxtLink :to="localePath('user')">
                                <Icon name="lucide:user-round" size="36" aria-hidden="true" />
                                {{ $t('navigation.profile') }}
                            </NuxtLink>
                            <button v-if="session.data" @click="handleSignOut">
                                <Icon name="ic:baseline-logout" size="36" aria-hidden="true" />
                                {{ $t('navigation.signOut') }}
                            </button>
                        </div>
                    </div>
                </nav>
            </template>
        </header>

        <main id="main-content">
            <slot />
        </main>
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
</script>

<style scoped lang="scss">
.menu {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: var(--background-color);
    transform: translateX(-100%);
    transition: transform var(--transition-speed) ease-in-out;
    z-index: 1000;

    &.is-open {
        transform: translateX(0);
    }
}

@media (prefers-reduced-motion: no-preference) {
    .menu {
        opacity: 0;
        visibility: hidden;
        transition: transform var(--transition-speed) ease-in-out,
            opacity var(--transition-speed) ease-in-out,
            visibility 0s linear var(--transition-speed);

        &.is-open {
            opacity: 1;
            visibility: visible;
            transition: transform var(--transition-speed) ease-in-out,
                opacity var(--transition-speed) ease-in-out,
                visibility 0s linear;
        }
    }
}
</style>
