import numpy as np
import datetime

def recency_fac(num):
    recency = 1 - np.exp(-(28-num)/28)
    return recency

def year_to_months(year, month):
    x = datetime.datetime.now()
    curr_year = x.year
    curr_month = x.month
    
    # Januar 2019 als Start
    start_year_month = "201901"

    # Verstrichene Monate seit januar 2019
    months = (curr_year - year) * 12 + (curr_month - month)
    return months

def recency_fac_linear(num):
    passed_months = year_to_months(2019, 1) + 12
    if num <= 12:
        return 1
    elif num > 12 and num <= passed_months:
        num -= 12
        #passed_months -= 12
        recency = (passed_months - num + 1)/passed_months
        return recency
    else:
        return 0