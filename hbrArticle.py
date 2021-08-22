import requests
from bs4 import BeautifulSoup

class hbrArticle:
    def __init__(self, userURL, fileName) -> None:
        self.userURL = userURL
        self.fileName = fileName

    def getMarkup(self):
        self.userRequest = requests.get(url=self.userURL)
        self.markup = self.userRequest.text
        return self.markup

    def parseMarkup(self):
        self.soup = BeautifulSoup(markup=self.markup, features='html.parser')
        self.title = self.soup.title.text
        self.publicationDate = self.soup.find('div', {'class': 'pub-date'}).text.strip()
        self.summaryText = self.soup.find('span', {'class': 'summary-text'}).text.strip()
        if self.soup.find('div', {'class': 'article-body standard-content'}) is not None:
            self.mainArticle = self.soup.find('div', {'class': 'article-body standard-content'})
        else:
            self.mainArticle = self.soup.find('div', {'class': 'article-body'})
        return self.title, self.publicationDate, self.summaryText, self.mainArticle

    def writeMarkupToFile(self):
        with open(file=self.fileName, mode='a') as f:
            f.write(f'Title:\n{self.title}' + ('\n' * 2))
            f.write(f'Publication Date:\n{self.publicationDate}' + ('\n' * 2))
            f.write('Summary:' + '\n')

            for line in self.summaryText.split('. '):
                if line.endswith('.'):
                    f.write(line + '\n')
                else:
                    f.write(line + '.' + '\n')
    
            f.write('\n')
            f.write('Main Article:' + '\n')

            for para in self.mainArticle.find_all('p'):
                para = para.text.split('. ')

                for sentence in para:
                    if sentence.endswith('.'):
                        f.write(sentence + '\n')
                    else:
                        f.write(sentence + '.' + '\n')

# Instantiate the class and call the necessary functions
c = hbrArticle(userURL=input('Please enter the HBR article\'s URL:\n'), fileName=input('Please enter the text file\'s name:\n'))
c.getMarkup()
c.parseMarkup()
c.writeMarkupToFile()
