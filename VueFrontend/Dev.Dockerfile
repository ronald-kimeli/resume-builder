# syntax=docker/dockerfile:1
# Development image: pnpm dev server with HMR. Source is bind-mounted by
# docker-compose.dev.yml, so UI changes show up in the browser as you save.
ARG NODE_VERSION=26
FROM node:${NODE_VERSION}-alpine

ARG PNPM_VERSION=latest
ENV PNPM_HOME=/pnpm \
    PATH=/pnpm:$PATH \
    PUPPETEER_SKIP_DOWNLOAD=true \
    CHOKIDAR_USEPOLLING=true \
    NODE_ENV=development
# corepack is no longer bundled with current Node releases, so install pnpm directly
RUN npm install -g pnpm@${PNPM_VERSION}

WORKDIR /app
COPY package.json pnpm-lock.yaml* pnpm-workspace.yaml .npmrc ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install
COPY . .

EXPOSE 5173 24678
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
