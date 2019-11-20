source 'https://rubygems.org'
ruby '2.5.5'

gem 'airbrake', '~> 7.1'
gem 'bundler-audit', '~> 0.6'
gem 'concurrent-ruby', '>= 1.1.5'
gem 'devise', '~> 4.7'
gem 'geokit-rails'
gem 'haml', '~> 5.0'
gem 'http_accept_language', '~> 2.0'
gem 'local_time', '~> 2.0'
gem 'loofah', '~> 2.3.1'
gem 'obscenity', '>= 1.0.2'
gem 'pg', '~> 0.21'
gem 'rails', '~> 4.2.11.1'
gem 'rack', '~> 1.6.11'
gem 'rails_admin', '~> 1.0'
gem 'validates_formatting_of', '~> 0.9'

gem 'paranoia', '~> 2.4'
gem 'tzinfo-data', platforms: %i[mingw mswin x64_mingw]

gem 'byebug', groups: %i[development est]
gem 'dotenv-rails'
gem 'execjs'
gem 'therubyracer'
gem 'nokogiri', '~> 1.10.4'

group :assets do
  gem 'sass-rails', '>= 4.0.3'
  gem 'uglifier'
end

group :development do
  gem 'spring'
end

group :development, :test do
  gem 'pry-byebug'
end

group :production do
  gem 'puma'
  gem 'rails_12factor'
  gem 'skylight'
end

group :test do
  gem 'coveralls', require: false
  gem 'rubocop', '~> 0.68.1', require: false
  gem 'rubocop-performance'
  gem 'simplecov', require: false
  gem 'webmock'
  gem 'rspec-rails'
  gem 'capybara'
  gem 'webdrivers'
  gem 'database_cleaner'
end
