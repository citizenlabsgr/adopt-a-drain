class AddJurisdictionToThings < ActiveRecord::Migration
  def change
    add_column :things, :jurisdiction, :string
  end
end
