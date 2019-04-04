import pandas as pd
import numpy as np

class Categorize(dict):
    # base is classifier = {'type':'quartiles', 'breaks': 4, 'colors':colors, 'radii': radii }
    # colors = (1,1,1) if tuple then solid single
    # colors = [(1,1,1),(1,1,1)] if list and size == 2 high and low
    # colors = [(1,1,1),(1,1,1),(1,1,1),...] if list and size > 2 the fixed colors
    # radii = 25 if not list then single
    # radii = [minRadii,maxRadii] if list and size == 2 high and low
    def getColors(self):
        if not 'color_list' in self:
            msg = 'call catigorize before calling getColors()'
            raise AttributeError(msg)

        return self['color_list']
          
    def getRadii(self):
        if not 'radii_list' in self:
            msg = 'call catigorize before calling getRadii()'
            raise AttributeError(msg)

        return self['radii_list']

    def getGradient(self):
        if not 'gradient_list' in self:
            msg = 'call catigorize before calling getGradient()'
            raise AttributeError(msg)

        return self['gradient_list']

    def categorize(self,_serial):

        # apply colors to value_list
        #print(type(_serial))
        if isinstance(_serial,list):
            _serial = pd.Series(_serial)

        if not 'colors' in self:
            self['colors'] = ['b' for i in range(0,4)]
        if not 'radii' in self:
            self['radii'] = [10 for i in range(0,4)]
        if not 'gradient' in self:
            self['gradient'] = [1.0 for i in range(0, len(self['colors']))]

        if not 'color_list' in self:
            self['color_list']=[]
        if not 'radii_list' in self:
            self['radii_list']=[]
        if not 'gradient_list' in self:
            self['gradient_list']=[]

        #print(type(_serial))
        self['radii_list']=[]

        self['color_list']=[]
        self['gradient_list']=[]

        breaks = []
        if self['type'] == 'quantiles':

            breaks = _serial.quantile([0.25, 0.5, 0.75])

        color_list = []
        rad_list = []
        grd_llist = []
        for v in _serial:  # values

            i = 0
            clr = self['colors'][len(self['colors'])-1]
            rad = self['radii'][len(self['radii'])-1]
            grd = self['gradient'][len(self['gradient']) - 1]

            for c in breaks:

                if v < c:
                    #print('v: ', v , ' < ' , c , ' is ', i)
                    clr = self['colors'][i]
                    rad = self['radii'][i]
                    grd = self['gradient'][i]
                    break

                i += 1

            self['radii_list'].append(rad)
            self['color_list'].append(clr)
            self['gradient_list'].append(grd)

        return self

def get_gradient(values, start_gradient=0, end_gradient=1.0):
    sz = len(values)

    step = (end_gradient - start_gradient) / sz
    gradient = np.arange(start_gradient, end_gradient, step)
    return gradient

def test_colorize():
    import pandas as pd
    print('############# condense test')
    vals = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


    gradient = get_gradient(vals,start_gradient=0.1)


    c_dict = {'type':'quantiles','colors':['r', 'g', 'b', 'y'],'gradient':gradient ,'alpha': 1.0 ,'radii':[10 , 25, 75, 100]}
    #c_dict = {'type': 'graduated', 'colors': ['r', 'g', 'b', 'y'],'gradient':gradient, 'alpha': 1.0, 'radii': [10, 25, 75, 100]}

    print('vals: ', vals)

    cat = Categorize(c_dict).categorize(vals)
    color = cat.getColors()
    radii = cat.getRadii()
    gradient = cat.getGradient()

    print('radii: ', radii)
    print('color: ', color)
    print('gradient: ', gradient)

def main():
    test_colorize()

if __name__ == "__main__":
    # execute only if run as a script
    main()