class RenameDateAdoptedToAdoptedAtInThings < ActiveRecord::Migration
  def change
    def up
    rename_column :things, :date_adopted, :adopted_at
  end

  def down
    rename_column :things, :adopted_at, :date_adopted
  end
end
