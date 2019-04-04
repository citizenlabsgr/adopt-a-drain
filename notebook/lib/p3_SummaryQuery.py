import collections
from pprint import pprint
class SummaryQuery(dict):
    # self.group_names=[]
    # self.rack_groups=[]
    # def __init__(self):
    #    self.group_names=[]
    #    self.rack_groups=[]
    #    print('self.group_names: ', self.group_names)
    #    print('self.rack_groups: ',self.rack_groups)

    def get_pie_data(self,feature_name=None, title='add title'):
        new_dict = {title: {}}

        new_dict = {
            'titles': [title],
            'colors': ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'blue'],
            # 'F': [620],
            # 'M': [380]
        }

        try:
            test_ = {self.activityKey: {}}

        except:
            raise NameError('Use is undefined. Call Use before attempting to call get_pie_data')


        for act, actValue in self.items():  # if isinstance(actValue,dict):
            #print(act, ' activityKey: ', self.activityKey)
            if act == self.activityKey:
                if isinstance(actValue, dict):
                    # print('act: ', act)
                    for f, featValue in actValue.items():

                        if isinstance(featValue, dict):
                            #if f == self.activityKey:
                            new_dict['titles']=[f]
                            for cat, catValue in featValue.items():
                                new_dict[cat]=catValue
                                #print('cat',cat, ' cat: ', catValue)

        return new_dict

    def use(self,activityKey):
        self.activityKey = activityKey
        return self

    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if not val:  # init val
                val = dict.get(self, key, default)
            else:  # key:list or key:value
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)

            if not val:
                break;

        return val

    def get_features_as_labels(self):

        try:
            test = {self.activityKey: {}}
        except:
            raise NameError('Use is undefined. Call Use before attempting to call get_features_as_labels')
        feature_list = []
        for act, actValue in self.items():  # if isinstance(actValue,dict):
            if isinstance(actValue, dict):

                for f, featValue in actValue.items():
                    #print('f: ', f)
                    if isinstance(featValue, dict):
                        feature_list.append(f)
                        #new_dict[self.activityKey][f]={}
                        #for cat, catValue in featValue.items():

                        #    new_dict[self.activityKey][f][cat] = round(catValue / sum_val, 7)
        return feature_list


    def normalize(self):
        new_dict = {}
        try:
            new_dict = {self.activityKey: {}}
        except:
            raise NameError('Use is undefined. Call Use before attempting to call normalize')

        for act, actValue in self.items():  # if isinstance(actValue,dict):
            if isinstance(actValue, dict):
                #print('act: ', act)

                for f, featValue in actValue.items():
                    #print('f: ', f)
                    if isinstance(featValue, dict):
                        #print('featValue: ', featValue)
                        # max_values.append(max(zip(featValue.values(), featValue.keys())))
                        sum_val = sum(featValue.values())
                        #print('max: ', max_val)
                        new_dict[self.activityKey][f]={}
                        for cat, catValue in featValue.items():
                            # print('normal', catValue/max_val)
                            #print('before: ', new_dict[act][f][cat] )
                            #print('self.activityKey: ', self.activityKey)
                            #print('cat: ', cat)
                            #new_dict[act][f][cat] = round(catValue / sum_val, 7)
                            if sum_val > 0 or sum_val < 0 :
                                new_dict[self.activityKey][f][cat] = round(catValue / sum_val, 7)
                            else:
                                new_dict[self.activityKey][f][cat] = 0.0


        return SummaryQuery(new_dict).use(self.activityKey)

    def subtract(self, summary):
        new_dict = {}
        try:
            new_dict = {self.activityKey: {}}
        except:
            raise NameError('Use is undefined. Call Use before attempting to call subtract')

        for act, actValue in summary.items():  # if isinstance(actValue,dict):
            if isinstance(actValue, dict):
                #print('act: ', act)

                for f, featValue in actValue.items():
                    #print('f: ', f)
                    if isinstance(featValue, dict):

                        new_dict[self.activityKey][f]={}
                        for cat, catValue in featValue.items():

                            new_dict[self.activityKey][f][cat] = self[self.activityKey][f][cat] - \
                                                                 summary[self.activityKey][f][cat]


        return SummaryQuery(new_dict).use(self.activityKey)

    def setLastSelection(self,selection):
        #print('set last: ',selection)
        self.lastselection = selection


    def lastSelection(self):

        return SummaryQuery(self.lastselection).use(self.activityKey)

    def select(self, feature_list):

        new_dict = {}
        self.lastselection = {}
        try:
            new_dict = {self.activityKey: {}}
        except:
            raise NameError('Use is undefined. Call Use before attempting to call select')

        #new_dict[self.activityKey] = {}
        for act, actValue in self.items():  # if isinstance(actValue,dict):
            if self.activityKey == act:
                if isinstance(actValue, dict):
                    #print('act: ', act)

                    for f, featValue in actValue.items():
                        #print('f: ', f)

                        if f in feature_list:
                            new_dict[self.activityKey][f] = featValue.copy()

        self.setLastSelection( new_dict )
        sq = SummaryQuery(self.lastselection).use(self.activityKey)
        sq.setLastSelection(self.lastselection)
        return sq


    def refactor(self, labels):

        #refactored = {}
        new_dict = {}
        try:
            new_dict = {self.activityKey: {}}
        except:
            raise NameError('Use is undefined. Call Use before attempting to call refactor')

        groupKeys = self.keys()


        for groupKey in groupKeys:
            group = dict.get(self, groupKey )
            #print('group: ', group)
            if not isinstance(group, dict):
                new_dict[groupKey] = group #summary[groupKey]
            else:

                new_dict[groupKey] = {}
                activityKeys = [x for x in group] #summary[groupKey]]

                for featureKey in activityKeys:

                    if isinstance(group[featureKey], collections.Iterable):
                        new_dict[groupKey][featureKey] = {}
                        #for classKey in summary[groupKey][featureKey]:
                        for classKey in group[featureKey]:
                            #classValue = summary[groupKey][featureKey][classKey]
                            classValue = group[featureKey][classKey]
                            # print('labels: ',labels)
                            # print('featureKey: ', featureKey)
                            # print()
                            # print('labels[featureKey]: ', labels[featureKey])
                            # print('len(labels[featureKey]): ', len(labels[featureKey]))
                            # print('classKey: ', classKey)
                            try:

                                if len(labels[featureKey]) > 0:  # swap out number for string
                                    newKey = labels[featureKey][classKey]
                                    new_dict[groupKey][featureKey][newKey] = classValue
                                else:  # no change
                                    new_dict[groupKey][featureKey][classKey] = classValue
                            except KeyError:
                                raise NameError('add feature ' + featureKey + ' to labels.')
                    else:
                        #value = summary[groupKey][featureKey]
                        value = group[featureKey]

                        new_dict[groupKey][featureKey] = value

        return SummaryQuery(new_dict).use(self.activityKey)

    def __prune(self, path, default=None):

        keys = path.split("/")
        val = None
        rc = False

        for key in keys:

            if not val:  # init val

                val = dict.get(self, key)

            else:  # key:list or key:value

                if not key in val.keys():
                    # path not found
                    break

                val.pop(key)
                rc = True

            if not val:
                raise NameError('prune bad path: ' + path)
                break;

        return rc

    def prune(self, path, default=None):
        '''
        the last item in path can be a list
        '''
        keys = path.split("/")
        val = None
        rc = False
        prune_list = []
        # print('keys: ',keys)
        # print(type(keys[1]))
        lst = keys[1].split(",")
        # print('lst: ', lst)
        prune_list = ['{}/{}'.format(keys[0], x) for x in keys[1].split(',')]

        #print(prune_list)
        for p in prune_list:
            # print("this.__prune('{}')".format(p))
            self.__prune(p)
        return rc

    def __get_bottom(self, lyrName, group_no, catName, rack_groups):
        '''
        return the first key of layer_no
        :param layer_no:
        :param rack_groups:
        :return:
        '''
        #print('lyrName: ',lyrName)
        #print('group: ',group_no)
        #print('group arry: ', rack_groups[group_no])
        #print('catName: ', catName )
        # print('catName index: ', rack_groups[group_no].index(catName))
        # print('type: ',type(rack_groups[group_no][0]).__name__)
        bottom_ = None

        #print('rack_group: ', rack_groups)

        bottomName = '{}-{}'.format(lyrName, rack_groups[group_no][0])

        cat_no = rack_groups[group_no].index(catName)


        if cat_no > 0:
            bottom_ = bottomName
        #print('bottom: ', bottomName)
        return bottom_

    def __get_alpha(self, lyrName, group_no, catName, rack_groups):
        alpha = 1.0

        # bottomName = '{}-{}'.format(lyrName, rack_groups[group_no][0])
        cat_no = rack_groups[group_no].index(catName)

        if cat_no > 0:
            alpha = 0.5

        return alpha

    def __get_color(self, group_no):
        colors_ = ['yellowgreen', 'lightcoral',
                   'lightskyblue', 'palevioletred',
                   'cornflowerblue',
                   'lightpink',
                   'deepskyblue', 'darkseagreen']
        find_no = group_no
        while find_no >= len(colors_):  # start over
            find_no -= len(colors_)

        return colors_[find_no]

    def __get_layer_name(self, lyrName, catName):
        # print('type(catName): ', type(catName))
        if type(catName).__name__ == 'int64' or type(catName).__name__ == 'int':
            layer_name = '{}-{}'.format(lyrName, catName)
        else:
            layer_name = catName

        return layer_name

    def __get_group_no(self, activityKey, feature, feature_list):
        grp_no = 0
        # activities = dict.get(self, activityKey)
        for feat in feature_list:
            if feat == feature:
                break
            grp_no += 1
        return grp_no

    '''
    def __get_group_no(self,layer_no,rack_groups):
        w_no = 0
        for g_no in range(0,len(rack_groups)):
            for l_no in rack_groups[g_no]:
                if layer_no == w_no:
                    return g_no
                w_no += 1

        return -1  

    '''

    # def __get_rack_groups(self,count_summary):
    def __get_rack_groups(self, activityKey,feature_list):
        '''
        one rack group per layer
        numbered by the order given in count_summary
        the rack can be referenced by layer_no
        :param count_summary:
        :return:
        '''
        rack_groups = []
        # show_all_flag = (len(selections) == 0)
        # for f in count_summary: # features
        activities = dict.get(self, activityKey)
        # print('activities: ',activities)

        #for f in activities:
        for f in feature_list:

            # if show_all_flag or f in selections:
            # print('activities f: ',f)

            # keys = count_summary[f].keys()
            keys = activities[f].keys()

            rack_groups.append(list(keys))

        return rack_groups

    # def __get_racked_data(self,lyrName,group_no,catName,count_summary, rack_groups):
    def __get_racked_data(self, lyrName, group_no, catName, activityKey, rack_groups, feature_list):
        '''

        :param group_no: is the position of the data in the rack
        :param count_summary:
        :param rack_groups:
        :return:
        '''

        rack = []  # list of groups from each feature
        racked_data = []  # [1,1,0,0]
        group_cnt = 0
        activities = dict.get(self, activityKey)
        # print('catName: ', catName)
        # print('rack_groups: ',rack_groups)
        # print('group_no: ', group_no)
        # print('catName B: ', catName)
        cat_index = -1
        try:
            cat_idx = rack_groups[group_no].index(catName)
        except ValueError:
            print('ValueError group_no B: ', group_no)
            print('ValueError catName B: ', catName)
            print('ValueError rack_groups B: ', rack_groups)
            # raise ValueError('category name not in rack_groups [{}][{}] and therefor not in '.format(group_no,catName))
            raise ValueError(' "{}" [{}][{}]  ' \
                             .format(lyrName, group_no, catName))

        # for f in count_summary: # feature name
        for f in feature_list: #activities:  # feature name

            if group_cnt == group_no:

                # values = list(count_summary[f].values())
                values = list(activities[f].values())

                #print('values: ',values)
                #print('cat_idx: ',cat_idx)
                racked_data.append(values[cat_idx])

            else:
                # for i in range(0,len(rack_groups[group_cnt])) :
                #    racked_data.append(0)

                racked_data.append(0)
            group_cnt += 1

        return racked_data

    def __is_category_in_labels(self, labels, group_name, cat_no):
        if len(labels) == 0:
            return False
        if not group_name in labels:
            return False

        if len(labels[group_name]) == 0:
            return False
        try:
            if isinstance(cat_no, str):
                if len(cat_no) == 0:
                    return False
            else:
                if cat_no < 0 or cat_no > len(labels[group_name]):
                    return False

        except TypeError:
            print('group_name: ', group_name)
            print('cat_no: ', cat_no, type(cat_no))
            print('labels: ', labels)
        return True



    def get_stacked_layers(self, activityKey='counts',feature_list=[],labels=[]):
        '''
         each key in the count_summary is a layer

        :param count_summary:
        :return:
        '''
        try:
            test_ = {self.activityKey: {}}

        except:
            raise NameError('Use is undefined. Call Use before attempting to call get_stacked_layers')

        #if activityKey != 'counts':
        #self.activityKey = activityKey
        # print('counts: ',self.counts())
        # print('get_stacked_layers 1')
        stacked_layers = {}
        # show_all_flag = (len(selections) == 0)
        # rack_groups = self.__get_rack_groups(self.get(activityKey))#(count_summary)

        #print('A rack_groups: ', rack_groups)
        layer_no = 0
        # add stub layers firs because the layers get sorted alpha
        # print('ignore_features_list: ',ignore_features_list)
        # print(type(self))

        activities = dict.get(self, self.activityKey)

        if len(feature_list) == 0 :
            feature_list = [ x for x in activities]

        # print('feature_list: ', feature_list)



        rack_groups = self.__get_rack_groups(self.activityKey,feature_list)  # (count_summary)

        #print('rack_groups: ', rack_groups)
        #if 1 == 1:
        #    return {'force stop':'stop'}

        for lyrName in feature_list:
            # for lyrName,lyrValue in dict.items(self):
            # for lyrName in self.get(activityKey):
            # for lyrName in count_summary:
            lyrValue = activities[lyrName]
            # print('activities[lyrName]',activities[lyrName])
            # print("#######")
            #print('lyrName: ',lyrName)
            # print('lyrName: ',lyrName,' lyrValues: ',lyrValue )
            #############

            # if show_all_flag or lyrName in selections:
            #########
            cat_no = 0
            if isinstance(lyrValue, dict):
                # print('type: ',type(lyrValue))

                # for catName in lyrValue: #for catName in count_summary[lyrName]:
                for catName, catValue in lyrValue.items():
                    # print('  catName A: ', catName)

                    # print('layer name: ',get_layer_name(lyrName,catName))

                    layer_ = {}

                    # group_no = self.__get_group_no(layer_no,rack_groups)
                    group_no = self.__get_group_no(self.activityKey, lyrName, feature_list)

                    # print('  self.activityKey: ', self.activityKey)
                    # print('  group_no: ', group_no)
                    layer_ = {'name': self.__get_layer_name(lyrName, catName),
                              'group': group_no,
                              'group_name': lyrName,
                              'layer': layer_no,
                              'category': catName,
                              'category_no': cat_no,
                              'data': self.__get_racked_data(lyrName, group_no, catName, self.activityKey, rack_groups, feature_list),
                              'color': self.__get_color(group_no),
                              'alpha': self.__get_alpha(lyrName, group_no, catName, rack_groups),
                              'bottom': self.__get_bottom(lyrName, group_no, catName, rack_groups)}

                    if layer_['category'] == 0:
                        # print('found 0 ', layer_)

                        layer_['bottom'] == '-1'
                        # print(' bottom: ', layer_['bottom'])

                    stacked_layers[self.__get_layer_name(lyrName, catName)] = layer_
                    cat_no += 1
                    layer_no += 1




        if len(labels) > 0:
            bottom_name = None
            for lyr in stacked_layers:
                #print(stacked_layers[lyr])
                cat_no  = stacked_layers[lyr]['category_no']
                group_name = stacked_layers[lyr]['group_name']
                if self.__is_category_in_labels(labels, group_name, cat_no):

                    if cat_no == 0:
                        bottom_name = labels[group_name][cat_no]

                        stacked_layers[lyr]['name'] = bottom_name
                        stacked_layers[lyr]['bottom'] = None
                    else:
                        stacked_layers[lyr]['name'] = labels[group_name][cat_no]
                        stacked_layers[lyr]['bottom'] = bottom_name



        return stacked_layers

    def deprecated_get_stacked_layers(self, activityKey='counts', feature_list=[], labels=[]):
        '''
         each key in the count_summary is a layer

        :param count_summary:
        :return:
        '''
        # if activityKey != 'counts':
        self.activityKey = activityKey
        # print('counts: ',self.counts())
        # print('get_stacked_layers 1')
        stacked_layers = {}
        # show_all_flag = (len(selections) == 0)
        # rack_groups = self.__get_rack_groups(self.get(activityKey))#(count_summary)

        # print('A rack_groups: ', rack_groups)
        layer_no = 0
        # add stub layers firs because the layers get sorted alpha
        # print('ignore_features_list: ',ignore_features_list)
        # print(type(self))

        activities = dict.get(self, self.activityKey)

        if len(feature_list) == 0:
            feature_list = [x for x in activities]

        # print('feature_list: ', feature_list)

        rack_groups = self.__get_rack_groups(self.activityKey, feature_list)  # (count_summary)

        # print('rack_groups: ', rack_groups)
        # if 1 == 1:
        #    return {'force stop':'stop'}

        for lyrName in feature_list:
            # for lyrName,lyrValue in dict.items(self):
            # for lyrName in self.get(activityKey):
            # for lyrName in count_summary:
            lyrValue = activities[lyrName]
            # print('activities[lyrName]',activities[lyrName])
            # print("#######")
            # print('lyrName: ',lyrName)
            # print('lyrName: ',lyrName,' lyrValues: ',lyrValue )
            #############

            # if show_all_flag or lyrName in selections:
            #########
            cat_no = 0
            if isinstance(lyrValue, dict):
                # print('type: ',type(lyrValue))

                # for catName in lyrValue: #for catName in count_summary[lyrName]:
                for catName, catValue in lyrValue.items():
                    # print('  catName A: ', catName)

                    # print('layer name: ',get_layer_name(lyrName,catName))

                    layer_ = {}

                    # group_no = self.__get_group_no(layer_no,rack_groups)
                    group_no = self.__get_group_no(self.activityKey, lyrName, feature_list)

                    # print('  self.activityKey: ', self.activityKey)
                    # print('  group_no: ', group_no)
                    layer_ = {'name': self.__get_layer_name(lyrName, catName),
                              'group': group_no,
                              'group_name': lyrName,
                              'layer': layer_no,
                              'category': catName,
                              'category_no': cat_no,
                              'data': self.__get_racked_data(lyrName, group_no, catName, self.activityKey, rack_groups,
                                                             feature_list),
                              'color': self.__get_color(group_no),
                              'alpha': self.__get_alpha(lyrName, group_no, catName, rack_groups),
                              'bottom': self.__get_bottom(lyrName, group_no, catName, rack_groups)}

                    if layer_['category'] == 0:
                        # print('found 0 ', layer_)

                        layer_['bottom'] == '-1'
                        # print(' bottom: ', layer_['bottom'])

                    stacked_layers[self.__get_layer_name(lyrName, catName)] = layer_
                    cat_no += 1
                    layer_no += 1

        if len(labels) > 0:
            bottom_name = None
            for lyr in stacked_layers:
                # print(stacked_layers[lyr])
                cat_no = stacked_layers[lyr]['category_no']
                group_name = stacked_layers[lyr]['group_name']
                if self.__is_category_in_labels(labels, group_name, cat_no):

                    if cat_no == 0:
                        bottom_name = labels[group_name][cat_no]

                        stacked_layers[lyr]['name'] = bottom_name
                        stacked_layers[lyr]['bottom'] = None
                    else:
                        stacked_layers[lyr]['name'] = labels[group_name][cat_no]
                        stacked_layers[lyr]['bottom'] = bottom_name

            ''' 
            for each layer
                set bottom_name = None 
                get the category number from layer
                get the group_name from layer

                if is_category_in_labels(labels,group_name,category):


                    if layer.category is zero then
                        set bottom_name to label.group_name.category
                        set layer.name to bottom_name
                        set layer.bottom to None
                    if layer.category is not zero then    

                        set layer.name = label[group_name][category]
                        set layer.bottom = bottom_name  
            '''

        return stacked_layers


