require 'socket'

Rails.application.configure do
  # Settings specified here will take precedence over those in config/application.rb.

  # In the development environment your application's code is reloaded on
  # every request. This slows down response time but is perfect for development
  # since you don't have to restart the web server when you make code changes.
  config.cache_classes = false

  # asset host
  config.action_controller.asset_host = Proc.new { |source, request|
    # source = "/assets/brands/stockholm_logo_horizontal.png"
    # request = A full-fledged ActionDispatch::Request instance

    # sometimes request is nil and everything breaks
    scheme = request.try(:scheme).presence || "http"
    host = request.try(:host).presence || "localhost:3000"
    port = request.try(:port).presence || nil

    ["#{scheme}://#{host}", port].reject(&:blank?).join(":")
  }
  config.action_mailer.asset_host = config.action_controller.asset_host

  # Do not eager load code on boot.
  config.eager_load = false

  # Show full error reports and disable caching.
  config.consider_all_requests_local       = true
  config.action_controller.perform_caching = false

  # Don't care if the mailer can't send.
  config.action_mailer.raise_delivery_errors = true
  config.action_mailer.default_url_options = {host: 'localhost:3000'}
}

  # Print deprecation notices to the Rails logger.
  config.active_support.deprecation = :log

  # Raise an error on page load if there are pending migrations.
  config.active_record.migration_error = :page_load

  # Debug mode disables concatenation and preprocessing of assets.
  # This option may cause significant delays in view rendering with a large
  # number of complex assets.
  config.assets.debug = true

  # Asset digests allow you to set far-future HTTP expiration dates on all assets,
  # yet still be able to expire them through the digest params.
  config.assets.digest = true

  # Adds additional error checking when serving assets at runtime.
  # Checks for improperly declared sprockets dependencies.
  # Raises helpful error messages.
  config.assets.raise_runtime_errors = true

  # Raises error for missing translations
  # config.action_view.raise_on_missing_translations = true

  # For Mailcatcher
  config.action_mailer.delivery_method = :smtp
  # config.action_mailer.smtp_settings = {address: 'localhost', port: 1025}

  if ENV['GMAIL_ADDRESS'] and ENV['GMAIL_PASSWORD']
    config.action_mailer.smtp_settings = {
      address:              'smtp.gmail.com',
      port:                 587,
      domain:               'example.com',
      user_name:            ENV['GMAIL_ADDRESS'],
      password:             ENV['GMAIL_PASSWORD'],
      authentication:       'plain',
      enable_starttls_auto: true }
  end

end
