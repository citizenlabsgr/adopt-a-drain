# Cleaning functions
import pandas as pd
import numpy as np
import time

def remove_obvious_outliers(_outliers,df):
    summary = {}
    outliers = _outliers['outliers']
    for outlier in outliers:
        col_name = outlier['column']
        summary[col_name] = {'range-drops':0,'category-drops':0}


        if 'range' in outlier:
            #print('range')

            low = outlier['range'][0]
            high = outlier['range'][1]
            sz = len(df)
            #print('colname: ', col_name)
            #print('type: ',type(low))

            if isinstance(low, np.datetime64):
                df = df[(df[col_name].to_datetime() >= low) & (df[col_name].to_datetime() <= high)]
            else:
                df = df[(df[col_name] >= low) & (df[col_name] <= high)]


            summary[col_name]['range-drops'] = sz - len(df)

        elif 'categories' in outlier:
            #print('categories')
            #col_name = outlier['column']

            _list = outlier['categories']
            sz = len(df)
            df = df[df[col_name].isin(_list)]

            summary[col_name]['category-drops'] = sz - len(df)

    return df, summary

def change_types(converts,df):
    summary = {}
    conversions = converts['conversions']
    straight_conversions = [x for x in conversions if not 'categories' in x]

    cat_conversions = [x for x in conversions if 'categories' in x]
    t = time.process_time()
    for cv in conversions:
        summary[cv['column']]={'int':False,'float':False,'datetime':False,'categorize':False}
    elapsed_time = time.process_time() - t
    print('E1 time: ', elapsed_time)
    t = time.process_time()
    for cv in straight_conversions:
        col_name = cv['column']

        if cv['to'] == 'int':
            df[cv['column']] = df[cv['column']].astype(int)
            summary[col_name]['int'] = True
        if cv['to'] == 'float':
            df[cv['column']] = df[cv['column']].astype(float)
            summary[col_name]['float'] = True
        if cv['to'] == 'datetime':
            df[cv['column']] = pd.to_datetime(df[cv['column']])
            summary[col_name]['datetime'] = True

    elapsed_time = time.process_time() - t
    print('E2 time: ', elapsed_time)

    t = time.process_time()
    new_cols = {}
    if len(cat_conversions): # ignore if nothing configured
        for index, row in df.iterrows(): # for each row
            for col_name in df.columns: # each column
                for conv in cat_conversions: # each cat config
                    cat_col = conv['column']
                    for cat in conv['categories']:
                        if col_name == cat_col : # config colname == row[col_name]
                            cat_value = cat['value']
                            cat_cat = cat['category']
                            if cat_value == row[col_name]: # conf value == row value
                                if not col_name in new_cols:

                                    new_cols[col_name]=[cat_cat]
                                    summary[col_name]['categorize'] = True

                                else:

                                    new_cols[col_name].append(cat_cat)



    elapsed_time = time.process_time() - t
    print('E3 time: ', elapsed_time)

    # add converted cols back into dataframe
    t = time.process_time()
    for colname in new_cols:
        df = df.drop(colname,1)
        df[colname]=new_cols[colname]
    elapsed_time = time.process_time() - t
    print('E4 time: ', elapsed_time)
    return df, summary

def get_clean_column_names(actual_col_list):
    '''
    convert each column to lowercase with underscore seperation

    e.g., ID to id
    e.g., County ID to county_id
    e.g., County-ID to county_id
    :param actual_col_list: list of column names
    :return: clean list of column names

    {
      'field-name': {}
    }

    '''
    summary_results = {} # summarize what happened
    clean_column_names = []
    for cn in actual_col_list:
        summary_results[cn] = {}
        ncn = cn
        # get rid of some unwanted characters
        summary_results[cn]['blanks'] = False
        if ' ' in cn:
            ncn = cn.replace(' ','_')
            summary_results[cn]['blanks']=True


        summary_results[cn]['dashes'] = False
        if '-' in cn:
            ncn = cn.replace('-', '_')
            summary_results[cn]['spaces'] = True
        # force first char to lower case
        nncn = ncn
        ncn = ''
        prev_upper = True #False
        case = False
        camelcase = False
        for c in nncn:
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                case = True
                if prev_upper:
                    ncn += c.lower()
                else:
                    ncn += '_' + c.lower()
                    camelcase = True
                prev_upper = True
            else:
                ncn += c
                prev_upper = False

        summary_results[cn]['case'] = case
        summary_results[cn]['camelcase'] = camelcase
        summary_results[cn]['clean-name']=ncn

        clean_column_names.append(ncn)

    return clean_column_names, summary_results

