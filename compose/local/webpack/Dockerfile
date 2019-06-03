FROM node:12

WORKDIR /app/frontend

COPY ./package.json /app/package.json

COPY ./compose/local/webpack/start /start-webpack
RUN sed -i 's/\r//' /start-webpack
RUN chmod +x /start-webpack

RUN cd /app && npm install --no-progress --ignore-optional