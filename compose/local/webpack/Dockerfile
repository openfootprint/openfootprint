FROM node:12

WORKDIR /frontend

COPY ./compose/local/webpack/package.json /package.json

COPY ./compose/local/webpack/start /start-webpack
RUN sed -i 's/\r//' /start-webpack
RUN chmod +x /start-webpack

RUN cd / && npm install --no-progress --ignore-optional