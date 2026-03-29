FROM node:18-alpine as build
WORKDIR /app

# Сначала копируем только файлы зависимостей
COPY app/package*.json ./

# Очищаем кэш npm внутри и устанавливаем всё заново
RUN npm cache clean --force && npm install

# Теперь копируем остальной код, ИГНОРИРУЯ локальные папки
COPY app/ .

# На всякий случай удаляем папку node_modules, если она вдруг просочилась
# и запускаем билд
RUN rm -rf node_modules/@emotion && npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]