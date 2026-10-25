# syntax=docker/dockerfile:1
ARG NODE_VERSION=26
FROM node:${NODE_VERSION}-alpine
ARG PNPM_VERSION=latest
ENV PNPM_HOME=/pnpm PATH=/pnpm:$PATH NODE_ENV=production
RUN npm install -g pnpm@${PNPM_VERSION}
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod
COPY server.js .
USER node
EXPOSE 4000
HEALTHCHECK --interval=10s --timeout=3s --retries=5 CMD wget -qO- http://127.0.0.1:4000/health >/dev/null || exit 1
CMD ["node", "server.js"]
