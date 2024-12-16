<template>
    <div role="region" aria-label="Highscore Tabelle">
        <table class="highscore-table" aria-describedby="highscore-description">
            <caption class="sr-only">{{ $t('highscore.tableCaption') }}</caption>
            <thead>
                <tr>
                    <th scope="col" aria-sort="none">#</th>
                    <th scope="col" aria-sort="none">Avatar</th>
                    <th scope="col" aria-sort="none">{{ $t('highscore.name') }}</th>
                    <th scope="col" aria-sort="none">{{ $t('highscore.points') }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(score, index) in scores" :key="score.id"
                    :class="{ 'current-user': score.user_id === userId }"
                    :aria-current="score.user_id === userId ? 'true' : undefined">
                    <td data-label="#">
                        <span class="rank">{{ index + 1 }}</span>
                        <span class="sr-only">{{ $t('highscore.rank') }}</span>
                    </td>
                    <td data-label="Avatar" class="avatar">
                        <img v-if="score.avatar_url" :src="score.avatar_url"
                            :alt="`${$t('highscore.avatarOf')} ${score.name}`" loading="lazy">
                        <div v-else class="avatar-placeholder" role="img"
                            :aria-label="`${$t('highscore.avatarPlaceholder')} ${score.name}`">
                            {{ score.name.charAt(0) }}
                        </div>
                    </td>
                    <td data-label="Name">{{ score.name }}</td>
                    <td data-label="Punkte">
                        {{ score.score?.toLocaleString() }}
                        <span class="sr-only">{{ $t('highscore.points') }}</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style lang="scss" scoped>
.highscore-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--body-font-size);
    background: var(--surface-color-light);
    border-radius: var(--border-radius);

    th {
        text-align: left;
        padding: var(--padding-small);
        font-weight: bold;
        color: var(--text-color);
        border-bottom: 1px solid var(--surface-color);
    }

    td {
        padding: var(--padding-small);
        text-align: left;
        vertical-align: middle;
    }

    tr {
        transition: background-color 0.2s ease;

        &:hover {
            background-color: var(--surface-color);
        }

        &.current-user {
            background: var(--primary-color-transparent);
            border-left: 3px solid var(--primary-color);
        }
    }

    .avatar {

        img,
        .avatar-placeholder {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }

        .avatar-placeholder {
            background: var(--primary-color);
            color: var(--surface-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            text-transform: uppercase;
        }
    }

    @media (max-width: 600px) {
        thead {
            display: none;
        }

        tr {
            display: block;
            margin-bottom: var(--padding-small);
            padding: var(--padding-small);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }

        td {
            display: block;
            text-align: right;
            padding: 8px 0;
            border-bottom: 1px solid var(--surface-color);

            &::before {
                content: attr(data-label);
                float: left;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.85em;
                color: var(--text-secondary);
            }

            &.avatar {
                text-align: center;
                border-bottom: none;
                margin: var(--padding-small) 0;

                img,
                .avatar-placeholder {
                    width: 60px;
                    height: 60px;
                }

                &::before {
                    display: none;
                }
            }

            &:last-child {
                border-bottom: none;
            }
        }
    }

    @media (prefers-reduced-motion: reduce) {

        tr,
        td {
            transition: none;
        }
    }

    tr:focus-within {
        outline: 2px solid var(--focus-outline-color);
        outline-offset: -2px;
    }
}

td,
th {
    color: var(--text-color);

    @media (forced-colors: active) {
        border: 1px solid currentColor;
    }
}
</style>

<script setup lang="ts">
defineProps<{
    scores: Array<any>,
    userId?: string
}>()
</script>
