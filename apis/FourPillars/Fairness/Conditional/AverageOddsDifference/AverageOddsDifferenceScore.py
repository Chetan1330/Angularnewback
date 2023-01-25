def average_odds_difference_score(model, test_dataset, factsheet, thresholds):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from ...HelperFunctions.FalsePositiveRates import false_positive_rates
    from ...HelperFunctions.TruePositiveRates import true_positive_rates
    """This function computes the average odds difference score.
    It subtracts the true positive rate of the unprotected group from
    the true positive rate of the protected group. 
    The same is done for the false positive rates.
    An equally weighted average is formed out of these two differences.
    This is then mapped to a score from one to five using the given thresholds.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        A score from one to five representing how fair the calculated
        average odds metric is.
        5 means that the metric is very fair/ low.
        1 means that the metric is very unfair/ high.

    """
    try:
        score = np.nan
        properties = {}
        properties["Metric Description"] = "Is the average of difference in false positive rates and true positive rates between the protected and unprotected group"
        properties["Depends on"] = "Model, Test Data, Factsheet (Definition of Protected Group and Favorable Outcome)"
        
        fpr_protected, fpr_unprotected, fpr_properties = false_positive_rates(model, test_dataset, factsheet)
        tpr_protected, tpr_unprotected, tpr_properties = true_positive_rates(model, test_dataset, factsheet)
            
        properties["----------"] = ''
        properties = properties|fpr_properties
        properties = properties|tpr_properties
        properties['-----------'] = ''
        
        average_odds_difference = abs(((tpr_protected - tpr_unprotected) + (fpr_protected - fpr_unprotected))/2)
        properties["Formula"] = "Average Odds Difference = |0.5*(TPR Protected - TPR Unprotected) + 0.5*(FPR Protected - FPR Unprotected)|"
        properties["Average Odds Difference"] = "{:.2f}%".format(average_odds_difference*100)
        
        score = np.digitize(abs(average_odds_difference), thresholds, right=False) + 1 
        
        properties["Score"] = str(score)   
        return result(score=int(score), properties=properties) 
    except Exception as e:
        print("ERROR in average_odds_difference_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)})