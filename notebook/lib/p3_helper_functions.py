# convenience functions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

from lib.p3_Chart import Chart
import lib.p3_bars as bars
import lib.p3_basic_summary as summary

import lib.p3_peaks as peaks
from lib.p3_Categorize import Categorize
#from lib.p3_clean import as clean
import lib.p3_clean as clean
from lib.p3_VisualizationModelValidator import VisualizationModelValidator,VisualizationModelValidatorUtilities
from lib.p3_Labels import Labels, get_feature_labels
import lib.p3_pie as piie
from lib.p3_ProcessLogger import ProcessLogger
from lib.p3_Filter import DF_Filter
from lib.p3_Categorize import Categorize

from lib.p3_VisualizationModelValidator import VisualizationModelValidator,VisualizationModelValidatorUtilities
from lib.p3_Visualization import QuantileVisualizationModel
from lib.p3_Visualization import GradientModel
from lib.p3_Visualization import CategoryFactory
from lib.p3_Filter import DF_Filter
import json

def get_configuration(filename='p3_configuration.json'):
    return json.load(open(filename))

def reference(log):
    log.clear()
    log.collect('# References:')
    conf = get_configuration()['references']
    #for ref in conf:
    #    print(config[ref])

    for ref in conf:
        #    print(ref)

        _type = conf[ref]['type']

        title = conf[ref]['title']
        provider = conf[ref]['provider']

        period = conf[ref]['period']
        #print('type: ',_type)
        if _type == 'data':
            website = conf[ref]['website']
            url = conf[ref]['url']
            log.collect('* "**{}**"; provider: [{}]({}); period: {}; data: {}'\
                .format(title, provider,website, period,url))
        if _type == 'website':
            website = conf[ref]['website']
            log.collect('* "**{}**"; provider: [{}]({}); period: {}'\
                .format(title, provider,website, period))



def graph_stats(df, _col):
    day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    _mean = df[_col].mean()
    _std = df[_col].std()
    _day = day_of_week[round(_mean) - 1]
    return _mean, _std, _day


def show_stats(df, _col):
    _mean, _std, _day = graph_stats(df, _col)

    print('* **{}** is the most favored day to schedule an appointment'.format(_day))
    print('* Center: The mean ({:0.5f}), standard deviation is {:0.5f}' \
          .format(_mean, _std))

    print('| Center Mean |  {:0.3f} | {:0.3f} | {:0.3f} |'.format())
    print('| Center  STD|  {:0.3f} |  {:0.3f} | {:0.3f} |'.format())


def open_data(appt_final_file_name, patient_final_file_name, neighbourhood_final_file_name, neighbourhood_first_visits_final_file_name, cell_log):
    cell_log.collect('<a id="open_condensed_data"></a>')
    cell_log.collect('# Open Condensed Data')
    #--------------------------------- Load appointments
    #_transform = condense_transforms.best_transform(df_source,hint='appt')
    cell_log.collect('* Open condensed appointment data from {}'.format(appt_final_file_name))
    df_appt = pd.read_csv(appt_final_file_name)
    #df_appt.info()
    #--------------------------------- Load patients
    #_transform = condense_transforms.best_transform(df_temp,hint='patient2')
    cell_log.collect('* Open condensed patient data from {}'.format(patient_final_file_name))
    df_patient = pd.read_csv(patient_final_file_name)
    #df_patient.info()

    #df_patient, convert_summary = clean.change_types(_convert_patient_types, df_patient)
    cell_log.collect('* Open condensed neighbourhood data from {}'.format(neighbourhood_final_file_name))
    df_neighbourhood = pd.read_csv(neighbourhood_final_file_name)
    #df_neighbourhood.info()

    cell_log.collect('* Load condensed neighbourhood first visit data from {}'\
        .format(neighbourhood_first_visits_final_file_name))
    df_neighbourhood_visit_1 = pd.read_csv(neighbourhood_first_visits_final_file_name)

    return df_appt,df_patient,df_neighbourhood,df_neighbourhood_visit_1



def add_hist_plot(plt, x, bins=None, xylabels=['xlbl_name', 'frequency'], legend_label='labelme', grid=True):
    '''
    add a histogram layer to a plot
    '''
    # plt.figure( figsize=(10,3))
    plt.plot(kind='hist')

    plt.hist(x, bins, alpha=0.5, label=legend_label)
    # plt.figure( figsize=(10,3))
    plt.grid(True)

def get_colors():
    '''
    return a common set of colors for general use

    '''
    return ['yellowgreen', 'lightcoral',
               'lightskyblue', 'palevioletred',
               'cornflowerblue',
               'lightpink',
               'deepskyblue', 'darkseagreen']
def get_color(search_no):
    '''
    return a color for a given index. if index exceeds the number of color then start over

    '''
    colors_ = get_colors()
    find_no = search_no
    while find_no >= len(colors_):  # start over
        find_no -= len(colors_)

    return colors_[find_no]

def test_get_color():
    '''
      test color array wrap around
    '''
    for c in range(0,25):
        print(' color: ',get_color(c))
    assert get_color(8) == 'yellow'


def start_scatter_plot(plt, x, y, legend_label,
                       title='title me',xylabels=['xlbl', 'ylbl'],
                       color=('blue',1.0),
                       sizes=None
                       ,figsize=None):

    '''

    organizies the parameters for creating a scatter plot
    :param plt:
    :param x:
    :param y:
    :param legend_label:
    :param title:
    :param xylabels:
    :param color:
    :param sizes:
    :param figsize:
    :return:
    '''
    if not isinstance(color,tuple):
        msg = 'expected {} to be a tuple ([\'r\',\'g\',...],1.0)'.format(color)
        raise TypeError(msg)
    ''' title ea scatter plot layer to plot'''

    plt.xlabel(xylabels[0])
    plt.ylabel(xylabels[1])
    plt.title(title)

    plt.scatter(x,
                y,
                #label=legend_label,
                c=color[0],
                alpha=color[1],
                s=sizes
                );
    # plt.legend().get_texts()[0].set_text('make it short')



def add_scatter_plot(plt, x, y,legend_label , color=('black',1.0) ):
    '''
    add a second scatter plot on top of previous
    :param plt:
    :param x:
    :param y:
    :param legend_label:
    :param color:
    :return:
    '''
    ''' add a scatter plot layer to plot'''
    #plt.xlabel(xylabels[0])
    #plt.ylabel(xylabels[1])

    #color = interpret_color(x,color)

    plt.scatter(x, y, label=legend_label,color=color[0],alpha=color[1]);

    #plt.figure(figsize=figsize)
    #plt.figure(figsize=figsize)

def end_plot(plt,title='title'):
    '''
    end a series of sctter plot calls
    :param plt:
    :param title:
    :return:
    '''
    #plt.figure(figsize=(3, 3))
    plt.show()
    plt.gcf().clear()


