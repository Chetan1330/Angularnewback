def class_balance_score(training_data, factsheet):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    import numpy as np
    from .ClassBalanceMetric import class_balance_metric
    """Compute the class balance for the target_column
    If this fails np.nan is returned.

    Args:
        training_data: pd.DataFrame containing the used training data.
        target_column: name of the label column in the provided training data frame.

    Returns:
        On success, returns a score from 1 - 5 for the class balance.
        On failure, a score of np.nan together with an empty properties dictionary is returned.

    """
    try:
        class_balance = class_balance_metric(training_data, factsheet)
        properties = {}
        properties['Metric Description'] = "Measures how well the training data is balanced or unbalanced"
        properties['Depends on'] = 'Training Data'
        if(class_balance == 1):
            score = 5
        else:
            score = 1
        
        properties["Score"] = str(score)
        return result(score=score, properties=properties)     
    except Exception as e:
        print("ERROR in class_balance_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)}) 