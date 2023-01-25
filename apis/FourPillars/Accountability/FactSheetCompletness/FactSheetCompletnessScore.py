def get_factsheet_completeness_score(model, training_dataset, test_dataset, factsheet, methodology_config):
    import collections
    info = collections.namedtuple('info', 'description value')
    result = collections.namedtuple('result', 'score properties')

    score = 0
    properties= {"dep" :info('Depends on','Factsheet')}
    GENERAL_INPUTS = ["model_name", "purpose_description", "domain_description", "training_data_description", "model_information", "authors", "contact_information"]

    n = len(GENERAL_INPUTS)
    ctr = 0
    for e in GENERAL_INPUTS:
        if "general" in factsheet and e in factsheet["general"]:
            ctr+=1
            properties[e] = info("Factsheet Property {}".format(e.replace("_"," ")), "present")
        else:
            properties[e] = info("Factsheet Property {}".format(e.replace("_"," ")), "missing")
    score = round(ctr/n*5)
    return result(score=score, properties=properties)