def get_test_labels():
    return {
        'age': [n for n in range(0, 116)],
        'age_group': ['0 to 14', '15 to 24', '25 to 54', '55 to 65', '65+'],
        'appointments': [],
        'appointment_group': ['1', '2 to 12', '13 to 24', '25 to 42', '43+'],
        'attendance': ['No-Show', 'Show'],
        'alcoholism': ['Non-alcoholic', 'Alcoholic'],

        'diabetes': ['Non-diabetic', 'Diabetic'],
        'disabled': ['Non-disabled', '1', '2', '3', '4'],

        'gender': ['Female', 'Male'],

        'handcap': ['Not', '1-HC', '2-HC', '3-HC', '4-HC'],
        'hipertension': ['Non-hipertensive', 'Hipertensive'],

        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'no_show': ['Show', 'No-Show'],
        'no_shows': [],  # leave empty... unclassified data

        'scholarship': ['Non-Scholar', 'Scholar'],

        'scheduled_day_of_week': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'scheduled_time': [],
        'scheduled_hour': ['{}:00'.format(hour) for hour in range(0, 25)],
        'sms': ['Not-cancelled', 'SMS Cancelled'],

        'skipper': ['Non-skipper', 'Skipper']

    }
def test_sum1():
    return  {'patients': 62253, 'counts': {'appointments': {1: 37886, 2: 13886, 3: 5499, 4: 2365, 5: 1119, 6: 553, 7: 306, 8: 202, 9: 104, 10: 85, 11: 63, 12: 36, 13: 35, 14: 22, 15: 15, 16: 10, 17: 10, 18: 8, 19: 6, 20: 8, 21: 3, 22: 1, 23: 2, 24: 1, 29: 1, 30: 2, 33: 1, 34: 2, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 50: 1, 51: 1, 54: 1, 55: 1, 57: 1, 62: 4, 65: 1, 70: 1, 84: 1, 88: 1}, 'appointment_group': {0: 37886, 1: 24218, 2: 121, 3: 13, 4: 15}, 'no_shows': {0: 44605, 1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 56469, 1: 5784}, 'hipertension': {0: 50048, 1: 12205}, 'diabetes': {0: 57844, 1: 4409}, 'alcoholism': {0: 60747, 1: 1506}, 'handcap': {0: 61123, 1: 1022, 2: 99, 3: 6, 4: 3}, 'gender': {0: 40011, 1: 22242}, 'age': {0: 2028, 1: 1476, 2: 1081, 3: 955, 4: 840, 5: 915, 6: 874, 7: 829, 8: 839, 9: 745, 10: 727, 11: 703, 12: 650, 13: 662, 14: 622, 15: 679, 16: 790, 17: 831, 18: 848, 19: 901, 20: 803, 21: 822, 22: 768, 23: 734, 24: 717, 25: 743, 26: 714, 27: 758, 28: 782, 29: 765, 30: 812, 31: 791, 32: 812, 33: 820, 34: 847, 35: 733, 36: 843, 37: 815, 38: 848, 39: 828, 40: 766, 41: 753, 42: 673, 43: 717, 44: 764, 45: 757, 46: 765, 47: 810, 48: 791, 49: 847, 50: 883, 51: 885, 52: 915, 53: 883, 54: 841, 55: 817, 56: 899, 57: 906, 58: 857, 59: 814, 60: 842, 61: 773, 62: 759, 63: 745, 64: 704, 65: 640, 66: 656, 67: 565, 68: 535, 69: 487, 70: 441, 71: 408, 72: 384, 73: 411, 74: 345, 75: 311, 76: 339, 77: 306, 78: 306, 79: 235, 80: 284, 81: 247, 82: 214, 83: 182, 84: 182, 85: 157, 86: 151, 87: 121, 88: 92, 89: 90, 90: 62, 91: 39, 92: 46, 93: 30, 94: 22, 95: 14, 96: 14, 97: 9, 98: 4, 99: 1, 100: 3, 102: 2, 115: 2}, 'age_group': {0: 13948, 1: 7894, 2: 23961, 3: 8117, 4: 8333}}, 'sums': {}, 'total': {'count': 62253}}

