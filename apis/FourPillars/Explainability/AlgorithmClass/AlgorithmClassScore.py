
def algorithm_class_score(clf, clf_type_score):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    import numpy as np
    clf_name = type(clf).__name__
    exp_score = clf_type_score.get(clf_name,np.nan)
    properties= {"dep" :info('Depends on','Model'),
        "clf_name": info("model type",clf_name)}
    
    return  result(score=exp_score, properties=properties)