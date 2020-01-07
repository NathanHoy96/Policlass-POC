from newspaper import Article
import requests
import json

def getNewsArticle(url):

    #Given a URL, find the article and parse it into plain text
    article = Article(url)
    article.download()
    article.parse()

    title = str(article.title)

    #Find some of the keywords in the article we can use to search
    article.nlp()
    keywords = article.keywords

    #Find only the first 5 keywords to search on and create a query
    topkeys = ""
    for i in range(5):
        topkeys = topkeys+" "+keywords[i]

    query = "q=" + topkeys + "&"

    print(query)

    #Pass the query to the News API endpoint
    url = ('https://newsapi.org/v2/everything?'
       'q='+topkeys+'&'
       'apiKey=b99ee89980184edabe6a5a603b5310ee')

    response = requests.get(url)
    #print(response.content)
    r = json.loads(response.content)
    keys = len(r['articles'])
    print(keys)

    alternatives = []
    
    #Loop through the response to find all the URLs returned
    for i in range(len(r['articles'])):
        print(r['articles'][i]['url'])
        alternatives.append(r['articles'][i]['url'])

    return alternatives    

    #Return URLs for classification

toclassify = getNewsArticle('https://news.sky.com/story/manchester-attacks-thugs-hunted-over-seven-robberies-in-two-hours-11901697')
