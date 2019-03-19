class AddDateAdoptedToThings < ActiveRecord::Migration
  def change
    add_column :things, :date_adopted, :datetime
  end
end
