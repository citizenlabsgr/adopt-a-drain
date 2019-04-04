
class deprecated_CondenseTransforms:

    #def preProcess(self):
    #    substituteJSON()

    #def substituteJSON(self):



    def get_categories(self):
        return {
            'attendance' : [  # reorganize no-show, flip values
                {'label': 'show', 'range': (0, 0), 'category': 1},
                {'label': 'no-show', 'range': (1, 1), 'category': 0}
            ],
            'age' : [  #
                {'label': '0 to 14 yrs', 'range': (0, 15), 'category': 0},
                {'label': '15 to 24', 'range': (15, 25), 'category': 1},
                {'label': '25 to 54', 'range': (25, 55), 'category': 2},
                {'label': '55 to 64', 'range': (55, 65), 'category': 3},
                {'label': '65', 'range': (65, 115), 'category': 4}
            ],

            #'agexappts': [  #
            #    {'label': '0 to 14 yrs', 'range': (0, 15), 'category': 0},
            #    {'label': '15 to 24', 'range': (15, 25), 'category': 1},
            #    {'label': '25 to 54', 'range': (25, 55), 'category': 2},
            #    {'label': '55 to 64', 'range': (55, 65), 'category': 3},
            #    {'label': '65', 'range': (65, 115), 'category': 4}
            #],
            'no_show_group' : [  # no show category conversion
                {'value': 'Yes', 'category': 1},
                {'value': 'No', 'category': 0}
            ],
            'f_m_group' : [  # male female category conversion
                {'value': 'F', 'category': 0},
                {'value': 'M', 'category': 1}
            ],
            'deprecated_age_category' : [  # group pass
                {'label': '0 to 14 appts', 'range': (0, 15), 'category': 0},
                {'label': '15 to 24', 'range': (15, 25), 'category': 1},
                {'label': '25 to 54', 'range': (25, 55), 'category': 2},
                {'label': '55 to 64', 'range': (55, 65), 'category': 3},
                {'label': '65', 'range': (65, 115), 'category': 4}
            ],
            'deprecated_attend_category' : [  # categorize pass
                {'label': '0 to 9', 'range': (0, 10), 'category': 0},
                {'label': '10 to 19', 'range': (10, 20), 'category': 1},
                {'label': '20 to 29', 'range': (20, 30), 'category': 2},
                {'label': '30 to 39', 'range': (30, 40), 'category': 3},
                {'label': '40 to 50', 'range': (40, 100), 'category': 4}
            ],
            'no_show_count' : [
                {'count': [1]}
            ],  # count if value is equal to 1 or any other value in list

            'appointments' : [
                {'label': '1 appt', 'range': (0, 1), 'category': 0},
                {'label': '2 to 12', 'range': (2, 13), 'category': 1},
                {'label': '13 to 24', 'range': (13, 25), 'category': 2},
                {'label': '25 to 42', 'range': (25, 43), 'category': 3},
                {'label': '43+', 'range': (43, 100), 'category': 4}

            ]
        }
    def addMissingDefaults(self, trans):

        fields = trans['fields']
        for row in fields:
            if not 'function' in row:
                row['function']=None
            if not 'virtual' in row:
                row['virtual'] = False
            if not 'categories' in row:
                row['categories'] = None
            if not 'field_out' in row:
                row['field_out'] = row['field_in']
            if not 'field_in_2' in row:
                row['field_in_2'] = None

    def getTransforms(self):

        trans = {
            'appt_transform' : {
                'out_file_name': '03.appointments.csv',
                    'fields': [
                        {'field_in': 'appointment_id', 'field_out': 'appointment_id', 'function': None},
                        {'field_in': 'patient_id', 'field_out': 'patient_id', 'function': None},
                        {'field_in': 'no_show', 'field_out': 'attendance', 'categories': self.get_categories()['attendance'],
                         'function': 'categorize'},
                        {'field_in': 'scheduled_day', 'field_out': 'scheduled_day_of_week', 'function': 'day_of_week'},
                        {'field_in': 'scheduled_day', 'field_out': 'scheduled_hour', 'function': 'hour'},
                        {'field_in': 'scheduled_day', 'field_out': 'scheduled_time', 'function': 'time'},
                        {'field_in': 'no_show', 'field_out': 'no_show', 'function': None},
                        {'field_in': 'lon', 'field_out': 'lon', 'function': None},
                        {'field_in': 'lat', 'field_out': 'lat', 'function': None},

                    ]
            },
            'patient1_transform' : {
                    'out_file_name': '03.01.patients.csv',
                    'group_by': 'patient_id',
                    'fields': [
                        {'field_in': 'patient_id', 'field_out': 'patient_id'},
                        {'field_in': 'no_show', 'field_out': 'appointments', 'function': 'count'},
                        {'field_in': 'no_show', 'field_out': 'no_shows', 'categories': self.get_categories()['no_show_count'],
                         'function': 'count-category'},
                        # {'field_in': 'no_show', 'field_out': 'appointment_group', 'categories': appointment_category, 'function': 'categorize'},

                        {'field_in': 'scholarship', 'field_out': 'scholarship', 'function': 'high-value'},
                        {'field_in': 'hipertension', 'field_out': 'hipertension', 'function': 'high-value'},
                        {'field_in': 'diabetes', 'field_out': 'diabetes', 'function': 'high-value'},
                        {'field_in': 'alcoholism', 'field_out': 'alcoholism', 'function': 'high-value'},
                        {'field_in': 'handcap', 'field_out': 'handcap', 'function': 'high-value'},
                        {'field_in': 'gender', 'field_out': 'gender'},
                        {'field_in': 'age', 'field_out': 'age', 'function': 'high-value'},
                        {'field_in': 'age', 'field_out': 'age_group', 'categories': self.get_categories()['age'],
                         'function': 'categorize'},
                        #{'field_in': 'no_show', 'field_out': 'skipper', 'function': 'ratio'}
                        {'field_in': 'no_show', 'field_out': 'skipper', 'function': 'high-value'},
                        {'field_in': 'no_shows', 'field_in_2':'appointments','virtual':True, 'field_out': 'proporttion_of_no_shows',
                         'function': 'ratio'},
                        {'field_in': 'lon', 'field_out': 'lon', 'function': None},
                        {'field_in': 'lat', 'field_out': 'lat', 'function': None},
                    ]
            },
            'patient2_transform' : {  # unable to group and count derived features, so run again
                    'out_file_name': '03.02.patients.csv',
                    'condensed': 'patients.csv',
                    'fields': [
                        {'field_in': 'patient_id', 'field_out': 'patient_id'},  # pass through

                        {'field_in': 'appointments', 'field_out': 'appointments'},
                        {'field_in': 'no_shows', 'field_out': 'no_shows'},
                        {'field_in': 'appointments', 'field_out': 'appointment_group',
                         'categories': self.get_categories()['appointments'], 'function': 'categorize'},

                        {'field_in': 'scholarship', 'field_out': 'scholarship'},
                        {'field_in': 'hipertension', 'field_out': 'hipertension'},
                        {'field_in': 'diabetes', 'field_out': 'diabetes'},
                        {'field_in': 'alcoholism', 'field_out': 'alcoholism'},
                        {'field_in': 'handcap', 'field_out': 'handcap'},
                        {'field_in': 'gender', 'field_out': 'gender'},
                        {'field_in': 'age', 'field_out': 'age'},
                        {'field_in': 'age_group', 'field_out': 'age_group'},
                        {'field_in': 'proportion_of_no_shows'},
                        #{'field_in': 'age', 'field_2': 'appointments', 'field_out': 'agexappts',
                        # 'categories': self.get_categories()['agxappts'],
                        # 'function': 'cross_categorize'},
                        {'field_in': 'skipper', 'field_out': 'skipper'},
                        {'field_in': 'lon', 'field_out': 'lon', 'function': None},
                        {'field_in': 'lat', 'field_out': 'lat', 'function': None},
                    ]
            }

        }
        for item in trans:
            self.addMissingDefaults(trans[item])

        return trans

    def best_transform(self,df_data, hint=None):
        '''
            field_in has to match all fields of df_data
        :param df_data:
        :return:
        '''
        tranform = {}
        #print('df_data: ',df_data)
        col_names = df_data.columns
        #print('col_names: ', col_names)
        transforms = self.getTransforms()
        likely_transforms = transforms.items()
        if hint != None:
            likely_transforms = []
            for t,item in transforms.items():
                if hint in t:
                    likely_transforms.append(item)

        # TODO: need key_in and key_out validation here

        for item in likely_transforms: # process all features
            #print('item: ', item)
            #self.addMissingDefaults(item)
            #print('addMissing: ', item)
            fields = [x for x in item['fields']]
            #print('fields: ',fields)
            for rec in fields:  # process item fields
                # print('rec: ', rec)
                if 'field_in' in rec:
                    if not rec['virtual']:
                        # print('virtual')
                        if rec['field_in'] in col_names:
                            transform = item  # over and over and over
                        else:
                            msg = 'field: {} not in dataframe columns: {}'.format(rec['field_in'],col_names)
                            transform = {'error':msg}
                            raise NameError(msg)
                            break

            if len(transform) > 0:
                #print('transform: ', t)
                break



        return transform


def main():
    import pandas as pd
    df = pd.read_csv('03.source_clean.csv')
    #df.info()
    #print(df.head)
    #trans = CondenseTransforms().best_transform(df)


    #print(trans)
    df.info()
    print(CondenseTransforms().best_transform(df,hint='patient1_transform'))




if __name__ == "__main__":
    # execute only if run as a script
    main()