require 'test_helper'

class ThingsControllerTest < ActionController::TestCase
  include Devise::Test::ControllerHelpers
  setup do
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    stub_request(:get, geocode_url).
      with(query: {latlng: '42.383339,-71.049226', sensor: 'false'}).
      to_return(body: File.read(File.expand_path('../../fixtures/city_hall.json', __FILE__)))

    @thing = things(:thing_1)
    @user = users(:dan)
  end

  test 'should list drains' do
    get :show, format: 'json', lat: 42.358431, lng: -71.059773
    assert_not_nil assigns :things
    assert_response :success
  end

  test 'should 404 if there are no drains' do
    Thing.all.map(&:destroy!)
    get :show, format: 'json', lat: 43.358431, lng: -71.059773
    assert_response :missing
    assert_equal ['Could not find drain.'], JSON.parse(response.body)['errors']['address']
  end

  test 'should return true if a drain is owned by logged in user' do
    sign_in @user
    @thing.user_id = @user.id
    get :show, format: 'json', lat: 42.358431, lng: -71.059773
    assert_not_nil assigns :things
    assert_response :success
  end

  test 'should update drain display name' do
    sign_in @user
    assert_not_equal 'Birdsill', @thing.display_name
    put :update, format: 'json', id: @thing.id, thing: {user_id: @user.id, adopted_name: 'Birdsill'}
    @thing.reload
    assert_equal 'Birdsill', @thing.display_name
    assert_not_nil assigns :thing
    assert_response :success
  end

  test 'should error when updating drain with invalid data' do
    Thing.stub(:find, @thing) do
      @thing.stub(:update_attributes, false) do
        put :update, format: 'json', id: @thing.id, thing: {adopted_name: 'hello'}
      end
    end
    assert_response :error
  end

  test 'should update drain and send an adopted confirmation email' do

    sign_in @user
    num_deliveries = ActionMailer::Base.deliveries.size

    time_str = Time.now.to_formatted_s(:db)
    put :update, format: 'json', id: @thing.id, thing: {adopted_name: 'Drain', user_id: @user.id, adopted_at: time_str}

    assert @thing.reload.adopted?
    assert_equal num_deliveries + 1, ActionMailer::Base.deliveries.size
    assert_response :success

    email = ActionMailer::Base.deliveries.last
    assert_equal [@user.email], email.to
    assert_equal 'Thanks for adopting a drain', email.subject
  end

  test 'should send second confirmation email' do
    sign_in @user
    @user.things = [things(:thing_2)]

    time_str = Time.now.to_formatted_s(:db)
    put :update, format: 'json', id: @thing.id, thing: {adopted_name: 'Drain', user_id: @user.id, adopted_at: time_str }

    assert @thing.reload.adopted?
    assert_response :success

    email = ActionMailer::Base.deliveries.last
    assert_equal [@user.email], email.to
    assert_equal 'Thanks for adopting another drain, Dan!', email.subject
  end

  test 'should update drain but not send an adopted confirmation email upon abandonment' do
    sign_in @user
    num_deliveries = ActionMailer::Base.deliveries.size
    put :update, format: 'json', id: @thing.id, thing: {adopted_name: 'Another Drain', user_id: nil, adopted_at: nil } # a nil user_id is an abandonment

    assert_not @thing.reload.adopted?
    assert_equal num_deliveries, ActionMailer::Base.deliveries.size
    assert_response :success
  end
end
