FROM node:24-slim AS construcao
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
RUN npm run build

FROM node:24-slim
ENV NODE_ENV=production PORT=3000 HOSTNAME=0.0.0.0
WORKDIR /app
COPY --from=construcao /app/.next/standalone ./
COPY --from=construcao /app/.next/static ./.next/static
COPY --from=construcao /app/public ./public
USER node
EXPOSE 3000
CMD ["node", "server.js"]
