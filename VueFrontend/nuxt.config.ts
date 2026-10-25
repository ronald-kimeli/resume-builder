// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  devServer: {
    host: "0.0.0.0",
    port: 5173, // you can replace this port with any port
  },

  // Production output is minified (JS via esbuild, CSS, and the Nitro server bundle)
  nitro: {
    minify: true,
  },

  vite: {
    build: {
      minify: 'esbuild',
      cssMinify: true,
    },
    server: {
      // bind mounts inside Docker don't always deliver file events; poll so edits hot-reload
      watch: { usePolling: !!process.env.CHOKIDAR_USEPOLLING },
      hmr: { port: 24678, clientPort: 24678 },
    },
  },

  app: {
    head: {
      title: 'Resume Builder',
      meta: [
        {name: 'description', content: 'ATS friendly resume'}
      ],
      link: [
        {rel: 'stylesheet', href: 'https://fonts.googleapis.com/icon?family=Material+Icons'},
      ],
      script: [
        {
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
        },
      ]
    }
  },

  css: ['~/assets/css/main.css', '~/assets/scss/styles.scss', '~/assets/css/dashboard.css'],

  runtimeConfig: {
    public: {
      BASE_URL: process.env.BASE_URL,
      SOCKET_URL: process.env.SOCKET_URL || 'ws://localhost:4000'
    }
  },
  plugins: [
    '~/plugins/useAxios.ts',
  ],

  compatibilityDate: '2024-10-06'
})