def test_sum2():
    return  {'patients': 17648, 'counts': {'appointments': {1: 7110, 2: 4911, 3: 2530, 4: 1330, 5: 694, 6: 365, 7: 223, 8: 144, 9: 77, 10: 67, 11: 50, 12: 28, 13: 28, 14: 20, 15: 11, 16: 9, 17: 6, 18: 6, 19: 4, 20: 7, 21: 3, 22: 1, 23: 2, 29: 1, 30: 2, 33: 1, 34: 1, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 54: 1, 55: 1, 57: 1, 62: 3, 84: 1, 88: 1}, 'appointment_group': {0: 7110, 1: 10419, 2: 97, 3: 12, 4: 10}, 'no_shows': {1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 15734, 1: 1914}, 'hipertension': {0: 14642, 1: 3006}, 'diabetes': {0: 16499, 1: 1149}, 'alcoholism': {0: 17128, 1: 520}, 'handcap': {0: 17373, 1: 244, 2: 27, 3: 3, 4: 1}, 'gender': {0: 11496, 1: 6152}, 'age': {0: 555, 1: 383, 2: 226, 3: 224, 4: 235, 5: 268, 6: 248, 7: 227, 8: 255, 9: 261, 10: 228, 11: 196, 12: 206, 13: 223, 14: 217, 15: 227, 16: 267, 17: 291, 18: 278, 19: 295, 20: 275, 21: 285, 22: 285, 23: 257, 24: 258, 25: 269, 26: 249, 27: 274, 28: 272, 29: 261, 30: 269, 31: 245, 32: 252, 33: 276, 34: 264, 35: 226, 36: 269, 37: 243, 38: 255, 39: 251, 40: 233, 41: 247, 42: 199, 43: 223, 44: 241, 45: 215, 46: 222, 47: 225, 48: 199, 49: 248, 50: 228, 51: 242, 52: 248, 53: 242, 54: 210, 55: 205, 56: 209, 57: 225, 58: 205, 59: 209, 60: 189, 61: 166, 62: 174, 63: 144, 64: 150, 65: 144, 66: 140, 67: 122, 68: 133, 69: 93, 70: 84, 71: 99, 72: 87, 73: 79, 74: 70, 75: 62, 76: 70, 77: 61, 78: 74, 79: 46, 80: 67, 81: 54, 82: 56, 83: 48, 84: 29, 85: 33, 86: 32, 87: 27, 88: 11, 89: 19, 90: 19, 91: 11, 92: 12, 93: 8, 94: 6, 95: 4, 96: 1, 97: 2, 98: 1, 115: 1}, 'age_group': {0: 3953, 1: 2719, 2: 7297, 3: 1876, 4: 1803}}, 'sums': {}, 'total': {'count': 17648}}

