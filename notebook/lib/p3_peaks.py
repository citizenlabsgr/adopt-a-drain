import numpy as np

from scipy.signal import find_peaks_cwt

def get_maxima_large(value_list):
    '''
    value_list is list from which to determine maxima
    maxima are True values
    returns list [<boolean>,<boolean>]
    '''
    cb = np.array(value_list)
    indexes = find_peaks_cwt(cb, np.arange(1, 10))  # ?????

    # create list as long as value_list initialized to False or not a maxima

    maxima = [False] * len(value_list)

    for i in indexes:
        maxima[i] = True
        if i > 0 and value_list[i - 1] > value_list[i]:  # this is a work around for a bad maxima
            # print('fix: ',i)
            maxima[i] = False
            maxima[i - 1] = True
            # print(i, 'maxima',value_list[i])

    return maxima


# test
value_test = [1.0, 3.0, 5.0, 10.0, 4.0, 3.0, 1.0]
expected_list = [False, False, False, True, False, False, False]
result_list = get_maxima_large(value_test)
assert expected_list == result_list