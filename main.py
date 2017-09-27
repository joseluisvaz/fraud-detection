import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import seaborn as sns
import calendar

pd.set_option('chained_assignment',None)

cd ~/crabi/fraud-detection
import utils
sns.set_style("white")


data = pd.read_csv('claims.csv')
data = utils.clean_data(data)

utils.fraud_percentage(data, "Delay").plot(style = 'o');
plt.xlim(0,100)
sns.despine()
plt.show()


data[data["AddressChange_Claim"] == "4 to 8 years"].shape[0]
