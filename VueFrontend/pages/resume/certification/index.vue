<template>
    <PartialsHeader title="Certification Section">
        <div class="row">
            <p class="d-inline">Certification List
                <button class="btn btn-sm btn-success float-end" @click="openModal">
                    <i class="bi bi-plus-square"></i>{{ ' ' }}Create
                </button>
            </p>
        </div>

        <div class="modal fade" id="certificationModal" tabindex="-1" aria-labelledby="certificationModalLabel"
            aria-hidden="true" ref="modal">
            <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable"> 
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="certificationModalLabel">Create New Certification</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="createCertification" class="form form-horizontal needs-validation"
                            novalidate>
                            <div class="form-body">
                                <div class="row">
                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="certified_on">Certified
                                                On</label>
                                            <input v-model="newCertification.certified_on" type="text" id="certified_on"
                                                class="form-control border-primary" placeholder="Certified On"
                                                name="certified_on" required>
                                            <span class="invalid-feedback">Certified On is
                                                required</span>
                                        </div>
                                    </div>

                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="card_title">Card
                                                Title</label>
                                            <select v-model="newCertification.card_title"
                                                class="form-select border-primary" aria-label="Default select example"
                                                required>
                                                <option disabled value="">Please Select</option>
                                                <option>Certification</option>
                                                <option>Awards</option>
                                            </select>
                                            <span class="invalid-feedback">Please Select Card
                                                Title</span>
                                        </div>
                                    </div>

                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="school_name">School
                                                Name</label>
                                            <input v-model="newCertification.school_name" type="text" id="school_name"
                                                class="form-control border-primary" placeholder="School Name"
                                                name="school_name" required>
                                            <span class="invalid-feedback">School Name is
                                                required</span>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="school_type">School
                                                Type</label>
                                            <input v-model="newCertification.school_type" type="text" id="school_type"
                                                class="form-control border-primary" placeholder="School Type"
                                                name="school_type" required>
                                            <span class="invalid-feedback">School Type is required</span>
                                        </div>
                                    </div>

                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="start_date">Start
                                                Date</label>
                                            <input v-model="newCertification.start_date" type="date" id="start_date"
                                                class="form-control border-primary" placeholder="Start
                                                            Date" name="start_date" required>
                                            <span class="invalid-feedback">Start
                                                Date is required</span>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="form-group mb-2">
                                            <label class="label-control" for="end_date">End
                                                date</label>
                                            <input v-model="newCertification.end_date" type="date" id="end_date"
                                                class="form-control border-primary" placeholder="End date"
                                                name="end_date" required>
                                            <span class="invalid-feedback">End date is required</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-actions my-2">
                                    <button type="button" class="btn btn-sm btn-danger mx-2 float-start"
                                        data-bs-dismiss="modal">
                                        <i class="bi bi-x-lg"></i>{{ ' ' }}Cancel
                                    </button>
                                    <button type="submit" class="btn btn-sm btn-success mx-2 float-end">
                                        <i class="bi bi-check2-square"></i>{{ ' ' }}Save
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <div v-for="(certification, index) in certifications" :key="index" class="card mt-2">
            <div class="card-content collapse show">
                <div class="card-body card-dashboard">

                    <div class="row">
                        <p class="float-start"><strong>{{ index + 1 }}</strong></p>
                    </div>

                    <form @submit.prevent="submitCertificationForm(index)" class="form form-horizontal needs-validation"
                        novalidate>
                        <div class="form-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="certified_on">Certified
                                            On</label>
                                        <input v-model="certification.certified_on" type="text" id="certified_on"
                                            class="form-control border-primary" placeholder="Certified On"
                                            name="certified_on" required>
                                        <span class="invalid-feedback">Certified On is
                                            required</span>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="card_title">Card
                                            Title</label>
                                        <select v-model="certification.card_title" class="form-select border-primary"
                                            aria-label="Default select example" required>
                                            <option selected :value="certification.card_title">{{
                                                certification.card_title }}</option>
                                            <option>Certification</option>
                                            <option>Awards</option>
                                        </select>
                                        <span class="invalid-feedback">Please Select Card
                                            Title</span>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="school_name">School
                                            Name</label>
                                        <input v-model="certification.school_name" type="text" id="school_name"
                                            class="form-control border-primary" placeholder="School Name"
                                            name="school_name" required>
                                        <span class="invalid-feedback">School Name is
                                            required</span>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="school_type">School
                                            Type</label>
                                        <input v-model="certification.school_type" type="text" id="school_type"
                                            class="form-control border-primary" placeholder="School Type"
                                            name="school_type" required>
                                        <span class="invalid-feedback">School Type is required</span>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="start_date">Start
                                            Date</label>
                                        <input v-model="certification.start_date" type="date" id="start_date"
                                            class="form-control border-primary" placeholder="Start
                                                            Date" name="start_date" required>
                                        <span class="invalid-feedback">Start
                                            Date is required</span>
                                    </div>
                                </div>

                                <div class="col-md-4">
                                    <div class="form-group mb-2">
                                        <label class="label-control" for="end_date">End
                                            date</label>
                                        <input v-model="certification.end_date" type="date" id="end_date"
                                            class="form-control border-primary" placeholder="End date" name="end_date"
                                            required>
                                        <span class="invalid-feedback">End date is required</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="form-actions my-2">
                                <button type="submit" class="btn btn-sm btn-warning mx-2 float-start">
                                    <i class="bi bi-pencil-square"></i>{{ ' ' }}Update
                                </button>

                                <button @click="deleteCertification(certification.certification_id)"
                                    class="btn btn-sm btn-danger float-end mx-2"><i class="bi bi-trash3"></i>
                                    {{ ' ' }}Delete
                                </button>
                            </div>
                        </div>

                    </form>
                </div>
            </div>
        </div>
    </PartialsHeader>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const certifications = ref([]);
