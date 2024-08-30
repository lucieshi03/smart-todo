# TEXT CLASSIFICATION ML MODEL

# website: dylancastillo


# import required libraries
import joblib #saves model artifacts(output created by training process)
import re # re and string processes the text
import string
import pickle

import numpy as np # numpy and pandas read and transform the data
import pandas as pd

# from sklearn.datasets import fetch_20newsgroups (I HAVE MY OWN DATASET)
from sklearn.feature_extraction.text import CountVectorizer #used for bag of words
from sklearn.metrics import classification_report #used for training
from sklearn.model_selection import train_test_split #used
from sklearn.naive_bayes import MultinomialNB #used for training


# load data
data = pd.read_csv('data.csv')

# extract text part of csv
task_to_be_classified = data['text']

# clean up text
# define stopwords
stopwords = set(["the", "a", "to", "from", "and", "in", "on", "at", "with", "for", "by", "of", "this", "that"])

def clean_up(task_to_be_classified) :
    # lowercase
    task_to_be_classified = str(task_to_be_classified).lower()

    # remove punctuation
    task_to_be_classified = re.sub(f'[{string.punctuation}]', '', task_to_be_classified)

    #remove digits
    task_to_be_classified = re.sub(r'\d+', '', task_to_be_classified)

    #remove stopwords
    task_to_be_classified = ' '.join([word for word in task_to_be_classified.split() if word not in stopwords])

    return task_to_be_classified

# apply fct to text
data['cleaned_text'] = data['text'].apply(clean_up)

# split data (training and testing)
x = data['cleaned_text']
y = data['category']

# note: 0.2 means that 20% of the data is used for testing and 80% for training
# note: setting random_state ensures that split is reproducible (you get same training/testing sets each time you run), its like seed for math.random
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# create bag of words (turn text into numerical values)
# initialize the CountVectorizer
vec = CountVectorizer(
    ngram_range=(1, 3), # will consider unigrams, bigrams, and trigrams
    stop_words="english", # removes common English stopwords DID I NEED TO LIST STOPWORDS ABOVE?
)

# fit and transform the training data
# fitting: learning from data
# transforming: apply what was learned
x_train = vec.fit_transform(x_train)
x_test = vec.transform(x_test)

'''
!! target variables (already split)
y_train = y_train
y_test = y_test
'''

# train the model
# use instance of 'MultinomialNB' classifier and fit it to the training data

#initialize Naive Bayes model
nb = MultinomialNB()

# train
nb.fit(x_train, y_train)

# compute precision, recall, and f1 scores
# predict category for test data
preds = nb.predict(x_test)

# print classification report
# print(classification_report(y_test, preds))

# save model
joblib.dump(nb, 'nb.joblib') # joblib.dump or pickle.dump??

# save vectorizer
joblib.dump(vec, 'vec.joblib')


# TESTING
'''
nb_saved = joblib.load("nb.joblib")
vec_saved = joblib.load("vec.joblib")

sample_text = ["Study for exam."]
cleaned_sample_text = clean_up(sample_text)
sample_vec = vec_saved.transform(sample_text)
predicted_category = nb_saved.predict(sample_vec)


print(f"The result is: {predicted_category}")
'''