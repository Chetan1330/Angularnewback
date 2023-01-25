from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def analyse(model, training_dataset, test_dataset, factsheet, methodology_config):
    import collections
    info = collections.namedtuple('info', 'description value')
    import json
    import os
    import numpy as np
    import collections
    from FourPillars.helperfunctions import list_of_metrics
    from FourPillars.Accountability.FactSheetCompletness.FactSheetCompletnessScore import get_factsheet_completeness_score
    from FourPillars.Accountability.MissingData.MissingDataScore import missing_data_score
    from FourPillars.Accountability.Normalization.NormalizationScore import normalization_score
    from FourPillars.Accountability.Regularization.RegularizationScore import regularization_score
    from FourPillars.Accountability.TrainTestSplit.TrainTestSplitScore import train_test_split_score
    import tensorflow as tf
    from math import isclose
    import re
    result = collections.namedtuple('result', 'score properties')
    normalization_mapping = methodology_config["parameters"]["score_normalization"]["mappings"]["value"]
    missing_data_mapping = methodology_config["parameters"]["score_missing_data"]["mappings"]["value"]
    train_test_split_mapping = methodology_config["parameters"]["score_train_test_split"]["mappings"]["value"]

    metrics = list_of_metrics("methodology")
    output = dict(
        #output[metric] = exec("%s_score(model, training_dataset, test_dataset, factsheet, methodology_config)" % metric)
        normalization  = normalization_score(model, training_dataset, test_dataset, factsheet, normalization_mapping),
        missing_data = missing_data_score(model, training_dataset, test_dataset, factsheet, missing_data_mapping),
        regularization   = regularization_score(model, training_dataset, test_dataset, factsheet, methodology_config),
        train_test_split = train_test_split_score(model, training_dataset, test_dataset, factsheet, train_test_split_mapping),
        #test_accuracy = test_accuracy_score(model, training_dataset, test_dataset, factsheet, accuracy_thresholds),
        #f1_score = f1_score(model, training_dataset, test_dataset, factsheet, f1_score_thresholds),
        factsheet_completeness= get_factsheet_completeness_score(model, training_dataset, test_dataset, factsheet, methodology_config)
    )

    scores = dict((k, v.score) for k, v in output.items())
    properties = dict((k, v.properties) for k, v in output.items())
    
    return  result(score=scores, properties=properties)

path_testdata=os.path.join(BASE_DIR,'apis/TestValues/test.csv')
path_traindata=os.path.join(BASE_DIR,'apis/TestValues/train.csv')
path_module=os.path.join(BASE_DIR,'apis/TestValues/model.pkl')
path_factsheet=os.path.join(BASE_DIR,'apis/TestValues/factsheet.json')
path_mapping_accountabiltiy=os.path.join(BASE_DIR,'apis/MappingsWeightsMetrics/Mappings/Accountability/default.json')
print(analyse(path_module,path_traindata,path_testdata,path_factsheet,path_mapping_accountabiltiy))
