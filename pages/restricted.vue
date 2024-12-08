<template>
    <section>
        <p>This page is restricted.</p>
    </section>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
})
</script>
