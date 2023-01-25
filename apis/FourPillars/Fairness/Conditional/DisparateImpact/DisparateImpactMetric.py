def disparate_impact_metric(model, test_dataset, factsheet):
    import numpy as np
    import tensorflow as tf
    from ...helperfunctions import load_fairness_config

    """This function computes the disparate impact metric.
    It separates the data into a protected and an unprotected group 
    based on the given definition for protected groups.
    Then it computes the ratio of individuals receiving a favorable outcome
    divided by the total number of observations in the group.
    This is done both for the protected and unprotected group.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        test_dataset: pd.DataFrame containing the used test data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        1. The ratio of people from the protected group receiving a favorable outcome.
        2. The ratio of people from the unprotected group receiving a favorable outcome.

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
        protected_group_size = len(protected_group)
        unprotected_group_size = len(unprotected_group)

        protected_favored_group = protected_group[protected_group['y_pred'].isin(favorable_outcomes)]
        unprotected_favored_group = unprotected_group[unprotected_group['y_pred'].isin(favorable_outcomes)]
        protected_favored_group_size = len(protected_favored_group)
        unprotected_favored_group_size = len(unprotected_favored_group)
        
        protected_favored_ratio = protected_favored_group_size / protected_group_size
        unprotected_favored_ratio = unprotected_favored_group_size / unprotected_group_size
        
        properties["|{x|x is protected, y_pred is favorable}"] = protected_favored_group_size
        properties["|{x|x is protected}|"] = protected_group_size
        properties["Protected Favored Ratio"] = "P(y_hat=favorable|protected=True) = {:.2f}%".format(protected_favored_ratio*100)
        properties["|{x|x is not protected, y_pred is favorable}|"] = unprotected_favored_group_size
        properties["|{x|x is not protected}|"] = unprotected_group_size
        properties["Unprotected Favored Ratio"] = "P(y_hat=favorable|protected=False) = {:.2f}%".format(unprotected_favored_ratio*100) 

        disparate_impact = abs(protected_favored_ratio / unprotected_favored_ratio)
        return disparate_impact, properties

    except Exception as e:
        print("ERROR in disparate_impact_metric(): {}".format(e))
        raise
