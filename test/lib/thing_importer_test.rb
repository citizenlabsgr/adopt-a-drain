require 'test_helper'

require 'thing_importer'

class ThingImporterTest < ActiveSupport::TestCase
  fake_response = '[
  {
    "dr_asset_id": "TEST-3",
    "dr_lat": 42.38,
    "dr_lon": -71.07,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "ABC"
  },
  {
    "dr_asset_id": "TEST-10",
    "dr_lat": 36.75,
    "dr_lon": -121.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "DEF"
  },
  {
    "dr_asset_id": "TEST-11",
    "dr_lat": 37.75,
    "dr_lon": -122.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "ABC"
  },
  {
    "dr_asset_id": "TEST-12",
    "dr_lat": 39.75,
    "dr_lon": -121.40,
    "dr_type": "Catch Basin Drain",
    "dr_subwatershed": "DEF"
  }
  ]'

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

    # We are not currently sending import reports
    # email = ActionMailer::Base.deliveries.last
    # assert_equal email.to, [admin.email]
    # assert_equal email.subject, 'Adopt-a-Drain Lower Grand River Watershed import (1 adopted drains removed, 1 drains added, 7 unadopted drains removed)'

    thing11.reload
    thing10.reload

    # Asserts thing_1 is deleted
    assert_nil Thing.find_by(dr_asset_id: thing1.dr_asset_id)

    # Asserts thing_3 is reified
    expected = deleted_thing.id
    actual = Thing.find_by(dr_asset_id: 'TEST-3').dr_asset_id

    assert_equal actual, deleted_thing.dr_asset_id

    # Asserts creates new thing
    new_thing = Thing.find_by(dr_asset_id: 'TEST-12')
    assert_not_nil new_thing

    assert_equal new_thing.lat, BigDecimal.new(39.75, 16)

    assert_equal new_thing.lng, BigDecimal.new(-121.40, 16)

    # Asserts properties on thing_11 have been updated
    assert_equal thing11.lat, BigDecimal.new(37.75, 16)

    assert_equal thing11.lng, BigDecimal.new(-122.40, 16)

    # Asserts properties on thing_10 have been updated
    assert_equal 'Storm Drain', thing10.name

    assert_equal BigDecimal.new(36.75, 16), thing10.lat

    assert_equal BigDecimal.new(-121.40, 16), thing10.lng

  end

end
