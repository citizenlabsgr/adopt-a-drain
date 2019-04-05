class CreateAdoptions < ActiveRecord::Migration
  def change
    create_table :adoptions do |t|
      t.string :adpt_assetid, :null => false
      t.integer :adpt_userid, :null => false
      t.string :adpt_name
      t.string :adpt_jurisdiction
      t.string :adpt_flows_to
      t.datetime :adpt_created_at, :null => false, :default => Time.now
    end
    add_index :adoptions, :adpt_assetid, unique: true
  end
end
