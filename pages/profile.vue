<template>
    <NuxtLayout name="default" :show-header="true" :show-menu="true">
        <main class="profile-page">
            <section class="profile-header">
                <div class="profile-info">
                    <h1>{{ $t('profile.title') }}</h1>
                    <div class="profile-edit-section">
                        <div class="profile-image-container">
                            <img :src="profileImageUrl" alt="Profilbild" class="profile-image">
                            <label v-if="isEditing" class="image-upload-label">
                                <input type="file" @change="handleImageUpload" accept="image/*" class="hidden">
                                <Icon name="material-symbols:add-a-photo" size="24" />
                            </label>
                        </div>

                        <div class="edit-toggle">
                            <button v-if="!isEditing" @click="startEditing" class="edit-button">
                                <Icon name="material-symbols:edit" size="24" />
                            </button>
                            <div v-else class="edit-actions">
                                <button @click="saveChanges" class="save-button">
                                    <Icon name="material-symbols:save" size="24" />
                                </button>
                                <button @click="cancelEditing" class="cancel-button">
                                    <Icon name="material-symbols:close" size="24" />
                                </button>
                            </div>
                        </div>

                        <div class="profile-form">
                            <div class="form-group">
                                <label>{{ $t('profile.name') }}</label>
                                <input v-if="isEditing" v-model="editableUserData.name" type="text"
                                    :placeholder="$t('profile.namePlaceholder')">
                                <span v-else class="profile-value">{{ userData.name }}</span>
                            </div>

                            <div class="form-group">
                                <label>{{ $t('profile.username') }}</label>
                                <input v-if="isEditing" v-model="editableUserData.username" type="text"
                                    :placeholder="$t('profile.usernamePlaceholder')">
                                <span v-else class="profile-value">{{ userData.username }}</span>
                            </div>

                            <div class="form-group">
                                <label>{{ $t('profile.email') }}</label>
                                <input v-if="isEditing" v-model="editableUserData.email" type="email"
                                    :placeholder="$t('profile.emailPlaceholder')">
                                <span v-else class="profile-value">{{ userData.email }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="points-container">
                        <span class="points">{{ userData.totalPoints?.toLocaleString() }}</span>
                        <span class="points-label">{{ $t('profile.points') }}</span>
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
const isEditing = ref(false)

const userData = ref({
    name: session.value?.data?.user?.name || '',
    username: session.value?.data?.user?.username || '',
    email: session.value?.data?.user?.email || '',
    totalPoints: 0,
    wonLPs: [],
    profileImage: null
})

const editableUserData = ref({
    name: '',
    username: '',
    email: ''
})

const profileImageUrl = computed(() => {
    return userData.value.profileImage || userData.value.image || '/default-profile.png'
})

const startEditing = () => {
    editableUserData.value = {
        name: userData.value.name,
        username: userData.value.username,
        email: userData.value.email
    }
    isEditing.value = true
}

const cancelEditing = () => {
    isEditing.value = false
}

const saveChanges = async () => {
    try {
        const response = await fetch('/api/user/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: session.value?.data?.user?.id,
                ...editableUserData.value
            })
        })

        if (!response.ok) throw new Error('Fehler beim Aktualisieren des Profils')

        await loadUserData()
        isEditing.value = false
    } catch (error) {
        console.error('Fehler beim Aktualisieren des Profils:', error)
    }
}

// Lade Benutzerdaten
const loadUserData = async () => {
    if (!session.value?.data?.user) return

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

        if (!response.ok) throw new Error('Unauthorized')

        const data = await response.json()
        console.log('Geladene Benutzerdaten:', data)
        userData.value = {
            ...data,
            email: data.email || session.value.data.user.email || ''
        }
    } catch (error) {
        console.error('Error loading user data:', error)
    }
}

const handleImageUpload = async (event: Event) => {
    const file = (event.target as HTMLInputElement).files?.[0]
    const userId = session.value?.data?.user?.id

    if (!file) {
        console.error('Keine Datei ausgewählt')
        return
    }

    if (!userId) {
        console.error('Kein Benutzer angemeldet')
        return
    }

    const formData = new FormData()
    formData.append('image', file)
    formData.append('userId', userId.toString())

    try {
        const response = await fetch('/api/user/upload-profile-image', {
            method: 'POST',
            body: formData
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.message || 'Fehler beim Hochladen des Bildes')
        }

        const data = await response.json()
        userData.value.image = data.imageUrl
    } catch (error) {
        console.error('Fehler beim Bildupload:', error)
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

.profile-edit-section {
    position: relative;
    margin-bottom: var(--padding-large);
}

.edit-toggle {
    position: absolute;
    top: 0;
    right: 0;
    padding: var(--padding-small);
}

.edit-button,
.save-button,
.cancel-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: var(--padding-small);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;

    &:hover {
        background: var(--surface-color-hover);
    }
}

.edit-actions {
    display: flex;
    gap: var(--padding-small);

    .save-button {
        color: var(--success-color);
    }

    .cancel-button {
        color: var(--error-color);
    }
}

.profile-form {
    max-width: 400px;
    margin: 0 auto;

    .form-group {
        margin-bottom: var(--padding-medium);

        label {
            display: block;
            margin-bottom: 4px;
            color: var(--text-secondary);
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 8px;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            background: var(--surface-color);
            color: var(--text-primary);

            &:focus {
                border-color: var(--primary-color);
                outline: none;
            }
        }

        .profile-value {
            display: block;
            padding: 8px;
            color: var(--text-primary);
            background: var(--surface-color);
            border-radius: var(--border-radius);
        }
    }
}

.profile-image-container {
    position: relative;
    width: 150px;
    height: 150px;
    margin: 0 auto var(--padding-large);

    .profile-image {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid var(--primary-color);
    }

    .image-upload-label {
        position: absolute;
        bottom: 0;
        right: 0;
        background: var(--primary-color);
        border-radius: 50%;
        padding: 8px;
        cursor: pointer;

        &:hover {
            background: var(--primary-color-dark);
        }
    }

    .hidden {
        display: none;
    }
}
</style>
