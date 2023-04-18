import pandas as pd
import numpy as np
from src.helper.helper_functions import year_to_months, recency_fac_linear

def create_transaction_style_buckets(raw_data):
    transaction_table = raw_data.copy()

    transaction_table["Farbe"] = transaction_table["Farbe"].map({0.0:"undefiniert", 1.0: "Weiß", 2.0: "Rosé", 3.0:"Rot"})

    ### Remove leading and trailing spacecs in Geschmacksnote
    transaction_table["Geschmacksnote"] = transaction_table["Geschmacksnote"].replace(np.nan, '', regex=True)
    transaction_table["Geschmacksnote"] = transaction_table["Geschmacksnote"].apply(lambda x: x.strip())

    transaction_table = transaction_table.fillna(0)

    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    transaction_table["year"] = pd.DatetimeIndex(transaction_table['docdate']).year
    transaction_table["month"] = pd.DatetimeIndex(transaction_table['docdate']).month

    transaction_table["recency_factor"] = year_to_months(transaction_table["year"], transaction_table["month"])
    transaction_table["recency_factor"] = v_rec_fac(transaction_table["recency_factor"]).astype(float)

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

    v_fac_rating = np.vectorize(lambda x , y: fac_rating(x, y), otypes=[np.float32]) # vectorize behandelt bei default alles als int, daher float sonst rundet er
    v_pos_rating = np.vectorize(lambda x , y: pos_rating(x, y), otypes=[np.float32])

    transaction_table["factored_number"] = v_fac_rating(transaction_table["quantity"], transaction_table["recency_factor"])
    transaction_table["positive_number"] = v_pos_rating(transaction_table["quantity"], transaction_table["factored_number"])

    transaction_table = transaction_table.round(4)

    grouped_num = transaction_table.groupby(["uuid", "inhalt_liter", "Untergruppe", "Farbe", "Geschmacksnote"]).agg({"factored_number": np.sum, "positive_number": np.sum})

    grouped_num = grouped_num.reset_index()

    return grouped_num