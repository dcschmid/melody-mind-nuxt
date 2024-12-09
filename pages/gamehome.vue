<template>
    <section>
        <p>This is the restricted Gamehome page.</p>
    </section>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})
</script>