def test_get_features_as_labels():
    print('############ test_get_features_as_labels Summary')

    start = test_sum1()
    qs = SummaryQuery(start).use('counts').select([ 'no_shows', 'scholarship', 'hipertension', 'diabetes'])
    feature_list = qs.get_features_as_labels()
    print('refactor: ', feature_list)
    print('start: ', start)

def test_refactor():
    print('############ Refactor Summary')
    #start = {'patients': 62253, 'counts': {'appointments': {1: 37886, 2: 13886, 3: 5499, 4: 2365, 5: 1119, 6: 553, 7: 306, 8: 202, 9: 104, 10: 85, 11: 63, 12: 36, 13: 35, 14: 22, 15: 15, 16: 10, 17: 10, 18: 8, 19: 6, 20: 8, 21: 3, 22: 1, 23: 2, 24: 1, 29: 1, 30: 2, 33: 1, 34: 2, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 50: 1, 51: 1, 54: 1, 55: 1, 57: 1, 62: 4, 65: 1, 70: 1, 84: 1, 88: 1}, 'appointment_group': {0: 37886, 1: 24218, 2: 121, 3: 13, 4: 15}, 'no_shows': {0: 44605, 1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 56469, 1: 5784}, 'hipertension': {0: 50048, 1: 12205}, 'diabetes': {0: 57844, 1: 4409}, 'alcoholism': {0: 60747, 1: 1506}, 'handcap': {0: 61123, 1: 1022, 2: 99, 3: 6, 4: 3}, 'gender': {0: 40011, 1: 22242}, 'age': {0: 2028, 1: 1476, 2: 1081, 3: 955, 4: 840, 5: 915, 6: 874, 7: 829, 8: 839, 9: 745, 10: 727, 11: 703, 12: 650, 13: 662, 14: 622, 15: 679, 16: 790, 17: 831, 18: 848, 19: 901, 20: 803, 21: 822, 22: 768, 23: 734, 24: 717, 25: 743, 26: 714, 27: 758, 28: 782, 29: 765, 30: 812, 31: 791, 32: 812, 33: 820, 34: 847, 35: 733, 36: 843, 37: 815, 38: 848, 39: 828, 40: 766, 41: 753, 42: 673, 43: 717, 44: 764, 45: 757, 46: 765, 47: 810, 48: 791, 49: 847, 50: 883, 51: 885, 52: 915, 53: 883, 54: 841, 55: 817, 56: 899, 57: 906, 58: 857, 59: 814, 60: 842, 61: 773, 62: 759, 63: 745, 64: 704, 65: 640, 66: 656, 67: 565, 68: 535, 69: 487, 70: 441, 71: 408, 72: 384, 73: 411, 74: 345, 75: 311, 76: 339, 77: 306, 78: 306, 79: 235, 80: 284, 81: 247, 82: 214, 83: 182, 84: 182, 85: 157, 86: 151, 87: 121, 88: 92, 89: 90, 90: 62, 91: 39, 92: 46, 93: 30, 94: 22, 95: 14, 96: 14, 97: 9, 98: 4, 99: 1, 100: 3, 102: 2, 115: 2}, 'age_group': {0: 13948, 1: 7894, 2: 23961, 3: 8117, 4: 8333}}, 'sums': {}, 'total': {'count': 62253}}
    start = test_sum1()
    refactor = SummaryQuery(start).use('counts').refactor(get_test_labels())
    print('refactor: ', refactor)
    print('start: ', start )


