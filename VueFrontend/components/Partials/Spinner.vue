<template>
    <div v-if="items.length === 0" class="spinner-container">
        <div class="spinner"></div>
    </div>
    <div v-else>
        <slot />
    </div>
</template>

<script setup lang="ts">
defineProps({
    items: {
        type: Array as () => string[],
        required: true
    }
});
</script>

<style scoped src="~/assets/css/components/Partials/Spinner.css"></style>