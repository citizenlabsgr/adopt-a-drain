import pandas as pd
import csv # read and write csv files

from lib.p3_Transforms import Transforms, get_raw_transforms_json


class Condenser(dict): # built on tranform

    #def __init__(self):
        #self.transform = _transform_dict
        #self.categories = _categories_dict
        #self.results = {}

    def __get_category(self, value, cat_values, value2=None):
        '''

        :param value:
        :param categories:
        :param value2: is used by 'cross_sum'
        :return:
        '''
        rc = -1
        if value in cat_values:
            rc = cat_values.index(value)

        '''
        
        for c in categories:
            if len(c['range']) == 1:  # for singleton range ie ('m')
                if value == c['range'][0]:
                    return c['category']
            elif c['range'][0] == c['range'][1]:
                if value == c['range'][0]:
                    return c['category']
            else:
                if value >= c['range'][0] and value < c['range'][1]:
                    return c['category']
        '''


        return rc

    def __deprecated_get_category(self, value, categories):
        #print('val: ',value)
        #print('categories: ',categories)
        for c in categories:
            if len(c['range']) == 1:  # for singleton range ie ('m')
                if value == c['range'][0]:
                    return c['category']
            elif c['range'][0] == c['range'][1]:
                if value == c['range'][0]:
                    return c['category']
            else:
                if value >= c['range'][0] and value < c['range'][1]:
                    return c['category']
        return 0
    def __condense_group(self, df_data, limit=0):
        # def condense_data(in_file, out_file, city):
        '''
        This function takes full data from the specified input file
        and writes the condensed data to a specified output file. The city
        argument determines how the input file will be parsed.

        HINT: See the cell below to see how the arguments are structured!


        df_data is DataFrame of originating data
        exports is
            {
                'condensed':'<output-condenced-file-name>',
                'fields':[
                    {field_in':'<col-name>','field_out':'<col-name>', 'function':None}

                ]
            }
        '''
        #print('condense_group: 1')
        self.results = {}
        #summary = {}
        data_dict = {}
        data_col_names =df_data.columns

        group_by = None
        if 'group_by' in self:
            group_by = self['group_by']

        df_colnames = []
        for f in self['fields']:
            if not f['field_in'] in df_colnames:
                if not f['virtual']:
                    df_colnames.append(f['field_in'])

        if group_by == None:
            raise NameError('group_by is not defined in transform')

        if df_colnames[0] != group_by:
            raise NameError('group_by must be first column in transform')

        out_fields = [item['field_out']for item in self['fields']]

        cat_values =[]
        for f in self['fields']:
            field_in = f['field_in']
            self.results[f['field_out']] = {'source': field_in} # reporting
            if not field_in in data_col_names and not field_in in out_fields:
                raise NameError('{} is not defined in dataframe.'.format(field_in))

            if not 'categories' in f:
                f['categories'] = None # add empty categories


            if f['categories'] != None:

                if 'value' in f['categories']:
                    cat_values.append([x['value'] for x in f['categories']])

            else:
                cat_values.append([])

            if not 'function' in f:
                f['function'] = None  # this is a pass through
            if not 'field_out' in f:
                f['field_out'] = None  # this is a pass through to same name

        in_colnames = [f['field_in'] for f in self['fields'] if not f['virtual']]
        out_colnames = [f['field_out'] for f in self['fields']  if not f['virtual']]
        cat_list = [f['categories'] for f in self['fields']  if not f['virtual']]

        func_list = [f['function'] for f in self['fields']  if not f['virtual']]
        out_file = self['out_file_name']

        lim = limit
        i = 0

        for idx, row in df_data[df_colnames].iterrows():

            ci = 0  # index to column name, zero is group by index
            gb_keyvalue = None

            for col_name in in_colnames: # interate over row columns

                self.results[out_colnames[ci]]['name-change'] = False
                self.results[out_colnames[ci]]['pass-through'] = False
                self.results[out_colnames[ci]]['high-value'] = False
                self.results[out_colnames[ci]]['categorize'] = False

                self.results[out_colnames[ci]]['count'] = False
                self.results[out_colnames[ci]]['count-category'] = False
                self.results[out_colnames[ci]]['cross_sum'] = False

                if ci == 0:  # key value
                    gb_keyvalue = row.loc[col_name]


                if in_colnames[ci] != out_colnames[ci]:
                    self.results[out_colnames[ci]]['name-change'] = out_colnames[ci]

                # add key
                if not gb_keyvalue in data_dict:  # dictionary key order is NOT maintained
                    # alway a
                    data_dict[gb_keyvalue] = {out_colnames[ci]: gb_keyvalue}  # alway pass through the initating value

                # detect name change
                if not out_colnames[ci] in data_dict[gb_keyvalue]:  # and column
                    data_dict[gb_keyvalue][out_colnames[ci]] = None
                    if func_list[ci] == 'count':
                        data_dict[gb_keyvalue][out_colnames[ci]] = 0
                    if func_list[ci] == 'count-category': # initalize counter to zero
                        #print('init count-category col_name: ', col_name)
                        data_dict[gb_keyvalue][out_colnames[ci]] = 0

                # process functions
                if func_list[ci] == None:  # pass through is default function when not defined in transfrom
                    self.results[out_colnames[ci]]['pass-through'] = True
                    data_dict[gb_keyvalue][out_colnames[ci]] = row.loc[col_name]#col
                elif func_list[ci] == 'high-value':  # stores the bigger of values
                    self.results[out_colnames[ci]]['high-value'] = True
                    if data_dict[gb_keyvalue][out_colnames[ci]] == None \
                            or data_dict[gb_keyvalue][out_colnames[ci]] < row.loc[col_name]: #col:
                        data_dict[gb_keyvalue][out_colnames[ci]] = row.loc[col_name] # col
                elif func_list[ci] == 'categorize':
                    self.results[out_colnames[ci]]['categorize'] = True

                    data_dict[gb_keyvalue][out_colnames[ci]] \
                        = self.__get_category(row.loc[col_name], cat_values[ci])

                elif func_list[ci] == 'count':
                    self.results[out_colnames[ci]]['count'] = True
                    data_dict[gb_keyvalue][out_colnames[ci]] += 1

                elif func_list[ci] == 'count-category':
                    self.results[out_colnames[ci]]['count-category'] = True

                    if row.loc[col_name] in cat_list[ci][0]['count']:
                        data_dict[gb_keyvalue][out_colnames[ci]] += 1

                else:
                    raise NameError('undefined function {}'.format(func_list[ci]))
                ci += 1

            if i != 0 and i == lim:
                break
            i += 1


            #### deal with virtual key calculations
        in_colnames_virtual = [f['field_in'] for f in self['fields'] if f['virtual']]
        in_field_2_virtual = [f['field_in_2'] for f in self['fields'] if f['virtual']]

        out_colnames_virtual = [f['field_out'] for f in self['fields'] if f['virtual']]
        func_list_virtual = [f['function'] for f in self['fields'] if f['virtual']]
        #print('func_list_virtual: ',func_list_virtual)
        i = 0
        for gb_keyvalue, row in data_dict.items():
            #if i <10:
            #    print('gb_keyvalue: ',gb_keyvalue, ' row: ', row)
            i_v = 0
            for col_name in in_colnames_virtual:  # interate over row columns
                #if i< 10:
                #    print('colname: ', col_name)
                #self.results[out_colnames[i]]['ratio'] = False
                # process functions
                #print('len(func_list_virtual[i_v]): ',len(func_list_virtual[i_v]))
                if func_list_virtual[i_v] == None:  # pass through is default function when not defined in transfrom
                    #self.results[out_colnames[ci]]['pass-through'] = True
                    data_dict[gb_keyvalue][out_colnames_virtual[i_v]] = row[col_name]  # col
                elif func_list_virtual[i_v] == 'ratio':  # stores the bigger of values
                    #self.results[out_colnames[ci]]['high-value'] = True
                    #print('row: ', row)
                    #print('in_colnames_virtual[i_v]: ',in_colnames_virtual[i_v])
                    numerator = data_dict[gb_keyvalue][in_colnames_virtual[i_v]]
                    denominator = data_dict[gb_keyvalue][in_field_2_virtual[i_v]]
                    #print('numerator: ', numerator, '  denominator: ', denominator)
                    data_dict[gb_keyvalue][out_colnames_virtual[i_v]] = numerator / denominator
                i_v += 1

            i += 1



        # update outcolnames for dictwriter
        for c in out_colnames_virtual:
            #print('c: ',c)
            if not c in out_colnames:
                out_colnames.append(c)

        #print('out_colnames x: ', out_colnames)

        with open(out_file, 'w') as f_out:
            csv_writer = csv.DictWriter(f_out, fieldnames=out_colnames)
            csv_writer = csv.DictWriter(f_out, fieldnames=out_colnames, quotechar='"', quoting=csv.QUOTE_NONNUMERIC,
                                        delimiter=',')
            csv_writer.writeheader()

            for row in data_dict:
                #print(data_dict[row])
                csv_writer.writerow(data_dict[row])

        #return summary


    def __condense_data(self, df_data):
        # def condense_data(in_file, out_file, city):
        '''
        This function takes full data from the specified input file
        and writes the condensed data to a specified output file. The city
        argument determines how the input file will be parsed.

        HINT: See the cell below to see how the arguments are structured!


        df_data is DataFrame of originating data
        exports is
            {
                'condensed':'<output-condenced-file-name>',
                'fields':[
                    {field_in':'<col-name>','field_out':'<col-name>', 'function':None}

                ]
            }
        '''



        #summary = {}
        self.results ={}
        #print(self)
        out_colnames = [f['field_out'] for f in self['fields']]
        #in_colnames = [f['field_in'] for f in self.transform['fields']]
        in_colnames = [f['field_in'] for f in self['fields']]

        in_colnames_2 = []
        cat_list = []
        cat_values = []
        for f in self['fields']:
            field_in = f['field_in']
            self.results[f['field_out']] = {'source': field_in}
            if f['categories'] != None:

                cat_list.append(f['categories'])
                cat_values.append([x['value'] for x in f['categories']])

            else:
                cat_list.append([])
                cat_values.append([])

            if not 'function' in f:
                f['function'] = None  # this is a pass through

            if not 'field_2' in f:
                in_colnames_2.append(None)
            else:
                in_colnames_2.append(f['field_2'])

        #print('cat_list: ', cat_list)
        #print('cat_values: ', cat_values)
        function_list = [f['function'] for f in self['fields']]
        out_file = self['out_file_name']#export['condensed']

        with open(out_file, 'w') as f_out:
            csv_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
            csv_writer = csv.DictWriter(f_out, fieldnames=out_colnames, quotechar = '"', quoting = csv.QUOTE_NONNUMERIC, delimiter = ',')
            csv_writer.writeheader()

            for row in df_data.as_matrix(in_colnames):
                data_point = {}
                for i in range(0,len(in_colnames)):
                    self.results[out_colnames[i]]['name-change'] = False
                    self.results[out_colnames[i]]['pass-through'] = False
                    self.results[out_colnames[i]]['extact-year'] = False
                    self.results[out_colnames[i]]['extact-month'] = False
                    self.results[out_colnames[i]]['extact-day'] = False
                    self.results[out_colnames[i]]['extact-hour'] = False
                    self.results[out_colnames[i]]['extact-minute'] = False
                    self.results[out_colnames[i]]['extact-second'] = False
                    self.results[out_colnames[i]]['extact-day-of-week'] = False
                    self.results[out_colnames[i]]['extact-time'] = False
                    self.results[out_colnames[i]]['categorize'] = False
                    self.results[out_colnames[i]]['cross_categorize'] = False
                    #if function_list[i] == None:
                        #data_point[out_colnames[i]] = row[i]
                    if in_colnames[i] != out_colnames[i]:
                        self.results[out_colnames[i]]['name-change'] = True

                    if function_list[i] == None:
                        data_point[out_colnames[i]] = row[i]

                        self.results[out_colnames[i]]['pass-through'] = True

                    elif function_list[i] == 'year':
                        #try:
                        data_point[out_colnames[i]] = row[i].year
                        self.results[out_colnames[i]]['extract-year'] = True
                        #except ValueError:
                        #    print('function_list[{}]'.format(i),function_list[i])
                        #    print('out_colnames[{}]'.format(i), out_colnames[i])
                        #    print('row[{}] {}'.format(i,row[i]))
                        #    print('type: ',type(row[i]))

                    elif function_list[i] == 'month':

                        data_point[out_colnames[i]] = row[i].month
                        self.results[out_colnames[i]]['extract-month'] = True
                    elif function_list[i] == 'day':
                        data_point[out_colnames[i]] = row[i].day
                        self.results[out_colnames[i]]['extract-day'] = True
                    elif function_list[i] == 'hour':
                        data_point[out_colnames[i]] = row[i].hour
                        self.results[out_colnames[i]]['extract-hour'] = True
                    elif function_list[i] == 'minute':
                        data_point[out_colnames[i]] = row[i].minute
                        self.results[out_colnames[i]]['extract-minute'] = True
                    elif function_list[i] == 'second':
                        data_point[out_colnames[i]] = row[i].second
                        self.results[out_colnames[i]]['extract-second'] = True
                    elif function_list[i] == 'time':
                        data_point[out_colnames[i]] = float(row[i].hour) + (float(row[i].minute) / 60.0) + (float(row[i].second)/3600.0)
                        self.results[out_colnames[i]]['extract-time'] = True
                    elif function_list[i] == 'day_of_week':
                        #df_data.info()
                        #print('row:', row)
                        #print('row[i]: ', row[i])

                        #print('type(row[i]): ',type(row[i]))
                        if type(row[i]).__name__ == 'str':
                            msg = 'value {} is object, should be Date'.format(row[i])
                            raise AttributeError(msg)
                        data_point[out_colnames[i]] = row[i].dayofweek


                        self.results[out_colnames[i]]['extract-day-of-week'] = True
                    elif function_list[i] == 'categorize':
                        #data_point[out_colnames[i]] = self.__get_category(row[i], cat_list[i])
                        data_point[out_colnames[i]] = self.__get_category(row[i], cat_values[i])
                        self.results[out_colnames[i]]['categorize'] = True
                    #elif function_list[i] == 'cross_categorize':
                        #where is the second value
                        #k = df_data.columns.index(in_colnames_2)
                        #second_value = row[k]
                        #data_point[out_colnames[i]] = self.__get_category(row[i], cat_list[i],value2=second_value)
                        #self.results[out_colnames[i]]['cross_categorize'] = True
                    elif function_list[i] == 'sum':
                        if not out_colnames[i]  in data_point:
                            data_point[out_colnames[i]] = row[i]
                            #print('a data_point: ', data_point)
                        else:
                            data_point[out_colnames[i]] += row[i]
                            #print('a data_point: ', data_point)

                #print(data_point)
                csv_writer.writerow(data_point)



    def get_results(self):
        return self.results

    def condense(self,df_data, limit=0):
        keys = self.keys()
        if 'group_by' in keys:
            #print('condense group_by')
            #if(df_data != None):
            self.__condense_group(df_data, limit)
            #else:
            #    self.results
        else:
            #print('condense normal')
            #if(df_data != None):

            self.__condense_data(df_data)
            #else:
            #    self.results

        return self.get_results()




