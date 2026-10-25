<template>
    <div class="sidenav">
        <NuxtLink to="/resume/start">Lets start</NuxtLink>
        <NuxtLink to="/resume/profile"><i class="bi bi-person"></i>{{' '}}Profile</NuxtLink>
        <NuxtLink to="/resume/education"><i class="bi bi-book"></i>{{' '}}Education</NuxtLink>
        <NuxtLink to="/resume/experience"><i class="bi bi-list-stars"></i>{{' '}}Experience</NuxtLink>
        <NuxtLink to="/resume/language"><i class="bi bi-translate"></i>{{' '}}Languages</NuxtLink>
        <NuxtLink to="/resume/certification"><i class="bi bi-patch-check"></i>{{' '}}Certification</NuxtLink>
        <NuxtLink to="/resume/project"><i class="bi bi-blockquote-left"></i>{{' '}}Projects</NuxtLink>
        <NuxtLink to="/resume/referee"><i class="bi bi-sliders2"></i>{{' '}}Referees</NuxtLink>
        <NuxtLink to="/template"><i class="bi bi-eye-fill"></i>{{' '}}Preview</NuxtLink>
        <!-- <div class="float-start">
            <p>Logged in as</p>
            <p>Test</p>
            <form action="" method="post">
                <button type="button" class="btn btn-sm btn-danger">logout</button>
            </form>
        </div> -->
    </div>
    <div class="main py-4 d-flex justify-contents-center">
            <slot />
    </div>
</template>

<script>

</script>

<style scoped src="~/assets/css/components/Helpers/sidenav/sidestar.css"></style>