def test_normalize():
    print('############ Normalize Summary')

    #start = {'patients': 62253, 'counts': {'appointments': {1: 37886, 2: 13886, 3: 5499, 4: 2365, 5: 1119, 6: 553, 7: 306, 8: 202, 9: 104, 10: 85, 11: 63, 12: 36, 13: 35, 14: 22, 15: 15, 16: 10, 17: 10, 18: 8, 19: 6, 20: 8, 21: 3, 22: 1, 23: 2, 24: 1, 29: 1, 30: 2, 33: 1, 34: 2, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 50: 1, 51: 1, 54: 1, 55: 1, 57: 1, 62: 4, 65: 1, 70: 1, 84: 1, 88: 1}, 'appointment_group': {0: 37886, 1: 24218, 2: 121, 3: 13, 4: 15}, 'no_shows': {0: 44605, 1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 56469, 1: 5784}, 'hipertension': {0: 50048, 1: 12205}, 'diabetes': {0: 57844, 1: 4409}, 'alcoholism': {0: 60747, 1: 1506}, 'handcap': {0: 61123, 1: 1022, 2: 99, 3: 6, 4: 3}, 'gender': {0: 40011, 1: 22242}, 'age': {0: 2028, 1: 1476, 2: 1081, 3: 955, 4: 840, 5: 915, 6: 874, 7: 829, 8: 839, 9: 745, 10: 727, 11: 703, 12: 650, 13: 662, 14: 622, 15: 679, 16: 790, 17: 831, 18: 848, 19: 901, 20: 803, 21: 822, 22: 768, 23: 734, 24: 717, 25: 743, 26: 714, 27: 758, 28: 782, 29: 765, 30: 812, 31: 791, 32: 812, 33: 820, 34: 847, 35: 733, 36: 843, 37: 815, 38: 848, 39: 828, 40: 766, 41: 753, 42: 673, 43: 717, 44: 764, 45: 757, 46: 765, 47: 810, 48: 791, 49: 847, 50: 883, 51: 885, 52: 915, 53: 883, 54: 841, 55: 817, 56: 899, 57: 906, 58: 857, 59: 814, 60: 842, 61: 773, 62: 759, 63: 745, 64: 704, 65: 640, 66: 656, 67: 565, 68: 535, 69: 487, 70: 441, 71: 408, 72: 384, 73: 411, 74: 345, 75: 311, 76: 339, 77: 306, 78: 306, 79: 235, 80: 284, 81: 247, 82: 214, 83: 182, 84: 182, 85: 157, 86: 151, 87: 121, 88: 92, 89: 90, 90: 62, 91: 39, 92: 46, 93: 30, 94: 22, 95: 14, 96: 14, 97: 9, 98: 4, 99: 1, 100: 3, 102: 2, 115: 2}, 'age_group': {0: 13948, 1: 7894, 2: 23961, 3: 8117, 4: 8333}}, 'sums': {}, 'total': {'count': 62253}}
    start = test_sum1()
    query = SummaryQuery(start).use('counts').normalize()

    print('subtracted: ', query)
    print('sum1: ', start)

