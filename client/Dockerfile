FROM node:20-alpine
# RUN mkdir /frontend
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .