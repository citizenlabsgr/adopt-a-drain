require 'test_helper'

class AddressesControllerTest < ActionController::TestCase
  test 'should return latitude and longitude for a valid address' do
    # google_geocoder = 'https://maps.google.com/maps/api/geocode/json'
    google_geocoder = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, google_geocoder).
      with(query: {address: 'Rosa Parks Circle, Grand Rapids, MI', key: ENV['GOOGLE_MAPS_JAVASCRIPT_API_KEY'], sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/city_hall.json', __FILE__)))
    get :show, address: 'Rosa Parks Circle', city_state: 'Grand Rapids, MI', format: 'json'
    assert_not_nil assigns :address
  end
=begin
  test 'should return an error for an invalid address' do
    # google_geocoder = 'https://maps.google.com/maps/api/geocode/json'
    google_geocoder = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, google_geocoder).
      with(query: {address: ', ', sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))

    stub_request(:get, 'http://geocoder.us/service/csv/geocode').
      with(query: {address: ', '}).
      to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))

    get :show, address: '', city_state: '', format: 'json'
    assert_response :missing
  end
=end

test 'should return an error for an invalid address' do
  # google_geocoder = 'https://maps.google.com/maps/api/geocode/json'
  #google_geocoder = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + ENV['GOOGLE_MAPS_JAVASCRIPT_API_KEY'] + '&sensor=false'
  google_geocoder = 'https://maps.googleapis.com/maps/api/geocode/json'
  stub_request(:get, google_geocoder).
    with(query: {address: ', ', key: ENV['GOOGLE_MAPS_JAVASCRIPT_API_KEY'], sensor: 'false'}).
    to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))

  stub_request(:get, 'http://geocoder.us/service/csv/geocode').
    with(query: {address: ', '}).
    to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))

  get :show, address: '', city_state: '', format: 'json'
  assert_response :missing
end

end
