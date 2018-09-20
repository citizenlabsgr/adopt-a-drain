require 'open-uri'
require 'uri'
require 'net/http'
require 'json'
# class for importing things from JSON data.world datasource
# is currently very specific to drains from Grand River Basin
#
# Dataset:
# https://api.data.world/v0/sql/citizenlabs/grb-storm-drains
# Data Flow (TABLES):
#   json -> temp_thing_import -> things
# App Flow
# -> ThingImporter
class ThingImporter
  class << self
    def load(source_url)

      Rails.logger.info('Downloading Things... ... ...')

      ActiveRecord::Base.transaction do

        import_temp_things(source_url)

        deleted_things_with_adoptee, deleted_things_no_adoptee = delete_non_existing_things

        created_things = upsert_things

        # ThingMailer.thing_update_report(deleted_things_with_adoptee, deleted_things_no_adoptee, created_things).deliver_now

      end

    end

    def integer?(string)
      return true
    end

    def normalize_thing(json_thing)

      norm = {
        name: json_thing['dr_type'],
        city_id: json_thing['dr_facility_id'],
        lat: json_thing['dr_lat'],
        lng: json_thing['dr_lon'],
        type: json_thing['dr_type'],
        system_use_code: json_thing['dr_subwatershed'],
        jurisdiction: json_thing['dr_jurisdiction']
      }

      return norm
    end

    def invalid_thing(thing)
      # bare minimum validation of imported data
      rc = true
      # make sure type value is a "Storm Water Inlet Drain" or "Catch Basin Drain"
      if not ['Storm Water Inlet Drain', 'Catch Basin Drain'].include?(thing[:type])
        rc = false
        raise "Unknown drain type: "
      end
      # check value city_id is integer
      if not integer?(thing[:city_id])
        rc = false
        raise "City_id is not integer "
      end

      return rc
    end

    def import_temp_things(source_url)

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
          system_use_code varchar,
          jurisdiction varchar
        )
      SQL
      conn.raw_connection.prepare(insert_statement_id, 'INSERT INTO temp_thing_import (name, lat, lng, city_id, system_use_code, jurisdiction) VALUES($1, $2, $3, $4, $5, $6)')

      # data.world code
      url = URI(source_url)

      http = Net::HTTP.new(url.host, url.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE

      request = Net::HTTP::Post.new(url)
      request["content-type"] = 'application/json'
      request["authorization"] = "Bearer #{ENV['DW_AUTH_TOKEN']}"

      # get all the data
      request.body = "{\"query\":\"select * from grb_drains\",\"includeTableSchema\":false}"

      response = http.request(request)
      json_string = response.read_body

      # patch up to work around error
      json_string = '{ "data": ' + json_string + '}'
      # end data world code

      # move data.world data into app db
      JSON.parse(json_string)['data']
      .map { |t| normalize_thing(t) }
      .select { |t| invalid_thing(t) }
      .each do |drain|
        conn.raw_connection.exec_prepared(
           insert_statement_id,
           [drain[:name], drain[:lat], drain[:lng], drain[:city_id], drain[:system_use_code], drain[:jurisdiction]],
        )
      end

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

      created_things = ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        SELECT temp_thing_import.city_id
        FROM things
        RIGHT JOIN temp_thing_import ON temp_thing_import.city_id = things.city_id
        WHERE things.id IS NULL
      SQL

      ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        INSERT INTO things(name, lat, lng, city_id, system_use_code, jurisdiction)
        SELECT name, lat, lng, city_id, system_use_code, jurisdiction FROM temp_thing_import
        ON CONFLICT(city_id) DO UPDATE SET
          lat = EXCLUDED.lat,
          lng = EXCLUDED.lng,
          name = EXCLUDED.name,
          deleted_at = NULL
      SQL

      return created_things
    end
  end
end
