class AddAssetIdToThings < ActiveRecord::Migration
  def change
    add_column :things, :dr_asset_id, :string
    add_index :things, :dr_asset_id, unique: true
  end
end
