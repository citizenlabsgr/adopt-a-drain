require 'test_helper'

require 'thing_importer'

class ThingImporterTest < ActiveSupport::TestCase
  #  'PUC_Maximo_Asset_ID,Drain_Type,System_Use_Code,Location',
  #  'N-3,Catch Basin Drain,ABC,"(42.38, -71.07)"',
  #  'N-10,Catch Basin Drain,DEF,"(36.75, -121.40)"',
  #  'N-11,Catch Basin Drain,ABC,"(37.75, -122.40)"',
  #  'N-12,Catch Basin Drain,DEF,"(39.75, -121.40)"',
  fake_response = '[
  {
    "dr_facility_id": 3,
    "dr_lat": 42.38,
    "dr_lon": -71.07,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "ABC"
  },
  {
    "dr_facility_id": 10,
    "dr_lat": 36.75,
    "dr_lon": -121.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "DEF"
  },
  {
    "dr_facility_id": 11,
    "dr_lat": 37.75,
    "dr_lon": -122.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "ABC"
  },
  {
    "dr_facility_id": 12,
    "dr_lat": 39.75,
    "dr_lon": -121.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "DEF"
  }
  ]'
=begin
  fake_response = '[
      {
        "dr_asset_no": 40208317,
        "dr_facility_id": 40208317,
        "dr_jurisdiction": "City of East Grand Rapids",
        "dr_lat": 42.9481700591,
        "dr_local_id": "CB2-764",
        "dr_location": "POINT(-85.6102988883 42.9481700591)",
        "dr_lon": -85.6102988883,
        "dr_owner": "City of East Grand Rapids",
        "dr_subtype": 14,
        "dr_subwatershed": "Direct Drainage to Lower Grand River",
        "dr_sync_id": "EGR_40208317",
        "dr_type": "Storm Water Inlet Drain"
      },
      {
        "dr_asset_no": 40208316,
        "dr_facility_id": 40208316,
        "dr_jurisdiction": "City of East Grand Rapids",
        "dr_lat": 42.948276425100005,
        "dr_local_id": "CB2-767",
        "dr_location": "POINT(-85.6104086108 42.948276425100005)",
        "dr_lon": -85.6104086108,
        "dr_owner": "City of East Grand Rapids",
        "dr_subtype": 14,
        "dr_subwatershed": "Direct Drainage to Lower Grand River",
        "dr_sync_id": "EGR_40208316",
        "dr_type": "Storm Water Inlet Drain"
      },
      {
        "dr_asset_no": 40087031,
        "dr_facility_id": 40087031,
        "dr_jurisdiction": "City of East Grand Rapids",
        "dr_lat": 42.9387053237,
        "dr_local_id": "CB4-1523",
        "dr_location": "POINT(-85.6142482835 42.9387053237)",
        "dr_lon": -85.6142482835,
        "dr_owner": "City of East Grand Rapids",
        "dr_subtype": 15,
        "dr_subwatershed": "Plaster Creek",
        "dr_sync_id": "EGR_40087031",
        "dr_type": "Storm Water Inlet Drain"
      },
      {
        "dr_asset_no": 40156713,
        "dr_facility_id": 40156713,
        "dr_jurisdiction": "City of East Grand Rapids",
        "dr_lat": 42.9520658791,
        "dr_local_id": "CB2-463",
        "dr_location": "POINT(-85.5945558134 42.9520658791)",
        "dr_lon": -85.5945558134,
        "dr_owner": "City of East Grand Rapids",
        "dr_subtype": 15,
        "dr_subwatershed": "Direct Drainage to Lower Grand River",
        "dr_sync_id": "EGR_40156713",
        "dr_type": "Storm Water Inlet Drain"
      }
    ]'
=end
  test 'import does not modify data if endpoint fails' do

    thing1 = things(:thing_1)

    fake_url ='https://grb-storm-drains'

    stub_request(:post, fake_url) \
      .to_return(status: [500, 'Internal Server Error'], body: nil)

    assert_raises JSON::ParserError, OpenURI::HTTPError do

      ThingImporter.load(fake_url)
    end
    assert_not_nil Thing.find(thing1.id)

  end

  test 'loading things, deletes existing things not in data set, updates properties on rest' do

    admin = users(:admin)
    thing1 = things(:thing_1)
    thing11 = things(:thing_11)
    thing10 = things(:thing_10).tap do |thing|
      thing.update!(name: 'Erik drain', user_id: users(:erik).id)
    end
    things(:thing_9).tap do |thing|
      thing.update!(user_id: users(:erik).id)
    end

    deleted_thing = things(:thing_3)
    deleted_thing.destroy!

    fake_url = 'https://api.data.world/v0/sql/citizenlabs/grb-storm-drains'

    stub_request(:post, fake_url) \
    .to_return(status: [200, 'OK'], body: fake_response, headers: {})

    ThingImporter.load(fake_url)

    email = ActionMailer::Base.deliveries.last
    assert_equal email.to, [admin.email]
    assert_equal email.subject, 'Adopt-a-Drain Grand River Basin import (1 adopted drains removed, 1 drains added, 7 unadopted drains removed)'
    thing11.reload
    thing10.reload

    # Asserts thing_1 is deleted
    assert_nil Thing.find_by(id: thing1.id)

    # Asserts thing_3 is reified
    expected = deleted_thing.id
    actual = Thing.find_by(city_id: 3).id

    assert_equal actual, deleted_thing.id

    # Asserts creates new thing
    new_thing = Thing.find_by(city_id: 12)
    assert_not_nil new_thing

    assert_equal new_thing.lat, BigDecimal.new(39.75, 16)

    assert_equal new_thing.lng, BigDecimal.new(-121.40, 16)

    # Asserts properties on thing_11 have been updated
    assert_equal thing11.lat, BigDecimal.new(37.75, 16)

    assert_equal thing11.lng, BigDecimal.new(-122.40, 16)

    # Asserts properties on thing_10 have been updated
    assert_equal 'Catch Basin Drain', thing10.name

    assert_equal BigDecimal.new(36.75, 16), thing10.lat

    assert_equal BigDecimal.new(-121.40, 16), thing10.lng

  end

end
