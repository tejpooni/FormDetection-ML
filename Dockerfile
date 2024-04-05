# Use an official base image as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt or package.json
# For Python-based projects, you might use pip install -r requirements.txt
# For Node.js-based projects, use npm install or yarn install
RUN npm install

# Make port 80 available to the world outside this container
# Adjust the port based on your application's needs
EXPOSE 80

# Define environment variables
# ENV NAME World

# Run your program when the container launches
# For a Python Flask app, you might use something like `python app.py`
# For a Node.js app, you might use `npm start` or `node server.js`
CMD ["npm", "start"]
