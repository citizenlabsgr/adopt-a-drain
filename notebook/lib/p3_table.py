import collections
from pprint import pprint

def format_series(series):
    '''
      series is a pandas.core.series.Series
      return a markdown table string
    :param in_data:
    :return: markdown
    '''

    header = ['| id | label | value |\n']
    line = ['| :--- |' ,'| :--- |' ,'| :--- |\n']
    rows = []
    for i, item in series.iteritems():
        # i is a tuple (0, 'label')
        # item is a value
        rows.append('| {} | {} | {} |\n'.format(i[0] ,i[1], item))
    tbl = ''.join(header) +''.join(line) + ''.join(rows)

    return tbl

def isKeyValue(summary):
    for v in summary:
        if isinstance(summary[v], dict):
            return False
    return True

def format_summary(summary, title=''):
    mark_down = ''
    row = []
    expectedKeys = ['counts','sums','total']

    if len(title) == 0:
        title = 'Needs a Title'

    parentKeys = summary.keys()
    mark_down = '### {}\n'.format(title)

    #print('parentKeys: ',parentKeys)
    for pk in parentKeys:
        #print('    pk: ',pk)
        if pk in expectedKeys:
            mark_down += format_row_h(summary[pk], title='') + '\n'

    return mark_down

def format_row_h(summary, title=''):
    mark_down = ''
    row = []

    if len(title) == 0:
        title = 'Needs a Title'

    parentKeys = summary.keys()

    m_down = ''

    if isKeyValue(summary): # has key and only values
        #print(parentKey, 'row me')
        row += ' row me |'
        m_down = row
    else:
        for pk in parentKeys:
            #print('        pkB: ', pk)
            m_down = ''

            if isinstance(summary[pk], dict):
                titles = [' feature |'] + [' {} |'.format(y) for y in summary[pk]]
                line = [' :--- |'] + [' :--- |' for y in summary[pk]]
                row = [' **{}** |'.format(pk)] + [' {} |'.format(summary[pk][y]) for y in summary[pk]]
                # m_down = '### {} \n'.format(title)
                m_down += ''.join(titles).strip() + '\n'
                m_down += ''.join(line).strip() + '\n'
                m_down += ''.join(row).strip() + '\n'

                mark_down += m_down + '\n'

    return mark_down

def deprecated_format_row_h(summary, title=''):
    mark_down = ''
    row = []

    if len(title) == 0:
        title = 'Needs a Title'


    parentKeys = summary.keys()

    for pk in parentKeys:
        m_down = ''
        print('pk: ', pk)
        if isKeyValue(summary): # has key and only values
            #print(parentKey, 'row me')
            row += ' row me |'
            m_down = row
        else:

            for x in summary[pk]:
                print('pk: ',pk)
                print('x: ', x)
                titles = [' feature |']+[' {} |'.format(y) for y in summary[pk]]
                line = [' :--- |'] + [' :--- |' for y in summary[pk]]
                row = [' {} |'.format(pk)] + [' {} |'.format(summary[pk][y]) for y in summary[pk]]

            m_down = '### {} \n'.format(title)
            m_down += ''.join(titles).strip() + '\n'
            m_down += ''.join(line).strip() + '\n'
            m_down += ''.join(row).strip() + '\n'

        mark_down = m_down + '\n'
        #rows.append(row)
    #mark_down = ''.join(titles) + '\n'
    #mark_down += ''.join(line) + '\n'
    #mark_down += ''.join(rows)
    return mark_down


def deprecated_format_pairs(summary):
    mark_down = ''
    titles = []
    line = []
    if isinstance(summary, collections.Iterable):
        titles = [' {} |'.format(x) for x in summary]
        line = [' :--- |' for x in summary]
        rows = []
        for x in summary:
            #rows.append(summary[x])
            if isinstance(summary[x],dict):
                astr =  str(summary[x])
                row = ' {} |'.format( astr)
            elif isinstance(summary[x],list):
                astr = str(summary[x])
                row = ' {} |'.format('list')
            else:
                row = ' {} |'.format(summary[x])

            rows.append(row)
        mark_down = ''.join(titles) + '\n'
        mark_down += ''.join(line) + '\n'
        mark_down += ''.join(rows)

    else:
        mark_down = "hi"


    return mark_down


