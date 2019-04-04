import pandas as pd
import matplotlib.pyplot as plt


def to_pie_data(summary):
    '''
    convert a summary to a pie_data
    summary is {'gender': {'F': 620, 'M': 380}}
    pie_data is {'titles':['gender'],'F':[620],'M':[380]}
    '''
    #print(summary)
    _dict = {
        'titles': [t for t in summary]
    }

    labels = [l for t in summary for l in summary[t]]

    for t in summary:
        for l in summary[t]:
            if not l in _dict:
                _dict[l] = [summary[t][l]]

            else:
                _dict[l].append(summary[t][l])
    return _dict, labels

def to_pie_series(summary_list):
    '''
        combines all summaries in list
        pies all have the same final fields i.e., F and M
        pies is {
            'gender': {'F': 71839, 'M': 38687},
            'gender-no-show': {'F': 7183, 'M': 3868}
        }
        pies is [
            {'gender': {'F': 71839, 'M': 38687}},
            {'gender-no-show': {'F': 7183, 'M': 3868}}
        ]
    '''
    _dict = {'titles': []}
    _labels = []
    # merge pies
    for summary in summary_list:
        # print('summary: ', summary)
        for title in summary:
            # print('title: ',title)
            _dict['titles'].append(title)
            for cat in summary[title]:
                if not cat in _dict:
                    # _dict['labels'].append(cat)
                    _labels.append(cat)

                if not cat in _dict:
                    _dict[cat] = [summary[title][cat]]
                else:
                    _dict[cat].append(summary[title][cat])

    return _dict, _labels


def pie(pie_data, labels=[], cells=()):
    '''
      single pie data is {
            'titles': ['gender'],
            'colors': ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue'],
            'F': [620],
            'M': [380]}
      }
      colors is optional


    '''

    slice_labels = []
    # Single Pie
    if len(pie_data['titles']) == 1:
        slice_data = []
        slice_labels = []

        for l in pie_data:
            if not l in ['titles', 'colors']:
                slice_labels.append(l)
                slice_data.append(pie_data[l])
        if len(labels) > 0:
            slice_labels = labels

        title_ = 'Add title to summary'
        title_ = pie_data['titles'][0]
        plt.title(title_)
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cornflowerblue']
        if 'colors' in pie_data:
            colors = pie_data['colors']

        # Plot

        plt.pie(slice_data,
                labels=slice_labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=30)
        plt.axis('equal')
        plt.show()
    elif len(pie_data['titles']) > 1:  # Many Pie
        if len(cells) == 0:
            print('cell is undefined.')
            return

        rows = cells[0]
        cols = cells[1]
        figsize_ = (10, 6)  # this ratio makes circles round rather than ellipic
        if rows > cols and figsize_[0] > figsize_[1]:
            figsize_ = (figsize_[1], figsize_[0])  # adjust aspect

        # fig, axes = plt.subplots(rows, cols, figsize=figsize_)
        # plt.axis('equal')
        fig, axes = plt.subplots(rows, cols)

        df = pd.DataFrame.from_dict(pie_data)

        for i, (idx, row) in enumerate(df.set_index('titles').iterrows()):
            #print('i: ',i, ' idx: ', idx,' row: ', row)

            p_row = i // cols
            p_col = i % cols

            if p_row >= rows:
                break
            if p_col >= cols:
                break
            # if p_row == 0:
            #    p_row = 1
            #if p_col == 0:
            #    p_col = len(pie_data['titles'])
            #print(p_row,p_col)
            ax = axes[p_row, p_col]

            row = row[row.gt(row.sum() * .01)]  # use to get rid of no value columns
            if len(labels) == 0:
                slice_labels = row.index
            else:
                slice_labels = labels

            ax.pie(row, labels=slice_labels, startangle=30)
            ax.set_title(idx)

            ax.set_aspect(
                'equal')  # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.axes.html#matplotlib.pyplot.axes

        fig.subplots_adjust(wspace=.2)
        plt.show()
def pie_data1():
    return {'titles': ['add title'], 'colors': ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'blue'], 0: 56469,
     1: 5784}

def pie_data2():
    return {'titles': ['scholarship'], 'colors': ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'blue'], 0: 56469, 1: 5784}

def test_pie():
    print('################ pie')
    dat = pie_data2()

    pie(dat, labels=['Non-Scholar', 'Scholar'], cells=(2, 2))

def main():
    print('###############################')

    ######################
    # to_pie_data()
    ########
    pie_summary = {'gender': {'F': 620, 'M': 380}}
    pie_test = {'titles': ['gender'], 'F': [620], 'M': [380]}
    _actual, _labels  = to_pie_data(pie_summary)
    assert pie_test ==  _actual


    # convert dict to a datafame
    df = pd.DataFrame.from_dict({
        'Business': 'Beauty & Spas;Burgers-Restaurants;Pizza;Mexican Restaurants;Modern European-Restaurants;Chineese'.split(
            ';'),
        'aniticipation': [0] * 6,
        'enjoyment': [6., 1., 6., 33., 150., 19.5],
        'sad': [1., 2., 1., 3., 13.5, 0.],
        'disgust': [1, 1, 0, 3, 37, 3],
        'anger': [1.5, 2., 4., 9., 19., 3.],
        'surprise': [3, 0, 0, 2, 12, 1],
        'fear': [0, 1, 1, 9, 22, 1],
        'trust': [0] * 6
    })
    '''    
    # funky conversion of lists to dict to dataframe
    df = pd.DataFrame(dict(
            Business='Beauty & Spas;Burgers-Restaurants;Pizza;Mexican Restaurants;Modern European-Restaurants;Chineese'.split(';'),
            aniticipation=[0] * 6,
            enjoyment=[6., 1., 6., 33.,150., 19.5],
            sad=[1., 2., 1., 3., 13.5, 0.],
            disgust=[1, 1, 0, 3, 37, 3],
            anger=[1.5, 2., 4., 9., 19., 3.],
            surprise=[3, 0, 0, 2, 12, 1],
            fear=[0, 1, 1, 9, 22, 1],
            trust=[0] * 6
        ))
    '''
    ########################
    # one at a time
    #########
    pie_summary = {'gender': {'F': 620, 'M': 380}}
    # pie_test = {'titles': ['gender'], 'F': [620], 'M': [380]}
    _actual, _labels = to_pie_data(pie_summary)
    print('pie_data: ', _actual)
    pie(_actual)



    ########################
    # plot series one at a time
    ############


    pie_data_singles = []
    _actual, _labels = to_pie_data({'gender': {'F': 620, 'M': 380}})
    pie_data_singles.append(_actual)

    _actual, _labels = to_pie_data({'gender': {'F': 62, 'M': 38}})
    pie_data_singles.append(_actual)

    for pi in pie_data_singles:
        pie(pi,labels=['Female','Male'])

    #########################
    # plot group
    ########
    summary_list = [
      {'gender': {'F': 6200, 'M': 3800}},
      {'gender': {'F': 620, 'M': 380}},
      {'gender': {'F': 62, 'M': 38}},
      {'gender': {'F': 6, 'M': 3}}
    ]

    test = {
        'titles':['gender','gender','gender','gender'],
        'F':[6200,620,62,6],
        'M':[3800,380,38,3]
    }

    pie_dict,labels = to_pie_series(summary_list)


    print('labels: ', labels)
    print('pie_dict: ', pie_dict)
    print('    test: ', test)


    assert test == pie_dict

    pie(pie_dict,labels=['Female','Male'],cells=(2,2))

    test_pie()


if __name__ == "__main__":
    # execute only if run as a script
    main()

