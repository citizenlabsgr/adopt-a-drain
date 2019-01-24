
## Prerequisites

### Developers
The easiest way to get Adopt a Drain installed is using Docker-Compose
* Install [Docker](https://www.docker.com/get-started) and [Docker-Compose](https://docs.docker.com/compose/install/) on your development box
* A Developer needs a [data.world](https://data.world) account to get an API token 
* A Developer needs a  [github](https://github.com) account
* A Developer needs a [google map] (https://cloud.google.com/maps-platform/)

### Production
* Adopt a Drain requires [Postgres](http://www.postgresql.org/) to be installed.
* We also recommend using a ruby version manager such as [rbenv](https://github.com/rbenv/rbenv).
* An Administrator needs a [data.world](https://data.world) account to get an API token 
* An Administrator needs a  [github](https://github.com) account
* An Administrator needs a [google map] (https://cloud.google.com/maps-platform/)

## Installation
### Developer
#### Clone the Repo
On your local machine, open a Terminal window
```
    git clone git://github.com/sfbrigade/adopt-a-drain.git
    cd adopt-a-drain
```

#### Add an Environment Variables (.env)
Put .env in the adopt-a-drain folder of the cloned repo
```
    # Postgres db variables:
    DB_HOST=db
    DB_USER=postgres

    # Enable google maps with your dev or prod google map api key
    GOOGLE_MAPS_JAVASCRIPT_API_KEY=<get-google-map-api-key> >>

    # Provide an owner id for the drain data.
    DW_USER=citizenlabs

    # Enable data.world data with your "read/write" api token
    DW_AUTH_TOKEN=<get-data.world-api-token> 

    # URL for drain data
    OPEN_SOURCE=https://api.data.world/v0/sql/citizenlabs/grb-storm-drains
```
* A Developer's will find it convenient to create an file (.env) to hold these variables. Put .env in the repo's adopt-a-drain/ folder.
* An Administrator will need to configure these in Heroko.

See the [wiki](https://github.com/citizenlabsgr/adopt-a-drain/wiki/Windows-Development-Environment) for a guide on how to install this application on Windows.

At this point you should be good to start jamming on issues [here](https://github.com/citizenlabsgr/adopt-a-drain/issues).

#### Build & Run Adopt a Drain with Compose
Open a Terminal Window
```
    # you should be in the adopt-a-drain/ folder
    cd adopt-a-drain/ 

    # make the application ready to accept connections
    docker-compose up

```
#### Connect to Adopt-a-drain Application
* Open a browser at http://localhost:3000

#### What just happened? 
* Sofware Install: The docker-compose command installed all the software necessary to run the Adopt-a-Drain application. The biggies are Postgres and Ruby on Rails.   
* Database Install: Docker-compose created data tables in Postgres, e.g,  "things", "users", "reminders" tables.
* Data Install: Docker-compose calls rails tasks to load drain data into the things table.
* Data Storage: By default, data is stored on a developer's local machine in the ~/data_cl_aad folder.
* On success, Docker-compose makes the Adopt-a-drain ready to accept connections.

### Set Environment Variables (.env)
```

    # Setup your docker based postgres database:
    docker-compose run --rm web bundle exec rake db:setup

    # Load data:
    docker-compose run --rm web bundle exec rake data:load_things
    # OR: don't load all that data, and load the seed data:
    # docker-compose run --rm web bundle exec rake db:seed

    # Start the web server:
    docker-compose up

    # Visit your website http://localhost:3000 (or the IP of your docker-machine)
```    


## Production Deployment

### Prerequisites
* Adopt a Drain requires and install of Postgres [Postgres](http://www.postgresql.org/).
* We also recommend using a ruby version manager such as [rbenv](https://github.com/rbenv/rbenv).
* You will need a data.world account to get an API token.
* You will need to install the environment variables, listed above, in [Heroku]().

### Deploying to Heroku
A successful deployment to Heroku requires a few setup steps:

1. Generate a new secret token:

    ```
    rake secret
    ```

2. Set the token on Heroku:

    ```
    heroku config:set SECRET_TOKEN=the_token_you_generated
    ```

3. [Precompile your assets](https://devcenter.heroku.com/articles/rails3x-asset-pipeline-cedar)

    ```
    RAILS_ENV=production bundle exec rake assets:precompile

    git add public/assets

    git commit -m "vendor compiled assets"
    ```

4. Add a production database to config/database.yml

5. Seed the production db:

    `heroku run bundle exec rake db:seed`

Keep in mind that the Heroku free Postgres plan only allows up to 10,000 rows,
so if your city has more than 10,000 fire drains (or other thing to be
adopted), you will need to upgrade to the $9/month plan.

### Google Analytics
If you have a Google Analytics account you want to use to track visits to your
deployment of this app, just set your ID and your domain name as environment
variables:

    heroku config:set GOOGLE_ANALYTICS_ID=your_id
    heroku config:set GOOGLE_ANALYTICS_DOMAIN=your_domain_name

An example ID is `UA-12345678-9`, and an example domain is `adoptadrain.org`.




## Submitting a Pull Request
1. [Fork the repository.][fork]
2. [Create a topic branch.][branch]
3. Add specs for your unimplemented feature or bug fix.
4. Run `bundle exec rake test`. If your specs pass, return to step 3.
5. Implement your feature or bug fix.
6. Run `bundle exec rake test`. If your specs fail, return to step 5.
7. Run `open coverage/index.html`. If your changes are not completely covered
   by your tests, return to step 3.
8. Add, commit, and push your changes.
9. [Submit a pull request.][pr]

[fork]: http://help.github.com/fork-a-repo/
[branch]: https://guides.github.com/introduction/flow/
[pr]: http://help.github.com/send-pull-requests/

## Supported Ruby Version
This library aims to support and is [tested against][travis] Ruby version 2.5.0
and Postgres 9.6.

If something doesn't work on this version, it should be considered a bug.

This library may inadvertently work (or seem to work) on other Ruby
implementations, however support will only be provided for the version above.

If you would like this library to support another Ruby version, you may
volunteer to be a maintainer. Being a maintainer entails making sure all tests
run and pass on that implementation. When something breaks on your
implementation, you will be personally responsible for providing patches in a
timely fashion. If critical issues for a particular implementation exist at the
time of a major release, support for that Ruby version may be dropped.