def add_fit_line(plt,dom,rng, x, y, color=('black',1.0),label='label'):
    '''
    calulate a line and plot it
    '''
    try:
        color[1]
    except IndexError:
        msg = 'color is a tuple format = (\'<color_name>\',<alpha-value>)'
        raise AttributeError(msg)

    fit_summary = fit_linear(dom, rng, x, y)

    # b, m = best_fit(x, y)
    b = fit_summary['intercept']
    m = fit_summary['slope']
    yfit = [b + m * xi for xi in x]

    plt.plot(x, yfit, color=color[0],alpha=color[1],label=label);


#def deprection_get_fit_line_eq(dom,x, rng,y):

    # return the description of a line


    #b, m = best_fit(x, y)
    #eq = 'y = {}x + {}'.format(m,b)

    #desc = slope_interpretation(dom, rng, m)


    #return eq,desc

def graph_scatter_layers(df_layers,
                         dom,
                         rng,
                         layer_name=[],
                         layer_colors=[(.7, 0.7, 0.7)],
                         title="Add Title",
                         figsize=(15,5),
                         legend_label='Set legend_label'
                         ):
    '''
    take list of scatter plot definitions an plot them
    :param df_layers:
    :param dom:
    :param rng:
    :param layer_name:
    :param layer_colors:
    :param title:
    :param figsize:
    :return:
    '''
    # all
    bcolor = 'grey'
    if figsize != None:
        plt.figure(figsize=figsize);
    i = 0
    for lyr in df_layers:
        if i == 0:
            data = None
            if isinstance(lyr,dict):
                data = lyr['df']
            else:
                data = lyr

            start_scatter_plot(plt, data[dom], data[rng], \
                                      title=title, legend_label=legend_label, \
                                      xylabels=[dom, rng], color=(layer_colors[i], 0.5)

                               )

            add_fit_line(plt, dom,rng, data[dom], data[rng], color=('r', 1.0))

        else:

            no_show_color = 'darkmagenta'
            data = None
            if isinstance(lyr,dict):
                data = lyr['df']
            else:
                data = lyr

            add_scatter_plot(plt,
                                    data[dom],
                                    data[rng],
                                    legend_label='no-show',
                                    color=(layer_colors[i], 1.0))
            # fit line to second layer
            add_fit_line(plt, dom,rng,
                                data[dom],
                                data[rng],
                                color=(layer_colors[i], 1.0))
            #print('graph_scatter_layers B color: ', layer_colors[i])

        i += 1

    plt.legend();
    end_plot(plt)


def test_scatter_layers():
    '''TEST code '''
    print('############## test_scatter_layers')
    df = pd.DataFrame()
    df['x'] = [1,2,3,4,5,6,7,8,9]
    df['y'] = [9,8,7,6,5,4,3,2,1]
    #z = [12,35,60,75,96]
    #s = [40,5,60,7,80]

    df_layers = [
        df.query('x<5'),
        df.query('x>=5')
    ]


    layer_colors = ['grey'] + get_colors()

    graph_scatter_layers(df_layers, 'x', 'y', layer_colors=layer_colors)

    #eq, desc = get_fit_line_eq('x',df['x'], 'y',df['y'])

    #print('linear equation: ', eq )
    #print('description: ', desc)


def test_scatter():
    '''TEST code '''
    print('############ test_scatter')
    x = [1,2,3,4,5]
    y = [5,4,3,2,1]

    #colors = (['g','g','b','b','r'],0.5)
    colors = {'type': 'quartiles', 'color': ['r', 'g', 'b', 'y']}

    start_scatter_plot(plt,
                       x,
                       y,
                       'one',
                       color=(colors,0.5),
                       title='Example Scatter A')

    add_fit_line(plt, x, y, color=('g',0.5))

    y = [1, 2, 3, 4, 5]
    x = [1, 2, 3, 4, 5]


    plt.legend()

    end_plot(plt)


def test_scatter_colors():
    '''TEST code '''
    print('############## test_scatter_colors')
    x = [1,2,3,4,5]
    y = [5,4,3,2,1]
    z = [12,35,60,75,96]
    s = [40,5,60,7,80]
    alpha = [1.0, 1.0, 1.0, 1.0]
    alpha = 1.0
    # ('grey', 0.5) singleton
    # ([], 0.5 )
    # ( {'type': 'quartiles', 'color': ['r', 'g', 'b', 'y']} )


    classifier = {'type':'quartiles','colors':['snow1', 'snow2', 'snow3', 'snow4'], 'alpha': alpha,'radii':[25, 50, 75, 100] }
    classifier = {'type': 'quartiles', 'colors': ['r', 'g', 'b', 'grey'], 'alpha': alpha,
                  'radii': [25, 50, 100, 200]}

    categories = Categorize(classifier).categorize(z)
    g = categories.getGradient()
    c = categories.getColors()
    radii = categories.getRadii()
    ct = (c,1.0)
    start_scatter_plot(plt,
                       x,
                       y,
                       'one',
                       color = ct,
                       title='Example Scatter B',
                        sizes = radii
                       )

    print('figsize: ',plt.rcParams["figure.figsize"])
    '''
    add_fit_line(plt, x, y, color=('g',0.5))


    #y = [1, 2, 3, 4, 5]
    #x = [1, 2, 3, 4, 5]


    plt.legend()
    '''
    #plt.figure(figsize=(3, 3))
    end_plot(plt)



def test_scatter_sizes():
    '''TEST code '''
    print('############## test_scatter_sizes')
    x = [1,2,3,4,5]
    y = [5,4,3,2,1]
    z = [12,35,60,75,96]
    s = [40,5,60,7,80]
    # ('grey', 0.5) singleton
    # ([], 0.5 )
    # ( {'type': 'quartiles', 'color': ['r', 'g', 'b', 'y']} )
    classifier = {'type': 'quartiles', 'color': ['r', 'g', 'b', 'y']}

    start_scatter_plot(plt,x,y,z,'one',
                       color=(classifier,0.5),
                       title='Example Scatter B',
                       sizes=s
                       )

    print('figsize: ',plt.rcParams["figure.figsize"])
    '''
    add_fit_line(plt, x, y, color=('g',0.5))


    #y = [1, 2, 3, 4, 5]
    #x = [1, 2, 3, 4, 5]


    plt.legend()
    '''
    #plt.figure(figsize=(3, 3))
    end_plot(plt)


def get_hist(df, config_dic, legend=False, bins=10, figsize=(6, 4)):
    '''
    attempts drawing a histogram from the col
    config_dic is {'col':'','title':'add title','xlabel':'add lab'}
    '''
    feature = config_dic['feature']
    title = config_dic['title']
    xlabel = config_dic['xlabel']

    df[[feature]].plot(title=title, kind='hist', legend=legend, bins=bins, figsize=figsize) \
        .set_xlabel(xlabel);
    plt.figure(figsize=figsize);
    plt.show()


