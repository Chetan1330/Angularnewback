def get_final_score(model, train_data, test_data, config_weights, mappings_config, factsheet, solution_set_path, recalc=False):
    config_fairness = mappings_config["fairness"]
    config_explainability = mappings_config["explainability"]
    config_robustness = mappings_config["robustness"]
    config_methodology = mappings_config["methodology"]
    
    with open('configs/mappings/default.json', 'r') as f:
          default_map = json.loads(f.read())
    #print("mapping is default:")
    #print(default_map == mappings_config)
    if default_map == mappings_config:
        if "scores" in factsheet.keys() and "properties" in factsheet.keys() and not recalc:
            scores = factsheet["scores"]
            properties = factsheet["properties"]
        else:
            result = trusting_AI_scores(model, train_data, test_data, factsheet, config_fairness, config_explainability, config_robustness, config_methodology, solution_set_path)
            scores = result.score
            factsheet["scores"] = scores
            properties = result.properties
            factsheet["properties"] = properties
            try:
                write_into_factsheet(factsheet, solution_set_path)
            except Exception as e:
                print("ERROR in write_into_factsheet: {}".format(e))
    else:
        result = trusting_AI_scores(model, train_data, test_data, factsheet, config_fairness, config_explainability, config_robustness, config_methodology, solution_set_path)
        scores = result.score
        properties = result.properties
    
    final_scores = dict()
    for pillar in scores.items():
        config = config_weights[pillar]
        weighted_scores = list(map(lambda x: scores[pillar][x] * config[x], scores[pillar].keys()))
        sum_weights = np.nansum(np.array(list(config.values()))[~np.isnan(weighted_scores)])
        if sum_weights == 0:
            result = 0
        else:
            result = round(np.nansum(weighted_scores)/sum_weights,1)
        final_scores[pillar] = result

    return final_scores, scores, properties