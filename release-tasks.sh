#!/bin/bash
echo 'Starting data process'
# bundle update;
# bundle update rake;
bundle exec rake db:create;
bundle exec rake db:schema:load;
bundle exec rake db:migrate;
bundle exec rake data:load_things;
echo 'Ending data process'
