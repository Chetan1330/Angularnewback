def correlated_features_score(train_data, test_data, thresholds=[0.05, 0.16, 0.28, 0.4], target_column=None, high_cor=0.9):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    import pandas as pd
    import numpy as np

    test_data = test_data.copy()
    train_data = train_data.copy()
     
    if target_column:
        X_test = test_data.drop(target_column, axis=1)
        X_train = train_data.drop(target_column, axis=1)
    else:
        X_test = test_data.iloc[:,:-1]
        X_train = train_data.iloc[:,:-1]
        
    
    df_comb = pd.concat([X_test, X_train])
    corr_matrix = df_comb.corr().abs()

    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool_))
    
    # Find features with correlation greater than 0.95
    to_drop = [column for column in upper.columns if any(upper[column] > high_cor)]
    
    pct_drop = len(to_drop)/len(df_comb.columns)
    
    bins = thresholds
    score = 5-np.digitize(pct_drop, bins, right=True) 
    properties= {"dep" :info('Depends on','Training Data'),
        "pct_drop" : info("Percentage of highly correlated features", "{:.2f}%".format(100*pct_drop))}
    
    return  result(score=int(score), properties=properties)
