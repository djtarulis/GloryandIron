FROM node:20

WORKDIR /app

COPY package*.json ./

# Clean install and ignore optional native modules that fail
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