const { $axios, $showToast } = useNuxtApp();
const user_id = 1;
const router = useRouter();

definePageMeta({
    layout: "sidestar",
});

useHead({
    title: 'Certifications',
    meta: [
        { name: 'description', content: 'View Certification' },
        { property: 'og:title', content: 'Certification' },
        { property: 'og:description', content: 'View Certification.' }
    ]
});

const modal = ref(null);
const newCertification = ref({ card_title: '', school_name: '', education_level: '', course_title: '', location: '', final_grade: '', start_date: '', end_date: '' });

const openModal = () => {
    const modalInstance = new bootstrap.Modal(modal.value);
    modalInstance.show();
};

const createCertification = async () => {
    const form = document.querySelector('.needs-validation');
    const user_id = 1;
    if (form.checkValidity()) {
        try {
            await $axios.post(`/user/${user_id}/certification/`, newCertification.value);
            $showToast("Certification created!");
               // Programmatically hide the modal
      const modalElement = document.getElementById('certificationModal'); 
      const modal = bootstrap.Modal.getInstance(modalElement);
      modal.hide(); 
            // router.push('/resume/certification');
        } catch (error) {
            console.log(error);
        }

    } else {
        form.classList.add('was-validated');
    };
};


const getCertification = async () => {
    try {
        const response = await $axios.get(`/user/${user_id}/certification/`);
        certifications.value = response.data;
    } catch (error) {
        console.error('Error fetching certifications:', error);
    }
};

const updateCertification = async (certificationIndex) => {
    try {
        await $axios.patch(
            `/user/${certificationIndex.user_id}/certification/${certificationIndex.certification_id}`,
            certificationIndex
        ).then(function (response) {
            console.log(response);
            $showToast("Certification updated!");
            router.push('/resume/certification');
        });
    } catch (error) {
        console.error('Error updating:', error);
    }
};

const deleteCertification = async (certification_id) => {
    try {
        await $axios.delete(`/user/${user_id}/certification/${certification_id}`);
        $showToast("Certification deleted!");
        getCertification();
    } catch (error) {
        console.error('Error deleting certification:', error);
    }
};

const submitCertificationForm = async (certificationIndex) => {
    const certificationToUpdate = certifications.value[certificationIndex];
    const form = document.querySelector('.needs-validation');

    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    updateCertification(certificationToUpdate);
};


// End of certifications

onMounted(() => {
    getCertification();
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            event.preventDefault();
            event.stopPropagation();

            if (!form.checkValidity()) {
                form.classList.add('was-validated');
            } else {
                createCertification();
            }
        }, false);
    });
});
</script>

<style src="~/assets/css/pages/resume/certification/index.css"></style>