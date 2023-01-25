def underfitting_score(model, training_dataset, test_dataset, factsheet, underfitting_thresholds):
    import numpy as np
    from ...HelperFunctions.Accuracy import compute_accuracy
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')
    """This function computes the training and test accuracy for the given model and then
    compares how much lower the training accuracy is than the test accuracy.
    If this is the case then we consider our model to be underfitting.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.
        thresholds: Threshold values used to determine the final score

    Returns:
        A score from one to five representing the level of underfitting.
        5 means the model is not underfitting
        1 means the model is strongly underfitting

    """
    try:
        properties = {}
        properties['Metric Description'] = "Compares the models achieved test accuracy against a baseline."
        properties['Depends on'] = 'Model, Test Data'
        score = 0
        test_accuracy = compute_accuracy(model, test_dataset, factsheet)
        score = np.digitize(abs(test_accuracy), underfitting_thresholds, right=False) + 1 

        properties["Test Accuracy"] = "{:.2f}%".format(test_accuracy*100)

        if score == 5:
            properties["Conclusion"] = "Model is not underfitting"
        elif score == 4:
            properties["Conclusion"] = "Model mildly underfitting"
        elif score == 3:
            properties["Conclusion"] = "Model is slighly underfitting"
        elif score == 2:
            properties["Conclusion"] = "Model is underfitting"
        else:
            properties["Conclusion"] = "Model is strongly underfitting"

        properties["Score"] = str(score)
        return result(score=int(score), properties=properties)
    
    except Exception as e:
        print("ERROR in underfitting_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)}) 