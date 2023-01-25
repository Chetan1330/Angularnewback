def disparate_impact_score(model, test_dataset, factsheet, thresholds):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from .DisparateImpactMetric import disparate_impact_metric

    
    """This function computes the disparate impact score.
    It divides the ratio of favored people within the protected group by
    the ratio of favored people within the unprotected group in order
    to receive the disparate impact ratio.
    This is then mapped to a score from one to five using the given thresholds.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        A score from one to five representing how fair the calculated
        disparate impact metric is.
        5 means that the disparate impact metric is very fair/ low.
        1 means that the disparate impact metric is very unfair/ high.

    """
    try:
        score = np.nan
        properties = {}
        properties["Metric Description"] = "Is quotient of the ratio of samples from the protected group receiving a favorable prediction divided by the ratio of samples from the unprotected group receiving a favorable prediction"
        properties["Depends on"] = "Model, Test Data, Factsheet (Definition of Protected Group and Favorable Outcome)"
        disparate_impact, dim_properties = disparate_impact_metric(model, test_dataset, factsheet)
        
        properties["----------"] = ''
        properties = properties|dim_properties
        properties['-----------'] = ''
        
        properties["Formula"] = "Disparate Impact = Protected Favored Ratio / Unprotected Favored Ratio"
        properties["Disparate Impact"] = "{:.2f}".format(disparate_impact)

        score = np.digitize(disparate_impact, thresholds, right=False)+1
            
        properties["Score"] = str(score)
        return result(score=int(score), properties=properties) 
    except Exception as e:
        print("ERROR in disparate_impact_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)})


