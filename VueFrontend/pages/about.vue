<template>
  <div class="page-wrapper">
    <div class="button-wrapper prev-button-wrapper">
      <button class="prev-button" @click="goToPrevious">Previous</button>
    </div>
    <div class="button-wrapper next-button-wrapper">
      <button class="next-button" @click="goToNext">Next</button>
    </div>
    <div class="container">
      <div class="card border-light">
        <!-- <div class="card-header">
          Quote
        </div> -->
        <div class="card-body">
          <blockquote class="blockquote mb-0">
            <p>Welcome to Resume Builder Home page.</p>
            <footer class="blockquote-footer">Find more</footer>
          </blockquote>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    goToPrevious() {
      // Implement logic to navigate to the previous quote
    },
    goToNext() {
      // Implement logic to navigate to the next quote
    },
  },
};
</script>

<style src="~/assets/css/pages/about.css"></style>
