import pandas as pd

def get_category_list(feature_list):
    '''
    returns all unique values from feature_list
    '''
    category_list = []
    for f in feature_list:
        if not f in category_list:
            category_list.append(f)
    return category_list

def get_year_range(date_list):
    '''
    date_list conains datetimes
    returns tuple of the oldest date first and most recent last

    '''
    low_yr = 9999
    high_yr = -1
    for date_ in date_list:
        #year = pd.to_datetime(date_)
        #print(date_.year)
        year = date_.year
        if year > high_yr:
            high_yr = year
        if year < low_yr:
            low_yr = year
    return (low_yr, high_yr)


def get_datetime_range(date_list):
    '''
        return oldest and most recent datetime
    '''
    low =  pd.to_datetime('2050-01-01') 
    high = pd.to_datetime('1900-01-01')
    for date_ in date_list:
        if date_ > high:
            high = date_
        if date_ < low:
            low = date_
    return (low,high)


def get_date_range(df_source):
    '''
        return oldest and most recent date
    '''

    high = df_source.max()['scheduled_day']
    low = df_source.min()['scheduled_day']
    return (low, high)

def deprecated_get_date_range(date_list):
    '''
        return oldest and most recent date
    '''
    low =  pd.to_datetime('2050-01-01')
    high = pd.to_datetime('1900-01-01')
    #print('high: ', type(high), high)
    for date_ in date_list:
        #tmp_date = pd.to_datetime(date_)
        #print('date_: ' , type(tmp_date), tmp_date)
        if date_ > high:
            high = date_
        if date_ < low:
            low = date_

    return (low, high)

def get_date_range_vebose(date_period):
    '''
    date_period is a tuple of Timestamps
    convert to a hyhenated string of two dates
    :param date_period:
    :return:
    '''
    one = str(date_period[0])
    two = str(date_period[1])
    rc = '{} to {}'.format(one.split(' ')[0], two.split(' ')[0])
    return rc

def main():


    date_list = []

    date_list.append(pd.to_datetime('2010-03-01'))
    date_list.append(pd.to_datetime('2010-03-01'))
    date_list.append(pd.to_datetime('2011-03-01'))
    date_list.append(pd.to_datetime('2011-03-01'))
    date_list.append(pd.to_datetime('2012-03-01'))
    date_list.append(pd.to_datetime('2012-03-01'))
    date_list.append(pd.to_datetime('2013-03-01'))
    date_list.append(pd.to_datetime('2013-03-01'))
    date_list.append(pd.to_datetime('2014-03-01'))
    date_list.append(pd.to_datetime('2014-03-01'))
    date_list.append(pd.to_datetime('2015-03-01'))
    date_list.append(pd.to_datetime('2015-03-01'))
    date_list.append(pd.to_datetime('2016-03-01'))
    date_list.append(pd.to_datetime('2016-03-01'))

    actual = get_year_range(date_list)

    expected = (2010,2016)
    assert actual == expected


    actual = get_date_range(date_list)

    expected = (pd.to_datetime('2010-03-01'),pd.to_datetime('2016-03-01'))

    assert actual == expected
    print('actual: ', actual)


    expected = '2010-03-01 to 2016-03-01'
    actual = get_date_range_vebose(actual)
    assert actual == expected
    print('actual: ', actual)


if __name__ == "__main__":
    # execute only if run as a script
    main()