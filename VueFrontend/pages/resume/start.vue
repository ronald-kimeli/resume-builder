<template>
   <div class="container py-4">
      <div class="row">
         <div class="col-xl-12 col-lg-12 col-md-12">
            <div class="card mb-2">
               <div class="card-body rounded">
                  <h4 class="text-center text-uppercase bold">Let's start!</h4>
               </div>
            </div>
            <div class="card mb-2">
               <div class="card-body">
                  <blockquote class="blockquote mb-0">
                     <p>Please! Make sure that you complete follow steps before you preview and download your resume
                        Once your profile is complete edit, add sections, preview resume and download resume.</p>
                     <footer class="blockquote-footer">Someone famous in <cite title="Source Title">Source Title</cite>
                     </footer>
                  </blockquote>
               </div>
            </div>

            <div class="text-center">
               <NuxtLink class="next-link float-start" :to="'/resume/profile'">Next</NuxtLink>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
definePageMeta({
   layout: "sidestar",
});

// Set meta information
useHead({
   title: 'Start',
   meta: [
      { name: 'description', content: 'View Start' },
      { property: 'og:title', content: 'Start' },
      { property: 'og:description', content: 'View Start.' }
   ]
});
</script>

<style src="~/assets/css/pages/resume/start.css"></style>