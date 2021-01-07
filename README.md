# Sentiment Time-Series Prediction in Twitter with LSTM 

Project support Python 3.6.x+
Note: It is recommended to use Anaconda distribution of Python.

*NOTE Please extract csvData to your Directory
## **

### 1. Run GUI.py -> Authenticate using twitter developer account. 


### 2. Insert a Hashtag that you want to predict 
       Note : It is recommended to use hot topics.
       
       If you want to run **LSTM only** please Insert Hashtag and select 'Run LSTM Only ' -> And skip to step #5
       *NOTE : You must have the following path : 'predict_yourInput_hashtag_tweets.csv'
       

### 3. Set duration for fetching tweets 
       Note : The more data, the better prediction


### 4. Select Run -> 

   * Fetching Tweets 
   Produce csv : yourInput_hashtag_tweets.csv
   
   * Preprocessing
   Preprocessing the data
   Produce csv : preprocess_yourInput_hashtag_tweets.csv
   
   * NLP
   Using NLP feature extraction,countvectorizer,stop words ...
   Builds a ML using linear SVM algorithm
   Produce csv : yourInput_hashtag_tweets_pred
   
   
### 5. Select percentage for prediction & Select Stationary/Non-Stationary Data
       Example : 10% Out of 24 hours will be 2.4 hours -> 2 hours prediction.
  
   
### 6. Select Start -> 

   #### LSTM  :
   
   * Time-Series
   Creating stationary data by smoothing trends. replacing NaN values with Moving average algorithm 
   Produce csv : predict_yourInput_hashtag_tweets.csv
   CSV contains number of positive,negative tweets. if time was NaN - cells will be empty.
   
   * LSTM
   Building a neural network using LSTM units.
   Produce CSV : train_predict_yourInput_hashtag_tweets
   
   NOTE :   Each Date will plot time-series graph 
   
   
