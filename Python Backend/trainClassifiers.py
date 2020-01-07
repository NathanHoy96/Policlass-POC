import nltk
import random
import os
import pickle
from nltk.stem import *
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.corpus import stopwords


rightroot = "C:\\Users\\Nathan Hoy\\Documents\\Dataset\\DS1ASC\\RIGHT"
leftroot = "C:\\Users\\Nathan Hoy\\Documents\\Dataset\\DS1ASC\\LEFT"
centreroot = "C:\\Users\\Nathan Hoy\\Documents\\Dataset\\All Sides Collection\\CENTRE"
documents = []
allwords = []
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

for file in os.listdir(rightroot):
    content = open(rightroot+"\\"+file, encoding = 'utf-16').read()    
    tokenize = nltk.word_tokenize(content)
    documents.append((content,"right"))

    for w in tokenize:
        w = ps.stem(w)
        if w not in stop_words:
            allwords.append(w.lower())

for file in os.listdir(leftroot):
    content = open(leftroot+"\\"+file, encoding = 'utf-16').read()
    tokenize = nltk.word_tokenize(content)
    documents.append((content,"left"))

    for w in tokenize:
        w = ps.stem(w)
        if w not in stop_words:
            allwords.append(w.lower())

##for file in os.listdir(centreroot):
##    content = open(centreroot+"\\"+file, encoding = 'utf-16').read()
##    tokenize = nltk.word_tokenize(content)
##    documents.append((content,"centre"))
##
##    for w in tokenize:
##        w = ps.stem(w)
##        if w not in stop_words:
##            allwords.append(w.lower())


print(len(allwords))
allwords = nltk.FreqDist(allwords)
random.shuffle(allwords)
random.shuffle(documents)

#print(allwords.most_common(15))
#print(documents[1])

word_features = list(allwords.keys())[:10000]
save_features = open("wordfeatures.pickle","wb")
pickle.dump(word_features, save_features)
save_features.close()

def find_features(document):
    words = nltk.word_tokenize(document)
    words = set(words)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

#targetfile="C:\\Users\\Nathan Hoy\\Documents\\Dataset\\LEFT\\Atlantic1.txt"
#tf = open(targetfile, encoding='utf-16')
#targetcontent = tf.read()
#print((find_features(targetcontent)))

featuresets = [(find_features(article),category) for (article,category) in documents]

training_set = featuresets[:6000]
#print(trainingset)
testing_set = featuresets[4500:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("NB Algo Accuracy: ",
      (nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

save_classifier = open("logisticregression.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

save_classifier = open("SGDC.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()

save_classifier = open("SVC.pickle","wb")
pickle.dump(SVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("linearSVC.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("nuSVC.pickle","wb")
pickle.dump(NuSVC_classifier, save_classifier)
save_classifier.close()

