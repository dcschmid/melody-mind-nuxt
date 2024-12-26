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
definePageMeta({
  redirect: '/'
})
</script>

<style lang="scss" scoped>
.profile-page {
    max-width: var(--content-width);
    margin: 0 auto;
    padding: var(--padding-large);
}

.profile-header {
    background: #1E1E1E;
    border-radius: 24px;
    padding: var(--padding-xl);
    margin: 20px;
    text-align: center;

    h1 {
        font-size: 2.5rem;
        color: white;
        margin-bottom: 2rem;
    }
}

.profile-image-container {
    position: relative;
    width: 150px;
    height: 150px;
    margin: 0 auto 60px;

    .profile-image {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #8B5CF6;
    }

    .image-upload-label {
        position: absolute;
        bottom: -40px;
        left: 50%;
        transform: translateX(-50%);
        background: #8B5CF6;
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        color: white;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
    }
}

.profile-form {
    max-width: 600px;
    margin: 0 auto;

    .form-group {
        background: #27272A;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;

        label {
            display: block;
            color: #71717A;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .profile-value {
            color: white;
            font-size: 1rem;
            padding: 8px 0;
            background: transparent;
        }

        input {
            width: 100%;
            background: #18181B;
            border: none;
            border-radius: 8px;
            padding: 12px;
            color: white;
            font-size: 1rem;
        }
    }
}

.edit-toggle {
    position: absolute;
    top: 20px;
    right: 20px;

    button {
        background: rgba(139, 92, 246, 0.2);
        border: 2px solid #8B5CF6;
        border-radius: 50%;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #8B5CF6;

        &:hover {
            background: #8B5CF6;
            color: white;
            transform: scale(1.1);
        }

        &.save-button {
            color: #22C55E;
            background: rgba(34, 197, 94, 0.2);
            border-color: #22C55E;

            &:hover {
                background: #22C55E;
                color: white;
            }
        }

        &.cancel-button {
            color: #EF4444;
            background: rgba(239, 68, 68, 0.2);
            border-color: #EF4444;

            &:hover {
                background: #EF4444;
                color: white;
            }
        }
    }
}

.points-container {
    text-align: center;
    margin: 2rem 0;
    padding: var(--padding-large);
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    backdrop-filter: blur(10px);

    .points {
        font-size: 4rem;
        font-weight: bold;
        background: linear-gradient(45deg, var(--primary-color), #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        display: block;
    }

    .points-label {
        color: #888;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
}

// Überschrift für LP-Sammlung
h2 {
    text-align: center;
    font-size: 2rem;
    margin: 3rem 0 2rem;
    color: white;
    background: linear-gradient(45deg, var(--primary-color), #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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
    top: 20px;
    right: 20px;
    display: flex;
    gap: 10px;

    button {
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }

        &.save-button {
            color: var(--success-color);
        }

        &.cancel-button {
            color: var(--error-color);
        }
    }
}

.points-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: var(--padding-medium) var(--padding-large);
    border-radius: 20px;

    .points {
        font-size: 3rem;
        background: linear-gradient(45deg, var(--highlight-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
}
</style>
