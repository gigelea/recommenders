import pandas as pd
import numpy as np
from src.helper.helper_functions import year_to_months, recency_fac_linear

def purchase(dataframe):    
    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x))

    dataframe["year"] = pd.DatetimeIndex(dataframe['docdate']).year
    dataframe["month"] = pd.DatetimeIndex(dataframe['docdate']).month

    dataframe["recency_factor"] = year_to_months(dataframe["year"], dataframe["month"])
    dataframe["recency_factor"] = v_rec_fac(dataframe["recency_factor"])

    def fac_rating(num_of_purchases, recency_factor):
        if num_of_purchases <= 3:
            rating = recency_factor * 0.7 # low quantity full buys
        elif num_of_purchases > 3:
            rating = recency_factor * 0.8 # high quantity full buys
        return rating

    def pos_rating(num_of_purchases, factored_number):
        if num_of_purchases <= 3:
            rating = factored_number * 0.8 # low quantity rating
        elif num_of_purchases > 3:
            rating = factored_number * 0.9 # high quantity rating
        return rating

    v_fac_rating = np.vectorize(lambda x , y: fac_rating(x, y), otypes=[np.float32])
    v_pos_rating = np.vectorize(lambda x , y: pos_rating(x, y), otypes=[np.float32])

    dataframe["factored_number"] = v_fac_rating(dataframe["quantity"], dataframe["recency_factor"])
    dataframe["positive_number"] = v_pos_rating(dataframe["quantity"], dataframe["factored_number"])

    dataframe['itemPrice'] = dataframe['itemPrice'] / dataframe['quantity']

    dataframe["itemPrice"] = dataframe["itemPrice"] *.75 /dataframe["inhalt_liter"].astype(float)

    dataframe = dataframe.round(4)

    grouped_num = dataframe.groupby(["uuid", "itemcode", "itemPrice", "inhalt_liter", "Untergruppe", "Farbe"]).agg({"factored_number": np.sum, "positive_number": np.sum})
    grouped_num = grouped_num.reset_index()

    return grouped_num