def get_attendance_summary(df_patient, labels):
    '''
    sums the patient shows and no_shows
    returns {'no_shows':<value>,'shows':<value>}
    '''
    feature = 'no_shows'
    df1 = df_patient.groupby(feature).count()
    lst = df1['patient_id']
    tmp_list = [x for x in lst]
    no_shows = sum(tmp_list[1:])
    shows = tmp_list[0]

    return {labels['attendance'][0]: no_shows, labels['attendance'][1]: shows}


def show_stacked_bar_chart(summary_query, config={'title':'add title','xlabel':'xlabel','ylabel':'ylabel'}):
    '''
    display a stacked bar chart based on a summary data structure

    :param summary_query:
    :param config:
    :return:
    '''
    title = config['title']
    xlabel = config['xlabel']
    ylabel = config['ylabel']

    layers = summary_query.get_stacked_layers()

    domain_labels = summary_query.get_features_as_labels()

    patient_chart= Chart(title,layers)\
        .setXLabel(xlabel)\
        .setYLabel(ylabel)\
        .setFigSize((10,5))\
        .setDomainLabels(domain_labels)\
        .setBboxToAnchor((1.15,1.0)) # \


    bars.stacked_bar(patient_chart.toDict())



def get_appt_summaries(df_appt):#,summary):
    '''
       calculate apppointment counts
    '''
    appt_summary_config = {'context': 'appointments',  # what does row represent
                           'fields': [
                               {'field': 'attendance', 'sort': 'domain', 'function': 'kind-count'},
                               # count for all gender types
                               {'field': 'scheduled_day_of_week', 'function': 'kind-count'},
                               # count for all scholarship types
                               {'field': 'scheduled_hour', 'sort': 'domain', 'function': 'kind-count'},
                               # count for all age types

                               # {'field': 'scheduled_hour','sort':'domain', 'function': 'kind-count'},
                               # {'field': 'scheduled_time','sort':'domain', 'function': 'kind-count'},
                               # {'field': 'age', 'sort':'domain','function': 'kind-count'},
                               {'field': 'no_show', 'sort': 'domain', 'function': 'kind-count'},
                               # {'field': 'no_show', 'sort':'domain','function': 'sum'},

                           ]}

    print('* summerizing all appointments... please wait')
    appt_summary = \
        summary.get_basic_summary(df_appt,appt_summary_config)

    print('* summerizing appointment no_shows... please wait')
    df_appt_no_shows = df_appt.query('no_show == 1')

    appt_no_show_summary = \
        summary.get_basic_summary(df_appt_no_shows,appt_summary_config)
    print('* summerizing appointment show ups... please wait')
    df_appt_show_ups = df_appt.query('no_show == 0')

    appt_show_up_summary = \
        summary.get_basic_summary(df_appt_show_ups,appt_summary_config)
    #print('* Done')
    return appt_summary, appt_no_show_summary, appt_show_up_summary


def get_patient_summaries(df_patient): #,summary):
    '''
    calculate patient counts
    '''
    patient_summary_config = {
        'context': 'patients',  # what does row represent
        'fields': [

            {'field': 'appointments', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'appointment_group', 'sort': 'domain', 'function': 'kind-count'},

            {'field': 'no_shows', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'scholarship', 'sort': 'domain', 'function': 'kind-count'},

            {'field': 'hipertension', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'diabetes', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'alcoholism', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'handcap', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'gender', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'age', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'age_group', 'sort': 'domain', 'function': 'kind-count'},
            {'field': 'skipper', 'function': 'high-value'},
        ]
    }
    # Calculate the summaryies
    print('* summarizing all patients... please wait')
    patient_summary = summary.get_basic_summary(df_patient, patient_summary_config)
    # query the no_shows
    df_patient_no_shows = df_patient.query('skipper == 1')
    # summerize the no show
    print('* summarizing no-show patients... please wait')

    patient_no_show_summary = summary.get_basic_summary(df_patient_no_shows, patient_summary_config)
    # print('patient summary done')
    print('* summarizing show-up patients... please wait')

    df_patient_show_ups = df_patient.query('skipper == 0')
    patient_show_up_summary = summary.get_basic_summary(df_patient_show_ups, patient_summary_config)
    #print('* Done')
    return patient_summary, patient_no_show_summary, patient_show_up_summary



def get_neighbourhood_summaries(df_neighbourhood):#,summary):
    '''
       calculate apppointment counts
    '''
    neighbourhood_summary_config = {'context': 'neighbourhood',  # what does row represent
                           'fields': [
                               {'field': 'appointments', 'sort': 'domain', 'function': 'kind-count'},
                               {'field': 'shows', 'sort': 'domain', 'function': 'kind-count'},
                               {'field': 'no_shows', 'sort': 'domain', 'function': 'kind-count'},
                               {'field': 'lon', 'sort': 'domain', 'function': None},
                               {'field': 'lat', 'sort': 'domain', 'function': None},
                           ]}

    print('* summerizing all neighbourhood... please wait')
    neighbourhood_summary = \
        summary.get_basic_summary(df_neighbourhood,neighbourhood_summary_config)

    #print('* summerizing neighbourhood no_shows... please wait')
    #df_neighbourhood_no_shows = df_neighbourhood.query('no_show == 1')
    neighbourhood_no_show_summary={}
    #neighbourhood_no_show_summary = \
    #    summary.get_basic_summary(df_appt_no_shows,neighbourhood_summary_config)
    #print('* summerizing neighbourhood show ups... please wait')
    #df_neighbourhood_show_ups = df_neighbourhood.query('no_show == 0')
    neighbourhood_show_up_summary = {}
    #neighbourhood_show_up_summary = \
    #    summary.get_basic_summary(df_neighbourhood_show_ups,neighbourhood_summary_config)

    return neighbourhood_summary, neighbourhood_no_show_summary, neighbourhood_show_up_summary




def get_favorites(df,feature_name,feature_labels):
    '''

    :param df:
    :param feature_name:
    :param feature_labels:
    :return:
    '''
    df1 = df.groupby([feature_name]).count()
    lst = df1['appointment_id']
    tmp_list =[x for x in lst]
    maxima = peaks.get_maxima_large(tmp_list)
    if sum(maxima) <= 1:
        large = max(tmp_list)
        maxima = [x == large for x in tmp_list ]
    best = [feature_labels[x] for x in range(0,len(maxima)) if maxima[x]]
    return best

def open_source_data(sources,transforms, process_logger=None):
    '''
    open all data from a list of sources
    sources is [
        {'transform':'appt_transform','type_conversion': convert_appt_types},
        {'transform':'patient2_transform','type_conversion': convert_patient_types},
        {'transform':'neighbourhood1_transform','type_conversion': convert_neighbourhood_types},
    ]
    '''
    if process_logger == None:
        process_logger = ProcessLogger()
    data = []
    #transforms = Transforms(get_raw_transforms_json('conf.raw.transforms.json'))  # categroies, tranform, file_names
    i = 0
    for source in sources:

        trans = transforms.getTransforms()[source['transform']]
        type_conversion = source['type_conversion']
        final_file_name = trans['out_file_name']

        process_logger.collect('* Open and Load condensed data from {}'.format(final_file_name))

        df = pd.read_csv(final_file_name)

        if source['type_conversion'] != None:
            process_logger.collect('* Opent and Convert types from {}'.format( final_file_name))

            df, convert_summary = clean.change_types(source['type_conversion'], df)
        data.append(df)
        i += 1
    return data


