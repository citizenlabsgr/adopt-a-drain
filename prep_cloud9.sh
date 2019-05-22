# This script is what's known as (in technical circles) a "hot mess".
# It's overly specialized to the one environment it's intended to run on: a
# fresh Cloud9 instance of Amazon Linux.
#
# Expect his setup process to take 10-15 minutes even if everything goes 
# swimmingly.
#
# Once you're logged in to an appropriate AWS account (don't do this as the 
# root user, please!), the steps for creating a working environment under Cloud9 
# are as follows:
#
# 1. Create a base Cloud9 environment, using an Amazon Linux base
# 2. Clone the repository into that instance.
# 3. Setup .env (including DB_PASSWORD="password")
# 4. Run this script: `sudo ./prep_cloud9.sh`
# 5. `./serve.sh`
#
# At that point, a server is running. If you hit the 'Preview' button a browser
# will open. That browser will contain an error message, because Cloud9
# perversely doesn't allow a local connection via http. Hit the "Pop out into
# new window" button to get a *working* preview in a new tab of your browser.
#
# If you like, you can set `./serve.sh` as the default project runner in the 
# IDE's preferences pane.
#
# You're probably setting this up for someone else; don't forget to invite a 
# guest account so that they have access.

yum install postgresql95 postgresql95-server postgresql95-devel postgresql95-contrib postgresql95-docs;
service postgresql95 initdb;
pushd /
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'password'";
popd
chkconfig postgresql95 on;
service postgresql95 start;
echo -e "local all all trust\nhost all all 127.0.0.1/32 trust\nhost all all ::1/128 ident" > /var/lib/pgsql95/data/pg_hba.conf;

su -c "source /home/ec2-user/.rvm/scripts/rvm; rvm install ruby-2.5.5; gem install bundler; bundle install; bundle exec rake db:reset; bundle exec rake data:load_things" $SUDO_USER;