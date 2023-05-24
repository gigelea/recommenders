import pandas as pd
import numpy as np
from recency_functions import year_to_months, recency_fac_linear

def herkunft_buckets_transaction(raw_data, path):
    transaction_table = raw_data.copy()

    v_rec_fac = np.vectorize(lambda x: recency_fac_linear(x), otypes=[np.float32])

    transaction_table["recency_factor"] = year_to_months(transaction_table['docdate'].dt.year, transaction_table['docdate'].dt.month)
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

    v_fac_rating = np.vectorize(lambda x , y: fac_rating(x, y), otypes=[np.float32])
    v_pos_rating = np.vectorize(lambda x , y: pos_rating(x, y), otypes=[np.float32])

    transaction_table["factored_number"] = v_fac_rating(transaction_table["quantity"], transaction_table["recency_factor"])
    transaction_table["positive_number"] = v_pos_rating(transaction_table["quantity"], transaction_table["factored_number"])

    grouped_num = transaction_table.groupby(["uuid", "u_b1cw_gebiet"]).agg({"factored_number": np.sum, "positive_number": np.sum})
    grouped_num = grouped_num.reset_index()

    num_of_occurences = transaction_table[["uuid", "u_b1cw_gebiet", "bookingNumber"]].groupby(["uuid", "u_b1cw_gebiet"]).count()
    num_of_occurences = num_of_occurences.reset_index()

    num_of_occurences["bookingNumber"] = num_of_occurences["bookingNumber"] - 1
    num_of_occurences = num_of_occurences[num_of_occurences["bookingNumber"] > 0]

    merge = pd.merge(num_of_occurences, transaction_table[["uuid", "u_b1cw_gebiet", "recency_factor"]], left_on = ['uuid', 'u_b1cw_gebiet'], right_on = ['uuid', 'u_b1cw_gebiet'], how="inner")
    merge.drop_duplicates(inplace=True)
    merge["positive_number"] = merge["bookingNumber"] * merge["recency_factor"]

    merge.drop(columns=["bookingNumber", "recency_factor"], inplace=True)

    grouped_again = merge.groupby(["uuid", "u_b1cw_gebiet"]).agg({"positive_number": np.sum})
    grouped_again["factored_number"] = grouped_again["positive_number"]
    grouped_again.reset_index(inplace=True)

    merge_gesamt = grouped_num.set_index(["uuid", "u_b1cw_gebiet"]).add(grouped_again.set_index(["uuid", "u_b1cw_gebiet"]), fill_value=0).reset_index()

    merge_gesamt.to_csv(path, index = False)