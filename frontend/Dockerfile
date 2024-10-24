# frontend/Dockerfile

FROM node:22

WORKDIR /frontend

COPY . .

COPY package.json package-lock.json ./
RUN npm install

CMD ["npm", "run", "dev"]
