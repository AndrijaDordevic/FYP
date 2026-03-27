import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_path = "\DepMap\"

rna_expression = pd.read_csv("data_path" + "Expression_Public_25Q3_subsetted", index_col = 0)
rna_expression.shape
