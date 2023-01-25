
def train_test_split_score(model, training_dataset, test_dataset, factsheet, mappings):
    from .TrainTestSplitMetric import train_test_split_metric    
    import collections
    import re
    import numpy as np
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    try:
        training_data_ratio, test_data_ratio = train_test_split_metric(training_dataset, test_dataset)
        properties= {"dep" :info('Depends on','Training and Testing Data'),
            "train_test_split": info("Train test split", "{:.2f}/{:.2f}".format(training_data_ratio, test_data_ratio))}
        for k in mappings.keys():
            thresholds = re.findall(r'\d+-\d+', k)
            for boundary in thresholds:
                [a, b] = boundary.split("-")
                if training_data_ratio >= int(a) and training_data_ratio < int(b):
                    score = mappings[k]
        return result(score=score, properties=properties)
    except Exception as e:
        print(e)
        return result(score=np.nan, properties={})
