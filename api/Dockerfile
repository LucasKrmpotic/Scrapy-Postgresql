FROM debian
EXPOSE 3000
RUN apt-get update -q
RUN apt-get install -y curl build-essential
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs build-essential
#RUN npm install -g n semver && n lts
COPY . .
RUN npm install
CMD ["node", "server"]
