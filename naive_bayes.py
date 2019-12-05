"""
Description: Naive Bayes Model
Authors: Diptanu Sarkar, ds9297@rit.edu

Dependencies:
        1. Python libraries
"""

# Importing python3 libraries for the project
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


def process_input_dataset(file):
    """
    To process the input dataset.
    :param file:
    :return: None
    """
    dataset = pd.read_excel(file)
    dataset.dropna(subset=["Data", "Language"], inplace=True)
    print(dataset.groupby("Language")["Data"].nunique())
    X = dataset.iloc[:, 0].values
    y = dataset.iloc[:, 1].values
    return X, y


def fit_transform_data(X, y, max_features=1500, test_size=0.20):
    """
    To split and apply count vectorizer to the test and train data.
    :param X:
    :param y:
    :param max_features:
    :param test_size:
    :return:
    """
    cv = CountVectorizer(max_features=max_features)
    X = cv.fit_transform(X).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test


def naive_bayes_classifier(X_train, y_train):
    """
    The naive bayes classifier.
    :param X_train:
    :param y_train:
    :return:
    """
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    return classifier


def predict(classifier, X_test, y_test):
    """
    To predict and display the confusion matrix and accuracy of
    the model.
    :param classifier:
    :param X_test:
    :param y_test:
    :return:
    """
    y_pred = classifier.predict(X_test)
    print("\n")
    print("Accuracy :", accuracy_score(y_test, y_pred) * 100)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    return cm


def main():
    """
    The main method to run the program.
    :return: None
    """
    try:
        no_of_features = 2000
        X, y = process_input_dataset("wiki_data_10K words.xls")
        X_train, X_test, y_train, y_test = fit_transform_data(X, y, no_of_features, 0.20)
        classifier = naive_bayes_classifier(X_train, y_train)
        predict(classifier, X_test, y_test)
    except Exception as e:
        print("ERROR: An exception occurred: " + str(e))
        exit
    finally:
        print("MESSAGE: Everything successfully executed.")


# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()