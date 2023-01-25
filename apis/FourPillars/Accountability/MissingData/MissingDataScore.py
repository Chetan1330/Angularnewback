def missing_data_score(model, training_dataset, test_dataset, factsheet, mappings):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    try:
        missing_values = training_dataset.isna().sum().sum() + test_dataset.isna().sum().sum()
        if missing_values > 0:
            score = mappings["null_values_exist"]
        else:
            score = mappings["no_null_values"]
        return result(score=score,properties={"dep" :info('Depends on','Training Data'),
            "null_values": info("Number of the null values", "{}".format(missing_values))})
    except:
        return result(score=np.nan, properties={})