def test_accuracy_score(model, training_dataset, test_dataset, factsheet, thresholds):
    try:
        test_accuracy = test_accuracy_metric(model, test_dataset, factsheet)
        score = np.digitize(test_accuracy, thresholds)
        #return result(score=float(score), properties={"test_accuracy": info("Test Accuracy", "{:.2f}".format(test_accuracy))})
        return result(score=np.nan, properties={})
    except Exception as e:
        #_return result(score=np.nan, properties={})
        return result(score=np.nan, properties={})
        
def test_accuracy_metric(model, test_dataset, factsheet):
    target_column = None
    if "general" in factsheet and "target_column" in factsheet["general"]:
        target_column = factsheet["general"]["target_column"]
    
    if target_column:
        X_test = test_dataset.drop(target_column, axis=1)
        y_test = test_dataset[target_column]
    else:
        X_test = test_dataset.iloc[:,:DEFAULT_TARGET_COLUMN_INDEX]
        y_test = test_dataset.iloc[:,DEFAULT_TARGET_COLUMN_INDEX: ]
    
    y_true =  y_test.values.flatten()
    y_pred = model.predict(X_test)

    if isinstance(model, tf.keras.models.Sequential):
        y_pred = np.argmax(y_pred, axis=1)

    accuracy = metrics.accuracy_score(y_true, y_pred).round(2)
    return accuracy

# --- F1 Score ---
def f1_score(model, training_dataset, test_dataset, factsheet, thresholds):
    try:
        f1_score = f1_metric(model, test_dataset, factsheet)
        score = np.digitize(f1_score, thresholds)
        #return result(score=float(score), properties={"f1_score": info("F1 Score", "{:.2f}".format(f1_score))})
        return result(score=np.nan, properties={})
    except:
        return result(score=np.nan, properties={})
         
        
def f1_metric(model, test_dataset, factsheet):
    target_column = None
    if "general" in factsheet and "target_column" in factsheet["general"]:
        target_column = factsheet["general"]["target_column"]
    
    if target_column:
        X_test = test_dataset.drop(target_column, axis=1)
        y_test = test_dataset[target_column]
    else:
        X_test = test_dataset.iloc[:,:DEFAULT_TARGET_COLUMN_INDEX]
        y_test = test_dataset.iloc[:,DEFAULT_TARGET_COLUMN_INDEX: ]
    
    y_true =  y_test.values.flatten()
    y_pred = model.predict(X_test)
    if isinstance(model, tf.keras.models.Sequential):
        y_pred = np.argmax(y_pred, axis=1)
    f1_metric = metrics.f1_score(y_true, y_pred,average="weighted").round(2)
    return f1_metric