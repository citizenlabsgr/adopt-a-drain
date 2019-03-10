require 'rails_helper'

RSpec.feature "Sign Up", type: :feature, js: true do
  it 'can be signed up on' do
    visit '/'
    click_on 'Register / Sign in'

    fill_in 'user[email]', with: 'test@example.com'
    fill_in 'user[first_name]', with: 'Testy'
    fill_in 'user[last_name]', with: 'Test Person'
    fill_in 'user[password_confirmation]', with: 'foo-foo-bar'
    click_on "Sign up"

    expect(page).to have_content('Edit profile')
  end
end