def neighbourhood_counts(df_patient):
    '''
    determine which neighbourhood has the most patients
    :param df_patient:
    :return:
    '''
    cols = ['appointments', 'no_show_rate', 'hipertension', 'diabetes', 'alcoholism', 'handcap']

    q_str_one_plus_mal = 'hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0'
    q_str_no_mal = 'hipertension == 0 and diabetes==0 and alcoholism == 0 and handcap == 0'

    # patient_count = len(df_patient)
    df_local = df_patient
    col_nm = 'neighbourhood'
    df_groupby = df_local.groupby(col_nm)[col_nm].count()
    df_sort = df_groupby.sort_values(ascending=False)

    dmn = range(len(df_sort))
    domain_labels = list(
        df_sort.keys())  # ['ssssssssssssssssssssssssss','vvvvvvvvvvvvvvvvvvvvvvv','fffffffffffffffffffffff']

    rnge = df_sort.values
    plt.figure(figsize=(15, 4));
    plt.bar(dmn, rnge, align='center')
    plt.xticks(dmn, domain_labels, rotation=90)
    plt.grid(True)
    plt.ylabel('patients')
    plt.xlabel('neighbourhood')
    plt.title('Patients by Neigbhourhood')
    # plt.plot()
    plt.show()
    mx = max(df_sort.values)
    idx = list(df_sort.values).index(mx)
    name = domain_labels[idx]
    print('* **{} has the most patients **'.format(name))
    print('* {} patients in JARDIM CAMBURI'.format(mx, name))


def map_neighbourhood_scatter(df_neighbourhood, zed='appointments', filter=None):
    x_name = 'lon'
    y_name = 'lat'
    z_name = zed

    context = 'Vitória, Brazil Neighbourhood'
    filter_str = ''
    # Extract the data we're interested in
    if filter == None:
        df_0 = df_neighbourhood  # .query('lon <-38.0')
    else:
        filter_str = filter.getFilter()
        df_0 = df_neighbourhood.query(filter_str)

    lat = df_0['lat']
    lon = df_0['lon']

    df_z0 = df_0[z_name]

    # Scatter the points, using size and color but no label

    vis_model_z0 = GradientModel(QuantileVisualizationModel({'category_count': 4}))

    category_factory = CategoryFactory()
    vis_package = category_factory.getDataCategories(df_z0, vis_model_z0)

    color_pos = 0
    radii_pos = 1
    color = vis_package[color_pos]
    sizes = vis_package[radii_pos]

    plt.figure(figsize=(8, 8))
    # NW

    plt.plot([-40.34, -40.34, -40.33, -40.33, -40.34], [-20.29, -20.27, -20.27, -20.29, -20.29])
    # SW (-40.36, -20.33) and (-40.34, -20.31)
    plt.plot([-40.36, -40.36, -40.34, -40.34, -40.36], [-20.33, -20.31, -20.31, -20.33, -20.33])
    # SE  (-40.33, -20.32) and (-40.29, -20.295)
    plt.plot([-40.33, -40.33, -40.29, -40.29, -40.33], [-20.32, -20.295, -20.295, -20.32, -20.32])
    #plt.plot(-40.34, -20.29, 'b', label='NW')
    #plt.legend(loc=2)

    plt.scatter(lon, lat, label=None,
                c=color,
                s=sizes, linewidth=0, alpha=0.75)


    plt.axis(aspect='equal')
    plt.xlabel('longitude')
    plt.ylabel('latitude')

    # plt.colorbar(label='log$_{10}$(population)')
    plt.clim(3, 7)

    # Here we create a legend:
    # we'll plot empty lists with the desired size and label
    break_z0 = vis_model_z0.getBreaks(df_z0)
    break_z0_labels = vis_model_z0.getLegendLabels(break_z0)

    i = 0

    for area in vis_model_z0.getRadii():  # sizes: #[100, 300, 500]:
        plt.scatter([], [], c='k', alpha=0.3, s=area,
                    label=break_z0_labels[i])
        i += 1

    plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title=z_name.replace('_', ' ').title())

    plt.title('{} {}'.format(context, z_name.replace('_', ' ').title() + '\n' + filter_str));


def map_neighbourhood_appointments(df_neighbourhood):
    '''
    show map of neighbourhood appointments
    :param df_neighbourhood:
    :return:
    '''
    from lib.p3_Visualization import QuantileVisualizationModel
    from lib.p3_Visualization import GradientModel
    from lib.p3_Visualization import CategoryFactory
    dom = 'lon'
    rng = 'lat'
    zed = 'appointments'
    value_col = 'no_shows'

    df_0 = df_neighbourhood.query('lon <-38.0')
    vis_model = GradientModel(QuantileVisualizationModel())
    category_factory = CategoryFactory()
    vis_package = category_factory.getDataCategories(df_0[zed],vis_model)

    plt.figure(figsize=(10,10));

    plt.grid(True)

    color_pos = 0
    radii_pos = 1
    start_scatter_plot(plt, df_0[dom], df_0[rng],\
                              title='Appointments by Neighbourhoods',\
                              legend_label='appointments', \
                              xylabels=[ dom, rng],\
                              color=(vis_package[color_pos],1.0),
                              sizes=vis_package[radii_pos])
    plt.legend()


def map_passive(df_0, visualizationModel):
    '''
    this funciton is passive and displays symbols given it
    df_neigbourhood is encoded with lat,lon,symbol,color,size
    '''
    dom = visualizationModel['x_name']  # 'lon'
    rng = visualizationModel['y_name']  # 'lat'

    # value_col = 'no_shows'

    plt.figure(figsize=(10, 10));

    plt.grid(True)
    colors = df_0['color']
    radii = df_0['radii']
    #legend_label is meaningless
    start_scatter_plot(plt, df_0[dom], df_0[rng], \
                              title=visualizationModel['title'], \
                              legend_label='appointments', \
                              xylabels=[dom, rng], \
                              color=(colors, 1.0),
                              sizes=radii)
    import matplotlib.patches as mpatches

    if visualizationModel['legend_overide']:
        patches = []
        for category in visualizationModel['categories']:
            idx = visualizationModel['categories'].index(category)
            clr = visualizationModel['color_grade'][idx]
            lbl = visualizationModel['categories'][idx]
            patches.append(mpatches.Patch(color=clr, label=lbl))
        plt.legend(handles=patches)
    else:
        plt.legend()


