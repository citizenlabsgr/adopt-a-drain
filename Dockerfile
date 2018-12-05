FROM ruby:2.5
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
# RUN bundle config --global frozen 1
# RUN config --global frozen 1 apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
# Run bundle update throws exeption 10

RUN mkdir /myapp
WORKDIR /myapp
#RUN mkdir /usr/src/app
#WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .

# ADD Gemfile /myapp/Gemfile
# ADD Gemfile.lock /myapp/Gemfile.lock

# RUN bundle install
