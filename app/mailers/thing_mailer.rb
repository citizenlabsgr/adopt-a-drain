class ThingMailer < ApplicationMailer
  def first_adoption_confirmation(thing)
    @thing = thing
    @user = thing.user

    attachments.inline['adopt-a-drain-300.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/logos/adopt-a-drain-300.png'}")
    attachments.inline['facebook.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/facebook.png'}")
    attachments.inline['twitter.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/twitter.png'}")
    attachments.inline['instagram.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/instagram.png'}")
    attachments.inline['major-runoff-cleaning.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/major-runoff-cleaning-opt.png'}")

    mail(to: @user.email, subject: ["Thanks for adopting a drain"])
  end

  def second_adoption_confirmation(thing)
    @thing = thing
    @user = thing.user

    attachments.inline['adopt-a-drain-300.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/logos/adopt-a-drain-300.png'}")
    attachments.inline['facebook.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/facebook.png'}")
    attachments.inline['twitter.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/twitter.png'}")
    attachments.inline['instagram.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/icons/instagram.png'}")
    attachments.inline['major-runoff-thumbs-up.png'] = File.read("#{Rails.root.to_s + '/app/assets/images/major-runoff-thumbs-up-opt.png'}")

    mail(to: @user.email, subject: ["Thanks for adopting another drain, #{@user.name.split.first}!"])
  end

  # This email is unused at this time
  # def third_adoption_confirmation(thing)
  #   @thing = thing
  #   @user = thing.user
  #   mail(to: @user.email, subject: ["We really do love you, #{@user.name.split.first}!"])
  # end

  def reminder(thing)
    @thing = thing
    @user = thing.user
    mail(to: @user.email, subject: ['Remember to clear your adopted drain'])
  end

  # rubocop:disable Metrics/AbcSize
  def thing_update_report(deleted_things_with_adoptee, deleted_things_no_adoptee, created_things)

    @deleted_thing_ids_with_adoptee = deleted_things_with_adoptee.map { |t| t['dr_asset_id'] }

    @deleted_thing_ids_with_no_adoptee = deleted_things_no_adoptee.map { |t| t['dr_asset_id'] }

    @created_thing_ids = created_things.map { |t| t['dr_asset_id'] }

    subject = t('subjects.update_report',
                title: t('titles.main', thing: t('defaults.thing').titleize, context:t('context.place')),
                deleted_adopted_count: deleted_things_with_adoptee.count,
                created_count: created_things.count,
                deleted_unadopted_count: deleted_things_no_adoptee.count,
                things: t('defaults.things'))

    mail(to: User.where(admin: true).pluck(:email), subject: subject)

  end
  # rubocop:enable Metrics/AbcSize
end
