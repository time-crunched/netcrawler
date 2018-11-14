from textblob import TextBlob

class SentimentAnalyzer(object):

    def __init__(self,text):
        self.input_text = text
        self.en_text = self.input_text

    def translate(self):
        self.trans_obj = TextBlob(self.input_text)
        self.language = self.trans_obj.detect_language()

        if not self.language == 'en':
            self.en_text = self.trans_obj.translate(to = 'en')

        else:
            self.en_text = self.input_text

    def analyze(self):
        self.ana_obj = TextBlob(str(self.en_text))
        self.polarity = self.ana_obj.sentiment.polarity
        self.polarity = '{0:.3g}'.format(self.polarity)
        return self.polarity

if __name__ == '__main__':
    text_obj = SentimentAnalyzer('Dette er helt utrolig!')
    #text_obj.translate()
    polarity = text_obj.analyze()

    print(text_obj.input_text)
    print(text_obj.en_text)
    print(polarity)
