require 'test_helper'

class UsersControllerTest < ActionController::TestCase
  include Devise::Test::ControllerHelpers
  setup do
    request.env['devise.mapping'] = Devise.mappings[:user]
    @user = users(:erik)
  end

  test 'should render edit form' do
    sign_in @user
    get :edit
    assert_response :success
    assert_select 'form#edit_form' do
      assert_select '[action=?]', '/users'
      assert_select '[method=?]', 'post'
    end
    assert_select 'input', count: 10
    assert_select 'label', count: 6
    assert_select 'input[name="commit"]' do
      assert_select '[type=?]', 'submit'
      assert_select '[value=?]', 'Update'
    end
    assert_select 'a.btn', 'Back'
  end

  test 'should update user if password is correct' do
    sign_in @user
    assert_not_equal 'New Name', @user.name
    put :update, user: {first_name: 'New', last_name: 'Name', current_password: 'correct'}
    @user.reload
    assert_equal 'New Name', @user.name
    assert_response :redirect
    assert_redirected_to controller: 'sidebar', action: 'search'
  end

  test 'should return error if password is incorrect' do
    sign_in @user
    put :update, user: {name: 'New Name', current_password: 'incorrect'}
    assert_response :error
  end

  test 'should create user if information is valid' do
    post :create, user: {email: 'user@example.com', first_name: 'User', last_name: '123', password: 'correct', password_confirmation: 'correct'}
    assert_response :success
  end

  test 'should return error if information is invalid' do
    post :create, user: {email: 'user@example.com', first_name: 'User', password: 'correct', password_confirmation: 'incorrect'}
    assert_response :error
  end
end
