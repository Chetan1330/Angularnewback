def feature_relevance_score(clf, train_data, target_column=None, threshold_outlier = 0.03, penalty_outlier = 0.5, thresholds = [0.05, 0.1, 0.2, 0.3]):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    import pandas as pd
    import numpy as np
    pd.options.mode.chained_assignment = None  
    train_data = train_data.copy()
    if target_column:
        X_train = train_data.drop(target_column, axis=1)
        y_train = train_data[target_column]
    else:
        X_train = train_data.iloc[:,:-1]
        y_train = train_data.iloc[:,-1: ]
        
    scale_factor = 1.5
    distri_threshold = 0.6
    if (type(clf).__name__ == 'LogisticRegression') or (type(clf).__name__ == 'LinearRegression'): 
        #normalize 
        #for feature in X_train.columns:
        #    X_train.loc[feature] = X_train[feature] / X_train[feature].std()
        clf.max_iter =1000
        clf.fit(X_train, y_train.values.ravel())
        importance = clf.coef_[0]
        #pd.DataFrame(columns=feat_labels,data=importance.reshape(1,len(importance))).plot.bar()
        
    elif  (type(clf).__name__ == 'RandomForestClassifier') or (type(clf).__name__ == 'DecisionTreeClassifier'):
         importance=clf.feature_importances_
         
    else:
        return result(score= np.nan, properties={"dep" :info('Depends on','Training Data and Model')}) 
   
    # absolut values
    importance = abs(importance)
    
    feat_labels = X_train.columns
    indices = np.argsort(importance)[::-1]
    feat_labels = feat_labels[indices]

    importance = importance[indices]
    
    # calculate quantiles for outlier detection
    q1, q2, q3 = np.percentile(importance, [25, 50 ,75])
    lower_threshold , upper_threshold = q1 - scale_factor*(q3-q1),  q3 + scale_factor*(q3-q1) 
    
    #get the number of outliers defined by the two thresholds
    n_outliers = sum(map(lambda x: (x < lower_threshold) or (x > upper_threshold), importance))
    
    # percentage of features that concentrate distri_threshold percent of all importance
    pct_dist = sum(np.cumsum(importance) < 0.6) / len(importance)
    
    dist_score = np.digitize(pct_dist, thresholds, right=False) + 1 
    
    if n_outliers/len(importance) >= threshold_outlier:
        dist_score -= penalty_outlier
    
    score =  max(dist_score,1)
    properties = {"dep" :info('Depends on','Training Data and Model'),
        "n_outliers":  info("number of outliers in the importance distribution",int(n_outliers)),
                  "pct_dist":  info("percentage of feature that make up over 60% of all features importance", "{:.2f}%".format(100*pct_dist)),
                  "importance":  info("feature importance", {"value": list(importance), "labels": list(feat_labels)})
                  }
    
    return result(score=int(score), properties=properties)