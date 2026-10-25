<template>
  <div class="resume-export-container">
    <div class="export-button-wrapper d-flex justify-content-center mb-3">
      <button
        class="btn btn-primary export-button"
        @click="generatePDF"
        :disabled="isDownloading"
        v-tooltip="isDownloading ? 'Exporting...' : 'Export to PDF'"
      >
        <span v-if="isDownloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span v-if="!isDownloading">{{ isDownloading ? 'Exporting...' : 'Export to PDF' }}</span>
      </button>
    </div>

    <div ref="pdfContent" class="template3" v-for="(user, index) in users" :key="index">
      <ResumeTemp3.Title :user_profile="user.user_profile" />
      <div class="parent">
        <ResumeTemp3.Summary :summary="user.summary" />
        <ResumeTemp3.Education :education="user.education" />
        <ResumeTemp3.Experience :experience="user.experience" />
        <ResumeTemp3.Skills :skills="user.skills" />
        <ResumeTemp3.Objective :objective="user.objectives" />
        <ResumeTemp3.Certification :certification="user.certification" />
        <ResumeTemp3.Frameworks />
        <ResumeTemp3.Programming />
        <ResumeTemp3.Languages :languages="user.language" />
        <ResumeTemp3.Operating_Systems />
        <ResumeTemp3.Hobbies :hobbies="user.hobbies" />
        <ResumeTemp3.Projects :projects="user.project" />
        <ResumeTemp3.Referees :referee="user.referee" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useNuxtApp } from "#app";

export default defineComponent({
  name: "fetchData",
  setup() {
    const users = ref([]);
    const pdfContent = ref(null);
    const isDownloading = ref(false);

    definePageMeta({
      layout: "sidestar",
    });

    useHead({
      title: "Preview",
      meta: [
        {
          name: "description",
          content: "Generate and export a PDF of the user profile with ease. Click the button to download the resume in PDF format.",
        },
        { property: "og:title", content: "Resume Preview - Export PDF" },
        {
          property: "og:description",
          content: "Generate and export a PDF of the user profile with ease. Click the button to download the resume in PDF format.",
        },
      ],
    });

    const generatePDF = async () => {
      if (process.client) {
        isDownloading.value = true;
        try {
          const { default: html2pdf } = await import("html2pdf.js");
          const content = pdfContent.value[0];

          if (content) {
            const options = {
              margin: [10, 10, 10, 10],  // Adjust margins if needed (in mm for jsPDF)
              filename: "resume.pdf",
              image: { type: "jpeg", quality: 0.98 },
              html2canvas: { scale: 2 },
              jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },  // A4 format
            };

            await html2pdf().from(content).set(options).save();
          } else {
            console.error("Content element not found");
          }
        } catch (error) {
          console.error("PDF generation error:", error);
        } finally {
          isDownloading.value = false;
        }
      } else {
        console.error("Code is not running on the client side");
      }
    };

    const fetchData = async () => {
      try {
        const response = await useNuxtApp().$axios.get(`/user/1/full_profile`, {
          headers: { "Content-Type": "application/json" },
        });
        users.value = [response.data];
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    onMounted(() => {
      fetchData();
    });

    return {
      users,
      pdfContent,
      generatePDF,
      isDownloading,
    };
  },
});
</script>

<style src="~/assets/css/pages/resume/previewsss.css"></style>