def graph_Most_Common_Neighbourhood_Malady(df_patient):
    '''
    displays the most common neighbourhoood malady in graph form
    :param df_patient:
    :return:
    '''

    df_local = df_patient

    cols = ['hipertension', 'diabetes', 'alcoholism', 'handcap']

    q_str_one_plus_mal = 'hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0'
    q_str_no_mal = 'hipertension == 0 and diabetes==0 and alcoholism == 0 and handcap == 0'

    # individual
    # df_local = df_patient  #.query(q_str_one_plus_mal)


    df_sum = df_local[cols].mean()

    df_groupby = df_local.groupby(['neighbourhood'])[cols].mean()

    df_groupby.plot(kind='bar', figsize=(15, 10), subplots=True);


def map_Most_Common_Neighbourhood_Malady(df_neighbourhood, df_patient):
    '''
    display map of most common neighbourhood malady
    :param df_neighbourhood:
    :param df_patient:
    :return:
    '''
    df_local = df_neighbourhood
    cols = ['hipertension', 'diabetes', 'alcoholism', 'handcap']
    q_str_one_plus_mal = 'hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0'
    q_str_no_mal = 'hipertension == 0 and diabetes==0 and alcoholism == 0 and handcap == 0'

    ########
    df_groupby = df_patient.groupby(['neighbourhood'])[cols].mean()
    # print('df_groupby: ', len(df_groupby))
    # print('df_neighbourhood: ', len(df_neighbourhood))

    max_mal = df_groupby.idxmax(axis=1)  # find most common from neighbourhood
    # print('max_mal: ', len(max_mal))
    df_local['common_malady'] = list(max_mal)

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
    my_utils = VisualizationModelValidatorUtilities()

    #######
    df_local['color'] = [my_utils.get_category_colors(cat, my_vis) for cat in max_mal]
    df_local['radii'] = [my_utils.get_category_radii(cat, my_vis) for cat in max_mal]
    df_local['symbol'] = [my_utils.get_category_symbols(cat, my_vis) for cat in max_mal]

    df_local = df_neighbourhood.sort_values('neighbourhood')
    df_0 = df_local.query('lon <-38.0')
    map_passive(df_0, my_vis)


def graph_Scheduled_Day_of_Week(df_appt,title='title'):
    '''
    display scheduled days of the week as layered histograms
    :param df_appt:
    :return:
    '''
    df_local = df_appt
    fig,ax = plt.subplots(figsize=(10,5))
    col_ = 'scheduled_day_of_week'
    days = ['xxx','Mon','Tue','Wed','Thr','Fri','Sat']
    layers = {
        'All Appointments':{'data':df_local[col_] },
        'Shows':{'data':df_local.query('attendance == 1')[col_]},
        'No-Shows':{'data':df_local.query('attendance == 0')[col_]}
    }

    bins_ = [0, 1, 2, 3, 4, 5]

    plt.title(title)


    for lyr in layers:
        ax.hist(layers[lyr]['data'], bins=bins_, alpha=0.5, label=lyr)

    ax.grid(True)

    ax.set_xticklabels(days)


    # all
    meanx = layers['All Appointments']['data'].mean()
    std1 = layers['All Appointments']['data'].std()
    ax.plot([meanx, meanx], [0, 29000], 'b-', label='All Mean')
    ax.plot([meanx+std1, meanx+std1], [0, 29000], 'b--', label='All STD')
    ax.plot([meanx - std1, meanx - std1], [0, 29000], 'b--', label='All STD')

    # Shows
    meanx = layers['Shows']['data'].mean()
    std1 = layers['Shows']['data'].std()
    ax.plot([meanx, meanx],[0, 29000], 'r-', label='Show Mean')
    ax.plot([meanx + std1, meanx + std1], [0, 29000], 'r--', label='Shows STD')
    ax.plot([meanx - std1, meanx - std1], [0, 29000], 'r--', label='Shows STD')


    # No-Shows
    meanx = layers['No-Shows']['data'].mean()
    std1 = layers['No-Shows']['data'].std()
    ax.plot([meanx, meanx], [0, 29000], 'g-', label='No-Show Mean')
    ax.plot([meanx + std1, meanx + std1], [0, 29000], 'g--', label='No-Shows STD')
    ax.plot([meanx - std1, meanx - std1], [0, 29000], 'g--', label='No-Shows STD')

    ax.legend(loc='upper right')
    #plt.figure(figsize=(15,5))
    plt.show()




def graph_What_is_Most_Common_Time_of_Day_for_Appointments(df_appt,title='title'):
    '''
    display times of days as bar chart
    :param df_appt:
    :return:
    '''

    labels = Labels(get_feature_labels())  # load verbose feature labels
    intel_dic = {"id": "appointment_id", "feature": "scheduled_hour", "title": "scheduled_hour",
                 "xlabel": "scheduled_hour", "table_labels": labels['scheduled_hour']}

    df_local = df_appt

    fig, ax = plt.subplots(figsize=(15, 5))


    col_ = intel_dic['feature']

    layers = {
        'All Appointments': {'data': df_local[col_]},
        'Shows': {'data': df_local.query('attendance == 1')[col_]},
        'No-Shows': {'data': df_local.query('attendance == 0')[col_]}
    }
    hours = ['{}:00'.format(x) for x in range(0, 24)]
    # bins_ = 16
    bins_ = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    bins_ = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

    bins_ = 14

    grid_ = True

    plt.title(title) #'Scheduled Hour of the Day')
    plt.xlabel('Hour of the Day (24hr clock)')
    plt.ylabel('frequency')

    #plt.hist(layers['All Appointments']['data'])
    for lyr in layers:
        ax.hist(layers[lyr]['data'], bins=bins_, alpha=0.5, label=lyr)
        # add_hist_plot(plt, layers[lyr]['data'], bins=bins_, legend_label=lyr, grid=grid_)
    #hours = ['{}:00'.format(x) for x in range(6, 20)]
    #ax.set_xticklabels(hours)


    plt.legend(loc='upper right')
    plt.show()


def graph_What_do_no_shows_look_like(df_patient):
    '''
    display scatter plot age vs appointment for no shows
    :param df_patient:
    :return:
    '''
    dom = 'age'
    rng = 'appointments'
    filters = [
        'skipper == 1',
        '( appointments > 0 and appointments < 20 )',
        '(age > 0 and age < 100)',
        '(hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0)'
    ]
    filter_out = ' and '.join(filters)

    df_layers = [
        {'df': df_patient.query(filter_out)}
    ]

    layer_colors =  ['purple'] + get_colors()
    title = 'No-Show over Age vs Appointments'
    graph_scatter_layers(df_layers,dom,rng
                         ,layer_colors=layer_colors
                         ,title=title
                         ,figsize=(15, 4), legend_label='no-show')
    for f in filters:
        print('* limit to patients where : ', f)
    eq, desc = get_fit_line_eq(dom, df_layers[0]['df'][dom], rng,df_layers[0]['df'][rng])
    print('* linear equation: ', eq)
    print('* description: ', desc)

