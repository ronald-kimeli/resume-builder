# syntax=docker/dockerfile:1
# Production image: built inside Docker (nothing built on the host / committed),
# JS + CSS minified by `nuxt build`, only the self-contained Nitro output is shipped.
ARG NODE_VERSION=26

FROM node:${NODE_VERSION}-alpine AS build
ARG PNPM_VERSION=latest
ENV PNPM_HOME=/pnpm \
    PATH=/pnpm:$PATH \
    PUPPETEER_SKIP_DOWNLOAD=true \
    NODE_ENV=production
RUN npm install -g pnpm@${PNPM_VERSION}
WORKDIR /app
COPY package.json pnpm-lock.yaml* pnpm-workspace.yaml .npmrc ./
# devDependencies (nuxt) are needed to build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod=false
COPY . .
ARG BASE_URL
ENV BASE_URL=${BASE_URL}
RUN pnpm build

FROM node:${NODE_VERSION}-alpine AS prod
# Chromium is used server-side by server/api/generate-pdf.ts
RUN apk add --no-cache chromium
ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000 \
    PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
WORKDIR /app
COPY --from=build /app/.output ./
USER node
EXPOSE 3000
CMD ["node", "/app/server/index.mjs"]
