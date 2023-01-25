def clique_method(model, train_data, test_data, thresholds, factsheet):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from art.estimators.classification import SklearnClassifier
    import json
    from art.metrics import clever_u, RobustnessVerificationTreeModelsCliqueMethod
    import numpy as np
    from pathlib import Path
    import os
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    # from .....apis.MappingsWeightsMetrics.Mappings.robustness import 
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
    print("Clique BASEDIR",BASE_DIR)
    """For a given tree-based model this function calculates the Clique score.
    First checks the factsheet to see if the score is already calculated.
    If not it uses RobustnessVerificationTreeModelsCliqueMethod function from
    IBM art library to calculate the score. Returns a score according to the thresholds.

    Args:
        model: ML-model (Tree-based).
        train_data: pd.DataFrame containing the data.
        test_data: pd.DataFrame containing the data.
        threshold: list of threshold values
        factsheet: factsheet dict

    Returns:
        Clique score
        Error bound
        Error
    """
    with open(os.path.join(BASE_DIR,'apis/MappingsWeightsMetrics/Mappings/robustness/default.json')) as f:
          default_map = json.loads(f.read())
    
    if thresholds == default_map["score_clique_method"]["thresholds"]["value"]:
        if "scores" in factsheet.keys() and "properties" in factsheet.keys():
            score = factsheet["scores"]["robustness"]["clique_method"]
            properties = factsheet["properties"]["robustness"]["clique_method"]
            return result(score=score, properties=properties)
    
    try:
        X_test = test_data.iloc[:, :-1]
        y_test = test_data.iloc[:, -1:]
        classifier = SklearnClassifier(model)
        rt = RobustnessVerificationTreeModelsCliqueMethod(classifier=classifier, verbose=True)

        bound, error = rt.verify(x=X_test.to_numpy()[100:103], y=y_test[100:103].to_numpy(), eps_init=0.5, norm=1,
                                 nb_search_steps=5, max_clique=2, max_level=2)
        score = np.digitize(bound, thresholds) + 1
        return result(score=int(score), properties={
            "error_bound": info("Average error bound", "{:.2f}".format(bound)),
            "error": info("Error", "{:.1f}".format(error)),
            "depends_on": info("Depends on", "Model")
        })
    except:
        return result(score=np.nan, properties={"non_computable": info("Non Computable Because", "Can only be calculated on Tree-Based models.")})



