def overfitting_score(model, training_dataset, test_dataset, factsheet, thresholds):
    import numpy as np
    import collections
    info = collections.namedtuple('info', 'description value')
    from ...HelperFunctions.Accuracy import compute_accuracy

    result = collections.namedtuple('result', 'score properties')
    """This function computes the training and test accuracy for the given model and then
    compares how much higher the training accuracy is compared to the test accuracy.
    If this is the case then we consider our model to be overfitting.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.
        thresholds: Threshold values used to determine the final score

    Returns:
        A score from one to five representing the level of overfitting.
        5 means the model is not overfitting
        1 means the model is strongly overfitting

    """
    try:
        properties = {}
        properties['Metric Description'] = "Overfitting is present if the training accuracy is significantly higher than the test accuracy"
        properties['Depends on'] = 'Model, Training Data, Test Data'
        overfitting_score = np.nan
        training_accuracy = compute_accuracy(model, training_dataset, factsheet)
        test_accuracy = compute_accuracy(model, test_dataset, factsheet)
        # model could be underfitting.
        # for underfitting models the spread is negative
        accuracy_difference = training_accuracy - test_accuracy
        
        underfitting_score = np.digitize(abs(test_accuracy), thresholds, right=False) + 1 
        
        if underfitting_score >= 3:
            overfitting_score = np.digitize(abs(accuracy_difference), thresholds, right=False) + 1 
            properties["Training Accuracy"] = "{:.2f}%".format(training_accuracy*100)
            properties["Test Accuracy"] = "{:.2f}%".format(test_accuracy*100)
            properties["Train Test Accuracy Difference"] = "{:.2f}%".format((training_accuracy - test_accuracy)*100)
        
            if overfitting_score == 5:
                properties["Conclusion"] = "Model is not overfitting"
            elif overfitting_score == 4:
                properties["Conclusion"] = "Model mildly overfitting"
            elif overfitting_score == 3:
                properties["Conclusion"] = "Model is slighly overfitting"
            elif overfitting_score == 2:
                properties["Conclusion"] = "Model is overfitting"
            else:
                properties["Conclusion"] = "Model is strongly overfitting"

            properties["Score"] = str(overfitting_score)
            return result(int(overfitting_score), properties=properties)
        else:
            return result(overfitting_score, properties={"Non computable because": "The test accuracy is to low and if the model is underfitting to much it can't be overfitting at the same time."})
    except Exception as e:
        print("ERROR in overfitting_score(): {}".format(e))
        return result(score=np.nan, properties={"Non computable because": str(e)}) 