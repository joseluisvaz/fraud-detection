import numpy
import datetime as dt
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

months_dic = { "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "Jun": 5, "Jul": 6, "Aug": 7,
            "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11 }
days_dic = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

def convert_to_date(row):
    monthdates = calendar.monthcalendar(row.Year, row.Month + 1)
    day = monthdates[row.WeekOfMonth][row.DayOfWeek]
    if day == 0 and row.WeekOfMonth == 0 :
        day = monthdates[row.WeekOfMonth + 1][row.DayOfWeek]
    elif day == 0 and (row.WeekOfMonth == 4 or row.WeekOfMonth == 3):
        day = monthdates[row.WeekOfMonth - 1][row.DayOfWeek]
    return dt.date(row.Year, row.Month + 1, day)

def convert_to_date_claim(row):
    monthdates = calendar.monthcalendar(int(row.Year), int(row.MonthClaimed + 1))
    day = monthdates[int(row.WeekOfMonthClaimed)][int(row.DayOfWeekClaimed)]
    if day == 0 and int(row.WeekOfMonthClaimed) == 0 :
        day = monthdates[int(row.WeekOfMonthClaimed + 1)][int(row.DayOfWeekClaimed)]
    elif day == 0 and (int(row.WeekOfMonthClaimed) == 4 or int(row.WeekOfMonthClaimed) == 3):
        day = monthdates[int(row.WeekOfMonthClaimed) - 1][int(row.DayOfWeekClaimed)]
    return dt.date(row.Year, int(row.MonthClaimed + 1), day)


def convert_to_categorical(df):
    df.Month = df.Month.map(months_dic)
    df.DayOfWeek = df.DayOfWeek.map(days_dic)

    df.MonthClaimed = df.MonthClaimed.map(months_dic)
    df.DayOfWeekClaimed = df.DayOfWeekClaimed.map(days_dic)
    return df

def transform_the_date(df):
    df.WeekOfMonth = df.WeekOfMonth - 1
    df.WeekOfMonthClaimed = df.WeekOfMonthClaimed -1
    df = convert_to_categorical(df)
    return df

def clean_data(df):
    df = transform_the_date(df)
    df = df.dropna()

    # CREATING PD.SERIES WITH DATE
    date = df.apply(convert_to_date, axis = 1)
    dateClaimed = df.apply(convert_to_date_claim, axis = 1)

    # CHANGING TYPE TO DATETIME
    date = pd.to_datetime(date, errors = "coerce")
    dateClaimed = pd.to_datetime(dateClaimed, errors = "coerce")

    # ASSIGNING TO DATAFRAME
    df.loc[:, "Date"] = date
    df.loc[:, "DateClaimed"] = dateClaimed

    # THERE ARE SOME MISSING VALUES ON THE AGE COLUMNS, LETS GET RID OF THEM
    df["Age"].replace(0, np.NaN, inplace = True)
    df["Age"].fillna(round(df["Age"].mean()), inplace = True)

    # ADDING A NEW COLUMN CALLED DELAY, THIS IS THE DELAY BETWEEN ACCIDENT AND CLAIM
    diff = df["DateClaimed"].copy() - df["Date"].copy()
    delay = diff/np.timedelta64(1, 'D')
    df["Delay"] = delay.astype(int)

    # THE DATA WAS FILLED MANUALLY, THEREFORE SOME ASSUMPTIONS WERE MADE FOR CLEANING
    # IT, SUCH AS MODIFYING THE NEGATIVE VALUES FOUND IN THE DELAY COLUMNS
    df.loc[(df["Delay"] < 0) & (df["Delay"] > -20), "Delay"] *= -1
    df.loc[df["Delay"] < -300, "Delay"] += 360
    # DROPPING ALL OTHER NEGATIVE VALUES
    df = df[df["Delay"] >= 0]
    return df

def fraud_percentage(df, togroupby):
    """
    Receives a dataframe and a paremeter and creates the percentage of fraudulent claims
    present in this variable
    """
    series = df.groupby([df.FraudFound_P, getattr(df, togroupby)]).count()
    frauds = series.PolicyNumber[1]
    non_frauds = series.PolicyNumber[0]

    percentage = frauds/non_frauds * 100

    return percentage

def plot_percent(df, togroupby, style='-', kind='line', xlims = None):
    """
    Receives two dataframes and a togroupby list of variables to groupby
    """
    percentage = fraud_percent(data, togroupby)
    percentage.plot(kind = kind, style = style)

    if xlims != None:
        plt.xlim(xlims)
    sns.despine()
    plt.show()

def plot_variable_percentage_datetime(data, togroupby, datetime_attr, style='-', kind='line'):
    """
    Receives two dataframes and a togroupby list of variables to groupby
    """

    to_group = data.groupby([data.FraudFound_P, getattr(data[togroupby].dt, datetime_attr)]).count()

    frauds = to_group.PolicyNumber[1]
    non_frauds = to_group.PolicyNumber[0]

    to_plot = (frauds/non_frauds * 100)
    to_plot.plot(kind = kind, style = style)

    sns.despine()
    plt.show()
