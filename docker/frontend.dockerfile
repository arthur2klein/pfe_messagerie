FROM node:21-alpine3.18

WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY ./frontend/ ./

# start app
CMD ["npm", "start"]

