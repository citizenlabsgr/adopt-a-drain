class Labels(dict):

    def getList(self,key):
        return self[key]

def get_feature_labels():
    '''
    returns dictionary of feature labels
    :return:
    '''
    return {
        'age': [n for n in range(0, 116)],
        'age_group': ['0 to 14', '15 to 24', '25 to 54', '55 to 65', '65+'],
        'appointments': [],
        'appointment_group': ['1 appt', '2 to 12', '13 to 24', '25 to 42', '43+'],
        'attendance': ['No-Show', 'Show'],
        'alcoholism': ['Non-alcoholic', 'Alcoholic'],

        'diabetes': ['Non-diabetic', 'Diabetic'],
        'disabled': ['Non-disabled', '1', '2', '3', '4'],

        'gender': ['Female', 'Male'],

        'handcap': ['Not', '1-HC', '2-HC', '3-HC', '4-HC'],
        'hipertension': ['Non-hipertensive', 'Hipertensive'],

        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'no_show': ['Show', 'No-Show'],
        'no_shows': [],  # leave empty... unclassified data

        'scholarship': ['Non-Scholar', 'Scholar'],

        'scheduled_day_of_week': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'scheduled_time': [],
        'scheduled_hour': ['{}:00'.format(hour) for hour in range(0, 25)],
        'sms': ['Not-cancelled', 'SMS Cancelled'],

        'skipper': ['Non-skipper', 'Skipper']

    }