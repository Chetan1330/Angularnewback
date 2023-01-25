# === Explainability ===
import numpy as np
import pandas as pd
import json
import collections
from .AlgorithmClass.AlgorithmClassScore import algorithm_class_score

from .CorrelatedFeatures.CorrelatedFeaturesScore import correlated_features_score
from .FeatureRelevance.FeatureRelevanceScore import feature_relevance_score
from .ModelSize.ModelSizeScore import model_size_score

result = collections.namedtuple('result', 'score properties')
info = collections.namedtuple('info', 'description value')


def analyse(clf, train_data, test_data, config, factsheet):
    #convert path data to values
    solution=pd.read_pickle(clf)
    train_data=pd.read_csv(train_data)
    test_data=pd.read_csv(test_data)
    config=pd.read_json(config)

    factsheet=pd.read_json(factsheet)
    #function parameters
    target_column = factsheet["general"].get("target_column")
    clf_type_score = config["parameters"]["score_algorithm_class"]["clf_type_score"]["value"]
    ms_thresholds = config["parameters"]["score_model_size"]["thresholds"]["value"]
    cf_thresholds = config["parameters"]["score_correlated_features"]["thresholds"]["value"]
    high_cor = config["parameters"]["score_correlated_features"]["high_cor"]["value"]
    fr_thresholds = config["parameters"]["score_feature_relevance"]["thresholds"]["value"]
    threshold_outlier = config["parameters"]["score_feature_relevance"]["threshold_outlier"]["value"]
    penalty_outlier = config["parameters"]["score_feature_relevance"]["penalty_outlier"]["value"]
    
    output = dict(
        algorithm_class     = algorithm_class_score(clf, clf_type_score),
        correlated_features = correlated_features_score(train_data, test_data, thresholds=cf_thresholds, target_column=target_column, high_cor=high_cor ),
        model_size          = model_size_score(train_data, ms_thresholds),
        feature_relevance   = feature_relevance_score(clf, train_data ,target_column=target_column, thresholds=fr_thresholds,
                                                     threshold_outlier =threshold_outlier,penalty_outlier=penalty_outlier )
                 )

    scores = dict((k, v.score) for k, v in output.items())
    properties = dict((k, v.properties) for k, v in output.items())
    
    return  result(score=scores, properties=properties)







