FROM ruby:2.5
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs netcat && apt-get clean

RUN gem install bundler

RUN mkdir /myapp
WORKDIR /myapp

COPY Gemfile ./
COPY Gemfile.lock ./

# RUN bundle install

COPY . .
RUN bundle update --bundler
RUN bundler
RUN bundler install
