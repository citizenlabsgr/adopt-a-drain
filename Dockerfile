FROM ruby:2.5
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
# RUN bundle config --global frozen 1
# RUN config --global frozen 1 apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
# Run bundle update throws exeption 10

RUN mkdir /myapp
WORKDIR /myapp

COPY Gemfile ./
COPY Gemfile.lock ./

RUN bundle install

COPY . .
