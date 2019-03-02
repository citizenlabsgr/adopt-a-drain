# Preview all emails at http://localhost:3000/rails/mailers/thing_mailer
class ThingMailerPreview < ActionMailer::Preview
    
    def first_adoption_confirmation
        # Note - for this to work, you must assign a valid user_id to thing id number 1 in the database
        ThingMailer.first_adoption_confirmation(Thing.first)
    end

    def second_adoption_confirmation
        # Note - for this to work, you must assign a valid user_id to thing id number 2 in the database
        ThingMailer.second_adoption_confirmation(Thing.second)
    end 

    def third_adoption_confirmation
        # Note - for this to work, you must assign a valid user_id to thing id number 3 in the database
        ThingMailer.third_adoption_confirmation(Thing.third)
    end

    def reminder
        # Note - for this to work, you must assign a valid user_id to thing id number 1 in the database
        ThingMailer.reminder(Thing.first)
    end 
end