def test_subtract():
    print('############ Subtract Summaries')
    #sum1 =  {'patients': 62253, 'counts': {'appointments': {1: 37886, 2: 13886, 3: 5499, 4: 2365, 5: 1119, 6: 553, 7: 306, 8: 202, 9: 104, 10: 85, 11: 63, 12: 36, 13: 35, 14: 22, 15: 15, 16: 10, 17: 10, 18: 8, 19: 6, 20: 8, 21: 3, 22: 1, 23: 2, 24: 1, 29: 1, 30: 2, 33: 1, 34: 2, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 50: 1, 51: 1, 54: 1, 55: 1, 57: 1, 62: 4, 65: 1, 70: 1, 84: 1, 88: 1}, 'appointment_group': {0: 37886, 1: 24218, 2: 121, 3: 13, 4: 15}, 'no_shows': {0: 44605, 1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 56469, 1: 5784}, 'hipertension': {0: 50048, 1: 12205}, 'diabetes': {0: 57844, 1: 4409}, 'alcoholism': {0: 60747, 1: 1506}, 'handcap': {0: 61123, 1: 1022, 2: 99, 3: 6, 4: 3}, 'gender': {0: 40011, 1: 22242}, 'age': {0: 2028, 1: 1476, 2: 1081, 3: 955, 4: 840, 5: 915, 6: 874, 7: 829, 8: 839, 9: 745, 10: 727, 11: 703, 12: 650, 13: 662, 14: 622, 15: 679, 16: 790, 17: 831, 18: 848, 19: 901, 20: 803, 21: 822, 22: 768, 23: 734, 24: 717, 25: 743, 26: 714, 27: 758, 28: 782, 29: 765, 30: 812, 31: 791, 32: 812, 33: 820, 34: 847, 35: 733, 36: 843, 37: 815, 38: 848, 39: 828, 40: 766, 41: 753, 42: 673, 43: 717, 44: 764, 45: 757, 46: 765, 47: 810, 48: 791, 49: 847, 50: 883, 51: 885, 52: 915, 53: 883, 54: 841, 55: 817, 56: 899, 57: 906, 58: 857, 59: 814, 60: 842, 61: 773, 62: 759, 63: 745, 64: 704, 65: 640, 66: 656, 67: 565, 68: 535, 69: 487, 70: 441, 71: 408, 72: 384, 73: 411, 74: 345, 75: 311, 76: 339, 77: 306, 78: 306, 79: 235, 80: 284, 81: 247, 82: 214, 83: 182, 84: 182, 85: 157, 86: 151, 87: 121, 88: 92, 89: 90, 90: 62, 91: 39, 92: 46, 93: 30, 94: 22, 95: 14, 96: 14, 97: 9, 98: 4, 99: 1, 100: 3, 102: 2, 115: 2}, 'age_group': {0: 13948, 1: 7894, 2: 23961, 3: 8117, 4: 8333}}, 'sums': {}, 'total': {'count': 62253}}
    #sum2 =  {'patients': 17648, 'counts': {'appointments': {1: 7110, 2: 4911, 3: 2530, 4: 1330, 5: 694, 6: 365, 7: 223, 8: 144, 9: 77, 10: 67, 11: 50, 12: 28, 13: 28, 14: 20, 15: 11, 16: 9, 17: 6, 18: 6, 19: 4, 20: 7, 21: 3, 22: 1, 23: 2, 29: 1, 30: 2, 33: 1, 34: 1, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 54: 1, 55: 1, 57: 1, 62: 3, 84: 1, 88: 1}, 'appointment_group': {0: 7110, 1: 10419, 2: 97, 3: 12, 4: 10}, 'no_shows': {1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 15734, 1: 1914}, 'hipertension': {0: 14642, 1: 3006}, 'diabetes': {0: 16499, 1: 1149}, 'alcoholism': {0: 17128, 1: 520}, 'handcap': {0: 17373, 1: 244, 2: 27, 3: 3, 4: 1}, 'gender': {0: 11496, 1: 6152}, 'age': {0: 555, 1: 383, 2: 226, 3: 224, 4: 235, 5: 268, 6: 248, 7: 227, 8: 255, 9: 261, 10: 228, 11: 196, 12: 206, 13: 223, 14: 217, 15: 227, 16: 267, 17: 291, 18: 278, 19: 295, 20: 275, 21: 285, 22: 285, 23: 257, 24: 258, 25: 269, 26: 249, 27: 274, 28: 272, 29: 261, 30: 269, 31: 245, 32: 252, 33: 276, 34: 264, 35: 226, 36: 269, 37: 243, 38: 255, 39: 251, 40: 233, 41: 247, 42: 199, 43: 223, 44: 241, 45: 215, 46: 222, 47: 225, 48: 199, 49: 248, 50: 228, 51: 242, 52: 248, 53: 242, 54: 210, 55: 205, 56: 209, 57: 225, 58: 205, 59: 209, 60: 189, 61: 166, 62: 174, 63: 144, 64: 150, 65: 144, 66: 140, 67: 122, 68: 133, 69: 93, 70: 84, 71: 99, 72: 87, 73: 79, 74: 70, 75: 62, 76: 70, 77: 61, 78: 74, 79: 46, 80: 67, 81: 54, 82: 56, 83: 48, 84: 29, 85: 33, 86: 32, 87: 27, 88: 11, 89: 19, 90: 19, 91: 11, 92: 12, 93: 8, 94: 6, 95: 4, 96: 1, 97: 2, 98: 1, 115: 1}, 'age_group': {0: 3953, 1: 2719, 2: 7297, 3: 1876, 4: 1803}}, 'sums': {}, 'total': {'count': 17648}}

    sum1 = test_sum1()
    sum2 = test_sum2()
    query = SummaryQuery(sum1).use('counts').subtract(sum2)

    print('subtracted: ', query)
    print('sum1: ', sum1)

