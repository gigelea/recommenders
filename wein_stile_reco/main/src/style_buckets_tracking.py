import pandas as pd
import numpy as np
from src.helper.helper_functions import year_to_months, recency_fac_linear

def create_tracking_style_buckets(raw_data):
    add_bas_pro_view_events = raw_data.drop_duplicates().copy()

    add_bas_pro_view_events["Farbe"] = add_bas_pro_view_events["Farbe"].map({0.0:"undefiniert", 1.0: "Weiß", 2.0: "Rosé", 3.0:"Rot"})

    ### Remove leading and trailing spacecs in Geschmacksnote
    add_bas_pro_view_events["Geschmacksnote"] = add_bas_pro_view_events["Geschmacksnote"].replace(np.nan, '', regex=True)
    add_bas_pro_view_events["Geschmacksnote"] = add_bas_pro_view_events["Geschmacksnote"].apply(lambda x: x.strip())

    add_bas_pro_view_events = add_bas_pro_view_events.fillna(0)

    ## productview und addtobasket wie im wilson_score
    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    add_bas_pro_view_events["year"] = pd.DatetimeIndex(add_bas_pro_view_events['timestamp']).year.astype(int)
    add_bas_pro_view_events["month"] = pd.DatetimeIndex(add_bas_pro_view_events['timestamp']).month.astype(int)

    add_bas_pro_view_events["recency_factor"] = year_to_months(add_bas_pro_view_events["year"], add_bas_pro_view_events["month"])
    add_bas_pro_view_events["recency_factor"] = v_rec_fac(add_bas_pro_view_events["recency_factor"]).astype(float)

    def fac_rating(eventType, recency_factor):
        if eventType == "productview":
            rating = recency_factor * 0.4
            return rating
        elif eventType == "addtobasket":
            rating = recency_factor * 0.5
            return rating

    def pos_rating(eventType, factored_number):
        if eventType == "productview":
            rating = factored_number * 0.7
            return rating
        elif eventType == "addtobasket":
            rating = factored_number * 0.8
            return rating

    v_fac_rating = np.vectorize(lambda x , y: fac_rating(x, y), otypes=[np.float32]) # vectorize behandelt bei default alles als int, daher float sonst rundet er
    v_pos_rating = np.vectorize(lambda x , y: pos_rating(x, y), otypes=[np.float32])

    # print(add_bas_pro_view_events)
    # print(add_bas_pro_view_events["recency_factor"])

    add_bas_pro_view_events["factored_number"] = v_fac_rating(add_bas_pro_view_events["event_type"], add_bas_pro_view_events["recency_factor"]) # <---- value_error
    add_bas_pro_view_events["positive_number"] = v_pos_rating(add_bas_pro_view_events["event_type"], add_bas_pro_view_events["factored_number"])

    grouped_num = add_bas_pro_view_events.groupby(["uuid", "inhalt_liter", "Untergruppe", "Farbe", "Geschmacksnote"]).agg({"factored_number": np.sum, "positive_number": np.sum})
    grouped_num = grouped_num.reset_index()

    return grouped_num