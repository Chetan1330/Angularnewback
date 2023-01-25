def train_test_split_metric(training_dataset, test_dataset):
    n_train = len(training_dataset)
    n_test = len(test_dataset)
    n = n_train + n_test
    return round(n_train/n*100), round(n_test/n*100)
