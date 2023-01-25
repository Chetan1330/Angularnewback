def statistical_parity_difference_metric(model, training_dataset, factsheet):
    from ...helperfunctions import load_fairness_config
    """This function computes the statistical parity metric.
    It separates the data into a protected and an unprotected group 
    based on the given definition for protected groups.
    Then it computes the ratio of individuals receiving a favorable outcome
    divided by the total number of observations in the group.
    This is done both for the protected and unprotected group.

    Args:
        model: ML-model.
        training_dataset: pd.DataFrame containing the used training data.
        factsheet: json document containing all information about the particular solution.

    Returns:
        1. The ratio of people from the unprotected group receiving a favorable outcome.
        2. The ratio of people from the protected group receiving a favorable outcome.
        3. The statistical parity differenc as the difference of the previous two values.

    """
    try: 
        properties = {}
        protected_feature, protected_values, target_column, favorable_outcomes = load_fairness_config(factsheet)
        
        minority = training_dataset[training_dataset[protected_feature].isin(protected_values)]
        minority_size = len(minority)
        majority = training_dataset[~training_dataset[protected_feature].isin(protected_values)]
        majority_size = len(majority)

        favored_minority = minority[minority[target_column].isin(favorable_outcomes)]
        favored_minority_size = len(favored_minority)

        favored_minority_ratio = favored_minority_size/minority_size

        favored_majority = majority[majority[target_column].isin(favorable_outcomes)]
        favored_majority_size = len(favored_majority)
        favored_majority_ratio = favored_majority_size/majority_size
        
        properties["|{x|x is protected, y_true is favorable}|"] = favored_minority_size
        properties["|{x|x is protected}|"] = minority_size
        properties["Favored Protected Group Ratio"] =  "P(y_true is favorable|protected=True) = {:.2f}%".format(favored_minority_ratio*100)
        properties["|{x|x is not protected, y_true is favorable}|"] = favored_majority_size
        properties["|{x|x is not protected}|"] = majority_size
        properties["Favored Unprotected Group Ratio"] =  "P(y_true is favorable|protected=False) = {:.2f}%".format(favored_majority_ratio*100)
        
        statistical_parity_difference = abs(favored_minority_ratio - favored_majority_ratio)
        return statistical_parity_difference, properties
    except Exception as e:
        print("ERROR in statistical_parity_difference_metric(): {}".format(e))
        raise
