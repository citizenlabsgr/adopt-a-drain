import pandas as pd
from pprint import pprint
import time
def load_neighbourhoods(file_name= 'neighbourhoods.csv'):
    #start_time = time.time()
    df_source = pd.read_csv(file_name)

    neighbourhoods = {}
    for idx, item in df_source.iterrows():
        #print('idx: ', idx, ' item: ',item[1])
        neighbourhoods[item[0]]={'name':item[0],
                                 'state':item[1].strip(),
                                 'lat':item[2],
                                 'lon':item[3]}
    #print('load_neighbourhoods: {}'.format(time.time()-start_time))
    return neighbourhoods

def attach_neighbourhood_lat_lon(df_source,dict_neighbourhoods, process_logger = None):
    '''
    load neighbourhood.csv and attach lat and lon to source

    '''
    #df_source.info()
    df_source['lon'] = df_source['neighbourhood'].apply(
        lambda x : dict_neighbourhoods[x]['lon'] )
    df_source['lat'] = df_source['neighbourhood'].apply(
        lambda x: dict_neighbourhoods[x]['lat'])

    #print('{}'.format(time.time() - start_time))

    return df_source

def deprecated_attach_neighbourhood_lat_lon(df_source,process_logger = None):
    '''
    load neighbourhood.csv and attach lat and lon to source

    '''
    #if process_logger != None:
    #    process_logger.collect('* Attach neighbourhood lat and lon ')
    neighbourhoods = load_neighbourhoods('../neighbourhoods.csv')

    lim = 10
    neighs = []
    lats = []
    lons = []
    start_time = time.time()
    for idx,item in df_source.iterrows():
        #if idx < lim:
            #print(item[6])
            #neighs.append(item[6])
        val = neighbourhoods[item[6]]
        lats.append(val['lat'])
        lons.append(val['lon'])

    print('{}'.format(time.time()-start_time))
    df_source['lat'] = lats
    df_source['lon'] = lons


    return df_source

def test_load_neighbourhoods():
    print('################## test_load_neighbourhoods')
    neighbourhoods = {}
    neighbourhoods = load_neighbourhoods('../neighbourhoods.csv')
    print('load_neighbourhoods: ', neighbourhoods)
    pprint(neighbourhoods)

def test_attach_lat_lon():
    print('################## test_attach_lat_lon')
    df_source = pd.read_csv('../03.01.01.appointments.csv')


    #neighbourhoods = {}
    df_neighbourhoods = load_neighbourhoods('../neighbourhoods.csv')

    df_source = attach_neighbourhood_lat_lon(df_source,df_neighbourhoods)
    df_source.info()

    # df_source.head()

def main():
    test_load_neighbourhoods()
    test_attach_lat_lon()


if __name__ == "__main__":
    # execute only if run as a script
    main()

