require 'test_helper'

class RemindersControllerTest < ActionController::TestCase
  include Devise::Test::ControllerHelpers
  setup do
    request.env['devise.mapping'] = Devise.mappings[:user]
    @thing = things(:thing_1)
    @dan = users(:dan)
    @user = users(:erik)
    @admin = users(:admin)
    @thing.user = @dan
    @thing.adopted_at = Time.now.to_formatted_s(:db)
    @thing.save!
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, geocode_url).
      with(query: {latlng: '42.383339,-71.049226', key: ENV["GOOGLE_MAPS_JAVASCRIPT_API_KEY"], sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/city_hall.json', __FILE__)))
  end

  test 'should send a reminder email if admin' do
    sign_in @admin
    num_deliveries = ActionMailer::Base.deliveries.size
    post :create, format: :json, reminder: {thing_id: @thing.id, to_user_id: @dan.id}
    assert_equal num_deliveries + 1, ActionMailer::Base.deliveries.size
    assert_response :success
    email = ActionMailer::Base.deliveries.last
    assert_equal [@dan.email], email.to
    assert_equal 'Remember to clear your adopted drain', email.subject
  end

  test 'should not send a reminder email if not admin' do
    sign_in @user
    num_deliveries = ActionMailer::Base.deliveries.size
    post :create, format: :json, reminder: {thing_id: @thing.id, to_user_id: @dan.id}
    assert_equal num_deliveries, ActionMailer::Base.deliveries.size
  end
end
