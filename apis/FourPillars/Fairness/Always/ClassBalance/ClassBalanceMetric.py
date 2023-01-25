def class_balance_metric(training_data, factsheet):
    from scipy.stats import chisquare
    from ...helperfunctions import load_fairness_config

    """This function runs a statistical test (chisquare) in order to
    check if the targe class labels are equally distributed or not

    Args:
        training_data: pd.DataFrame containing the used training data.
        target_column: name of the label column in the provided training data frame.

    Returns:
        If the label frequency follows a unit distribution a 1 is returned, 0 otherwise.

    """

    try:
        protected_feature, protected_values, target_column, favorable_outcomes = load_fairness_config(factsheet)
        absolute_class_occurences = training_data[target_column].value_counts().sort_index().to_numpy()
        significance_level = 0.05
        p_value = chisquare(absolute_class_occurences, ddof=0, axis=0).pvalue

        if p_value < significance_level:
            #The data does not follow a unit distribution
            return 0
        else:
            #We can not reject the null hypothesis assuming that the data follows a unit distribution"
            return 1
    except Exception as e:
        print("ERROR in class_balance_metric(): {}".format(e))
        raise