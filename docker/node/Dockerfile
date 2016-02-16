FROM node:5.6

RUN mkdir /code
WORKDIR /code

COPY package.json /code/package.json

RUN npm install

VOLUME /code/node_modules
