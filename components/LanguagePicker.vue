<template>
    <div class="language-picker">
        <select v-model="$i18n.locale">
            <option v-for="locale in $i18n.locales" :key="locale.code" :value="locale.code">
                {{ locale.name }}
            </option>
        </select>
    </div>
</template>
