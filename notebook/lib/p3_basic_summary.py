import pandas as pd
import csv # read and write csv files
from pprint import pprint
#import p3_mock_data as mock

import collections



def get_domain_values(field_name, _summary, _sort=False):
    #return [int(x.replace(prefix,'')) for x in _summary['counts'] if x.startswith(prefix)]
    return [x for x in _summary['counts'][field_name]]

def get_range_values(field_name, _summary):
    #return [_summary['counts'][x] for x in _summary['counts'] if x.startswith(prefix) ]
    return [_summary['counts'][field_name][x] for x in _summary['counts'][field_name]]

def format_layer(field_name, layer_label ,df_summary):
    _domain = get_domain_values(field_name, df_summary)
    _range = get_range_values(field_name,df_summary)
    return {'label': layer_label, 'domain': _domain, 'range': _range}


def mock_appt_summary_config():

    appt_summary_config = {'context': 'appointments',  # what does row represent
                           'fields': [
                               {'field': 'attendance', 'sort': 'domain', 'function': 'kind-count'},
                               # count for all gender types
                               {'field': 'scheduled_day_of_week', 'function': 'kind-count'},
                               # count for all scholarship types
                               {'field': 'scheduled_hour', 'sort': 'domain', 'function': 'kind-count'},
                               # count for all age types

                               # {'field': 'scheduled_hour','sort':'domain', 'function': 'kind-count'},
                               # {'field': 'scheduled_time','sort':'domain', 'function': 'kind-count'},
                               # {'field': 'age', 'sort':'domain','function': 'kind-count'},
                               {'field': 'no_show', 'sort': 'domain', 'function': 'kind-count'},
                               # {'field': 'no_show', 'sort':'domain','function': 'sum'},

                           ]}

    return appt_summary_config

def get_basic_summary(df_source,summary_config):
    '''
    takes clean source data and converts it into a summary structure:
                {'context': 'appointments',
                'counts': {'attendance': {}, 'scheduled_day_of_week': {}, 'scheduled_hour': {}, 'no_show': {}},
                'sums':{},
                'means':{}}
    config is {'context': 'appointments',  # what does row represent
                           'fields': [
                               {'field': 'attendance', 'sort': 'domain', 'function': 'kind-count'},
                               ...]
               }
    :param df_source: clean data from a csv
    :param summary_config: tells how each field should be summarized
    :return: summary of data
    '''
    fields = summary_config['fields']
    count_fields = [fld for fld in fields if fld['function'] == 'kind-count']
    sum_fields = [fld for fld in fields if fld['function'] == 'sum']

    domain_sorts = [fld['field'] for fld in fields if 'sort' in fld and fld['sort']=='domain']
    range_sorts = [fld['field'] for fld in fields if 'sort' in fld and fld['sort']=='range']

    # create activity place holders
    summary = {
        'context': summary_config['context'],

        'counts': {}, # add counter for all rows
        'sums': {},

        'means': {}

    }
    # initialize Features

    for fld in count_fields: #fields: # initialize the domains
        if 'domain' in fld:
            summary['counts'][fld['field']] = dict(fld['domain'])
        else:
            summary['counts'][fld['field']] = {}

    for fld in sum_fields: # initialize the domains
        if 'domain' in fld:
            summary['sums'][fld['field']] = dict(fld['domain'])
        else:
            summary['sums'][fld['field']] = {}

    # initialize Feature attributes
    # counts
    for c in count_fields:
        col_name = c['field']
        df = df_source.groupby([col_name])[col_name].count()
        for cat, catValue in df.items():
            summary['counts'][c['field']][cat]=catValue

    # Sums

    # Means
    return summary


def test_start_summary_basic():
    print('############ test_start_summary_basic')
    df_source = pd.read_csv('03.appointments.csv')
    config = mock_appt_summary_config()
    actual = get_basic_summary(df_source, config)
    expected = {'context': 'appointments',
                'counts': {'attendance': {}, 'scheduled_day_of_week': {}, 'scheduled_hour': {}, 'no_show': {}},
                'sums':{},
                'means':{}}

    print(actual)
    print(expected)
    #assert actual == expected




