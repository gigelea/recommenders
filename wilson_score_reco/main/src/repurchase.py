import pandas as pd
import numpy as np
import time
from src.helper.helper_functions import year_to_months, recency_fac_linear

def repurchase(dataframe):    
    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    dataframe["year"] = pd.DatetimeIndex(dataframe['docdate']).year
    dataframe["month"] = pd.DatetimeIndex(dataframe['docdate']).month

    dataframe["recency_factor"] = year_to_months(dataframe["year"], dataframe["month"])
    dataframe["recency_factor"] = v_rec_fac(dataframe["recency_factor"])

    dataframe['itemPrice'] = dataframe['itemPrice'] / dataframe['quantity']

    dataframe["itemPrice"] = dataframe["itemPrice"] *.75 /dataframe["inhalt_liter"]

    dataframe = dataframe.round(4)

    grouped_num = dataframe.groupby(["uuid", "itemcode", "bookingNumber", "itemPrice", "inhalt_liter", "Untergruppe", "Farbe"]).agg({"recency_factor": np.mean}) # durchschnitt weil die summe mehrerer gleicher objekte nicht sinnvoll wäre
    grouped_num = grouped_num.reset_index()

    # indices der ersten purchases finden
    all_users = grouped_num["uuid"].unique()

    rows_remover_list = []
    for user in all_users:
        single_user = grouped_num.loc[np.in1d(grouped_num["uuid"], user)] # sehr sehr langsam
        for item in single_user["itemcode"]:
            rows_remover_list.append(single_user.index[single_user["itemcode"].tolist().index(item)]) # runtime warning

    rows_remover_list = list(set(rows_remover_list))

    grouped_num.drop(rows_remover_list, inplace=True)

    # letzter groupby
    # Nochmal gruppieren für verschiedene bookingNumbers
    grouped_num_bnr = grouped_num.groupby(["uuid", "itemcode", "itemPrice", "inhalt_liter", "Untergruppe", "Farbe"]).agg({"recency_factor": np.sum})
    grouped_num_bnr = grouped_num_bnr.reset_index()

    grouped_num_bnr.rename(columns={"recency_factor": "factored_number"}, inplace=True)
    grouped_num_bnr["positive_number"] = grouped_num_bnr["factored_number"]

    return grouped_num_bnr