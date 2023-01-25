def analyse(model, train_data, test_data, config, factsheet):
    import numpy as np
    import collections
    import random
    import sklearn.metrics as metrics
    from art.attacks.evasion import FastGradientMethod, CarliniL2Method, DeepFool
    from art.estimators.classification import SklearnClassifier
    from sklearn.preprocessing import OneHotEncoder
    from art.metrics import clever_u, RobustnessVerificationTreeModelsCliqueMethod
    from art.estimators.classification import KerasClassifier
    from art.metrics import loss_sensitivity
    import tensorflow as tf
    import numpy.linalg as la
    import json

    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from FourPillars.Robustness.ConfidenceScore.ConfidenceScore import confidence_score
    from FourPillars.Robustness.CleverScore.CleverScore import clever_score
    from FourPillars.Robustness.CliqueMethod.CliqueMethodScore import clique_method
    from FourPillars.Robustness.LossSensitivity.LossSensitivityScore import loss_sensitivity_score
    from FourPillars.Robustness.ERFastGradientMethod.FastGradientAttackScore import fast_gradient_attack_score
    from FourPillars.Robustness.ERCWAttack.CarliWagnerAttackScore import carlini_wagner_attack_score
    from FourPillars.Robustness.ERDeepFool.DeepFoolAttackScore import deepfool_attack_score
    """Reads the thresholds from the config file.
    Calls all robustness metric functions with correct arguments.
    Organizes all robustness metrics in a dict. Then returns the scores and the properties.
        Args:
            model: ML-model.
            training_dataset: pd.DataFrame containing the used training data.
            test_dataset: pd.DataFrame containing the used test data.
            config: Config file containing the threshold values for the metrics.
            factsheet: json document containing all information about the particular solution.

        Returns:
            Returns a result object containing all metric scores
            and matching properties for every metric
    """

    clique_method_thresholds = config["parameters"]["score_clique_method"]["thresholds"]["value"]
    clever_score_thresholds = config["parameters"]["score_clever_score"]["thresholds"]["value"]
    loss_sensitivity_thresholds = config["parameters"]["score_loss_sensitivity"]["thresholds"]["value"]
    confidence_score_thresholds = config["parameters"]["score_confidence_score"]["thresholds"]["value"]
    fsg_attack_thresholds = config["parameters"]["score_fast_gradient_attack"]["thresholds"]["value"]
    cw_attack_thresholds = config["parameters"]["score_carlini_wagner_attack"]["thresholds"]["value"]
    deepfool_thresholds = config["parameters"]["score_carlini_wagner_attack"]["thresholds"]["value"]
    
    output = dict(
        confidence_score   = confidence_score(model, train_data, test_data, confidence_score_thresholds),
        clique_method      = clique_method(model, train_data, test_data, clique_method_thresholds, factsheet ),
        loss_sensitivity   = loss_sensitivity_score(model, train_data, test_data, loss_sensitivity_thresholds),
        clever_score       = clever_score(model, train_data, test_data, clever_score_thresholds),
        er_fast_gradient_attack = fast_gradient_attack_score(model, train_data, test_data, fsg_attack_thresholds),
        er_carlini_wagner_attack = carlini_wagner_attack_score(model, train_data, test_data, cw_attack_thresholds),
        er_deepfool_attack = deepfool_attack_score(model, train_data, test_data, deepfool_thresholds)
    )
    scores = dict((k, v.score) for k, v in output.items())
    properties = dict((k, v.properties) for k, v in output.items())
    
    return  result(score=scores, properties=properties)





