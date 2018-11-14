from django.shortcuts import render
from django.shortcuts import render_to_response
import pickle
import os
import glob
import random
import time
import datetime

def history(request):
    # Collect History
    cwd = os.getcwd()
    archive_dir = os.path.join(cwd,'archive')

    xdata = []
    ydata = []

    filenames = glob.glob(os.path.join(archive_dir, '*.p'), recursive = False)
    basenames = [os.path.basename(filename) for filename in filenames]
    filenames = [os.path.splitext(basename)[0] for basename in basenames]
    filenames = sorted(filenames)
    filenames = [str(filename) + '.p' for filename in filenames]
    
    for filename in filenames:
        filepath = os.path.join(archive_dir, filename)

        with open(filepath, "rb") as fp:
            data_list = pickle.load(fp)

        pol_scores = []
        for data_dict in data_list:
            # print(data_dict['url'])
            # print(data_dict['datetime'])
            # print(data_dict['datetime_plot'])
            # print(data_dict['polarity'])
            # print(data_dict['title'])

            pol_scores.append(float(data_dict['polarity']))

        #Append last datetime for last website in the datalist as current datetime
        xdata.append(data_dict['datetime_plot'])

        #Calculate average polariy for all websites on current date
        pol_avg = sum(pol_scores)/len(pol_scores)
        pol_avg = '{0:.3g}'.format(pol_avg)
        ydata.append(float(pol_avg))


    """
    lineChart page
    """
    # start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    # nb_element = 150
    # xdata = range(nb_element)
    # xdata = list(map(lambda x: start_time + x * 1000000000, xdata))
    # ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    # ydata2 = map(lambda x: x * 2, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    # extra_serie2 = {
    #     "tooltip": {"y_start": "", "y_end": " cal"},
    #     "date_format": tooltip_date,
    # }
    chartdata = {'x': xdata,
        'name1': 'Avg. polarity', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': { 'color': '#3947c6' },
    #     'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': { 'color': '#ff8af8' },
    }

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b %Y kl.%H:%M',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('linechart.html', data)
