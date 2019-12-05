"""
Description: Neural Network for Language Identification
Authors: Diptanu Sarkar, ds9297@rit.edu, Saral Nyathawada, sn5409@rit.edu
"""

import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def main():

    #File used to train the neural network
    filename = "../wiki_data_10KCharacters.xls"
    data = pd.read_csv(filename)
    # Assign data from first column to X variable
    X = data.iloc[:, 0:1]
    # Assign data from class column to Y variable
    Y = data.iloc[:, 1:2]
    #print(Y.Language.unique())
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20)

    # create a count vectorizer object
    #tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    #tfidf_vect.fit(X['Data'])
    
    # create a count vectorizer object
    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(X['Data'])
    # transform the training and validation data using count vectorizer object
    xtrain_count = count_vect.transform(X_train['Data'])
    xvalid_count = count_vect.transform(X_test['Data'])
    #Use mlp neural network classifier to train and fit
    mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
    mlp.fit(xtrain_count, y_train.values.ravel())
    #Make predictions on the given data
    predictions = mlp.predict(xvalid_count)
    #Print confusion matrix and classification report
    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))



# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()