import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import seaborn as sns
import calendar

import utils
sns.set_style("white")


data = pd.read_csv('claims.csv')

########### DATA PREPARATION AND CLEANING#####################
data = utils.transform_the_date(data)
data = data.dropna()

data["date"] = data.apply(utils.convert_to_date, axis = 1)
data["dateClaimed"] = data.apply(utils.convert_to_date_claim, axis = 1)
data["date"] = pd.to_datetime(data["date"], errors = "coerce")
data["dateClaimed"] = pd.to_datetime(data["dateClaimed"], errors = "coerce")

# THERE ARE SOME MISSING VALUES ON THE AGE COLUMNS, LETS GET RID OF THEM
data["Age"].replace(0, np.NaN, inplace = True)
data["Age"].fillna(data["Age"].mean(), inplace = True)

# ADDING A NEW COLUMN CALLED DELAY, THIS IS THE DELAY BETWEEN ACCIDENT AND CLAIM
data["delay"] = ((data["dateClaimed"] - data["date"]) / np.timedelta64(1, 'D')).astype(int)

# THE DATA WAS FILLED MANUALLY, THEREFORE SOME ASSUMPTIONS WERE MADE FOR CLEANING
# IT, SUCH AS MODIFYING THE NEGATIVE VALUES FOUND IN THE DELAY COLUMNS
data.loc[(data["delay"] < 0) & (data["delay"] > -20), "delay"] *= -1
data.loc[data["delay"] < -300, "delay"] += 360
# DROPPING ALL OTHER NEGATIVE VALUES
data = data[data["delay"] >= 0]

## Percentage of fraudulent claims
#data[data["FraudFound_P"] == 1].shape[0]
#data[data["FraudFound_P"] == 0].shape[0]


utils.plot_variable_percentage(data, "delay", style = 'o', xlims = (0,100))
