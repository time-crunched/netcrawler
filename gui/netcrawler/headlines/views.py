from django.shortcuts import render
from django.http import HttpResponse
from .headlines import Headlines
from .sentimentanalyzer import SentimentAnalyzer

import os
import pickle
import datetime
import time

def index(request):
    return render(request, 'index.html')

def overview(request):
    urls = [
        'https://www.ft.com/',
        'https://www.reuters.com/finance',
        'https://www.marketwatch.com',
        'https://www.fnlondon.com',
        'https://www.cnbc.com/finance/',
        #'https://www.theguardian.com/uk/business',
        #'https://www.wsj.com/news/markets',
        #'https://www.investing.com/news/',
        #'https://www.bbc.com/news/business',
        #'https://www.independent.co.uk/news/business',
        #'https://edition.cnn.com/business',
        #'https://www.nbcnews.com/business/business-news',
        'https://www.euronews.com/news/business',
        #'https://economictimes.indiatimes.com/markets',
        #'https://www.investing.com/news/stock-market-news',
        #'https://www.norconsult.com',
        # 'https://www.hegnar.no',
        #  'https://www.aftenposten.no/okonomi',
        # 'https://www.e24.no',
        # 'https://www.sysla.no',
        # 'https://kapital.no/investor',
        # 'https://www.nrk.no/nyheter/norsk-okonomi-1.11219446',
        # 'https://www.nettavisen.no/na24/',
        # 'https://www.dagbladet.no/emne/økonomi',
        #'https://www.tv2.no/nyheter/okonomi/',
        # 'https://www.abcnyheter.no/penger',
        ]
    data_list = []
    for url in urls:
        url_obj = Headlines(url)
        data_dict = url_obj.Scrape()
        data_list.append(data_dict)


        for data_dict in data_list:
            pol_scores = []
            for headline in data_dict['headlines']:
                headline_obj = SentimentAnalyzer(str(headline[0]))
                try:
                    #headline_obj.translate()
                    polarity = headline_obj.analyze()
                    headline.append(polarity)

                    if float(polarity) < 0.05 and float(polarity) > -0.05:
                        pass
                    else:
                        pol_scores.append(polarity)

                except:
                    pass

            #Calculate average polariy for website
            pol_scores = [float(i) for i in pol_scores]
            # Calculate arithmetic mean
            #pol_avg = sum(pol_scores)/len(pol_scores)
            #Calculate Mode-mean
            pol_avg = max(set(pol_scores), key=pol_scores.count)
            pol_avg = '{0:.3g}'.format(pol_avg)
            data_dict['polarity'] = pol_avg

    #Store acquired headlines and associated data
    #now = datetime.datetime.now()
    #filename = now.strftime("%M-%H %Y-%m-%d" + ".p")
    now = int(time.time())
    filename = str(now) + '.p'
    cwd = os.getcwd()
    archive_dir = os.path.join(cwd,'archive')

    if os.path.exists(archive_dir):
        pass
    else:
        os.makedirs(archive_dir)

    filepath = os.path.join(archive_dir, filename)

    with open(filepath, "wb") as fp:
        pickle.dump(data_list, fp)

    return render(request, 'overview.html', { 'data_list': data_list })
