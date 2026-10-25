<template>
  <div>
    <nav :class="['sb-topnav navbar navbar-expand navbar-dark', navbarColor]" class="text-white">
      <!-- Navbar Brand-->
      <NuxtLink class="navbar-brand ps-3" to="/resume/start">
        Resume Builder
      </NuxtLink>
      <!-- Sidebar Toggle-->
      <button class="btn btn-link btn-sm order-1 order-lg-0 me-4 me-lg-0" id="sidebarToggle">
        <i class="bi bi-columns-gap"></i>
      </button>
      <!-- Navbar Search-->
      <form class="d-none d-md-inline-block form-inline ms-auto me-0 me-md-3 my-2 my-md-0">
        <div class="input-group">
          <!-- <input class="form-control" type="text" placeholder="Search for..." aria-label="Search for..."
            aria-describedby="btnNavbarSearch" /> -->
          <!-- <button class="btn btn-primary" id="btnNavbarSearch" type="button"><i class="fas fa-search"></i></button> -->
        </div>
      </form>
      <!-- Navbar-->
      <ul class="navbar-nav ms-auto ms-md-0 me-3 me-lg-4">
        <li class="nav-item dropdown pe-3">
          <NuxtLink class="nav-link nav-profile d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown">
            <span class="mr-2 d-none d-lg-inline text-dark small">Daring Coder</span>
            <img :src="profileImage" class="img-profile rounded-circle" alt="Profile" />
          </NuxtLink>

          <!-- Dropdown - User Information -->
          <div class="dropdown-menu dropdown-menu-end shadow animated" aria-labelledby="userDropdown">
            <NuxtLink class="dropdown-item" to="/resume/profile">
              <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>Profile
            </NuxtLink>
            <NuxtLink class="dropdown-item" href="#">
              <i class="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>Settings
            </NuxtLink>
            <NuxtLink class="dropdown-item" href="#">
              <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>Activity Log
            </NuxtLink>
            <div class="dropdown-divider"></div>
            <!-- Logout -->
            <form action="/admin/logout" name="logout_form" method="post" style="margin: 0;">
              <button name="logout_btn" type="submit" class="dropdown-item">
                <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>Logout
              </button>
            </form>
          </div>
        </li>
      </ul>

    </nav>

    <div id="layoutSidenav">
      <div id="layoutSidenav_nav">
        <nav :class="['sb-sidenav accordion sb-sidenav-dark', sidebarColor]" id="sidenavAccordion">
          <div class="sb-sidenav-menu">
            <div class="nav">
              <!-- Loop through the navigation items returned from the utils function -->
              <CustomNuxtLink v-for="(item, index) in navLinks" :key="index" :to="item.to" :iconClass="item.iconClass"
                :title="item.title" :pathsToMakeActive="item.pathsToMakeActive" :isActiveGroup="isActiveGroup"
                :closeSidebarOnMobile="closeSidebarOnMobile" />

            </div>
          </div>

          <div class="sb-sidenav-footer">
            <div class="small">Logged in as:</div>
            Daring CoderPro1
          </div>
        </nav>
      </div>

      <div id="layoutSidenav_content">
        <main id="main">
          <slot />
        </main>
        <footer class="py-4 bg-light mt-auto">
          <div class="container-fluid px-4">
            <div class="d-flex align-items-center justify-content-between small">
              <div class="text-muted">Copyright &copy; {{ currentYear }}</div>
              <div>
                <a href="#">Be an inspiration!</a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNavLinks } from '~/assets/sidebar/js/navigation';
const navLinks = getNavLinks();
const currentYear = new Date().getFullYear();

// Import the image
import profileImage from '~/assets/img/admin.jpg'
import CustomNuxtLink from '~/components/Partials/CustomNuxtLink.vue';

// Reactive references for dynamic styles
const navbarColor = ref('bg-primary')
const sidebarColor = ref('bg-dark')

// Use Vue Router hooks
const router = useRouter()
const route = useRoute()

// Update document head
useHead({
  title: 'Resume Builder | Home',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'description', content: 'Welcome to the Resume Builder homepage page' },
  ],
})

// Watch for route changes and update styles
watch(route, (to) => {
  const currentUrl = to.path
  updateStyles(currentUrl)
})

// Initial setup on component mount
onMounted(() => {
  document.querySelector('body')?.classList.add('sb-nav-fixed')

  const action = document.getElementById('sidebarToggle')
  if (action) {
    action.addEventListener('click', handleSidebarToggle)
  }

  const currentUrl = window.location.pathname
  updateStyles(currentUrl)
})

// Handle sidebar toggle
function handleSidebarToggle() {
  document.body.classList.toggle('sb-sidenav-toggled')
  localStorage.setItem('sb|sidebar-toggle', String(document.body.classList.contains('sb-sidenav-toggled')))
}

// Update navbar and sidebar colors based on current URL
function updateStyles(currentUrl: string) {
  navbarColor.value = currentUrl.includes('/resume') ? 'bg-purple' : 'bg-primary'
  sidebarColor.value = currentUrl.includes('/resume') ? 'bg-dark' : 'bg-dark'
}

// Close sidebar on mobile when a link is clicked
function closeSidebarOnMobile() {
  if (window.matchMedia('(max-width: 768px)').matches) {
    document.body.classList.remove('sb-sidenav-toggled')
    localStorage.setItem('sb|sidebar-toggle', 'false')
  }
}

// Function to check if the current route matches any of the given paths
const isActiveGroup = (paths: string[]) => {
  return computed(() => paths.includes(route.path))
}

// Watch for route changes
watch(route, () => { }, { immediate: true })
</script>


