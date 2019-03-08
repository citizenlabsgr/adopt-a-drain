require 'rails_helper'

RSpec.feature "Sign Up", type: :feature, js: true do
  it 'can be signed up on' do
    visit '/'
    click_on 'Register / Sign in'
    fill_in 'user_email', with: 'test@example.com'

    choose "I haven't signed up yet"

    fill_in 'user_first_name', with: 'test@example.com'
    fill_in 'user_last_name', with: 'test@example.com'

    fill_in 'user_password_confirmation', with: 'foo-foo'

    click_on "Sign up"

    expect(page).to have_content('Edit profile')
  end
end
