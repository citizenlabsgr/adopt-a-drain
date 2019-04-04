class DF_Filter(dict):
    '''
      store and format query where clause
    '''
    def __init__(self,filter_value={}):

        self['filter_list'] = []


    def add(self,val):
        self['filter_list'].append(val)
        return self

    def getFilter(self):
        if len(self['filter_list'])==0:
            msg = 'Empty Filter, set to None or omit.'
            raise ValueError(msg)
        return ' and '.join(self['filter_list'])

def test_emptyfilter():
    print('###### Empty Filter')
    filter = DF_Filter()
    try:
        print('',filter.getFilter())
    except ValueError as inst:
        print(inst)


def test_filter():
    print('###### Filter')
    filter = DF_Filter()
    filter.add('a == b')\
    .add('c > 34')

    print('',filter.getFilter())

def main():
    test_emptyfilter()
    test_filter()



if __name__ == "__main__":
    # execute only if run as a script
    main()