import numpy as np
from sklearn import svm, datasets
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load



def load_crime_data(csv_path):
    crime_csv = pd.read_csv(csv_path, encoding='encoding')
    crime_df = pd.DataFrame(crime_csv)
    # df_vals = crime_df.columns.values
    lats = np.array(crime_df['LATITUDE'])
    longs = np.array(crime_df['LONGITUDE'])
    X = np.concatenate(lats, longs, axis=0)
    enc = LabelEncoder()
    enc.fit(crime_df['CATEGORIE'])
    y = enc.transform(crime_df['CATEGORIE'])
    enc = LabelEncoder()
    crime_df['QUART'] = enc.fit(crime_df['QUART'])
    return X, y


def learning(X, y):
    clf = svm.SVC(kernel='rbf', gamma=0.7, C=1.0)
    clf.fit(X, y)
    dump(clf, 'crime_clf.joblib')
    return clf


if __name__ == '__main__':
    crime_csv_path = '/home/alex/Documents/CODING/2018/Hackatown/csv_data/crimes.csv'
    X, y = load_crime_data(crime_csv_path)
    clf = learning(X, y)

    print(clf.predict(np.array([[1, 9]])))

