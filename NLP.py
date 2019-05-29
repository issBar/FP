# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 01:15:32 2019

@author: itsba
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import sys
import pickle
# Cleaning the texts
import re
import nltk
from nltk import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import sentiwordnet as swn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import sklearn.cross_validation as cross_validation


SAVE_FILENAME= './pickle/sentiment_analysis_finalized_model.sav'


#load a finalized machine from a pickle file
def load_sentiment_analysis_finalized_m(filename):
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model    


def get_list_of_sentences(in_data,size):
    dataset = []
    for i in range(size):
        review = str(in_data['Tweets'][i])
        review = review.split()
        review = ' '.join(review)
        dataset.append(review)
    return dataset


def run_natural_language_processing(inquery,flag):
    print("starting function run_natural_language_processing\n")
    # Importing the dataset
    big_dataset = pd.read_csv('./csvData/preprocess_dataset_sample.csv')
    selected_tweets= pd.read_csv('./csvData/'+inquery+'/preprocess_'+inquery+'_hashtag_tweets.csv')
    
    dataset_size=big_dataset.shape[0] #size of pp Dataset
    tweets_data_size=selected_tweets.shape[0] #size of fetched pp Tweets
    
    #list of tweets of each data
    X_big_dataset = get_list_of_sentences(big_dataset,dataset_size)
    X_selected_tweets=get_list_of_sentences(selected_tweets,tweets_data_size)
    
      
    #Load an existing trained pickle file
    if flag==True:
        
        try:
            loaded_model = pickle.load(open(SAVE_FILENAME, 'rb'))
            print("pickle loaded successfully")
            y_pred=loaded_model.predict(X_selected_tweets)
            
            print(y_pred)
        except (FileNotFoundError ,IOError):
            print("Error loading file")
    
      

        
    #mechine learning SVM  using straified kfold which divided to 10  
    else:
        Y_big_dataset=big_dataset.iloc[:, 0].values
        
        X_big_dataset=np.array(X_big_dataset)
        #X_train,X_test,y_train_y_test=train_test_split(X_big_dataset, Y_big_dataset, train_size=0.75,test_size=0.25, random_state=101)
        clf_score_list=[]
        cv_features_name_list=[]
        k_folds=StratifiedKFold(n_splits=10,shuffle=True,random_state=None)
        for train_big_dataset,test_big_dataset in k_folds.split(X_big_dataset,Y_big_dataset):
            X_train = X_big_dataset[train_big_dataset]
            X_test = X_big_dataset[test_big_dataset]
            y_train = Y_big_dataset[train_big_dataset]
            y_test = Y_big_dataset[test_big_dataset]
            
            #Created a pipeline which uses countverctorizer on any word  and we apply linear SVM classifier on the matrix
            clf=Pipeline([('vectorizer', CountVectorizer(analyzer="word",ngram_range=(1,2),tokenizer=word_tokenize, max_features=10000)),('classifier',LinearSVC())])
            clf.fit(X_train,y_train)
            clf_score_list.append(clf.score(X_test,y_test))
            cv_features_name_list.append(clf.named_steps['vectorizer'].get_feature_names())
        y_pred=clf.predict(X_selected_tweets)
        print("Svm Score =",clf_score_list)
        print("AVG accuracy svm= ",sum(clf_score_list)/10)
        
        #save score predicition 
        try:
            filename = './pickle/sentiment_score.txt'
            with open(filename,'w') as textfile:
                textfile.write(sum(clf_score_list)/10)    
                
        except (FileNotFoundError ,IOError):
            print("No file was found")
        
        #save sentiment analysis finalized model 
        try:
            filename = './pickle/sentiment_analysis_finalized_model.sav'
            pickle.dump(clf, open(filename, 'wb'))
            print("Saved sentiment_analysis_finalized_model.sav file")
        except (FileNotFoundError ,IOError):
            print("No file was found")
       
            
        
    #save prediction to csv file
    index=0 
    with open("./csvData/"+inquery+"/"+inquery+"_hashtag_tweets_pred.csv", 'w',encoding="utf-8") as csvfile:
        fieldnames=['Predict','Date','Tweets']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i  in range(tweets_data_size):
            writer.writerow({'Predict':y_pred[index],'Date':selected_tweets['Date'][i],'Tweets':selected_tweets['Tweets'][i]})
            index+=1
        print ('\nSaved prediction for tweets to: preprocess_'+inquery+'_hashtag_tweets_pred.csv\n')

    
#run_natural_language_processing("gameofthrones",True)    
    