def deprecate_format_summary_values(summary):
    mark_down = ''
    titles =  [ ' {} |'.format(x) for x in summary]
    #titles = ' item | values '
    line = [ ' :--- |' for x in summary]
    #line = ' :--- |' + ''.join(line)


    title = ''
    print(''.join(titles))
    print(''.join(line))
    rows =''
    for ttl in summary:

        if isinstance(summary[ttl], collections.Iterable):
            #row = ' {} |'.format(ttl)
            row = ''
            for y in summary[ttl]:
                row = ' {} |'.format(summary[ttl][y])
                rows += row + '\n'
        if isinstance(summary[ttl], collections.Iterable):
            print('x')

    #print(rows)
    return mark_down

def deprecated_format_summary(summary):
    return format_table_markdown(summary)

def format_table_markdown(in_data):
    '''
       in_data ={
            'column-name':{'row-name-1': value, 'row-name-2': value}
        }
        return a markdown table string
    :param in_data:
    :return:
    '''

    tbl = ''
    col_names = [x for x in in_data]
    #print('col_names: ' , col_names)
    row_names = [x for x in in_data[col_names[0]]]
    #print('row_names: ', row_names)
    header_ = '\n| | '
    for c in col_names:
        header_ +=  c + ' |'
    tbl = header_
    #print(header_)
    # line break
    seperator_line = '| '
    for i in range(0, len(col_names)):
        seperator_line += '-- | '
    tbl += '\n' + seperator_line

    #print(seperator_line)
    ln = ''
    # for i in range(0, len(row_names)):

    for r in row_names:

        #print('r: ', r)
        ln = '| **' + str(r) + '** | '

        for k in col_names:

            if k in in_data:
                if r in in_data[k]:
                    ln += str(in_data[k][r]) + ' | '


        tbl += '\n' + ln



        # print(in_data[col_names[i]])
    return tbl

def deprecated_format_table_markdown(in_data):
    '''
       in_data ={
            'column-name':{'row-name-1': value, 'row-name-2': value}
        }
        return a markdown table string
    :param in_data:
    :return:
    '''

    tbl = ''
    col_names = [x for x in in_data]
    #print('col_names: ' , col_names)
    row_names = [x for x in in_data[col_names[0]]]
    #print('row_names: ', row_names)


    header_ = '\n| | '
    for c in col_names:
        header_ +=  c + ' |'
    tbl = header_
    #print(header_)
    # line break
    seperator_line = '| '
    for i in range(0, len(col_names)):
        seperator_line += '-- | '
    tbl += '\n' + seperator_line

    #print(seperator_line)
    ln = ''
    # for i in range(0, len(row_names)):

    for r in row_names:
        # print(row_names[i],' |')
        #print('r: ', r)
        ln = '| **' + str(r) + '** | '

        for k in col_names:
            print('k: ',k, ' r: ', r)
            ln += str(in_data[k][r]) + ' | '

        tbl += '\n' + ln
        #print(ln)

        # print(in_data[col_names[i]])
    return tbl