# get ride of patients with no maladies
def graph_What_do_shows_look_like(df_patient):
    '''
    display scatter plot of age vs appointment for shows
    :param df_patient:
    :return:
    '''
    dom = 'age'
    rng = 'appointments'
    filters = [
        'skipper == 0',
        '( appointments > 0 and appointments < 20 )',
        '(age > 0 and age < 100)',
        '(hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0)'
    ]
    filter_out = ' and '.join(filters)

    df_layers =[
        {'df': df_patient.query( filter_out)}
    ]

    layer_colors =  ['orange'] + get_colors()
    title = 'Shows over Age vs Appointments'
    graph_scatter_layers(df_layers,dom,rng
                         ,layer_colors=layer_colors
                         ,title=title
                         ,figsize=(15, 4), legend_label='show')

    for f in filters:
        print('* limit to patients where : ', f)

    eq, desc = get_fit_line_eq(dom,df_layers[0]['df'][dom], rng,df_layers[0]['df'][rng])
    print('* linear equation: ', eq)
    print('* description: ', desc)

def fit_linear(dom, rng, x,y):
    from numpy import arange
    from pylab import plot, show
    from scipy import stats

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    summary = {}
    summary= {
        'r-value':r_value,
        'p-value':p_value,
        'slope': slope,
        'intercept': intercept,
        'standard_error': std_err
    }

    if r_value > 0.9999:
        summary['description'] = '"{}" and "{}" have a perfect positive linear relationship'.format(dom.title(), rng.title())
    elif r_value > 0.7:
        summary['description'] = '"{}" and "{}" have a strong positive linear relationship'.format(dom.title(), rng.title())
    elif r_value > 0.5:
        summary['description'] = '"{}" and "{}" have a moderate positive linear relationship'.format(dom.title(), rng.title())
    elif r_value > 0.3:
        summary['description'] = '"{}" and "{}" have a weak positive linear relationship'.format(dom.title(), rng.title())
    elif r_value > 0.00001:  #and r_value > -0.9999:
        summary['description'] = '"{}" and "{}" have NO Linear Relationship'.format(dom.title(), rng.title())
    elif r_value > -0.3:
        summary['description'] = '"{}" and "{}" have a weak negative linear relationship'.format(dom.title(), rng.title())
    elif r_value > -0.5:
        summary['description'] = '"{}" and "{}" have a moderate negative linear relationship'.format(dom.title(), rng.title())
    elif r_value > -0.7:
        summary['description'] = '"{}" and "{}" have a strong negative linear relationship'.format(dom.title(), rng.title())
    elif r_value >= -1.0:
        summary['description'] = '"{}" and "{}" have a perfect negative linear relationship'.format(dom.title(), rng.title())
    else:
        msg='unclassified r-score: "{}"'.format(r_value)
        raise AttributeError(msg)

    summary['linear-equation']= 'y = {}x + {}'.format(summary['slope'], summary['intercept'])
    #print('summary: ', summary)

    return summary

def graph_attendance_scatter(df_patient,
                             context,
                             dom,
                             rng,
                              filters=None,
                              color='grey',
                              layer_label='layer_label',
                              logger=None,
                              binary_name='skipper'
                             ):
    '''
    display appointments vs no_shows/shows

   filters = [
      'skipper == 0',
      '( appointments > 0 and appointments < 20 )',
      '(age > 0 and age < 100)'
    ]
    '''

    #dom = 'appointments'
    #rng = 'no_shows'
    #rng = 'no_show_rate'
    if filters == None:
        filters = []

    df_layers = []
    subtitle = ''
    df_local = None
    if len(filters)==0:
        df_layers = [
            {'df': df_patient},
            {'df': df_patient.query(binary_name + ' == 0' )},
            {'df': df_patient.query(binary_name + ' == 1' )},
        ]
        df_local = df_patient
    else:
        filter_out = ' and '.join(filters)
        subtitle = '\n'+filter_out
        df_layers = [
            {'df': df_patient.query(filter_out )},
            {'df': df_patient.query(filter_out+' and '+ binary_name + ' == 0')},
            {'df': df_patient.query(filter_out+' and '+ binary_name + ' == 1')},

        ]
        df_local = df_patient.query(filter_out)

    layer_colors = [color] + get_colors()
    #title = '{}: {} vs. {}'.format(context, dom,rng).title() #'Appointments vs No-Show-Rate'

    title = '{}: {} vs. {} {}'.format(context, dom, rng, subtitle).title()  # 'Appointments vs No-Show-Rate'

    #plt.title(title)
    plt.figure(figsize=(15,5))
    plt.xlabel(dom)
    plt.ylabel(rng)
    plt.title(title)
    if len(df_layers[1]['df'])>0:
        plt.scatter(df_layers[1]['df'][dom], df_layers[1]['df'][rng], label='show', color='orange', alpha=.5);
    if len(df_layers[2]) >0:
        plt.scatter(df_layers[2]['df'][dom], df_layers[2]['df'][rng], label='no-shows', color='purple', alpha=.5);

    add_fit_line(plt, dom,rng, df_layers[0]['df'][dom], df_layers[0]['df'][rng], color=('black', 1.0),label='line of best fit')

    plt.legend()
    end_plot(plt)


    for f in filters:
        if logger != None:
            logger.collect('* limit to patients where : {}'.format( f))

    #eq, desc = get_fit_line_eq(
    #    dom,
    #    df_layers[0]['df'][dom],
    #    rng,
    #    df_layers[0]['df'][rng])

    fit_summary = fit_linear(dom, rng, df_layers[0]['df'][dom], df_layers[0]['df'][rng] )

    if logger != None:
        eq = 'y = {}x + {}'.format(fit_summary['slope'], fit_summary['intercept'])
        desc = fit_summary['description']
        logger.collect('* linear equation: {}'.format( eq))
        logger.collect('* description: {}'.format(desc))



