<template>
   <div class="container">
      <div class="row align-items-center">
         <div class="col-md-3 text-center">
            <NuxtLink class="prev-link" :to="'/'">Previous</NuxtLink>
         </div>
         <div class="col-md-6">
            <div class="card">
               <div class="card-header">
                  Quote
               </div>
               <div class="card-body">
                  <blockquote class="blockquote mb-0">
                     <p>The customer is very important, the customer will be followed by the customer. It was a complete
                        set from before.</p>
                     <footer class="blockquote-footer">Someone famous in <cite title="Source Title">Source Title</cite>
                     </footer>
                  </blockquote>
               </div>
            </div>
         </div>
         <div class="col-md-3 text-center">
            <NuxtLink class="next-link" :to="'/draggable'">Next</NuxtLink>
         </div>
      </div>
   </div>
</template>
 
<script>
export default {
   // ... (your script)
};
</script>
 
<style src="~/assets/css/pages/posts/index.css"></style>
 