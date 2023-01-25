def regularization_metric(factsheet):
    NOT_SPECIFIED = "not specified"
    if "methodology" in factsheet and "regularization" in factsheet["methodology"]:
        return factsheet["methodology"]["regularization"]
    else:
        return NOT_SPECIFIED