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

data.dtypes

data[data["AddressChange_Claim"] == "under 6 months"].shape[0]
utils.plot_variable_percentage(data, "BasePolicy", kind = "bar")


Month                            int64
WeekOfMonth                      int64
DayOfWeek                        int64
Make                            object
AccidentArea                    object
DayOfWeekClaimed               float64
MonthClaimed                   float64
WeekOfMonthClaimed               int64
Sex                             object
MaritalStatus                   object
Age                            float64
Fault                           object
PolicyType                      object
VehicleCategory                 object
VehiclePrice                    object
FraudFound_P                     int64
PolicyNumber                     int64
RepNumber                        int64
Deductible                       int64
DriverRating                     int64
Days_Policy_Accident            object
Days_Policy_Claim               object
PastNumberOfClaims              object
AgeOfVehicle                    object
AgeOfPolicyHolder               object
PoliceReportFiled               object
WitnessPresent                  object
AgentType                       object
NumberOfSuppliments             object
AddressChange_Claim             object
NumberOfCars                    object
Year                             int64
BasePolicy                      object
Date                    datetime64[ns]
DateClaimed             datetime64[ns]
Delay                            int64
dtype: object


utils.plot_variable_percentage_datetime(data, "DateClaimed", 'year', kind = 'bar', style = 'o')
