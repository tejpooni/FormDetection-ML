# Dockerfile for React App
FROM node:14

# Set a directory for the app
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

# Build static files
RUN npm run build

# Install serve to serve your app on port 3000
RUN npm install -serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define command to run the app using serve
CMD ["serve", "-s", "build", "-l", "3000"]
