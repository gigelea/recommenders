import pandas as pd
import numpy as np
from helper_functions import year_to_months, recency_fac_linear

def herkunft_buckets_tracking(add_bas_pro_view_events, path):
    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    add_bas_pro_view_events["recency_factor"] = year_to_months(add_bas_pro_view_events['timestamp'].dt.year, add_bas_pro_view_events['timestamp'].dt.month)
    add_bas_pro_view_events["recency_factor"] = v_rec_fac(add_bas_pro_view_events["recency_factor"]).astype(float)

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

    add_bas_pro_view_events["factored_number"] = v_fac_rating(add_bas_pro_view_events["event_type"], add_bas_pro_view_events["recency_factor"])
    add_bas_pro_view_events["positive_number"] = v_pos_rating(add_bas_pro_view_events["event_type"], add_bas_pro_view_events["factored_number"])

    grouped_num = add_bas_pro_view_events.groupby(["uuid", "u_b1cw_gebiet"]).agg({"factored_number": np.sum, "positive_number": np.sum})
    grouped_num = grouped_num.reset_index()

    grouped_num.to_csv(path, index = False)
