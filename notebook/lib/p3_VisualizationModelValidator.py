from pprint import pprint
class VisualizationModelValidatorUtilities:

    def get_category_colors(self,category, visualization):
        idx = visualization['categories'].index(category)
        return visualization['color_grade'][idx]

    def get_category_radii(self,category, visualization):
        idx = visualization['categories'].index(category)
        return visualization['radii_grade'][idx]

    def get_category_symbols(self,category, visualization):
        idx = visualization['categories'].index(category)
        return


class VisualizationModelValidator(dict):
    '''
    classifier_ =  {'type':'quantiles', 'category_count': 4, 'color_grades':[(.9,.9,.9),(0,0,1.0)], 'radii_grades': [25,300] }

    '''

    def __init__(self, inpt={}):
        super(VisualizationModelValidator, self).__init__(inpt)
        # set up quartile as default
        if not 'type' in self:
            self['type'] = 'quantiles'
        if not 'categories' in self:
            msg = "Visualization is missing 'categories' key and values."
            raise AttributeError(msg)
        if not 'x_name' in self:
            msg = "Visualization is missing 'x_name' key and value."
            raise AttributeError(msg)
        if not 'y_name' in self:
            msg = "Visualization is missing 'y_name' key and value."
            raise AttributeError(msg)

        if not 'category_count' in self:
            self['category_count'] = len(self['categories'])
        if not 'color_grade' in self:
            self['color_grade'] = [(.7, .7, .7), (0, 0, 1.0)]  # ltgrey to blue
        if not 'radii_grades' in self:
            self['radii_grades'] = [25, 300]  # low to high
        if not 'breaks' in self:
            self['breaks'] = []
        if not 'categories' in self:
            self['categories'] = len()
        if not 'title' in self:
            self['title'] = "Add 'title' to visualization model."
        if not 'legend_overide' in self:
            self['legend_overide'] = False

    #def getXName():
    #    return self['x_name']

    #def getYName():
    #    return self['y_name']

    #def getCategories(self):
    #    return get

    #def getColors(self, colorHigh=None, colorLow=None):
    #    return []

    #def getRadii(self, minRadius=None, maxRadius=None):
    #    return []

    #def getBreaks(self, _series):
    #    return []

def test_VisualizationModelValidator():
    my_vis = {
        'title': 'Most Common Neighbourhood Malady',
        'type': 'category',
        'categories': ['hipertension', 'diabetes', 'alcoholism', 'handcap'],
        'x_name': 'lon',
        'y_name': 'lat',
        'color_grade': ['b', 'orange', 'g', 'r'],
        'radii_grade': [25, 25, 25, 25],
        'symbols': ['o', 'v', 's', 'h'],
        'legend_overide': True

    }

    my_vis = VisualizationModelValidator(my_vis)
    pprint(my_vis)



def main():
    test_VisualizationModelValidator()


if __name__ == "__main__":
    # execute only if run as a script
    main()