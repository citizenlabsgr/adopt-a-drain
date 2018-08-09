require 'open-uri'
require 'uri'
require 'net/http'
require 'json'
# class for importing things from CSV datasource
# is currently very specific to drains from Grand River Basin
#
# Dataset:
# https://data.sfgov.org/City-Infrastructure/Stormwater-inlets-drains-and-catch-basins/jtgq-b7c5
# Data Flow (TABLES):
#   csv -> temp_thing_import -> things
# App Flow
# -> ThingImporter
class ThingImporter
  class << self
    def load(source_url)
      # puts 'Downloading Things '
      # puts 'DW_USER: ' + ENV['DW_USER']
      # puts 'OPEN_SOURCE: ' + ENV['OPEN_SOURCE']
      puts 'load 1'
      Rails.logger.info('Downloading Things... ... ...')

      ActiveRecord::Base.transaction do
        puts 'load 2'
        import_temp_things(source_url)
        puts 'load 3'
        deleted_things_with_adoptee, deleted_things_no_adoptee = delete_non_existing_things
        puts 'load 4'
        created_things = upsert_things
        puts 'load 5'
        ThingMailer.thing_update_report(deleted_things_with_adoptee, deleted_things_no_adoptee, created_things).deliver_now

      end

    end

    def integer?(string)
      return true if string =~ /\A\d+\Z/
      false
    end

    def normalize_thing(json_thing)
      # puts 'normalize_thing 1'
      # puts json_thing
      # (lat, lng) = json_thing['dr_location'].delete('()').split(',').map(&:strip)
      norm = {
        city_id: json_thing['dr_facility_id'],
        lat: json_thing['dr_lat'],
        lng: json_thing['dr_lon'],
        type: json_thing['dr_type'],
        system_use_code: json_thing['dr_subwatershed'],
      }
      # puts 'normalize_thing out'
      return norm
    end
    # def normalize_thing(csv_thing)
    #  (lat, lng) = csv_thing['Location'].delete('()').split(',').map(&:strip)
    #  {
    #    city_id: csv_thing['PUC_Maximo_Asset_ID'].gsub!('N-', ''),
    #    lat: lat,
    #    lng: lng,
    #    type: csv_thing['Drain_Type'],
    #    system_use_code: csv_thing['System_Use_Code'],
    #  }
    # end
    def invalid_thing(thing)
      # puts 'invalid_thing 1'
      rc = false
      false unless ['Storm Water Inlet Drain', 'Catch Basin Drain'].include?(thing["type"])
      false unless integer?(thing["city_id"])

      # puts 'invalid_thing out'
      return true
    end

    # def invalid_thing(thing)
    #  puts 'invalid_thing 1'
    #  false unless ['Storm Water Inlet Drain', 'Catch Basin Drain'].include?(thing[:type])
    #  false unless integer?(thing[:city_id])
    #  true
    # end

    # load all of the items into a temporary table, temp_thing_import
    # mappings
    #   id <-
    #   name <-
    #   lat  <- dr_lat
    #   lng  <- dr_lon
    #   city_id <- dr_facility_id
    #   system_use_code <-
    # codes
    #   system_use_codes = ['MS4', 'STORM', 'COMB', 'UNK']

    def import_temp_things(source_url)
      puts 'import 1'
      insert_statement_id = SecureRandom.uuid
      # connect and create temp table
      conn = ActiveRecord::Base.connection
      conn.execute(<<-SQL.strip_heredoc)
        CREATE TEMPORARY TABLE "temp_thing_import" (
          id serial,
          name varchar,
          lat numeric(16,14),
          lng numeric(17,14),
          city_id integer,
          system_use_code varchar
        )
      SQL
      conn.raw_connection.prepare(insert_statement_id, 'INSERT INTO temp_thing_import (name, lat, lng, city_id, system_use_code) VALUES($1, $2, $3, $4, $5)')
      puts 'import 2'
      # data.world code

      url = URI(source_url)
      puts 'import 3'
      http = Net::HTTP.new(url.host, url.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      puts 'import 4'
      request = Net::HTTP::Post.new(url)
      request["content-type"] = 'application/x-www-form-urlencoded'
      request["authorization"] = 'Bearer ' + ENV['DW_AUTH_TOKEN']
      puts 'import 5'
      # get all the data
      # request.body = "query=select%20*%20FROM%20gr_drains%20LIMIT%204"
      # request.body = "query=select%20dr_type%2Cdr_lat%2Cdr_lon%2Cdr_facility_id%2Cdr_subwatershed%20FROM%20gr_drains%20LIMIT%204"
      request.body = "query=select%20dr_type%2Cdr_lat%2Cdr_lon%2Cdr_facility_id%2Cdr_subwatershed%20FROM%20gr_drains"
      puts 'import 6'
      response = http.request(request)
      puts 'import 7'
      puts response.code
      puts response.msg
      puts 'import 8'

      json_string = response.read_body

      # patch up to work around error
      json_string = '{ "data": ' + json_string + '}'
      # end data world code
      # process json data.world data
      JSON.parse(json_string)['data']
      .map { |t| normalize_thing(t) }
      .select { |t| invalid_thing(t) }
      .each do |drain|
        # puts drain
        # puts "dr_type: #{drain[:type]}"
        # puts "dr_lat: #{drain["lat"]}"
        # puts drain["dr_lon"]
        # puts drain["dr_facility_id"]
        # puts drain["dr_subwatershed"]
        conn.raw_connection.exec_prepared(
           insert_statement_id,
           [drain[:name], drain[:lat], drain[:lng], drain[:city_id], drain[:system_use_code]],
        )
      end

      # csv_string = open(source_url).read # go get data
      # CSV.parse(csv_string, headers: true).
      #  map { |t| normalize_thing(t) }.
      #  select { |t| invalid_thing(t) }.
      #  each do |thing|
      #  conn.raw_connection.exec_prepared(
      #    insert_statement_id,
      #    [thing[:type], thing[:lat], thing[:lng], thing[:city_id], thing[:system_use_code]],
      #  )
      # end

      conn.execute('CREATE INDEX "temp_thing_import_city_id" ON temp_thing_import(city_id)')
    end

    # mark drains as deleted that do not exist in the new set
    # return the deleted drains partitioned by whether they were adopted
    def delete_non_existing_things
      # mark deleted_at as this is what the paranoia gem uses to scope
      deleted_things = ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        UPDATE things
        SET deleted_at = NOW()
        WHERE things.city_id NOT IN (SELECT city_id from temp_thing_import) AND deleted_at IS NULL
        RETURNING things.city_id, things.user_id
      SQL
      deleted_things.partition { |thing| thing['user_id'].present? }
    end

    def upsert_things
      # postgresql's RETURNING returns both updated and inserted records so we
      # query for the items to be inserted first
      # puts 'upsert_things 1'
      created_things = ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        SELECT temp_thing_import.city_id
        FROM things
        RIGHT JOIN temp_thing_import ON temp_thing_import.city_id = things.city_id
        WHERE things.id IS NULL
      SQL
      # puts 'upsert_things 2'
      ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        INSERT INTO things(name, lat, lng, city_id, system_use_code)
        SELECT name, lat, lng, city_id, system_use_code FROM temp_thing_import
        ON CONFLICT(city_id) DO UPDATE SET
          lat = EXCLUDED.lat,
          lng = EXCLUDED.lng,
          name = EXCLUDED.name,
          deleted_at = NULL
      SQL
      # puts 'upsert_things out'
      return created_things
    end
  end
end
# ON CONFLICT(city_id) DO UPDATE SET
#  lat = EXCLUDED.lat,
#  lng = EXCLUDED.lng,
#  name = EXCLUDED.name,
#  deleted_at = NULL
