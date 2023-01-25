def confidence_score(model, train_data, test_data, thresholds):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from art.estimators.classification import SklearnClassifier
    import json
    from art.metrics import clever_u, RobustnessVerificationTreeModelsCliqueMethod
    import numpy as np
    from sklearn import metrics
    """For a given model this function calculates the Confidence score.
    It takes the average over confusion_matrix. Then returns a score according to the thresholds.
        Args:
            model: ML-model.
            train_data: pd.DataFrame containing the data.
            test_data: pd.DataFrame containing the data.
            threshold: list of threshold values

        Returns:
            Confidence score
        """
    try:
        X_test = test_data.iloc[:,:-1]
        y_test = test_data.iloc[:,-1: ]
        y_pred = model.predict(X_test)

        confidence = metrics.confusion_matrix(y_test, y_pred)/metrics.confusion_matrix(y_test, y_pred).sum(axis=1) 
        confidence_score = np.average(confidence.diagonal())*100
        score = np.digitize(confidence_score, thresholds, right=True) + 1
        return result(score=int(score), properties={"confidence_score": info("Average confidence score", "{:.2f}%".format(confidence_score)),
                                                    "depends_on": info("Depends on", "Model and Data")})
    except:
        return result(score=np.nan, properties={"non_computable": info("Non Computable Because", "Can only be calculated on models which provide prediction probabilities.")})
