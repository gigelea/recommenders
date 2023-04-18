import pandas as pd
import numpy as np
from src.helper.helper_functions import year_to_months, recency_fac_linear

def add_bas_prod_view(dataframe):
    dataframe = dataframe.drop_duplicates()

    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    dataframe["year"] = pd.DatetimeIndex(dataframe['timestamp']).year
    dataframe["month"] = pd.DatetimeIndex(dataframe['timestamp']).month
    
    dataframe["recency_factor"] = year_to_months(dataframe["year"], dataframe["month"])
    dataframe["recency_factor"] = v_rec_fac(dataframe["recency_factor"]).astype(float)

    def fac_rating(event_type, recency_factor):
        if event_type == "productview":
            rating = recency_factor * 0.4
            return rating
        elif event_type == "addtobasket":
            rating = recency_factor * 0.5
            return rating

    def pos_rating(event_type, factored_number):
        if event_type == "productview":
            rating = factored_number * 0.7
            return rating
        elif event_type == "addtobasket":
            rating = factored_number * 0.8
            return rating

    v_fac_rating = np.vectorize(lambda x , y: fac_rating(x, y), otypes=[np.float32]) # vectorize behandelt bei default alles als int, daher float sonst rundet er
    v_pos_rating = np.vectorize(lambda x , y: pos_rating(x, y), otypes=[np.float32])

    dataframe["factored_number"] = v_fac_rating(dataframe["event_type"], dataframe["recency_factor"])
    dataframe["positive_number"] = v_pos_rating(dataframe["event_type"], dataframe["factored_number"])

    dataframe["actualGrossPrice"] = dataframe["actualGrossPrice"] *.75 /dataframe["inhalt_liter"]
    
    # wichtig: groupby nach dem runden
    dataframe = dataframe.round(4)
    
    grouped_num = dataframe.groupby(["uuid", "itemid", "actualGrossPrice", "inhalt_liter", "Untergruppe", "Farbe"]).agg({"factored_number": np.sum, "positive_number": np.sum})

    grouped_num = grouped_num.reset_index()

    return grouped_num
