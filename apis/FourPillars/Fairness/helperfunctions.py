class MissingFairnessDefinitionError(Exception):
    def __init__(self, message="Salary is not in (5000, 15000) range"):
        self.message = message
        super().__init__(self.message)
        
def load_fairness_config(factsheet):
    message = ""
    protected_feature = factsheet.get("fairness", {}).get("protected_feature", '')
    if not protected_feature:
        message += "Definition of protected feature is missing."
        
    protected_values = factsheet.get("fairness", {}).get("protected_values", [])
    if not protected_values:
        message += "Definition of protected_values is missing."
        
    target_column = factsheet.get("general", {}).get("target_column", '')
    if not target_column:
        message += "Definition of target column is missing."
        
    favorable_outcomes = factsheet.get("fairness", {}).get("favorable_outcomes", [])
    if not favorable_outcomes:
        message += "Definition of favorable outcomes is missing."
        
    if message:
        raise MissingFairnessDefinitionError(message)
    
    return protected_feature, protected_values, target_column, favorable_outcomes