def list_of_metrics(pillar):
    import json
    import os
    metrics = []
    METRICS_CONFIG_PATH=r"MappingsWeightsMetrics\Metrics"

    with open(os.path.join(METRICS_CONFIG_PATH, "config_{}.json".format(pillar))) as file:
        config_file = json.load(file)
        for metric_name in config_file["weights"]:
            metrics.append(metric_name.lower())
    return metrics