def main():
    '''
    in_data = {'PatientId': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': True, 'name': 'patient_id'},
     'AppointmentID': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': True, 'name': 'appointment_id'},
     'Gender': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'gender'},
     'ScheduledDay': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': True, 'name': 'scheduled_day'},
     'AppointmentDay': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': True, 'name': 'appointment_day'},
     'Age': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'age'},
     'Neighbourhood': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'neighbourhood'},
     'Scholarship': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'scholarship'},
     'Hipertension': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'hipertension'},
     'Diabetes': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'diabetes'},
     'Alcoholism': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'alcoholism'},
     'Handcap': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'handcap'},
     'SMS_received': {'blanks': False, 'dashes': False, 'case': True, 'camelcase': False, 'name': 'sms_received'},
     'No-show': {'blanks': False, 'dashes': False, 'spaces': True, 'case': True, 'camelcase': False, 'name': 'no_show'}}
    cols = [x for x in in_data]
    print(len(cols),cols)


    table_config = {
        'columns': cols,
     }

    tbl = format_table_markdown(in_data)
    print(tbl)
    sum = {'appointments': {2: 4911, 1: 7110, 6: 365, 5: 694, 7: 223, 4: 1330, 3: 2530, 14: 20, 9: 77, 8: 144,
                         13: 28, 10: 67, 12: 28, 11: 50, 29: 1, 54: 1, 15: 11, 16: 9, 17: 6, 19: 4, 35: 1,
                         21: 3, 20: 7, 23: 2, 55: 1, 40: 1, 30: 2, 88: 1, 46: 2, 34: 1, 62: 3, 57: 1, 84: 1,
                         38: 2, 37: 1, 18: 6, 22: 1, 42: 2, 33: 1}}
    tbl = format_summary(sum)
    '''

    #print(tbl)
    sum5 = {'patient_id': {'source': 'patient_id', 'name-change': False, 'pass-through': True, 'high-value': False, 'categorize': False, 'count': False, 'count-category': False},
            'appointments': {'source': 'no_show', 'name-change': 'appointments', 'pass-through': False, 'high-value': False, 'categorize': False, 'count': True, 'count-category': False},
            'no_shows': {'source': 'no_show', 'name-change': 'no_shows', 'pass-through': False, 'high-value': False, 'categorize': False, 'count': False, 'count-category': True},
            'scholarship': {'source': 'scholarship', 'name-change': 'scholarship', 'pass-through': False, 'high-value': True, 'categorize': False, 'count': False, 'count-category': False},
            'hipertension': {'source': 'hipertension', 'name-change': 'hipertension', 'pass-through': False, 'high-value': True, 'categorize': False, 'count': False, 'count-category': False},
            'diabetes': {'source': 'diabetes', 'name-change': 'diabetes', 'pass-through': False, 'high-value': True, 'categorize': False, 'count': False, 'count-category': False},
            'alcoholism': {'source': 'alcoholism', 'name-change': 'alcoholism', 'pass-through': False, 'high-value': True, 'categorize': False, 'count': False, 'count-category': False},
            'handcap': {'source': 'handcap', 'name-change': 'handcap', 'pass-through': False, 'high-value': True, 'categorize': False, 'count': False, 'count-category': False},
            'gender': {'source': 'gender', 'name-change': 'gender', 'pass-through': True, 'high-value': False, 'categorize': False, 'count': False, 'count-category': False},
            'age': {'source': 'age','name-change': False},
            'age_group': {'source': 'age'},
            'skipper': {'source': 'no_show'}}
    sum4 = mock_summary = {
        'appointments': 110464,
        'counts': {'attendance': {0: 22300, 1: 88164},
            'no_show': {0: 88164, 1: 22300},
            'scheduled_day_of_week': {0: 23068,
                                      1: 26123,
                                      2: 24262,
                                      3: 18072,
                                      4: 18915,
                                      5: 24},
            'scheduled_hour': {6: 1578,
                               7: 19212,
                               8: 15341,
                               9: 12823,
                               10: 11039,
                               11: 8462,
                               12: 5422,
                               13: 9024,
                               14: 9102,
                               15: 8079,
                               16: 5542,
                               17: 2909,
                               18: 1340,
                               19: 488,
                               20: 100,
                               21: 3}},
    'sums': {},
    'total': {'count': 110464}}



    sum2 =  {
        'no_show': {0: 88164, 1: 22300},
        'scheduled_day_of_week': {0: 23068,
                                      1: 26123,
                                      2: 24262,
                                      3: 18072,
                                      4: 18915,
                                      5: 24}}

    sum1 = {'no_show': {0: 88164, 1: 22300}}

    sum0 = {0: 88164, 1: 22300}

    sum = sum5
    pprint(sum)
    print(format_table_markdown(sum))
    #print(format_row_h(sum,''))
    #print(format_summary(sum,'Appointment Counts'))
    #format_summary_values(sum)
    #print(format_pairs(sum))


if __name__ == "__main__":
    # execute only if run as a script
    main()