def get_clean_column_names_lean(actual_col_list):
    '''
    convert each column to lowercase with underscore seperation
    e.g., ID to id
    e.g., County ID to county_id
    e.g., County-ID to county_id
    :param actual_col_list: list of column names
    :return: clean list of column names
    '''
    clean_column_names = []
    for cn in actual_col_list:

        ncn = cn
        # get rid of some unwanted characters
        if ' ' in cn:
            ncn = cn.replace(' ','_')
        if '-' in cn:
            ncn = cn.replace('-', '_')
        # force first char to lower case
        nncn = ncn
        ncn = ''
        prev_upper = True #False
        for c in nncn:
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if prev_upper:
                    ncn += c.lower()
                else:
                    ncn += '_' + c.lower()
                prev_upper = True
            else:
                ncn += c
                prev_upper = False

        clean_column_names.append(ncn)

    return clean_column_names

def main():
    print('###############################')
    '''
    print('TEST: get_clean_column_names')

    col_nms = ['PatientId','AppointmentID','Gender',
                              'ScheduledDay','AppointmentDay','Age',
                              'Neighbourhood','Scholarship','Hipertension',
                              'Diabetes','Alcoholism','Handcap','SMS_received',
                              'No-show']
    # go get clean columns
    actual_cols = get_clean_column_names_lean(col_nms)
    print('actual_cols: ', actual_cols)
    # expected results
    expected_cols = ['patient_id','appointment_id','gender',
                              'scheduled_day','appointment_day','age',
                              'neighbourhood','scholarship','hipertension',
                              'diabetes','alcoholism','handcap','sms_received',
                              'no_show']

    assert actual_cols == expected_cols

    actual=cols, results = get_clean_column_names(col_nms)

    print('results: ',results)

    '''
    df_data = pd.DataFrame({
        'A': ['1','2','3','24','55','6','70'],
        'B': ['Yes','No','Yes','No','Yea','Nay','Yes'],
        'C': ['2011-01-01 01:00:00', '2012-01-01 02:00:00', '2013-01-01  03:00:00', '2014-01-01  03:00:00', '2015-01-01  04:00:00', '2016-01-01  05:00:00', '2017-01-01  06:00:00'],
        'D': [True,False,True,False,True,False,True],
        'E': [1,2,3,24,55,6,70],
        'F': ['M','F','M','F','M','F','M']
      }
    )

    # age to age category conversion
    yes_no = [
        {'value': 'Yes', 'category': 1},
        {'value': 'No', 'category': 0},
        {'value': 'Yea', 'category': 1},
        {'value': 'Nay', 'category': 0}
    ]

    true_false = [
        {'value': True, 'category': 1},
        {'value': False, 'category': 0}
    ]

    _converts = {
        'conversions': [
            {'column': 'C', 'range': (pd.to_datetime('2016-01-01'), pd.to_datetime('2017-01-01'))},

            {'column': 'A', 'to': 'int'},
            {'column': 'B', 'to': 'int', 'categories':yes_no},
            {'column': 'C', 'to': 'datetime'},
            {'column': 'D', 'to': 'int', 'categories':true_false}

        ]
    }

    #df,convert_summary = get_type_changes(_converts, df_data)

    #print(df.info())
    #print(convert_summary)

    print('################ Outliers')
    _outliers = {
      'outliers': [

        {'column':'C','range': (pd.to_datetime('2016-01-01'), pd.to_datetime('2017-01-01'))},
        #{'column': 'A', 'range': (1, 69)},
        #{'column':'F','categories':['M']}
      ]
    }
    df_data['C'] = pd.to_datetime(df_data['C'])
    df_data.info()

    remove_obvious_outliers(_outliers, df_data)

    #df, outlier_summary = get_with_outliers_removed(_outliers, df)
    #print('outlier_summary: ', outlier_summary)

if __name__ == "__main__":
    # execute only if run as a script
    main()