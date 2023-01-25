import tensorflow as tf


def false_positive_rates(model, test_dataset, factsheet):
    import numpy as np
    from ..helperfunctions import load_fairness_config
    """For a given model this function calculates the
    false positive rates for a protected and unprotected group
    based on the given true labels (y_true) and the model predicted
    labels (y_pred)

    Args:
        model: ML-model.
        test_dataset: pd.DataFrame containing the data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        1. false positive prediction rate for observations from the protected group
        2. false positive prediction rate for observations from the unprotected group

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

        protected_group = data[data[protected_feature].isin(protected_values)]
        unprotected_group = data[~data[protected_feature].isin(protected_values)]

        #2. Compute the number of negative samples y_true=False for the protected and unprotected group.
        protected_group_true_unfavorable = protected_group[~protected_group[target_column].isin(favorable_outcomes)]
        unprotected_group_true_unfavorable = unprotected_group[~unprotected_group[target_column].isin(favorable_outcomes)]
        protected_group_n_true_unfavorable = len(protected_group_true_unfavorable)
        unprotected_group_n_true_unfavorable = len(unprotected_group_true_unfavorable)

        #3. Calculate the number of false positives for the protected and unprotected group
        protected_group_true_unfavorable_pred_favorable = protected_group_true_unfavorable[protected_group_true_unfavorable['y_pred'].isin(favorable_outcomes)]
        unprotected_group_true_unfavorable_pred_favorable = unprotected_group_true_unfavorable[unprotected_group_true_unfavorable['y_pred'].isin(favorable_outcomes)]
        protected_group_n_true_unfavorable_pred_favorable = len(protected_group_true_unfavorable_pred_favorable)
        unprotected_group_n_true_unfavorable_pred_favorable = len(unprotected_group_true_unfavorable_pred_favorable)

        #4. Calculate fpr for both groups.
        fpr_protected = protected_group_n_true_unfavorable_pred_favorable/protected_group_n_true_unfavorable
        fpr_unprotected = unprotected_group_n_true_unfavorable_pred_favorable/unprotected_group_n_true_unfavorable
        
        #5. Adding properties
        properties["|{x|x is protected, y_true is unfavorable, y_pred is favorable}|"] = protected_group_n_true_unfavorable_pred_favorable
        properties["|{x|x is protected, y_true is Unfavorable}|"] = protected_group_n_true_unfavorable
        properties["FPR Protected Group"] = "P(y_pred is favorable|y_true is unfavorable, protected=True) = {:.2f}%".format(fpr_protected*100) 
        properties["|{x|x is not protected, y_true is unfavorable, y_pred is favorable}|"] = unprotected_group_n_true_unfavorable_pred_favorable
        properties["|{x|x is not protected, y_true is unfavorable}|"] = unprotected_group_n_true_unfavorable
        properties["FPR Unprotected Group"] = "P(y_pred is favorable|y_true is unfavorable, protected=False) = {:.2f}%".format(fpr_unprotected*100)
            
        return fpr_protected, fpr_unprotected, properties

    except Exception as e:
        print("ERROR in false_positive_rates(): {}".format(e))
        raise
   