def deprecated_get_basic_summary(df, _exports, _counts,limit=0, keys=[]):
    '''
    read csv of data, tally some counts
    configuration goes as
    keys are list of category names in order of the numeric seququec
    _counts is  {
        'context': '<context-name>', # what does a row represent
        'fields':[
            {'field':'<col-name>', sort:'domain', function':'kind-count'}, # count for <col-name> for all  types/kind/categories in values of <col-name>
            {'field':'<col-name>', 'function':'sum'}         # sum just the value in the <col-name>
            {'field':'<col-name>', kinds[{'key':<col-name>, 'value':'category-value'}],function':'sum'}    # sum just the value in the <col-name>

        ]
    }
    
    _summary is {
        'counts':{},
        'sums':{}
        
     }
    '''

    fields = _counts['fields']
    #count_fields = [fld['field'] for fld in fields if fld['function'] == 'kind-count']
    count_fields = [fld for fld in fields if fld['function'] == 'kind-count']

    #sum_fields = [fld['field'] for fld in fields if fld['function'] == 'sum']
    sum_fields = [fld for fld in fields if fld['function'] == 'sum']

    #print('fields: ', fields)
    #print('count_fields: ', count_fields)
    #print('sum_fields: ',sum_fields)
    domain_sorts = [fld['field'] for fld in fields if 'sort' in fld and fld['sort']=='domain']
    range_sorts = [fld['field'] for fld in fields if 'sort' in fld and fld['sort']=='range']
    #print('count_range: ', count_range)
    # intialize
    summary = {
        _counts['context']: 0,

        'counts': {}, # add counter for all rows
        'sums': {},
        'total': {'count': 0},
        #'means': {}
    }

    for fld in count_fields: #fields: # initialize the domains
        #print('fld A: ', fld)
        if 'domain' in fld:
            summary['counts'][fld['field']] = dict(fld['domain'])
            #summary['sums'][fld['field']] = dict(fld['domain'])
            #summary['means'][fld['field']] = dict(fld['domain'])
        else:
            summary['counts'][fld['field']] = {}
            #summary['sums'][fld['field']] = {}
            #summary['means'][fld['field']] = {}
    #print('sum_fields: ', sum_fields)
    for fld in sum_fields: # initialize the domains
        #print('fld B: ',fld)
        if 'domain' in fld:
            summary['sums'][fld['field']] = dict(fld['domain'])
        else:
            #print("fld['field']: ",fld['field'])
            summary['sums'][fld['field']] = {}

    '''
    for col_key in count_fields:
        summary['counts'][col_key] = {} # initialize for domain and range to come later
        #if 'domain' in _counts['fields'][col_key]:
        #    print(_counts['fields'][col_key])
        #print('col_key: ',col_key)
        #print(summary)
    '''
    i = 0
    # counts and sums
    for index, row in df.iterrows():

        #summary['counts'][_counts['context']] += 1 # count all records
        summary[_counts['context']] += 1  # count all records
        summary['total']['count'] += 1  # count all records

        for c in count_fields:
            grp = c['field']
            dmn = row[grp]
            if(type(dmn).__name__ == 'float64'):
                dmn = int(dmn)
            if not dmn in summary['counts'][grp] :
                #print('dmn: ', dmn)
                summary['counts'][grp][dmn] = 1 # initialize to 1
            else:
                summary['counts'][grp][dmn] += 1 # increment by 1

        for c in sum_fields:

            grp = c['field']

            dmn = row[grp]
            rng = row[grp]
            if not dmn in summary['sums'][grp]:
                summary['sums'][grp][dmn] = rng  # initialize to 1
            else:
                summary['sums'][grp][dmn] += rng  # increment by 1

        if limit != 0:
            i += 1
            if i >= limit:
                break
    #print(summary)
    # sort the domain ... x axis
    #if fn in domain_sorts:
    for fn in domain_sorts:
        #print('sorted A: ', sorted(summary['counts'][fn]) )

        #summary['counts'][fn] = sorted(summary['counts'][fn])
        newcounts = {}
        for k in sorted(summary['counts'][fn]):
            newcounts[k]=summary['counts'][fn][k]
        #print('sorted B: ', newcounts)

        summary['counts'][fn] = newcounts

    # sort by range

    '''
    newsums = {}
    for k in sorted(summary['sums']):
        newsums[k]=summary['sums'][k]
    summary['counts']= newcounts
    summary['sums']= newsums
    '''
    return summary


def main():
    #test_add_to_summary_basic()
    test_start_summary_basic()

if __name__ == "__main__":
    # execute only if run as a script
    main()

    