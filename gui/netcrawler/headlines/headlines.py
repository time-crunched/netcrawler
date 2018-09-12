import os
import datetime
import requests
import re
from bs4 import BeautifulSoup

class Headlines(object):
    def __init__(self, url):
        #All parsed data are stored in a dictionary.
        self.data_dict = {}

        #Add 'https://' to url if not already there.
        self.url = os.path.join('https://',url.strip('https://'))

        #Store url for later use.
        self.data_dict['url'] = self.url

        #Strip URL to obtain a representative title.
        self.url_core = self.url.split("/")[2]
        self.title = self.url_core.split(".")[-2] + '.' + self.url_core.split(".")[-1]
        self.title = self.title.capitalize()

        #Store title for later use.
        self.data_dict['title'] = self.title

        #Download html content.
        self.page = requests.get(self.url)

        #Get date and time.
        self.now = datetime.datetime.now()
        self.datetime = self.now.strftime("%Y-%m-%d kl.%H:%M")

        #Store date and time for later use
        self.data_dict['datetime'] = self.datetime

    def Scrape(self):
        #Define list for collecting headlines:
        self.headlines = []

        #Helper object:
        self.prev_obj = ''

        #Define BeautifulSoup object for scraping
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

        #Loop all 'a'-tags.
        for self.tag in self.soup.find_all('a'):
            #Get the accociated linkself.
            self.tag_href = self.tag.get('href')

            #Add url to tag_href if not already there.
            try:
                if re.match(r'http', self.tag_href) is None:
                    #Remove leading slash
                    try:
                        self.tag_href= self.tag_href.strip('/')
                    except:
                        pass

                    #Join url and tag_href.
                    try:
                        self.tag_href = os.path.join(self.url,self.tag_href)
                    except:
                        pass
            except:
                pass

            #Get the text self.tag_text from the HTML-tag
            self.tag_text = self.tag.get_text()

            #Remove "\n" from the beginning and end of the self.tag_text.
            self.tag_text = self.tag_text.strip() #Denne bør oppdateres slik at "\n" på slutten av setninger erstattes med punktum.

            #Convert text to list of all words and punctuations.
            self.text_list = list(self.tag_text)

            #Remove '\n' inside the self.tag_text and convert to '. ' when necassary.
            for i in range(1, len(self.text_list)):
                if self.text_list[i] == '\n':

                    if self.text_list[i-1] == '.':
                        self.text_list[i] = ' '

                    elif self.text_list[i-1] == '. ':
                        self.text_list[i] = ''

                    else:
                        self.text_list[i] = '. '

                    self.index = i
                    while self.text_list[self.index+1] == '\n':
                        self.text_list[self.index+1] = ''
                        self.index = self.index + 1

                #Add whitespace after numbers if the next character is a letter:
                if self.text_list[i - 1].isdigit() and self.text_list[i].isalpha():
                    self.text_list[i - 1] = self.text_list[i - 1] + ' '

                #Add whitespace before numbers if the previous character is a letter:
                if self.text_list[i - 1].isalpha() and self.text_list[i].isdigit():
                    self.text_list[i - 1] = self.text_list[i - 1] + ' '

                #Add whitespace before capitalized letters:
                if self.text_list[i - 1].isalpha() and self.text_list[i - 1].istitle() == False and self.text_list[i].istitle():
                    self.text_list[i - 1] = self.text_list[i - 1] + ' '

            #Remove redundant whitespace at the beginning of the self.tag_text.
            try:
                if self.text_list[0] == ' ':
                    del self.text_list[0]
            except:
                pass

            #Remove redundant whitespace at the end of the self.tag_text.
            try:
                while self.text_list[-1] == ' ':
                    del self.text_list[-1]
            except:
                pass


            #Convert self.text_list to self.tag_text
            self.tag_text = ''.join(self.text_list)

            #Replace unicode '\xa0' with whitespace
            self.tag_text = self.tag_text.replace(u'\xa0', u' ')

            #Remove redundant Whitespace.
            self.tag_text = re.sub(r' +',' ',self.tag_text)

            #Search for code-like characters.
            self.searchobj = re.search(r'{',self.tag_text)

            #Count the number of words in the self.tag_text
            self.word_num = len(self.tag_text.split())

            #Special treatment for e24.no:
            if self.url == 'https://www.e24.no':
                if self.prev_obj == '':
                    if 2 <= self.word_num <= 50  and self.searchobj == None:
                        self.touple = [self.tag_text,self.tag_href]
                        self.headlines.append(self.touple)

                else:
                    if 2 <= self.word_num <= 50  and self.searchobj == None:
                        self.headlines[-1][0] = self.headlines[-1][0] + ' ' + self.tag_text

                self.prev_obj = self.tag_text


            #Remove self.tag_texts with few words and code-like self.tag_texts.
            elif 5 <= self.word_num <= 50  and self.searchobj == None:
                self.touple = [self.tag_text,self.tag_href]
                self.headlines.append(self.touple)


        #Add all headlines and links to the url-dictionary
        self.data_dict['headlines'] = self.headlines

        #print(self.data_dict)
        return self.data_dict



if __name__ == '__main__':
    url_obj = Headlines(url = 'www.e24.no')
    data_dict = url_obj.Scrape()

    print(data_dict['url'])
    print(data_dict['datetime'])
    print(data_dict['title'])
    print('\n')

    for list in data_dict['headlines']:
        print(list[0])
        print(list[1])
        print('\n')
