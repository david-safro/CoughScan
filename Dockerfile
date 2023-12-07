# Use a base image that has both Python 3.10 and Node.js 18
FROM nikolaik/python-nodejs:python3.10-nodejs18

# Set the working directory inside the container to /CoughScan
WORKDIR /CoughScan

# Copy the current directory contents into the container at /CoughScan
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Change directory to /client/web
WORKDIR /CoughScan/client/web

# Install Node dependencies and build the project
RUN npm install
RUN npm run build

# Install pm2 globally
RUN npm install pm2 -g

EXPOSE 3000

# Start the application using pm2
CMD ["pm2-runtime", "start", "npm", "--", "start"]
