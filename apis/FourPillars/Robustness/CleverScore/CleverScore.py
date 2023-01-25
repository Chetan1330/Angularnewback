def clever_score(model, train_data, test_data, thresholds):
    import numpy as np
    from art.estimators.classification import KerasClassifier
    from art.metrics import clever_u, RobustnessVerificationTreeModelsCliqueMethod
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')

    """For a given Keras-NN model this function calculates the Untargeted-Clever score.
    It uses clever_u function from IBM art library.
    Returns a score according to the thresholds.
        Args:
            model: ML-model (Keras).
            train_data: pd.DataFrame containing the data.
            test_data: pd.DataFrame containing the data.
            threshold: list of threshold values

        Returns:
            Clever score
    """
    try:
        X_test = test_data.iloc[:,:-1]
        X_train = train_data.iloc[:, :-1]
        classifier = KerasClassifier(model, False)

        min_score = 100

        randomX = X_test.sample(10)
        randomX = np.array(randomX)

        for x in randomX:
            temp = clever_u(classifier=classifier, x=x, nb_batches=1, batch_size=1, radius=500, norm=1)
            if min_score > temp:
                min_score = temp
        score = np.digitize(min_score, thresholds) + 1
        return result(score=int(score), properties={"clever_score": info("CLEVER Score", "{:.2f}".format(min_score)),
                                                    "depends_on": info("Depends on", "Model")})
    except Exception as e:
        print(e)
        return result(score=np.nan, properties={"non_computable": info("Non Computable Because",
                                                                       "Can only be calculated on Keras models.")})
