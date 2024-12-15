<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <main class="profile-page">
            <!-- Profil-Header -->
            <section class="profile-header">
                <div class="profile-info">
                    <h1>{{ $t('profile.title') }}</h1>
                    <div class="user-details">
                        <p class="name">{{ userData.name }}</p>
                        <p class="username">@{{ userData.username }}</p>
                        <div class="points-container">
                            <span class="points">{{ userData.totalPoints?.toLocaleString() }}</span>
                            <span class="points-label">{{ $t('profile.points') }}</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- LP Sammlung -->
            <section class="lp-collection">
                <h2>{{ $t('profile.lps.title') }}</h2>
                <div v-if="uniqueLPs.length === 0" class="no-lps">
                    {{ $t('profile.lps.none') }}
                </div>
                <div v-else class="lp-grid">
                    <div v-for="lp in uniqueLPs" :key="`${lp.genre}-${lp.type}`" class="lp-card"
                        :class="lp.type.toLowerCase()">
                        <div class="lp-content">
                            <div class="lp-icon">
                                <Icon name="iconamoon:music-album" size="92" />
                            </div>
                            <div class="lp-info">
                                <span class="lp-type">{{ $t(`profile.lps.types.${lp.type.toLowerCase()}`) }}</span>
                                <span class="genre">{{ lp.genre }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { authClient } from '~/lib/auth-client'

const session = authClient.useSession()
const { t, locale } = useI18n()

const userData = ref({
    name: session.value?.data?.user?.name || '',
    username: session.value?.data?.user?.username || '',
    totalPoints: 0,
    wonLPs: []
})

// Lade Benutzerdaten
const loadUserData = async () => {
    if (!session.value?.data?.user) {
        return
    }

    try {
        const response = await fetch('/api/user/profile', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: session.value.data.user.id
            })
        })
        if (!response.ok) {
            throw new Error('Unauthorized')
        }
        const data = await response.json()
        userData.value = data
    } catch (error) {
        console.error('Error loading user data:', error)
    }
}

// Formatiere das Datum
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
}

const uniqueLPs = computed(() => {
    const unique = new Map();
    userData.value.wonLPs.forEach(lp => {
        if (lp.language === locale.value) {
            const key = `${lp.genre}-${lp.type}`;
            if (!unique.has(key)) {
                unique.set(key, lp);
            }
        }
    });
    return Array.from(unique.values());
});

watchEffect(() => {
    if (session.value?.data?.user) {
        loadUserData()
    }
})
</script>

<style lang="scss" scoped>
.profile-page {
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-large);
}

.profile-header {
    background: var(--surface-color);
    border-radius: var(--border-radius);
    padding: var(--padding-xl);
    margin-bottom: var(--padding-small);
    box-shadow: var(--shadow-elevation-medium);
    text-align: center;

    h1 {
        color: var(--primary-color);
        margin-bottom: var(--padding-large);
        font-size: 2.5rem;
    }

    .user-details {
        .name {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }

        .username {
            font-size: 1.2rem;
            color: var(--text-secondary);
        }

        .points-container {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            padding: var(--padding-small);
            background: var(--primary-color-transparent);
            border-radius: var(--border-radius);

            .points {
                font-size: 2.5rem;
                font-weight: bold;
                color: var(--highlight-color);
                line-height: 1;
                margin-bottom: 0.5rem;
            }

            .points-label {
                color: var(--text-secondary);
                font-size: 1rem;
            }
        }
    }
}

.lp-collection {
    h2 {
        color: var(--primary-color);
        margin-bottom: var(--padding-large);
        font-size: 2rem;
        text-align: center;
    }

    .no-lps {
        text-align: center;
        padding: var(--padding-xl);
        color: var(--text-secondary);
        background: var(--surface-color);
        border-radius: var(--border-radius);
        font-size: 1.2rem;
    }

    .lp-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: var(--padding-large);
    }

    .lp-card {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-elevation-low);
        transition: transform 0.2s ease, box-shadow 0.2s ease;

        &:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-elevation-medium);
        }

        &.gold {
            background: linear-gradient(135deg, #FFD700 0%, #B27E29 100%);

            .lp-type {
                color: #000000;
            }

            .genre {
                color: #000000;
            }
        }

        &.silver {
            background: linear-gradient(135deg, #E8E8E8 0%, #7A7A7A 100%);

            .lp-type {
                color: #000000;
            }

            .genre {
                color: #000000;
            }
        }

        &.bronze {
            background: linear-gradient(135deg, #CD7F32 0%, #614E1A 100%);

            .lp-type {
                color: #FFFFFF;
            }

            .genre {
                color: #FFFFFF;
            }
        }

        .lp-content {
            display: flex;
            align-items: center;
            gap: var(--padding-small);

            .lp-icon {
                padding: var(--padding-medium);
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .lp-info {
                flex-grow: 1;

                .lp-type {
                    display: block;
                    font-weight: bold;
                    text-transform: uppercase;
                    font-size: 0.9rem;
                    margin-bottom: 0.3rem;
                }

                .genre {
                    display: block;
                    font-size: 1.2rem;
                    font-weight: bold;
                }
            }
        }
    }
}

@media (max-width: 768px) {
    .profile-header {
        padding: var(--padding-large);

        h1 {
            font-size: 2rem;
        }

        .user-details {
            .name {
                font-size: 1.5rem;
            }

            .points-container .points {
                font-size: 2rem;
            }
        }
    }

    .lp-collection {
        .lp-grid {
            grid-template-columns: 1fr;
        }
    }
}
</style>
