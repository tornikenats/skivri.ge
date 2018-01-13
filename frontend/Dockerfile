FROM node:alpine

ADD package.json yarn.lock webpack.config.js run.js /
ADD src /src

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin

RUN yarn install && yarn build

EXPOSE 5010

CMD [ "yarn", "serve" ]