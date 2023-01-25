def statistical_parity_difference_score(model, training_dataset, factsheet, thresholds):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from .StatisticalParityDifferenceMetric import statistical_parity_difference_metric

    """This function scores the computed statistical parity difference
    on a scale from 1 (very bad) to 5 (very good)

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        factsheet: json document containing all information about the particular solution.
        thresholds: Threshold values used to determine the final score

    Returns:
        A score from one to five representing how fair the calculated
        statistical parity differnce is.
        5 means that the statistical parity difference is very fair/ low.
        1 means that the statistical parity difference is very unfair/ high.

    """
    try: 
        
        score = np.nan
        properties = {}
        properties["Metric Description"] = "The spread between the percentage of observations from the majority group receiving a favorable outcome compared to the protected group. The closes this spread is to zero the better."
        properties["Depends on"] = "Training Data, Factsheet (Definition of Protected Group and Favorable Outcome)"
        statistical_parity_difference, spdm_properties = statistical_parity_difference_metric(model, training_dataset, factsheet)

        properties['----------'] = ''
        properties = properties|spdm_properties
        properties['-----------'] = ''
        properties["Formula"] =  "Statistical Parity Difference = |Favored Protected Group Ratio - Favored Unprotected Group Ratio|"
        properties["Statistical Parity Difference"] = "{:.2f}%".format(statistical_parity_difference*100)
        
        score = np.digitize(abs(statistical_parity_difference), thresholds, right=False) + 1 
        
        properties["Score"] = str(score)
        return result(score=int(score), properties=properties)
    except Exception as e:
        print("ERROR in statistical_parity_difference_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)})