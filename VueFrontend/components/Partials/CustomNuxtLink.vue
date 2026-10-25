<template>
    <NuxtLink class="nav-link" :to="to" @click="closeSidebarOnMobile"
        :class="{ 'router-link-exact-active active': isActiveGroup(pathsToMakeActive).value }">
        <div class="sb-nav-link-icon"><i :class="iconClass"></i></div> {{ title }}
    </NuxtLink>
</template>

<script setup lang="ts">
defineProps({
    iconClass: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    to: {
        type: String,
        required: true
    },
    pathsToMakeActive: {
        type: Array,
        required: true
    },
    isActiveGroup: {
        type: Function,
        required: true
    },
    closeSidebarOnMobile: {
        type: Function,
        required: true
    }
});

const emits = defineEmits();
</script>

<style scoped src="~/assets/css/components/Partials/CustomNuxtLink.css"></style>
