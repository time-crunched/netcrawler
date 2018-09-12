from django.shortcuts import render
from django.http import HttpResponse
from .headlines import Headlines
from .sentimentanalyzer import SentimentAnalyzer

def index(request):
    return render(request, 'index.html')

def overview(request):
    urls = [
        'https://www.ft.com/',
        'https://www.wired.com',
        'https://www.norconsult.com',
        'https://www.ft.com/',
        'https://www.hegnar.no',
         'https://www.aftenposten.no/okonomi',
        # 'https://www.e24.no',
        # 'https://www.sysla.no',
        # 'https://kapital.no/investor',
        # 'https://www.nrk.no/nyheter/norsk-okonomi-1.11219446',
        # 'https://www.nettavisen.no/na24/',
        # 'https://www.dagbladet.no/emne/økonomi',
        # 'https://www.tv2.no/nyheter/okonomi/',
        # 'https://www.abcnyheter.no/penger',
        ]
    data_list = []
    for url in urls:
        url_obj = Headlines(url)
        data_dict = url_obj.Scrape()
        data_list.append(data_dict)

        for data_dict in data_list:
            for headline in data_dict['headlines']:
                headline_obj = SentimentAnalyzer(str(headline[0]))
                print(headline_obj.input_text)
                try:
                    #headline_obj.translate()
                    polarity = headline_obj.analyze()
                    print(polarity)
                    headline.append(polarity)
                except:
                    pass


    return render(request, 'overview.html', { 'data_list': data_list })
