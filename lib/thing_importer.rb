require 'open-uri'
require 'uri'
require 'net/http'
require 'json'
# class for importing things from JSON data.world datasource
# is currently very specific to drains from Lower Grand River Watershed
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

        # We are not currently sending import reports
        # ThingMailer.thing_update_report(deleted_things_with_adoptee, deleted_things_no_adoptee, created_things).deliver_now
      end

    end

    def integer?(string)
      return true
    end

    def inferDefaultName(currName)

      if ['Storm Drain', 'Storm Water Inlet Drain', 'Catch Basin Drain'].detect {|str| str == currName }
        return 'Storm Drain'
      end

      return currName
    end

    def normalize_thing(json_thing)

      norm = {
        name: inferDefaultName(json_thing['dr_type']),
        lat: json_thing['dr_lat'],
        lng: json_thing['dr_lon'],
        type: json_thing['dr_type'],
        system_use_code: json_thing['dr_subwatershed'],
        jurisdiction: json_thing['dr_jurisdiction'],
        dr_asset_id: json_thing['dr_asset_id'],
        dr_discharge: json_thig['dr_discharge']
      }

      return norm
    end

    def invalid_thing(thing)
      # bare minimum validation of imported data
      rc = true
      # make sure type value is a acceptable
      if not ['Storm Drain', 'Storm Water Inlet Drain', 'Catch Basin Drain'].include?(thing[:type])
        rc = false
        raise "Unknown drain type: "
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
          system_use_code varchar,
          jurisdiction varchar,
          dr_asset_id varchar,
          dr_discharge
        )
      SQL
      conn.raw_connection.prepare(insert_statement_id, 'INSERT INTO temp_thing_import (name, lat, lng, system_use_code, jurisdiction, dr_asset_id,dr_discharge) VALUES($1, $2, $3, $4, $5, $6, $7)')

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
           [drain[:name], drain[:lat], drain[:lng], drain[:system_use_code], drain[:jurisdiction], drain[:dr_asset_id], drain[:dr_discharge]],
        )
      end

      conn.execute('CREATE INDEX "temp_thing_import_dr_asset_id" ON temp_thing_import(dr_asset_id)')

    end

    # mark drains as deleted that do not exist in the new set
    # return the deleted drains partitioned by whether they were adopted
    def delete_non_existing_things
      # mark deleted_at as this is what the paranoia gem uses to scope
      deleted_things = ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        UPDATE things
        SET deleted_at = NOW()
        WHERE things.dr_asset_id NOT IN (SELECT dr_asset_id from temp_thing_import) AND deleted_at IS NULL
        RETURNING things.dr_asset_id, things.user_id
      SQL
      deleted_things.partition { |thing| thing['user_id'].present? }
    end

    def upsert_things
      # postgresql's RETURNING returns both updated and inserted records so we
      # query for the items to be inserted first

      created_things = ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        SELECT temp_thing_import.dr_asset_id
        FROM things
        RIGHT JOIN temp_thing_import ON temp_thing_import.dr_asset_id = things.dr_asset_id
        WHERE things.id IS NULL
      SQL

      ActiveRecord::Base.connection.execute(<<-SQL.strip_heredoc)
        INSERT INTO things(name, lat, lng, system_use_code, jurisdiction, dr_asset_id, dr_discharge)
        SELECT name, lat, lng, system_use_code, jurisdiction, dr_asset_id, dr_discharge FROM temp_thing_import
        ON CONFLICT(dr_asset_id) DO UPDATE SET
          lat = EXCLUDED.lat,
          lng = EXCLUDED.lng,
          name = EXCLUDED.name,
          deleted_at = NULL,
          jurisdiction = EXCLUDED.jurisdiction,
          dr_asset_id = EXCLUDED.dr_asset_id,
          dr_discharge = EXCLUDED.dr_discharge
      SQL

      return created_things
    end

  end
end
