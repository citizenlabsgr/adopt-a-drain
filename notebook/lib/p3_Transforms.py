import json
from pprint import pprint

def get_raw_transforms_json(file_name):
    '''
    read json and load up as transform configuration
    :param file_name:
    :return:
    '''
    return json.load(open(file_name))

class Transforms(dict):

    def getClassifiers(self):
        return self['classifiers']

    def getTransforms(self):
        self.substitute()
        return self['transforms']

    def __addMissingDefaults(self, trans):

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

    def substitute(self):
        try:
            if self.substituted:
                return self
        except AttributeError:
            self.substituted = False

        classifiers = self.getClassifiers()
        for ti, trans in self['transforms'].items():
            for flds in trans['fields']:
                if 'categories' in flds:
                    if isinstance(flds['categories'],str):
                        cat_name = flds['categories']
                        flds['categories']=classifiers[cat_name]
            self.__addMissingDefaults(trans)

            self.substituted = True
        return self


    def getBestTransform(self,df_data, hint=None):
        '''
            field_in has to match all fields of df_data
        :param df_data:
        :return:
        '''
        tranform = {}

        col_names = df_data.columns

        transforms = self.getTransforms()
        likely_transforms = transforms.items()
        if hint != None:
            likely_transforms = []
            for t,item in transforms.items():
                if hint in t:
                    likely_transforms.append(item)

        # TODO: need key_in and key_out validation here

        for item in likely_transforms: # process all features

            fields = [x for x in item['fields']]

            for rec in fields:  # process item fields

                if 'field_in' in rec:
                    if not rec['virtual']:

                        if rec['field_in'] in col_names:
                            transform = item  # over and over and over
                        else:
                            msg = 'field: {} not in dataframe columns: {}'.format(rec['field_in'],col_names)
                            transform = {'error':msg}
                            raise NameError(msg)
                            break

            if len(transform) > 0:

                break



        return transform


def test_get_raw_transforms_json():
    print('############ test_get_raw_transforms_json')
    transforms_raw = get_raw_transforms_json('../conf.raw.transforms.json')
    print(transforms_raw)


def test_transform_substitute():
    print('############ test_transform_substitute')
    transforms_raw = get_raw_transforms_json('../conf.raw.transforms.json')
    #print(transforms_raw)
    transforms = Transforms(transforms_raw).substitute()
    print(transforms)

def test_transform_best_transform():
    import pandas as pd
    print('############ test_transform_best_transform')
    # load tranforms
    transforms_raw = get_raw_transforms_json('../conf.raw.transforms.json')
    # get some data
    df = pd.read_csv('../03.source_clean.csv')

    trans = Transforms(transforms_raw).getBestTransform(df,'appt')

    print(trans)

def main():
    test_get_raw_transforms_json()
    test_transform_substitute()
    test_transform_best_transform()

if __name__ == "__main__":
    # execute only if run as a script
    main()