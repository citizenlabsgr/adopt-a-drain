# Cleaning functions
import pandas as pd
import numpy as np
import time
'''
def condense_group(group_name,fields,out_file_name, df_source):
    # fields is [{'name':'<column-name>','function':'<count-sum-mean>','new_name':'<column-name>'},...]
    print('######### condense_group')

    # assemble fields defaults
    # if no 'function' add 'function':None
    # if no 'new_name' add 'new_name': fields['name']
    for fld in fields:
        if not 'function' in fld:
            fld['function']=None
        if not 'new_name' in fld:
            fld['new_name'] = fld['name']
    #print('fields: ', fields)
    for fld in fields:
        #print('fld: ', fld)
        if fld['function']==None:
        #   print('function: None')
            #gb = df_source.groupby(group_name)[fld['name']].count()
            #print('gb: ', gb)
        elif fld['function']=='sum':
        #    print('function: sum')




        #
'''
def condense(out_file_name, df_source,columns=None):
    '''
        keeps wanted columns while exporting to csv
        outfile_name is path and file name of output file i.e "/Users/james/clean/table-name.csv"
        df_source is a dataframe 
        columns is a list of columns to keep i.e., ['appointment_id', 'patient_id', 'neighbourhood',...]
    '''
    #print('out_names: ', out_names)
    #print('out_file_name: ', out_file_name)
    start_time = time.time()
    if columns == None:
        columns == df_source.columns
    # write header
    df_source.to_csv(
        path_or_buf=out_file_name,
        columns=columns,
        header=True,
        index=False

    );
    print('* condense: {} {} sec'.format(out_file_name,time.time() - start_time))  # time_taken is in seconds

   
    
def clean_source_example(df_source):
    start_time = time.time()
    df_source['appointment_id'] = df_source['appointment_id'].astype(int)
    df_source['patient_id'] = df_source['patient_id'].astype(int)
    df_source['scheduled_day'] = pd.to_datetime(df_source['scheduled_day'])
    df_source['appointment_day'] = pd.to_datetime(df_source['appointment_day'])

    # categorize and type change
    gender_cats = ['M', 'F']
    df_source['gender'] = df_source['gender'].apply(lambda x: gender_cats.index(x))
    df_source['gender'] = df_source['gender'].astype(int)

    skip_cats = ['No','Yes']      # new col for neighbourhoods
    df_source['skipper'] = df_source['no_show'].apply(lambda x: skip_cats.index(x))
    df_source['skipper'] = df_source['skipper'].astype(int)

    show_cats = ['Yes', 'No']      # new col for neighbourhoods
    df_source['show'] = df_source['no_show'].apply(lambda x: show_cats.index(x))
    df_source['show'] = df_source['show'].astype(int)

    no_shows_cats = ['No', 'Yes']
    df_source['no_shows'] = df_source['no_show'].apply(lambda x: no_shows_cats.index(x))
    df_source['no_shows'] = df_source['no_shows'].astype(int)

    no_show_cats = ['No', 'Yes']
    df_source['no_show'] = df_source['no_show'].apply(lambda x: no_show_cats.index(x))
    df_source['no_show'] = df_source['no_show'].astype(int)

    attendance_cats = [1, 0] # must process after no_show converted to 0,1
    df_source['attendance'] = df_source['no_show'].apply(lambda x: attendance_cats.index(x) )
    df_source['appointments'] = [1 for x in range(0, len(df_source))]
    df_source['scheduled_day_of_week'] = df_source['scheduled_day'].apply(lambda x: x.dayofweek)
    df_source['scheduled_hour'] = df_source['scheduled_day'].apply(lambda x: x.hour)
    df_source['scheduled_time'] = df_source['scheduled_day'].apply(lambda x: float(x.hour) + (float(x.minute) / 60.0) + (float(x.second) / 3600.0))

    # year month day
    df_source['day'] = df_source['scheduled_day'].apply(lambda x: int(str(x.year) + str(x.month).zfill(2) + str(x.day).zfill(2) ))
    df_source['month'] = df_source['scheduled_day'].apply(lambda x: int(str(x.year) + str(x.month).zfill(2)  ))
    df_source['week'] = df_source['scheduled_day'].apply(lambda x: int(str(x.year) + str(x.isocalendar()[1]).zfill(2) ))
    print('* clean_source: {} sec'.format(time.time() - start_time))  # time_taken is in seconds

    return df_source

def clean_column_names(df_source):
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
    start_time = time.time()
    actual_col_list = df_source.columns
    clean_column_names = {}
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


        clean_column_names[cn]=ncn

    df_source = df_source.rename(columns=clean_column_names)
    print('* clean_column_names: {} sec'.format(time.time() - start_time))  # time_taken is in seconds

    return df_source

def remove_obvious_outliers(_outliers,df):
    '''
    remove individual observations
    remove range of observation
    
    _outliers is 
    {
      'outliers': [
        {'column':'scheduled_day',
         'range':(pd.to_datetime('2016-01-01'), pd.to_datetime('2017-01-01')),
         'reason':'Remove 2015. Appointment in 2015 has many gaps in the timeline numbers'},
        {'column': 'scheduled_day_of_week',
         'range': (0,4) ,
         'reason':'Remove Saturday and Sunday visits. These are so few that they could easily .'},
        {'column':'lon',
         'range':(-50.0,-35.0),
         'reason':'Remove neighbourhoods that have bad longitudes (too far east).'},
        {'column':'scheduled_hour',
         'range':(7,20),
         'reason':'Remove small number of observations at 6:00 and 21:00 hours.'}
      ]
    }

    '''
    #summary = {}
    start_time = time.time()
    outliers = _outliers['outliers']
    for outlier in outliers:
        col_name = outlier['column']
        #summary[col_name] = {'range-drops':0,'category-drops':0}


        if 'range' in outlier:
            # print('outlier: ', outlier)
            
            low = outlier['range'][0]
            high = outlier['range'][1]
            sz = len(df)
           
            #print('colname: ', col_name)
            tmp = None
            tmp1 = ''
          
            if isinstance(low, np.datetime64):
                df = df[(df[col_name].to_datetime() >= low) & (df[col_name].to_datetime() <= high)]
            else:   
                
                df = df[(df[col_name] >= low) & (df[col_name] <= high)]
                
            outlier["count"] = sz - len(df)
            
            #summary[col_name]['range-drops'] = sz - len(df)

        elif 'categories' in outlier:
            #print('categories')
            #col_name = outlier['column']

            _list = outlier['categories']
            sz = len(df)
            df = df[df[col_name].isin(_list)]
            outlier["count"] = sz - len(df)
        if "reason" in outlier:
                outlier["reason"] = outlier["reason"].format(  str(outlier["count"]) )
            
            #summary[col_name]['category-drops'] = sz - len(df)
    #end_time = time.time()
    #timediff= end_time - start_time
    print('* remove_obvious_outliers: {} sec'.format(time.time() - start_time))   # time_taken is in seconds
    # print(_outliers)
    return df #, summary



def main():
    print('add a test')


if __name__ == "__main__":
    # execute only if run as a script
    main()