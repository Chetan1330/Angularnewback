def compute_accuracy(model, dataset, factsheet):
    import numpy as np
    from sklearn import metrics
    import tensorflow as tf
    from ..helperfunctions import load_fairness_config
    # target_column = 'Target'
    """This function computes and returns 
    the accuracy a model achieves on a given dataset

    Args:
        model: ML-model.
        dataset: pd.DataFrame containing the data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        The prediction accuracy that the model achieved on the given data.

    """
    try:
        protected_feature, protected_values, target_column, favorable_outcomes = load_fairness_config(factsheet)
        X_data = dataset.drop(target_column, axis=1)
        y_data = dataset[target_column]

        y_true = y_data.values.flatten()
        if (isinstance(model, tf.keras.Sequential)):
            y_train_pred_proba = model.predict(X_data)
            y_pred = np.argmax(y_train_pred_proba, axis=1)
        else:
            y_pred = model.predict(X_data).flatten()
        return metrics.accuracy_score(y_true, y_pred)
    except Exception as e:
        print("ERROR in compute_accuracy(): {}".format(e))
        raise