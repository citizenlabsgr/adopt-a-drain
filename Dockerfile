FROM ruby:2.5
MAINTAINER James Wilfong
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs netcat && apt-get clean
RUN update_rubygems && gem install bundler

WORKDIR /tmp
ADD Gemfile .
ADD Gemfile.lock .
RUN bundle install 

COPY . /myapp
WORKDIR /myapp

