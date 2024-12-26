<template>
    <div role="region" aria-label="Highscore Tabelle">
        <table class="highscore-table" aria-describedby="highscore-description">
            <caption class="sr-only">{{ $t('highscore.tableCaption') }}</caption>
            <thead>
                <tr>
                    <th scope="col" aria-sort="none">#</th>
                    <th scope="col" aria-sort="none">{{ $t('highscore.name') }}</th>
                    <th scope="col" aria-sort="none">{{ $t('highscore.points') }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(score, index) in scores" :key="index">
                    <td data-label="#">
                        <span class="rank">{{ index + 1 }}</span>
                        <span class="sr-only">{{ $t('highscore.rank') }}</span>
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

<script setup lang="ts">
defineProps<{
    scores: Array<{
        name: string;
        score: number;
    }>
}>()
</script>

<style lang="scss" scoped>
.highscore-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--body-font-size);
    background: var(--surface-color-light);
    border-radius: var(--border-radius);
    overflow: hidden;

    th {
        text-align: left;
        padding: var(--padding-small);
        font-weight: bold;
        background: var(--surface-color);
        color: var(--text-primary);
    }

    td {
        padding: var(--padding-small);
        border-bottom: 1px solid var(--border-color);
        color: var(--text-secondary);
    }

    tr:last-child td {
        border-bottom: none;
    }

    .rank {
        font-weight: bold;
        color: var(--text-primary);
    }
}

@media (max-width: 768px) {
    .highscore-table {
        thead {
            display: none;
        }

        tbody tr {
            display: block;
            margin-bottom: 1rem;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
        }

        td {
            display: block;
            text-align: right;
            padding: 0.5rem;
            border: none;
            position: relative;

            &::before {
                content: attr(data-label);
                float: left;
                font-weight: bold;
                color: var(--text-primary);
            }
        }
    }
}
</style>
