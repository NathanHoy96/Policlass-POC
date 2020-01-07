from bs4 import BeautifulSoup
import requests
import re
import nltk
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.corpus import stopwords
from nltk.stem import *

def getArticleText(url):
    #print(url)
    html = requests.get(url).content
    #1 Recoding
    unicode_str = html.decode("utf8")
    encoded_str = unicode_str.encode("ascii",'ignore')
    news_soup = BeautifulSoup(encoded_str, "html.parser")
    a_text = news_soup.find_all('p')
    y=[re.sub(r'<.+?>',r'',str(a)) for a in a_text]
    return y

def find_features(document):
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    features_f = open("wordfeatures.pickle", "rb")
    word_features = pickle.load(features_f)
    features_f.close()
    words = nltk.word_tokenize(document)
    words = set(words)
    cleanedWords = []

    for w in words:
        w = ps.stem(w)
        if w not in stop_words:
            cleanedWords.append(w.lower())
    
    features = {}
    for w in word_features:
        features[w] = (w in cleanedWords)
    return features

def classify(url):
    #print(url)
    classifier_1 = open("naivebayes.pickle", "rb")
    nb = pickle.load(classifier_1)
    classifier_1.close()

    classifier_2 = open("linearSVC.pickle", "rb")
    linearSVC = pickle.load(classifier_2)
    classifier_2.close()

    classifier_3 = open("logisticregression.pickle", "rb")
    logisticregression = pickle.load(classifier_3)
    classifier_3.close()

    classifier_4 = open("nuSVC.pickle", "rb")
    classifier = pickle.load(classifier_4)
    classifier_4.close()

    classifier_5 = open("SVC.pickle", "rb")
    SVC = pickle.load(classifier_5)
    classifier_5.close()

    classifier_6 = open("SGDC.pickle", "rb")
    SGDC = pickle.load(classifier_6)
    classifier_6.close()
    
    article = getArticleText(url)
    print(str(article))
    features = find_features(str(article))
    #print(features)
    #print(tokenized_article)
    nbOut = nb.classify(features)
    linearSVCOut = linearSVC.classify(features)
    logisticregressionOut = logisticregression.classify(features)
    SVCOut = SVC.classify(features)
    SGDCOut = SGDC.classify(features)

    print("Naive Bayes Classification: " + nbOut)
    print("Linear SVC Classification: " + linearSVCOut)
    print("Logistic Regression Classification: " + logisticregressionOut)
    print("SVC Classification: " + SVCOut)
    print("SGDC Classification: " + SGDCOut)

classify("https://www.theguardian.com/uk-news/2019/dec/02/boris-johnson-denounced-for-politicising-london-bridge-attack")
