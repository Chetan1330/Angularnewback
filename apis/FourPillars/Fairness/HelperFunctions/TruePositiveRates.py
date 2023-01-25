def true_positive_rates(model, test_dataset, factsheet):
    import tensorflow as tf
    from ..helperfunctions import load_fairness_config
    import numpy as np
    """For a given model this function calculates the
    true positive rates for a protected and unprotected group
    based on the given true labels (y_true) and the model predicted
    labels (y_pred)

    Args:
        model: ML-model.
        test_dataset: pd.DataFrame containing the data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        1. true positive prediction rate for observations from the protected group
        2. true positive prediction rate for observations from the unprotected group

    """
    try: 
        properties = {}
        data = test_dataset.copy(deep=True)
        
        protected_feature, protected_values, target_column, favorable_outcomes = load_fairness_config(factsheet)
        
        X_data = data.drop(target_column, axis=1)
        if (isinstance(model, tf.keras.Sequential)):
            y_pred_proba = model.predict(X_data)
            y_pred = np.argmax(y_pred_proba, axis=1)
        else:
            y_pred = model.predict(X_data).flatten()
        data['y_pred'] = y_pred.tolist()

        favored_samples = data[data[target_column].isin(favorable_outcomes)]
        protected_favored_samples = favored_samples[favored_samples[protected_feature].isin(protected_values)]
        unprotected_favored_samples = favored_samples[~favored_samples[protected_feature].isin(protected_values)]

        num_unprotected_favored_true = len(unprotected_favored_samples)
        num_unprotected_favored_pred = len(unprotected_favored_samples[unprotected_favored_samples['y_pred'].isin(favorable_outcomes)])
        tpr_unprotected = num_unprotected_favored_pred/num_unprotected_favored_true

        num_protected_favored_true = len(protected_favored_samples)
        num_protected_favored_pred = len(protected_favored_samples[protected_favored_samples['y_pred'].isin(favorable_outcomes)])
        tpr_protected = num_protected_favored_pred / num_protected_favored_true 
        
        # Adding properties
        properties["|{x|x is protected, y_true is favorable, y_pred is favorable}|"] = num_protected_favored_pred
        properties["|{x|x is protected, y_true is favorable}|"] = num_protected_favored_true
        properties["TPR Protected Group"] = "P(y_pred is favorable|y_true is favorable, protected=True) = {:.2f}%".format(tpr_protected*100) 
        properties["|{x|x is not protected, y_true is favorable, y_pred is favorable}|"] = num_unprotected_favored_pred
        properties["|{x|x is not protected, y_true is favorable}|"] = num_unprotected_favored_true
        properties["TPR Unprotected Group"] = "P(y_pred is favorable|y_true is favorable, protected=False) = {:.2f}%".format(tpr_unprotected*100)
        
        return tpr_protected, tpr_unprotected, properties

    except Exception as e:
        print("ERROR in true_positive_rates(): {}".format(e))
        raise
