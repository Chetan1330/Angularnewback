def loss_sensitivity_score(model, train_data, test_data, thresholds):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from art.estimators.classification import SklearnClassifier
    import json
    from art.attacks.evasion import FastGradientMethod, CarliniL2Method, DeepFool
    import numpy as np
    from sklearn import metrics
    from sklearn.preprocessing import OneHotEncoder
    from art.estimators.classification import KerasClassifier
    from art.metrics import loss_sensitivity

    """For a given Keras-NN model this function calculates the Loss Sensitivity score.
    It uses loss_sensitivity function from IBM art library.
    Returns a score according to the thresholds.
        Args:
            model: ML-model (Keras).
            train_data: pd.DataFrame containing the data.
            test_data: pd.DataFrame containing the data.
            threshold: list of threshold values

        Returns:
            Loss Sensitivity score
    """
    try:
        X_test = test_data.iloc[:,:-1]
        X_test = np.array(X_test)
        y = model.predict(X_test)

        classifier = KerasClassifier(model=model, use_logits=False)
        l_s = loss_sensitivity(classifier, X_test, y)
        score = np.digitize(l_s, thresholds, right=True) + 1
        return result(score=int(score), properties={"loss_sensitivity": info("Average gradient value of the loss function", "{:.2f}".format(l_s)),
                                                    "depends_on": info("Depends on", "Model")})
    except Exception as e:
        print(e)
        return result(score=np.nan, properties={"non_computable": info("Non Computable Because",
                                                                       "Can only be calculated on Keras models.")})
