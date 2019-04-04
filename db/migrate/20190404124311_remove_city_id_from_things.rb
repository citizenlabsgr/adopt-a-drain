class RemoveCityIdFromThings < ActiveRecord::Migration
  def change
    remove_index :things, :column => :city_id
    remove_column :things, :city_id
  end
end
