from __future__ import absolute_import, division, print_function, unicode_literals
import pickle
import os
# Regular modules for data science and visualization:
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Keras (2.2.4) and tensorflow (1.13).
import tensorflow.compat.v1 as tf
import tensorflow_hub as hub
#import tf_sentencepiece

from keras.regularizers import l1, l2
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import backend
from keras import optimizers

#sklearn and imblearn modules:
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from imblearn.over_sampling import SMOTE

#Density:
print('Density')
p = 0.4
df = pd.read_csv('articles2.csv',header=None,skiprows=lambda i: 1>0 and random.random() > p)
print(df)
#First batch:
print('First Batch')
n_s_a = df[df[3] == 'Atlantic']
n_s_p = df[df[3] == 'New York Post']
#Second batch:
print('Second Batch')
df = pd.read_csv('articles1.csv',header=None,skiprows=lambda i: 1>0 and random.random() > p)
n_s_b = df[df[3] == 'Breitbart']
n_s_n = df[df[3] == 'New York Times']

n_s = list(n_s_b.iloc[:,9].values) + list(n_s_p.iloc[:,9].values) \
 + list(n_s_a.iloc[:,9].values) + list(n_s_n.iloc[:,9].values)

n_s = [word.replace('New York Post','') for word in n_s]
n_s = [word.replace('Breitbart','') for word in n_s]
n_s = [word.replace('New York Times','') for word in n_s]
n_s = [word.replace('Atlantic','') for word in n_s]

#Outlet classifier:
print('Outlet Classifier')
classes_All = np.asarray([1 for i in range(len(n_s_b))] + \
[2 for i in range(len(n_s_p))] + [3 for i in range(len(n_s_a))] + \
[4 for i in range(len(n_s_n))])
#Bias classifier:
print('Bias Classifier')
classes_Bias = np.asarray([1 for i in range(len(n_s_b))] + \
[1 for i in range(len(n_s_p))] + [2 for i in range(len(n_s_a))] + \
[2 for i in range(len(n_s_n))])

# Load the encoder:
print('Load Encoder')
g = tf.Graph()
with g.as_default():
  text_input = tf.placeholder(dtype=tf.string, shape=[None])
  embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-large/3")
  embedded_text = embed(text_input)
  init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
g.finalize()

# Initialize session:
print('Initialize session')
session = tf.Session(graph=g)
session.run(init_op)

#Function to compute all embeddings for each sentence:
#Be patient, takes a little while:
def similarity_matrix(merge_list):
    #initialize distance array:
    #initialize embeddings array:
    mergelen = len(merge_list)
    emb_all = np.zeros([mergelen,512])
    #Outer for loop:
    for i in range(0,mergelen):
        #print(str(i) + ' of ' + str(mergelen))
        #Here is where we run the previously started session, so it is important to run previous step succesfully:
        i_emb = session.run(embedded_text, feed_dict={text_input: [merge_list[i]]})
        emb_all[i,:] = i_emb
    save_emb = open("emb_all.pickle","wb")
    pickle.dump(emb_all, save_emb)
    save_emb.close()
    return emb_all

#Choose optimizer:
optim = optimizers.Adam(lr=0.00015) 

# create NN for news clissification:
print('Create NN for news')
news_DNN = Sequential()
news_DNN.add(Dense(40, input_dim=512, activation = 'relu',kernel_regularizer=l2(0.1)))
news_DNN.add(Dropout(0.25))
news_DNN.add(Dense(40, activation = 'relu',kernel_regularizer=l2(0.1)))
news_DNN.add(Dropout(0.25))


# Output layer with multiclass activation function:
print('Output layer with multiclass activation function')
news_DNN.add(Dense(4,activation='softmax'))

# Compile model:
print('Compile model')
news_DNN.compile(loss='sparse_categorical_crossentropy', optimizer=optim, metrics=['acc'])

# split into shuffled folds:
#Note that you should edit the class array accordingly: Bias (classes_Bias) or Outlet (classes_All)
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.33) # chose one split to make analysis faster. change it if required
#emb_pickle = open("emb_all.pickle", "rb")
#eAll = pickle.load(emb_pickle)
#emb_pickle.close()
scaler = StandardScaler()

eAll = similarity_matrix(n_s)
for t, te in sss.split(eAll,classes_Bias):
  # Scale the data with StandardScaler before splitting:
    X_train, X_test = scaler.fit_transform(eAll)[t], \
    scaler.fit_transform(eAll)[te]

    y_train, y_test = classes_All[t]-1,classes_All[te]-1


#fit the network. You can change parameters to see how this affects your training.
print('Fitting neural network')

checkpoint_path = "cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

m_h = news_DNN.fit(X_train, y_train, epochs=400, \
validation_data=(X_test, y_test),callbacks=[cp_callback],batch_size=32, verbose=1)

# Plot accuracy curves:
with sns.color_palette("Accent", n_colors=8):
    plt.figure(figsize=(8,6))
    sns.lineplot(data=np.asarray(m_h.history['acc']))
    sns.lineplot(data=np.asarray(m_h.history['val_acc']))
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.title("Accuracy for Media Bias Classification") # change title here
    plt.legend(labels=['training', 'validation'],loc='lower right')
    plt.text(330,0.755,'val Ac = ' + str(round(np.compressaccuracy_score(y_test,model.predict_classes(X_test)),2))) 
    plt.savefig('outlets_bias_acc.svg',format='svg') # edit file title here


# Plot loss curves:
with sns.color_palette("Accent", n_colors=8):
    plt.figure(figsize=(8,6))
    sns.lineplot(data=np.asarray(m_h.history['loss']))
    sns.lineplot(data=np.asarray(m_h.history['loss']))
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Loss functions for Media Bias Classification") #change title here
    plt.legend(labels=['training', 'validation'])
    plt.savefig('outlets_bias_loss.svg',format='SVG') # edit file title here
