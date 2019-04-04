import numpy as np
import pandas as pd
class VisualizationModel(dict):
    '''
    classifier_ =  {'type':'quantiles', 'category_count': 4, 'color_grades':[(.9,.9,.9),(0,0,1.0)], 'radii_grades': [25,300] }

    '''

    def __init__(self, inpt={}):
        super(VisualizationModel, self).__init__(inpt)
        # set up quartile as default
        if not 'type' in self:
            self['type']='quantiles'
        if not 'category_count' in self:
            self['category_count']=4
        if not 'color_grades' in self:
            self['color_grades'] = [(.7,.7,.7),(0,0,1.0)] # ltgrey to blue
        if not 'radii_grades' in self:
            self['radii_grades'] = [25,400] #low to high
        if not 'breaks' in self:
            self['breaks']=[]

    def setColors(self, colorHigh=None, colorLow=None):
        if colorLow != None:
            self['color_grades'][0] = colorLow
        if colorHigh != None:
            self['color_grades'][1] = colorHigh

    def setRadii(self, high=None, low=None):
        if low != None:
            self['radii_grades'][0] = low
        if high != None:
            self['radii_grades'][1] = high

    def getColors(self, colorHigh=None, colorLow=None):
        return []

    def getRadii(self,minRadius=None,maxRadius=None):
        return []

    def getBreaks(self,_series):
        return []

class QuantileVisualizationModel(VisualizationModel):
    def __init__(self, inpt={}):
        super(QuantileVisualizationModel, self).__init__(inpt)
        # set up quartile as default
        if not 'type' in self:
            self['type'] = 'quantiles'
        if not 'category_count' in self:
            self['category_count'] = 4
        if not 'color_grades' in self:
            self['color_grades'] = [(.9, .9, .9), (0, 0, 1.0)]  # ltgrey to blue
        if not 'radii_grades' in self:
            self['radii_grades'] = [25, 300]  # low to high

class CategoryVisualizationModel(VisualizationModel):
    def __init__(self, inpt={}):
        super(CategoryVisualizationModel, self).__init__(inpt)
        # set up quartile as default
        if not 'type' in self:
            self['type'] = 'categories'
        if not 'category_count' in self:
            self['category_count'] = 4
        if not 'color_grades' in self:
            self['color_grades'] = [(.9, .9, .9), (0, 0, 1.0)]  # ltgrey to blue
        if not 'radii_grades' in self:
            self['radii_grades'] = [25, 300]  # low to high


class GradientModel(VisualizationModel):
    '''
    dict is  {'type':'quartiles', 'category_count': 4, 'color_grades':colors, 'radii_grades': radii }
    # colors = (1,1,1) if tuple then solid single
    # colors = [(1,1,1),(1,1,1)] if list and size == 2 low and high
    # colors = [(1,1,1),(1,1,1),(1,1,1),...] if list and size > 2 the fixed colors
    # radii = 25 if not list then single
    # radii = [minRadii,maxRadii] if list and size == 2 high and low

    color is (r,g,b)
    r = is value 0.0 to 1.0
    g = is value 0.0 to 1.0
    b = is valur 0.0 to 1.0
    examples:
    ltGrey = (0.9,0.9,0.9)
    pureGreen = (0,1.0,0)
    pureBlue = (8/254, 123/254, 157/254)
    pureYellowGreen = (0,84/254,166/254)
    pureWhite = (1.0,1.0,1.0)
    pureRed = (1.0,0,0)
    '''

    def __init__(self, inpt={}):
        super(GradientModel, self).__init__(inpt)

    def getLtGrey(self):
        return (0.9, 0.9, 0.9)
    def getGreen(self):
        return (0, 1.0, 0)
    def getBlue(self):
        return (0,0,1.0)
    def getRed(self):
        return (1.0,0,0)

    def __arrayMultiply(self, array, c):
        return [element * c for element in array]

    def __arraySum(self, a, b):
        return map(sum, zip(a, b))  # add a to b

    def __intermediate(self, a, b, ratio):
        aComponent = self.__arrayMultiply(a, ratio)
        bComponent = self.__arrayMultiply(b, 1 - ratio)

        return tuple(self.__arraySum(aComponent, bComponent))

    def getColors(self, colorHigh=None, colorLow=None):

        if colorHigh == None:
            colorHigh = self['color_grades'][1]
        if colorLow == None:
            colorLow = self['color_grades'][0]

        steps = self['category_count']
        steps = [n / float(steps) for n in range(steps)]
        colors = []
        if colorHigh == None:
            colorHigh = self['color_grades'][1]
        if colorLow == None:
            colorLow = self['color_grades'][0]

        for step in steps:
            colors.append(self.__intermediate(colorHigh, colorLow, step))

        return colors

    def getRadii(self,minRadius=None,maxRadius=None):
        if minRadius==None:
            minRadius = self['radii_grades'][0]
        if maxRadius == None:
            maxRadius = self['radii_grades'][1]

        steps = self['category_count']
        step = (maxRadius - minRadius)/steps
        rc = np.arange(minRadius,maxRadius,step)
        rc[len(rc)-1] = maxRadius
        return rc

    def getLegendLabels(self, breaks):
        rc = []
        bottom = 0

        for b in breaks:
            if bottom == 0:
                label_str = '< {:0.4f}'.format( b)
            else:
                label_str = '{:0.4f} to {:0.4f}'.format(bottom, b)

            rc.append(label_str)
            bottom = b

        label_str = '{:0.4f} +'.format(bottom)
        rc.append(label_str)
        return rc

    def deprecated_getLegendLabels(self, breaks):
        rc = []
        bottom = 0

        for b in breaks:
            if bottom == 0:
                label_str = '< {:0.4f}'.format( b)
            else:
                label_str = '{:0.4f} to {:0.4f}'.format(bottom, b)

            rc.append(label_str)
            bottom = b

        label_str = '{:0.4f} +'.format(bottom)
        rc.append(label_str)
        return rc

    def getBreaks(self,_series):

        steps = self['category_count']

        if isinstance(_series, list):
            #print('convert list to series')
            _series = pd.Series(_series)
            print('type(_series): ',type(_series))

        if self['type'] == 'quantiles':
            q = np.arange(0.0, 1.0, 1.0/steps)
            br = _series.quantile(q)
            #print('q: ',q)
            #print('br: ', list(br)[1:])
            #self['breaks'] = br
            self['breaks'] = list(br)[1:]
            #_series.quantile([0.25, 0.5, 0.75])
            #self['breaks'] = _series.quantile([0.25, 0.5, 0.75])
        else:
            msg = 'Unknown type found in quantiles...{}'.format(self['type'])
            raise AttributeError(msg)

        return self['breaks']


