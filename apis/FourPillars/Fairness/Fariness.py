def analyse(model, training_dataset, test_dataset, factsheet, config): 
    from FourPillars.Fairness.Always.Overfitting.OverfittingScore import overfitting_score
    from FourPillars.Fairness.Always.Underfitting.UnderfittingScore import underfitting_score
    
    from FourPillars.Fairness.Conditional.StatisticalParityDifference.StatisticalParityDifferenceScore import statistical_parity_difference_score
    from FourPillars.Fairness.Conditional.EqualOpportunityDifference.EqualOpportunityDifferenceScore import equal_opportunity_difference_score
    from FourPillars.Fairness.Conditional.AverageOddsDifference.AverageOddsDifferenceScore import average_odds_difference_score
    from FourPillars.Fairness.Conditional.DisparateImpact.DisparateImpactScore import disparate_impact_score
    from FourPillars.Fairness.Always.ClassBalance.ClassBalanceScore import class_balance_score
    
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    """Triggers the fairness analysis and in a first step all fairness metrics get computed.
    In a second step, the scores for the fairness metrics are then created from
    mapping every metric value to a respective score.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.
        config: Config file containing the threshold values for the metrics.

    Returns:
        Returns a result object containing all metric scores
        and matching properties for every metric

    """
    import numpy as np
    np.random.seed(0)
    from scipy.stats import chisquare
    import operator
    import funcy
    statistical_parity_difference_thresholds = config["parameters"]["score_statistical_parity_difference"]["thresholds"]["value"]
    overfitting_thresholds = config["parameters"]["score_overfitting"]["thresholds"]["value"]
    underfitting_thresholds = config["parameters"]["score_underfitting"]["thresholds"]["value"]
    equal_opportunity_difference_thresholds = config["parameters"]["score_equal_opportunity_difference"]["thresholds"]["value"]
    average_odds_difference_thresholds = config["parameters"]["score_average_odds_difference"]["thresholds"]["value"]
    disparate_impact_thresholds = config["parameters"]["score_disparate_impact"]["thresholds"]["value"]
    
    output = dict(
        underfitting = underfitting_score(model, training_dataset, test_dataset, factsheet, underfitting_thresholds),
        overfitting = overfitting_score(model, training_dataset, test_dataset, factsheet, overfitting_thresholds),
        statistical_parity_difference = statistical_parity_difference_score(model, training_dataset, factsheet, statistical_parity_difference_thresholds),
        equal_opportunity_difference = equal_opportunity_difference_score(model, test_dataset, factsheet, equal_opportunity_difference_thresholds),
        average_odds_difference = average_odds_difference_score(model, test_dataset, factsheet, average_odds_difference_thresholds),
        disparate_impact = disparate_impact_score(model, test_dataset, factsheet, disparate_impact_thresholds),
        class_balance = class_balance_score(training_dataset, factsheet)
    )
    
    scores = dict((k, v.score) for k, v in output.items())
    properties = dict((k, v.properties) for k, v in output.items())

    return  result(score=scores, properties=properties)
    
