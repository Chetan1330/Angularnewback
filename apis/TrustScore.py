import sys
import os
import time
import random
import numpy as np
import pickle
import statistics
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json
from config import *
from math import pi
import sklearn.metrics as metrics
from FourPillars.Fairness.Fariness import analyse as analyse_fairness
from FourPillars.Explainability.Explainability import analyse as analyse_explainability
from FourPillars.Robustness.Robustness import analyse as analyse_robustness
from FourPillars.Accountability.Accountability import analyse as analyse_methodology
import collections




def get_trust_score(final_score, config):
    if sum(config.values()) == 0:
        return 0
    return round(np.nansum(list(map(lambda x: final_score[x] * config[x], final_score.keys())))/np.sum(list(config.values())),1)

