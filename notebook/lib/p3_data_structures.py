'''
def get_chart():
 return  {
    'title': 'Human readable title',
    'xlabel': 'xlabel',
    'ylabel': 'ylabel',
    'figsize': (6,4), # (15,5)
    'layers': {}, #
    'bar_labels': [], #['Scholarship','Alcoholism', 'Diabetes','Hipertension','Handcap','Gender'],
    'bbox_to_anchor': None # move the legend box (1.15, 1.00)
}
'''
'''
class Chart:


    def __init__(self, title):
        self.title = title
        self.layers={}
        self.xlabel = 'xlabel'
        self.ylabel = 'ylabel'
        self.figsize = (6, 4)
        self.domain_labels = []
        self.box_to_anchor = None
    def setXLabel(self,xlabel):
        self.xlabel = xlabel
        return self
    def setYLabel(self,ylabel):
        self.ylabel
        return self
    def setFigSize(self,figsizeTuple):
        self.figsize = figsizeTuple
        return self

    def setDomainLabels(self,domainLabels):
        self.domain_labels = domainLabels
        return self
    def setBboxToAnchor(self,boxtuple):
        self.box_to_anchor = boxtuple
        return self
    def setLayers(self,layers):
        self.layers=layers
        return self



    def toDict(self):
        return {
            'title': self.title,
            'xlabel': self.xlabel,
            'ylabel': self.ylabel,
            'figsize': self.figsize, #(6, 4),  # (15,5)
            'layers': self.layers,  #{},  #
            'domain_labels': self.domain_labels,  # ['Scholarship','Alcoholism', 'Diabetes','Hipertension','Handcap','Gender'],
            'bbox_to_anchor': None  # move the legend box (1.15, 1.00)
        }
'''
'''
class Group:
    #feature_name = 'no name'
    #feature_categeory_list = [] # list of cats, pos of cat in list is asso with dataset feature
    def __init__(self,feature_name,categroy_list):
        self.categeory_list = categroy_list
        self.feature_name = feature_name


    def toDict(self):
        return {'name':self.feature_name,'value':self.categeory_list}
'''
'''
class Grouping:

    #self.xgroup_list=[]

    def __init__(self,group):
        self.group_list = [group]



    def add(self, group):
        self.group_list.append(group)
        return self


    def toDict(self):
        d = {}
        for x in self.group_list:
            dic = x.toDict()
            d[dic['name']]=dic['value']

        return d
'''
def main():
    grp = Group('admin',['pres','vice'])
    print(grp.toDict())
    grps = Grouping(grp)\
        .add(Group('ug',['ss','ss'])).add(Group('xxx',['ffff','ddd']))

    print(grps.toDict())




    #grps grps.add(grp)
    #print(grps.toString())

    #grp = get_feature_groups('admin',['pres','vice'])
    #print(grp)
    #grp = add_feature_group(grp,'cat',['calico','ragdoll'])

    #print(grp)


if __name__ == "__main__":
    # execute only if run as a script
    main()

