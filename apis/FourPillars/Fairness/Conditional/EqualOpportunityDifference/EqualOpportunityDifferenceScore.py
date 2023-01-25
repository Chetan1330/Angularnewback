from ...HelperFunctions.TruePositiveRates import true_positive_rates


def equal_opportunity_difference_score(model, test_dataset, factsheet, thresholds):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    """This function computes the equal opportunity difference score.
    It subtracts the true positive rate of the unprotected group from
    the true positive rate of the protected group.
    This is then mapped to a score from one to five using the given thresholds.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        A score from one to five representing how fair the calculated
        equal opportunity metric is.
        5 means that the metric is very fair/ low.
        1 means that the metric is very unfair/ high.

    """
    try:
        properties = {}
        score=np.nan
        properties["Metric Description"] = "Difference in true positive rates between protected and unprotected group."
        properties["Depends on"] = "Model, Test Data, Factsheet (Definition of Protected Group and Favorable Outcome)"
        tpr_protected, tpr_unprotected, tpr_properties = true_positive_rates(model, test_dataset, factsheet)
        
        properties['----------'] = ''
        properties = properties|tpr_properties 
        equal_opportunity_difference = abs(tpr_protected - tpr_unprotected)
        properties['-----------'] = ''
        
        properties["Formula"] = "Equal Opportunity Difference = |TPR Protected Group - TPR Unprotected Group|"
        properties["Equal Opportunity Difference"] = "{:.2f}%".format(equal_opportunity_difference*100)

        score = np.digitize(abs(equal_opportunity_difference), thresholds, right=False) + 1 
        
        properties["Score"] = str(score)
        return result(score=int(score), properties=properties) 
    except Exception as e:
        print("ERROR in equal_opportunity_difference_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)})
