# Addiere die ergebnisse der beiden gebiet_bucket dataframes
import pandas as pd
import numpy as np
import math
import scipy.stats as st
import sys
from time import time
import gc

tracking_results_path_m = r"C:\Users\gia\Desktop\datascience\Wein_gebiet_reco\csv_results\gebiet_buckets_tracking.csv"
transaction_results_path_m = r"C:\Users\gia\Desktop\datascience\Wein_gebiet_reco\csv_results\gebiet_buckets_transaction.csv"
final_path_m = r"C:\Users\gia\Desktop\datascience\Wein_gebiet_reco\csv_results\herkunft_buckets_allusers.csv"


def merge_gebiet_buckets(tracking_results_path, transaction_results_path, final_path):
    # start = time()
    gebiet_buckets_tracking = pd.read_csv(tracking_results_path)
    gebiet_buckets_transaction = pd.read_csv(transaction_results_path)

    merge_gesamt = gebiet_buckets_tracking.set_index(["uuid", "itemU_B1CW_Gebiet"]).add(gebiet_buckets_transaction.set_index(["uuid", "itemU_B1CW_Gebiet"]), fill_value=0).reset_index()

    # stupid wilson_score
    def wilson_lower_bound(pos, n, confidence = 0.95):
        """
        Function to provide lower bound of wilson score
        :param pos: No of positive ratings: positive_number
        :param n: Total number of ratings: factored_number
        :param confidence: Confidence interval, by default is 95 %
        :return: Wilson Lower bound score
        """
        if n == 0:
            return 0
        z = st.norm.ppf(1 - (1 - confidence) / 2) # z-wert
        phat = 1.0 * pos / n
        return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

    all_user_data = merge_gesamt.groupby(["uuid", "itemU_B1CW_Gebiet"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    all_user_data.reset_index(inplace=True)
    # free up memory here
    del merge_gesamt
    # print(2)
    all_users = all_user_data["uuid"].unique()

    all_user_data["wilson_score_lb"] = all_user_data.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    all_user_data.reset_index(level=0, inplace=True)
    # print(sys.getsizeof(all_user_data))
    # print(3)
    ## Ab hier Region als Spalten
    all_user_data_pivot = all_user_data.pivot_table(index = ["uuid"], 
              columns = "itemU_B1CW_Gebiet" ,
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    
    gebiet_distance_df = all_user_data_pivot.corr(method='pearson')

    gebiet_distance_matrix = gebiet_distance_df.to_numpy()
    # free up memory here
    del all_user_data
    gc.collect()
    # print(4)
    all_list = []
    for user in all_users:
        user_vector = all_user_data_pivot.loc[user,:].values
        row = gebiet_distance_matrix.dot(user_vector)
        row = np.insert(row, 0, user) # prepend element to numpy array
        all_list.append(row)
    # print(sys.getsizeof(all_list))
    # print(5)
    all_distance_gebiet = pd.DataFrame(all_list, columns=["uuid"] + list(all_user_data_pivot.columns))
    all_distance_gebiet["uuid"] = all_distance_gebiet["uuid"].astype(np.int32)

    all_distance_gebiet.set_index("uuid", inplace=True)

    all_distance_gebiet = all_distance_gebiet.round(5)
    # print(6)
    all_distance_gebiet = all_distance_gebiet.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=1)

    all_distance_gebiet = all_distance_gebiet.drop(columns=["l"])
    all_distance_gebiet = all_distance_gebiet.round(5)
    # print(7)
    all_distance_gebiet.to_csv(final_path)

    # stop = time()
    # print(stop-start)

if __name__ == "__main__":
    merge_gebiet_buckets(tracking_results_path_m, transaction_results_path_m, final_path_m)