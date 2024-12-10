<template>
    <div>
        <a href="#main-content" class="skip-link">{{ $t('navigation.skipToMain') }}</a>

        <header v-if="showHeader" role="banner">
            <LanguagePicker />
            <template v-if="showMenu">

                <nav aria-label="Hauptnavigation">
                    <div class="slot left">
                        <button class="hamburger icon-button" :aria-label="$t('navigation.openMenu')"
                            aria-expanded="false" aria-controls="menu">
                            <Icon name="ic:baseline-menu" size="36" aria-hidden="true" />
                            <span class="sr-only">{{ $t('navigation.openMenu') }}</span>
                        </button>
                        <div id="menu" class="menu">
                            <button class="close-button" :aria-label="$t('navigation.closeMenu')">
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
                            <button v-if="session.data" @click="authClient.signOut()">
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

const { showHeader, showMenu, showCoins } = defineProps({
    showHeader: { type: Boolean, default: false },
    showMenu: { type: Boolean, default: false },
    showCoins: { type: Boolean, default: false }
})

onMounted(() => {
    const button = document.querySelector('.hamburger') as HTMLButtonElement
    const menu = document.querySelector('#menu') as HTMLDivElement
    const closeButton = menu?.querySelector('.close-button') as HTMLButtonElement
    const body = document.body

    const toggleMenu = () => {
        const isExpanded = button.getAttribute('aria-expanded') === 'true'
        button.setAttribute('aria-expanded', String(!isExpanded))
        menu.classList.toggle('is-open')
        body.classList.toggle('menu-open')
    }

    button?.addEventListener('click', toggleMenu)
    closeButton?.addEventListener('click', toggleMenu)

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu?.classList.contains('is-open')) {
            toggleMenu()
        }
    })
})
</script>
