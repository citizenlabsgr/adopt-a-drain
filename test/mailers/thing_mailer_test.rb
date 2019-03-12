require 'test_helper'

class ThingMailerTest < ActionMailer::TestCase
  test 'first_adopted_confirmation' do
    @user = users(:erik)
    @thing = things(:thing_1)
    @thing.user = @user

    email = ThingMailer.first_adoption_confirmation(@thing).deliver_now

    assert_not ActionMailer::Base.deliveries.empty?
    assert_equal ['hello@citizenlabs.org'], email.from
    assert_equal ['erik@example.com'], email.to
    assert_equal 'Thanks for adopting a drain, Erik!', email.subject
  end

  # https://github.com/rails/rails/blob/master/actionmailer/test/base_test.rb
  test "first_adopted_confirmation inline attachments" do
    @user = users(:erik)
    @thing = things(:thing_1)
    @thing.user = @user

    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/logos/adopt-a-drain.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/facebook.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/twitter.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/instagram.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/logos/drain-cleaner.png'}"))

    email = ThingMailer.first_adoption_confirmation(@thing)
    assert_nothing_raised { email.message }

    assert_equal ["image/png; filename=adopt-a-drain.png",
                    "image/png; filename=facebook.png",
                    "image/png; filename=twitter.png",
                    "image/png; filename=instagram.png",
                    "image/png; filename=drain-cleaner.png"],
                email.attachments.inline.map { |a| a["Content-Type"].to_s }
  end

  test 'second_adoption_confirmation' do
    @user = users(:erik)
    @thing = things(:thing_1)
    @thing.user = @user

    email = ThingMailer.second_adoption_confirmation(@thing).deliver_now

    assert_not ActionMailer::Base.deliveries.empty?
    assert_equal ['hello@citizenlabs.org'], email.from
    assert_equal ['erik@example.com'], email.to
    assert_equal 'Thanks for adopting another drain, Erik!', email.subject

  end

  test "second_adopted_confirmation inline attachments" do
    @user = users(:erik)
    @thing = things(:thing_1)
    @thing.user = @user

    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/logos/adopt-a-drain.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/facebook.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/twitter.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/instagram.png'}"))
    assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/logos/drain-cleaner.png'}"))

    email = ThingMailer.second_adoption_confirmation(@thing)
    assert_nothing_raised { email.message }

    assert_equal ["image/png; filename=adopt-a-drain.png",
                    "image/png; filename=facebook.png",
                    "image/png; filename=twitter.png",
                    "image/png; filename=instagram.png",
                    "image/png; filename=drain-cleaner.png"],
                email.attachments.inline.map { |a| a["Content-Type"].to_s }
  end

  # This email unused at this time
  # test 'third_adoption_confirmation' do
  #   @user = users(:erik)
  #   @thing = things(:thing_1)
  #   @thing.user = @user

  #   email = ThingMailer.third_adoption_confirmation(@thing).deliver_now

  #   assert_not ActionMailer::Base.deliveries.empty?
  #   assert_equal ['hello@citizenlabs.org'], email.from
  #   assert_equal ['erik@example.com'], email.to
  #   assert_equal 'We really do love you, Erik!', email.subject
  # end

  # This email unused at this time
  # test "third_adopted_confirmation inline attachments" do
  #   @user = users(:erik)
  #   @thing = things(:thing_1)
  #   @thing.user = @user

  #   assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/logos/adopt-a-drain.png'}"))
  #   assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/facebook.png'}"))
  #   assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/twitter.png'}"))
  #   assert(File.exists?("#{Rails.root.to_s + '/app/assets/images/icons/instagram.png'}"))

  #   email = ThingMailer.third_adoption_confirmation(@thing)
  #   assert_nothing_raised { email.message }

  #   assert_equal ["image/png; filename=adopt-a-drain.png",
  #                   "image/png; filename=facebook.png",
  #                   "image/png; filename=twitter.png",
  #                   "image/png; filename=instagram.png"],
  #               email.attachments.inline.map { |a| a["Content-Type"].to_s }
  # end

  test 'thing_update_report' do
    admin1 = users(:admin)
    admin2 = users(:admin)
    admin2.update(email: 'admin2@example.com')
    email = nil
    deleted_thing = things(:thing_1)

    assert_emails(1) do
      email = ThingMailer.thing_update_report([deleted_thing], [], []).deliver_now
    end

    assert_includes email.to, admin1.email
    assert_includes email.to, admin2.email

    assert_equal email.subject, 'Adopt-a-Drain Grand River Basin import (1 adopted drains removed, 0 drains added, 0 unadopted drains removed)'
  end
end