def test_selected():
    print('############ Select features')

    features = [
        'appointment_group', 'scholarship',
        'hipertension', 'diabetes',
        'alcoholism', 'handcap',
        'gender']
    start = test_sum1()
    #test_summary = {'patients': 62253, 'counts': {'appointments': {1: 37886, 2: 13886, 3: 5499, 4: 2365, 5: 1119, 6: 553, 7: 306, 8: 202, 9: 104, 10: 85, 11: 63, 12: 36, 13: 35, 14: 22, 15: 15, 16: 10, 17: 10, 18: 8, 19: 6, 20: 8, 21: 3, 22: 1, 23: 2, 24: 1, 29: 1, 30: 2, 33: 1, 34: 2, 35: 1, 37: 1, 38: 2, 40: 1, 42: 2, 46: 2, 50: 1, 51: 1, 54: 1, 55: 1, 57: 1, 62: 4, 65: 1, 70: 1, 84: 1, 88: 1}, 'appointment_group': {0: 37886, 1: 24218, 2: 121, 3: 13, 4: 15}, 'no_shows': {0: 44605, 1: 14426, 2: 2414, 3: 516, 4: 162, 5: 58, 6: 33, 7: 13, 8: 9, 9: 3, 10: 4, 11: 4, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 18: 1}, 'scholarship': {0: 56469, 1: 5784}, 'hipertension': {0: 50048, 1: 12205}, 'diabetes': {0: 57844, 1: 4409}, 'alcoholism': {0: 60747, 1: 1506}, 'handcap': {0: 61123, 1: 1022, 2: 99, 3: 6, 4: 3}, 'gender': {0: 40011, 1: 22242}, 'age': {0: 2028, 1: 1476, 2: 1081, 3: 955, 4: 840, 5: 915, 6: 874, 7: 829, 8: 839, 9: 745, 10: 727, 11: 703, 12: 650, 13: 662, 14: 622, 15: 679, 16: 790, 17: 831, 18: 848, 19: 901, 20: 803, 21: 822, 22: 768, 23: 734, 24: 717, 25: 743, 26: 714, 27: 758, 28: 782, 29: 765, 30: 812, 31: 791, 32: 812, 33: 820, 34: 847, 35: 733, 36: 843, 37: 815, 38: 848, 39: 828, 40: 766, 41: 753, 42: 673, 43: 717, 44: 764, 45: 757, 46: 765, 47: 810, 48: 791, 49: 847, 50: 883, 51: 885, 52: 915, 53: 883, 54: 841, 55: 817, 56: 899, 57: 906, 58: 857, 59: 814, 60: 842, 61: 773, 62: 759, 63: 745, 64: 704, 65: 640, 66: 656, 67: 565, 68: 535, 69: 487, 70: 441, 71: 408, 72: 384, 73: 411, 74: 345, 75: 311, 76: 339, 77: 306, 78: 306, 79: 235, 80: 284, 81: 247, 82: 214, 83: 182, 84: 182, 85: 157, 86: 151, 87: 121, 88: 92, 89: 90, 90: 62, 91: 39, 92: 46, 93: 30, 94: 22, 95: 14, 96: 14, 97: 9, 98: 4, 99: 1, 100: 3, 102: 2, 115: 2}, 'age_group': {0: 13948, 1: 7894, 2: 23961, 3: 8117, 4: 8333}}, 'sums': {}, 'total': {'count': 62253}}
    select = SummaryQuery(start).use('counts').select(features)
    print('selected: ', select )
    print('test_summary: ', start)

def test_get_pie_data():
    print('############ get_pie_data')
    start = test_sum1()
    #select = SummaryQuery(start).use('counts').select('scholarship')
    pie_data = SummaryQuery(start).use('counts').select('scholarship').get_pie_data()
    print('pie_data: ',pie_data)

    #print('select: ',select.get_pie_data())

def test_last_selection():
    print('############ lastSelection')
    start = test_sum1()
    select = SummaryQuery(start).use('counts').select('scholarship')
    print('select: ',select)

    last = select.lastSelection()
    print('lastselect: ', last)

def main():

    test_selected()
    test_subtract()
    test_normalize()
    test_refactor()
    test_get_features_as_labels()
    test_last_selection()
    test_get_pie_data()

if __name__ == "__main__":
    # execute only if run as a script
    main()

