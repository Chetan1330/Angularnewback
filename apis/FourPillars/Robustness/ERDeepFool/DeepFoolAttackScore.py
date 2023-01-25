def deepfool_attack_score(model, train_data, test_data, thresholds):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    from art.estimators.classification import SklearnClassifier
    import json
    from art.attacks.evasion import FastGradientMethod, CarliniL2Method, DeepFool
    import numpy as np
    from sklearn import metrics
    from sklearn.preprocessing import OneHotEncoder
    """For a given model this function calculates the deepfool attack score.
    First from the test data selects a random small test subset.
    Then measures the accuracy of the model on this subset.
    Next creates deepfool attacks on this test set and measures the model's
    accuracy on the attacks. Compares the before attack and after attack accuracies.
    Returns a score according to the thresholds.

    Args:
        model: ML-model (Logistic Regression, SVM).
        train_data: pd.DataFrame containing the data.
        test_data: pd.DataFrame containing the data.
        threshold: list of threshold values

    Returns:
        Deepfool attack score
        DF Before attack accuracy
        DF After attack accuracy
    """
    try:
        randomData = test_data.sample(4)
        randomX = randomData.iloc[:,:-1]
        randomY = randomData.iloc[:,-1: ]

        y_pred = model.predict(randomX)
        before_attack = metrics.accuracy_score(randomY,y_pred)

        classifier = SklearnClassifier(model=model)
        attack = DeepFool(classifier)
        x_test_adv = attack.generate(x=randomX)

        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(test_data.iloc[:,-1: ])
        randomY = enc.transform(randomY).toarray()

        predictions = model.predict(x_test_adv)
        predictions = enc.transform(predictions.reshape(-1,1)).toarray()
        after_attack = metrics.accuracy_score(randomY,predictions)
        print("Accuracy on before_attacks: {}%".format(before_attack * 100))
        print("Accuracy on after_attack: {}%".format(after_attack * 100))

        score = np.digitize((before_attack - after_attack)/before_attack*100, thresholds) + 1
        return result(score=int(score),
                      properties={"before_attack": info("DF Before attack accuracy", "{:.2f}%".format(100 * before_attack)),
                                  "after_attack": info("DF After attack accuracy", "{:.2f}%".format(100 * after_attack)),
                                  "difference": info("DF Proportional difference (After-Att Acc - Before-Att Acc)/Before-Att Acc", "{:.2f}%".format(100 * (before_attack - after_attack) / before_attack)),
                                  "depends_on": info("Depends on", "Model and Data")})
    except:
        return result(score=np.nan, properties={"non_computable": info("Non Computable Because",
                                                                       "Can be calculated on either SVC or Logistic Regression models.")})