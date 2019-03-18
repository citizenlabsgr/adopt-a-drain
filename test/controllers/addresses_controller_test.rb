require 'test_helper'

class AddressesControllerTest < ActionController::TestCase
  test 'should return latitude and longitude for a valid address' do
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, geocode_url).
      with(query: {address: 'City Hall, Grand Rapids, MI', sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/city_hall.json', __FILE__)))
    get :show, address: 'City Hall', city_state: 'Grand Rapids, MI', format: 'json'
    assert_not_nil assigns :address
  end

  test 'should return an error for an invalid address' do
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, geocode_url).
      with(query: {address: ', ', key: ENV["GOOGLE_MAPS_JAVASCRIPT_API_KEY"], sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))
    stub_request(:get, 'http://geocoder.us/service/csv/geocode').
      with(query: {address: ', '}).
      to_return(body: File.read(File.expand_path('../../fixtures/unknown_address.json', __FILE__)))
    get :show, address: '', city_state: '', format: 'json'
    assert_response :missing
  end
end
