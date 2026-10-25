<template>
   <div class="container">
      <div class="row">
         <div class="col-md-2 text-center">
            <NuxtLink class="prev-link" :to="'/'">Previous</NuxtLink>
         </div>
         <div class="col-md-8">
            <div>
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
            </div>
         </div>
         <div class="col-md-2 text-center">
            <NuxtLink class="next-link" :to="'/resume/education'">Next</NuxtLink>
         </div>
      </div>
   </div>
</template>
 
<script setup>
definePageMeta({
   layout: "sidestar",
})
</script>
 
<style src="~/assets/css/pages/resume/create.css"></style>
 