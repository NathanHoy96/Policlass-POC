import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import random
import pickle
from collections import Counter
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
hm_lines = 100000

def create_lexicon(left,right):

	lexicon = []
	with open(left,'r',encoding='utf-8',errors='ignore') as f:
		contents = f.readlines()
		for l in contents[:hm_lines]:
			all_words = word_tokenize(l)
			lexicon += list(all_words)

	with open(right,'r',encoding='utf-8',errors='ignore') as f:
		contents = f.readlines()
		for l in contents[:hm_lines]:
			all_words = word_tokenize(l)
			lexicon += list(all_words)

	lexicon = [lemmatizer.lemmatize(i) for i in lexicon]
	w_counts = Counter(lexicon)
	l2 = []
	for w in w_counts:
		#print(w_counts[w])
		if 10000 > w_counts[w] > 500:
			l2.append(w)
	print(len(l2))
	return l2





def sample_handling(sample,lexicon,classification):

	featureset = []

	with open(sample,'r',errors='ignore') as f:
		contents = f.readlines()
		for l in contents[:hm_lines]:
			current_words = word_tokenize(l.lower())
			current_words = [lemmatizer.lemmatize(i) for i in current_words]
			features = np.zeros(len(lexicon))
			for word in current_words:
				if word.lower() in lexicon:
					index_value = lexicon.index(word.lower())
					features[index_value] += 1

			features = list(features)
			featureset.append([features,classification])

	return featureset



def create_feature_sets_and_labels(left,right,test_size = 0.1):
	lexicon = create_lexicon(left,right)
	features = []
	features += sample_handling('left.txt',lexicon,[1,0])
	features += sample_handling('right.txt',lexicon,[0,1])
	random.shuffle(features)
	features = np.array(features)
	print(lexicon)

	testing_size = int(test_size*len(features))

	train_x = list(features[:,0][:-testing_size])
	train_y = list(features[:,1][:-testing_size])
	test_x = list(features[:,0][-testing_size:])
	test_y = list(features[:,1][-testing_size:])

	return train_x,train_y,test_x,test_y


if __name__ == '__main__':
	train_x,train_y,test_x,test_y = create_feature_sets_and_labels('left.txt','right.txt')
	# if you want to pickle this data:
	with open('sentiment_set.pickle','wb') as f:
		pickle.dump([train_x,train_y,test_x,test_y],f)
