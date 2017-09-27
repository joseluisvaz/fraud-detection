import numpy
import datetime as dt
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_variable_percentage(data, togroupby, style='line', xlims = None):
    """
    Receives two dataframes and a togroupby list of variables to groupby
    """
    to_group = data.groupby([data.FraudFound_P, data[togroupby]]).count()
    frauds = to_group.PolicyNumber[1]
    non_frauds = to_group.PolicyNumber[0]
    to_plot = (frauds/non_frauds * 100)
    to_plot.plot(style = 'o')
    if xlims != None:
        plt.xlim(xlims)
    sns.despine()
    plt.show()
