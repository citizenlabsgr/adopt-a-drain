
import matplotlib.pyplot as plt


def deprecate_pie_summary(group, summary, explode=[], labels=[]):
    '''


    :param group: is
    :param summary:
    :param explode:
    :param labels:
    :return:
    '''
    if len(labels) == 0:
        labels = [cat for cat in summary[group]]

    sizes = [summary[group][cat] for cat in summary[group]]

    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'cornflowerblue']

    if len(explode) == 0:
        explode = lst = [0] * len(sizes)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()


def show_histogram(graph, f_list):
    '''
    show histogram for a city
    city is the target city
    graph contain configuration setting for a histogram
    group is a filter designation to limit the categories shown

    _graph = {

        'title': 'Trip Durations in {}'.format(chosen_city),
        'x_label':'Duration (minutes)',
        'y_label':'Trips',
        'bins': int(75/5), # five minute wid intervals
        'range': (0.0, 75.0), # limit to trip of 75 minutes or less
        'facecolor':'blue',
        'alpha': 0.5

    }
    '''

    bins_ = 'auto'
    alpha_ = 1.0
    range_ = None
    facecolor_ = 'Blue'

    if 'bins' in graph:
        bins_ = graph['bins']
    if 'range' in graph:
        range_ = graph['range']
    if 'facecolor' in graph:
        facecolor_ = graph['facecolor']

    if 'alpha' in graph:
        alpha_ = graph['alpha']
    if 'facecolor' in graph:
        facecolor_ = graph['facecolor']
    if 'bin_labels' in graph:
        fig, ax = plt.subplots()
        ax.set_xticklabels(graph['bin_labels'])

        for tick in ax.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("left")

    # n, bins, patches = plt.hist(f_list, bins_, range = range_,
    #                            facecolor=facecolor_, alpha=alpha_)
    n, bins, patches = plt.hist(f_list, bins_,
                                facecolor=facecolor_,
                                range=range_,
                                alpha=alpha_)

    if 'title' in graph:
        plt.title(graph['title'])
    if 'x_label' in graph:
        plt.xlabel(graph['x_label'])
    if 'y_lable' in graph:
        plt.ylabel(graph['y_label'])

    plt.show()

    return patches


def show_line_plot_many(data_many, graph):
    # def show_line_plot_many(city, data_many, graph):
    '''
    plot a multi-line line graph
    city is a city name
    data_many contains lines for total,...
    data_many is list of lists
    data_many is [[],[],...]
    graph is {
        'title':'Ridership Totals by hour of the day (2016)',
        'x_label': 'hour of day',
        'y_label': 'total trips (2016)',
    }
    '''
    ########

    ########
    # plt.figure(num=None, figsize=(25,25),dpi=80, facecolor='w', edgecolor='k')

    if 'title' in graph:
        plt.title(graph['title'])
    if 'x_label' in graph:
        plt.xlabel(graph['x_label'])
    if 'y_label' in graph:
        plt.ylabel(graph['y_label'])
    if 'range' in graph:
        plt.range = graph['range']
        print('set range')
    for d in data_many:
        if 'label' in d:
            legend_label = d['label']
            plt.plot(d['domain'], d['range'], label=legend_label)

        else:
            plt.plot(d['domain'], d['range'])

    hm = max(data_many[0]['domain']) * 0.05

    vm = max(data_many[0]['range']) * 0.05

    plt.axis([0 - hm, max(data_many[0]['domain']) + hm, 0 - vm, max(data_many[0]['range']) + vm])

    plt.legend()

    plt.show()

def main():
    _graph = {
        'anchor': 'g_ridership_by_hour',
        'title': 'Ridership by hour of the Day \n(2016)',
        'x_label': 'hour of day',
        'y_label': 'total trips',
        'sizes': [10, 10, 10, 10],

        'ymaxima': []
    }
    data = []
    _domain = [1,2,3,4]
    _range = [10,11,13,14]
    _domain = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28 ]

    _range = [1312, 1635, 1424, 571, 1349, 1536, 1452, 1545, 1521, 1403, 1376, 1448, 1530, 1211 ]

    #_domain = [62, 56, 8, 76, 23, 39, 21, 19, 30, 29, 22, 28, 54, 15, 50, 40, 46, 4, 13, 65, 45, 51, 32, 12, 61, 38, 79, 18, 63, 64, 85, 59, 55, 71, 49, 78, 31, 58, 27, 6, 2, 11, 7, 0, 3, 1, 69, 68, 60, 67, 36, 10, 35, 20, 26, 34, 33, 16, 42, 5, 47, 17, 41, 44, 37, 24, 66, 77, 81, 70, 53, 75, 73, 52, 74, 43, 89, 57, 14, 9, 48, 83, 72, 25, 80, 87, 88, 84, 82, 90, 94, 86, 91, 98, 92, 96, 93, 95, 97, 102, 115, 100, 99, -1]
    #_range = [1312, 1635, 1424, 571, 1349, 1536, 1452, 1545, 1521, 1403, 1376, 1448, 1530, 1211, 1613, 1402, 1460, 1299, 1103, 1101, 1453, 1567, 1505, 1092, 1343, 1629, 390, 1487, 1374, 1331, 275, 1624, 1425, 695, 1652, 541, 1439, 1469, 1377, 1521, 1618, 1195, 1427, 3539, 1513, 2273, 832, 1012, 1411, 973, 1580, 1274, 1378, 1437, 1283, 1526, 1524, 1402, 1272, 1489, 1394, 1509, 1346, 1487, 1533, 1242, 1187, 527, 434, 724, 1651, 544, 725, 1746, 602, 1344, 173, 1603, 1118,]

    data.append({'label': 'Customer', 'domain': _domain, 'range': _range})
    #  data.append({'label': 'Customer', 'domain': _hours, 'range': _counts}]

    show_line_plot_many( data, _graph)


if __name__ == "__main__":
    # execute only if run as a script
    main()