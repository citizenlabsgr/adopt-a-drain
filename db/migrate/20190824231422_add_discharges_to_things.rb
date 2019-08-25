class AddDischargesToThings < ActiveRecord::Migration
  def change
    add_column :things, :dr_discharge, :string
  end
end
