#!/bin/bash
echo 'Starting data process'
bundle exec rake db:migrate;
echo 'Ending data process'
