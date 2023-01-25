def trusting_AI_scores(model, train_data, test_data, factsheet, config_fairness, config_explainability, config_robustness, methodology_config, solution_set_path):
    # if "scores" in factsheet.keys() and "properties" in factsheet.keys():
    #     scores = factsheet["scores"]
    #     properties = factsheet["properties"]
    # else:
        output = dict(
            fairness       = analyse_fairness(model, train_data, test_data, factsheet, config_fairness),
            explainability = analyse_explainability(model, train_data, test_data, config_explainability, factsheet),
            robustness     = analyse_robustness(model, train_data, test_data, config_robustness, factsheet),
            methodology    = analyse_methodology(model, train_data, test_data, factsheet, methodology_config)
        )
        scores = dict((k, v.score) for k, v in output.items())
        properties = dict((k, v.properties) for k, v in output.items())
        # factsheet["scores"] = scores
        # factsheet["properties"] = properties
        # write_into_factsheet(factsheet, solution_set_path)
    
        return  result(score=scores, properties=properties)