FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# 1. Выполняем сборку
RUN npm run build

# 2. ДОБАВЬТЕ ЭТУ КОМАНДУ ДЛЯ ОТЛАДКИ:
# Она покажет нам, что находится в папке /app после сборки.
RUN ls -l /app

# ==========================================================
# СТЭЙДЖ 2: PRODUCTION
# ==========================================================
FROM nginx:stable-alpine

# КОПИРУЕМ ИЗ /app/dist (для Vite)
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]