def graph_Describe_the_relationship_between_patient_age_and_no_shows(df_patient,filters=[]):
    '''
    display scatter plot of age vs no_shows
    filters is  filters = [
        '( appointments > 0 and appointments < 20 )',
        '(age > 0 and age < 100)',
        # '(hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0)'
    ]
    :param df_patient:
    :return:
    '''
    dom = 'age'
    #rng = 'no_show_ratio'
    rng = 'no_shows'
    #rng = 'no_show_rate'
    #filters = [
    #    '( appointments > 0 and appointments < 20 )',
    #    '(age > 0 and age < 100)',
    #    # '(hipertension > 0 or diabetes > 0 or alcoholism > 0 or handcap > 0)'
    #]

    #print(max(df_patient['no_shows']))

    '''
    df_layers = []
    if len(filters) == 0:
        df_layers = [
            {'df': df_patient}
        ]
    else:
        filter_out = ' and '.join(filters)
        df_layers = [
            {'df': df_patient.query(filter_out)}
        ]
    '''
    df_layers = []

    df_local = None
    if len(filters)==0:
        df_layers = [
            {'df': df_patient},
            {'df': df_patient.query('skipper == 0' )},
            {'df': df_patient.query('skipper == 1' )},
        ]
        df_local = df_patient
    else:
        filter_out = ' and '.join(filters)
        df_layers = [
            {'df': df_patient.query(filter_out )},
            {'df': df_patient.query(filter_out+' and skipper==0')},
            {'df': df_patient.query(filter_out+' and skipper==1')},

        ]
        df_local = df_patient.query(filter_out)


    layer_colors = ['grey'] + get_colors()

    title = '{} vs. {}'.format(dom, rng).title()  # 'Appointments vs No-Show-Rate'

    plt.figure(figsize=(15, 5))
    plt.xlabel(dom)
    plt.ylabel(rng)
    plt.title(title)


    graph_scatter_layers(df_layers, dom, rng, title=title, layer_colors=layer_colors,
                         figsize=(15, 4),legend_label='appointment')

    for f in filters:
        print('* limit to patients where : ', f)
    '''
    eq, desc = get_fit_line_eq(dom, df_layers[0]['df'][dom], rng, df_layers[0]['df'][rng])

    print('* equation: ', eq)
    
    print('* description: ', desc)
    '''
def graph_Patient_Attendance_and_Skipped_Visits(df_patient,df_appt):
    '''
    display sankey diagram of appointment > perfect and skipper > first, second, ... time patients
    :param df_patient:
    :return:
    '''
    clip_pos = 7 # don't show all
    ################## Trunk of diagram
    flow_1 = []
    #df_groupby = df_patient.groupby(['skipper'])['skipper'].count()
    df_groupby = df_appt.groupby(['attendance'])['attendance'].count()
    flow_1.append(-len(df_appt))

    flow_1 = flow_1 + sorted(list(df_groupby),reverse=True)

    total_patients = flow_1[0] # branch 1, perfect
    total_skippers = flow_1[2] # branch 2, skippers

    flow_1 = np.array(flow_1)
    flow_1 = flow_1 / flow_1[0]

    ################# skipper branch
    df_flow_2 = df_appt.query('attendance == 0') # get 1st
    flow_2 = list(df_flow_2.groupby(['visit'])['appointment_id'].count()) # sum up for graph

    flow_2 = [-total_skippers] + flow_2 # build branch with all visits

    tmp_sum = sum(flow_2[clip_pos:])  # sum up the groups that will make their own branch

    # adjust skipper_timer to 5
    flow_2 = flow_2[0:clip_pos] # get rid of small groups at end

    flow_2.append(tmp_sum)

    flow_2 = np.array(flow_2)
    flow_2 = flow_2 / (total_patients)

    ##################
    fig = plt.figure(figsize=(15,10));

    ax = fig.add_subplot(1, 1, 1,
                         xticks = [], yticks = [],
                         title='Appointment Attendance')

    sankey = Sankey(ax=ax,format='%.3G')

    # first diagram, indexed by prior=0
    sankey.add(flows=flow_1,
               orientations=[0,1,0],
           labels=['Appointments', 'Attended', 'Skipped'])

    # second diagram indexed by prior=1 [0.2834883459431674, -0.114211, -0.169277]
    sankey.add(flows=flow_2,
              orientations=[0,1,1,1,-1,-1,-1,-1],
              labels=['', '1st visit', '2nd','3rd','4th','5th','6th','7th-18th'],
              prior=0,
              connect=(2, 0))

    sankey.finish();

    #plt.plot([2.05,2.05],[0.09, .6], 'r-', label='Mean')
    plt.legend()


def qraph_Do_all_patient_have_maladies(df_patient):
    '''
    pie chart of patient with and without maladies
    :param df_patient:
    :return:
    '''
    cols = ['appointments', 'no_show_rate', 'hipertension', 'diabetes', 'alcoholism', 'handcap']
    q_str = 'hipertension == 0 and diabetes==0 and alcoholism == 0 and handcap == 0'
    df_no_maladies = df_patient[cols] \
        .query(q_str)

    no_maladies = len(df_no_maladies)
    maladies = len(df_patient) - no_maladies

    pie_data = {
        'titles': ['Maladies vs No-Maladies'],
        'colors': ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'blue'],
        'No-Malady': [no_maladies],
        'Malady': [maladies]
    }
    piie.pie(pie_data)

    print('* {} out of {} patients have no recorded malady'.format(len(df_no_maladies), len(df_patient)))
    print('* {}% of the patients have no useful health data on which to base a no-show prediction'.format(
        (len(df_no_maladies) / len(df_patient)) * 100.0))


