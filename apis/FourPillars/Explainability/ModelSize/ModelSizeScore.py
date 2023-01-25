import numpy as np
def model_size_score(test_data, thresholds = np.array([10,30,100,500])):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    import numpy as np
    dist_score = 5- np.digitize(test_data.shape[1]-1 , thresholds, right=True) 
         
    return result(score=int(dist_score), properties={"dep" :info('Depends on','Training Data'),
        "n_features": info("number of features", test_data.shape[1]-1)})
