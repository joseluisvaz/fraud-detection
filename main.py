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

# Cleaning 0 values in Age column
# Missing Values = 319
data[data["Age"] == 0].count()[0]
# Changing Missing Values to Nan
data["Age"].replace(0, np.NaN, inplace = True)
data["Age"].fillna(data["Age"].mean(), inplace = True)

delay = ((data["dateClaimed"] - data["date"]) / np.timedelta64(1, 'D')).astype(int)
data["delay"] = delay

condition = data["FraudFound_P"] == 1
a = np.where(condition, 'Fraud', "Not Fraud")
count = data.groupby(a)["FraudFound_P"].count()

frauds = data[data["FraudFound_P"] == 1]
not_frauds = data[data["FraudFound_P"] == 0]

print("Number of Frauds: " +  str(count["Fraud"]))
print("Number of Frauds: " +  str(count["Not Fraud"]))
print("Percentage: " +  str(count["Fraud"]/count["Not Fraud"]*100))

def plot_variable_percentage(data, fraud_data, not_fraud_data, togroupby, style='line'):
    """
    Receives two dataframes and a togroupby list of variables to groupby
    """
    fraud_count = data.groupby([fraud_data[togroupby]])["PolicyNumber"].count()
    not_frauds_count = data.groupby([not_fraud_data[togroupby]])["PolicyNumber"].count()
    to_plot = (fraud_count/not_frauds_count).fillna(0).plot(kind=style)
    sns.despine()
    plt.show()

plot_variable_percentage(data, frauds, not_frauds, "VehicleCategory", style = 'bar')



A = data.groupby([frauds["Age"]])["PolicyNumber"].count()
B = data.groupby([not_frauds["Age"]])["PolicyNumber"].count()
(A/B*100).fillna(0).plot()
sns.despine()
plt.show()