def graph_What_is_the_most_common_Malady_of_Visiting_Patients(df_patient):
    '''
    Bar chart of malady counts
    :param df_patient:
    :return:
    '''
    df_nomalady = df_patient.query('hipertension == 0 and diabetes==0 and alcoholism == 0 and handcap == 0')
    df_hiper = df_patient.query('hipertension == 1')
    df_diabetes = df_patient.query('diabetes == 1')
    df_alcolholism = df_patient.query('alcoholism == 1')
    df_handcap = df_patient.query('handcap >0')
    # data to plot
    n_groups = 5
    means_1 = (len(df_nomalady),0,0,0,0)
    means_A = (0,len(df_hiper), 0, 0, 0)
    means_B = (0,0, len(df_diabetes), 0, 0)
    means_C = (0,0, 0, len(df_alcolholism), 0)
    means_D = (0,0, 0, 0, len(df_handcap))

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, means_1, bar_width,
                     alpha=opacity,
                     color='gray',
                     label='no-malady')

    rects2 = plt.bar(index, means_A, bar_width,
                     alpha=opacity,
                     color='b',
                     label='hiper')

    rects3 = plt.bar(index , means_B, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Guido')
    rects4 = plt.bar(index , means_C, bar_width,
                     alpha=opacity,
                     color='r',
                     label='C')
    rects5 = plt.bar(index , means_D, bar_width,
                     alpha=opacity,
                     color='orange',
                     label='D')

    plt.xlabel('Malady')
    plt.ylabel('Patients')
    plt.title('Common Maladies')
    plt.xticks(index  , ('no-malady','hipertension', 'diabetes', 'alcoholism', 'handcap'))
    #plt.legend()

    plt.tight_layout()
    plt.show()
    total_patients = len(df_patient)
    print("* {}% ({}) of Patients have no malady ".format(100.0*(means_1[0]/total_patients), means_1[0]))
    print("* {}% ({}) of Patients have hipertension ".format(100.0*(means_A[1]/total_patients), means_A[1]))
    print("* {}% ({}) of Patients have diabetes ".format(100.0*(means_B[2]/total_patients), means_B[2]))
    print("* {}% ({}) of Patients have alcoholism ".format(100.0*(means_C[3]/total_patients), means_C[3]))
    print("* {}% ({}) of Patients have a handcap ".format(100.0*(means_D[4]/total_patients), means_D[4]))


def graph_appointments_by_week(df_appt, title='title'):
    '''
    display times of days as bar chart
    :param df_appt:
    :return:
    '''

    df_local = df_appt

    fig, ax = plt.subplots(figsize=(15, 5))

    col_ = 'week'

    layers = {
        'All Appointments': {'data': df_local[col_]},
        # 'Shows': {'data': df_local.query('attendance == 1')[col_]},
        # 'No-Shows': {'data': df_local.query('attendance == 0')[col_]}
    }

    hours = ['{}:00'.format(x) for x in range(0, 24)]

    bins_ = 23

    grid_ = True

    plt.title(title)  # 'Scheduled Hour of the Day')
    plt.xlabel('Week')
    plt.ylabel('frequency')
    plt.ticklabel_format(useOffset=False)

    for lyr in layers:
        ax.hist(layers[lyr]['data'], bins=bins_, alpha=0.5, label=lyr)

    meanx = layers['All Appointments']['data'].mean()
    std1 = layers['All Appointments']['data'].std()
    ax.plot([meanx, meanx], [0, 29000], 'b-', label='Mean')
    ax.plot([meanx + std1, meanx + std1], [0, 29000], 'b--', label='+ 1 STD')

    ax.plot([meanx - std1, meanx - std1], [0, 29000], 'b--', label='- 1 STD')


    ticks = [t for t in range(201601, 201623)]
    plt.xticks(ticks)
    plt.xticks(rotation='vertical')




    plt.legend(loc=2)

    plt.show()


def graph_daily_ratio(df_appt, title, log):
    '''
      daily ratio of no_shows to show
    '''
    dom = 'Business Day'
    rng = '(No-Show: Show) Ratio'
    

    qb_no_shows = df_appt.query('attendance == 0').groupby('scheduled_day_of_week')['appointments'].count()
    qb_shows = df_appt.query('attendance == 1').groupby('scheduled_day_of_week')['appointments'].count()
    lst_ratio = qb_no_shows / qb_shows
    ave_diff = sum(lst_ratio) / len(lst_ratio)

    idx_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    idx = [0, 1, 2, 3, 4]
    for d, v in zip(idx, lst_ratio):
        plt.bar(d, v, alpha=0.5)

    plt.xlabel(dom)
    plt.ylabel(rng)
    #plt.title('Relative Change in Skipping over a Week')
    plt.title(title)

    plt.xticks(idx, idx_labels)
    plt.yticks([0.25])
    plt.plot([-0.5, 4.55], [ave_diff, ave_diff], 'r-', 'mean {:0.2f}'.format(ave_diff))

    plt.show()
    log.collect('* Mean {} is {:0.2f}'.format(rng,ave_diff))

def graph_hourly_ratio(df_appt, title,log):
    '''
      daily ratio of no_shows to show
    '''
    dom = 'hour'
    rng = '(Show : No-Show) Ratio'
    plt.figure(figsize=(15, 5))
    qb_no_shows = df_appt.query('attendance == 0').groupby('scheduled_hour')['appointments'].count()
    qb_shows = df_appt.query('attendance == 1').groupby('scheduled_hour')['appointments'].count()
    lst_ratio = qb_no_shows / qb_shows
    ave_diff = sum(lst_ratio) / len(lst_ratio)

    idx = np.arange(6, 22, 1)
    idx = np.arange(7, 21, 1)

    idx_labels = ['{}:00'.format(t) for t in idx]  # ['mon','tue','wed','thu','fri']

    result = fit_linear(dom, rng, idx, lst_ratio)
    low = (result['slope'] * idx[0]) + result['intercept']
    high = result['slope'] * idx[len(idx) - 1] + result['intercept']

    for d, v in zip(idx, lst_ratio):
        plt.bar(d, v, alpha=0.5)

    plt.xlabel('Hours')
    plt.ylabel('(No-Shows : Shows) Ratio')
    #plt.title('Relative Change in Skipping over the Day')
    plt.title(title)
    plt.xticks(idx, idx_labels)
    plt.yticks([low, high])

    add_fit_line(plt, dom, rng, idx, lst_ratio, color=('black', 1.0), label='label')
    plt.show()

    log.collect('* {}'.format(result['description']))


def test_graph_What_is_Most_Common_Time_of_Day_for_Appointments():
    print('########### graph_What_is_Most_Common_Time_of_Day_for_Appointments')
    df_appt = pd.read_csv('../03.01.01.appointments.csv')
    graph_What_is_Most_Common_Time_of_Day_for_Appointments(df_appt)


#def test_graph_Describe_the_relationship_between_patient_appointments_and_no_shows():

    #print('########### test_graph_Describe_the_relationship_between_patient_appointments_and_no_shows')
    #df_appt = pd.read_csv('../03.01.03.patients.csv')
    #graph_Describe_the_relationship_between_patient_appointments_and_no_shows(df_appt)
def test_graph_attendance_scatter():
    print('########### test_graph_attendance_scatter')
    df_appt = pd.read_csv('../03.01.03.patients.csv')
    graph_attendance_scatter(df_appt,'Patient','age','no_shows')


def test_graph_attendance_scatter_filter():
    print('########### test_graph_attendance_scatter_filter')
    df_appt = pd.read_csv('../03.01.03.patients.csv')
    filters = [
        # '( appointments > 0 and appointments <= 1 )',
        '( age < 100 )',
    ]
    graph_attendance_scatter(df_appt,'Patient','age','no_shows',filters=filters)



def test_how_linear():
    df_patient = pd.read_csv('../03.01.03.patients.csv')
    output = fit_linear('age','no_shows',df_patient['age'],df_patient['no_shows'])
    print('output: ', output)

def test_graph_Scheduled_Day_of_Week():
    df_appt = pd.read_csv('../03.01.01.appointments.csv')
    df_appt.info()
    graph_Scheduled_Day_of_Week(df_appt, title='title')
def test_graph_What_is_Most_Common_Time_of_Day_for_Appointments():
    df_appt = pd.read_csv('../03.01.01.appointments.csv')
    graph_What_is_Most_Common_Time_of_Day_for_Appointments(df_appt, title='title')

def test_graph_appointments_by_week():
    df_appt = pd.read_csv('../03.01.01.appointments.csv')
    graph_appointments_by_week(df_appt, title='title')

def main():


    #test_get_color()
    #test_scatter()
    #test_scatter_sizes()
    #test_scatter_colors()
    #test_scatter_layers()
    #test_graph_What_is_Most_Common_Time_of_Day_for_Appointments()


    #test_graph_attendance_scatter()
    #test_graph_attendance_scatter_filter()

    #test_how_linear()


    #test_graph_Scheduled_Day_of_Week()
    #test_graph_What_is_Most_Common_Time_of_Day_for_Appointments()
    test_graph_appointments_by_week()

if __name__ == "__main__":
    # execute only if run as a script
    main()