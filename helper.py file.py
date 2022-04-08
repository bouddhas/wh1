#helper functions – helper.py file
import shap
import pickle

# score new data
def score_record(data, clf):

    return clf.predict(data)[0], clf.predict_proba(data)[:,1][0]