def test_condense():
    import time
    import lib.p3_clean as clean

    print('############# condense test')
    transforms = Transforms(get_raw_transforms_json('../conf.raw.transforms.json'))



    df_source = df_source = pd.read_csv('../03.source_clean.csv')

    _convert = {  # configure type changes
        'conversions': [

            {'column': 'scheduled_day', 'to': 'datetime'},
            {'column': 'appointment_day', 'to': 'datetime'},
                    ]
    }
    df_source, convert_summary = clean.change_types(_convert, df_source)

    df_source.info()

    transforms = Transforms(transforms)
    trans = transforms.getTransforms()['neighbourhood1_transform']
    trans = transforms.getTransforms()['appt_transform']
    trans = transforms.getTransforms()['patient1_transform']

    df_source.info()
    t = time.process_time()
    print('out_file_name: ',trans['out_file_name'])
    Condenser(trans).condense(df_source)
    elapsed_time = time.process_time() - t
    print('Condenser time: ', elapsed_time)

    #df_source.info()



def test_condense_group():
    import time
    import lib.p3_clean as clean

    print('############# condense test')
    transforms = Transforms(get_raw_transforms_json('../conf.raw.transforms.json'))



    df_source = df_source = pd.read_csv('../03.source_clean.csv')

    _convert = {  # configure type changes
        'conversions': [

            {'column': 'scheduled_day', 'to': 'datetime'},
            {'column': 'appointment_day', 'to': 'datetime'},
                    ]
    }
    df_source, convert_summary = clean.change_types(_convert, df_source)

    df_source.info()

    transforms = Transforms(transforms)

    trans = transforms.getTransforms()['patient1_transform']

    df_source.info()
    t = time.process_time()
    print('out_file_name: ',trans['out_file_name'])
    Condenser(trans).condense(df_source)
    elapsed_time = time.process_time() - t
    print('Condenser time: ', elapsed_time)

    #df_source.info()


def main():
    test_condense()

if __name__ == "__main__":
    # execute only if run as a script
    main()