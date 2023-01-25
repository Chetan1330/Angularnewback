def regularization_score(model, training_dataset, test_dataset, factsheet, methodology_config):
    import numpy as np
    from .RegularizationMetric import regularization_metric
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    score = 1
    regularization = regularization_metric(factsheet)
    properties = {"dep" :info('Depends on','Factsheet'),
        "regularization_technique": info("Regularization technique", regularization)}
    NOT_SPECIFIED = "not specified"

    if regularization == "elasticnet_regression":
        score = 5
    elif regularization == "lasso_regression" or regularization == "lasso_regression":
        score = 4
    elif regularization == "Other":
        score = 3
    elif regularization == NOT_SPECIFIED:
        score = np.nan
    else:
        score = 1
    return result(score=score, properties=properties)