class CategoryFactory:
    '''
    make lis ofcolors per data itme
    make list of radii per data item

    '''
    default_color = (0,1.0,0) # black
    default_radius = 25
    default_category = 0
    #def __init__(self, inpt={}):
    #    super(CategoryFactory, self).__init__(inpt)
    def getDataCategories(self,_series,model):
        if isinstance(_series, list):
            _series = pd.Series(_series)

        rc = []
        colors = model.getColors()
        radii = model.getRadii()
        breaks = model.getBreaks(_series)

        # catigorize, expect low open endde, upper is open ended
        #  classes                     [c1,  c2,   c3,   c4]
        # four classes create 3 breaks [  b1,   b2,   b3   ]

        category_list=[]
        color_list=[]
        radii_list=[]
        last_pos = len(colors)-1
        for v in _series:  # values

            i = 0
            clr =  colors[last_pos]# set default color
            rad = radii[last_pos] #self.default_radius

            k = len(breaks)
            for b in breaks:

                if v < b:
                    #
                    clr = colors[i] #self['colors'][i]
                    rad = radii[i] #self['radii'][i]

                    k = i
                    break

                i += 1

            color_list.append(clr)#self['color_list'].append(clr)
            radii_list.append(rad)

        return (color_list, radii_list)


def test_CategoryFactory():
    data = [x for x in range(0,8)]
    print('data: ', data)
    visModel = GradientModel(QuantileVisualizationModel())
    category_factory = CategoryFactory()
    cat_data = category_factory.getDataCategories(data,visModel)
    print('data cats: ')
    print('data cats: ',cat_data)

def test_ColorGradient():
    print('############ test_ColorGradient')

    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    colors = GradientModel(VisualizationModel()).getColors() #.gradientColor(pureBlue, pureRed, 6)

    print('colors: ',colors )

def test_gradientRadii():
    print('############ test_gradientRadii')

    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    radii = GradientModel(QuantileVisualizationModel()).getRadii() #.gradientRadii(25,100,4)
    print('radii: ', radii)

def test_getBreaks():
    print('############ test_getBreaks')
    vals = [1,2,3,4,5,6,7,8,9,10]

    gradient = GradientModel(QuantileVisualizationModel())

    gradient.getBreaks(vals)

    print('gradient: ', gradient)

def test_VisualizationModel():
    print('############ test_VisualizationModel')

    visModel = VisualizationModel({'category_count':5})
    print('quart', visModel)

def test_QuantileVisualizationModel():
    print('############ test_QuantileVisualizationModel')

    visModel = QuantileVisualizationModel()
    print('quart', visModel)


def main():
    test_VisualizationModel()
    test_ColorGradient()
    test_gradientRadii()
    test_getBreaks()
    test_QuantileVisualizationModel()
    test_QuantileVisualizationModel()
    test_CategoryFactory()

if __name__ == "__main__":
    # execute only if run as a script
    main()