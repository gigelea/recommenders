# Addiere die ergebnisse der beiden style_bucket dataframes
import pandas as pd
import numpy as np
import math
import scipy.stats as st
def merge_style_buckets(style_buckets_tracking, style_buckets_transaction, final_path):

    # style_buckets_tracking = pd.read_csv(tracking_results_path)
    # style_buckets_transaction = pd.read_csv(transaction_results_path)

    style_buckets_tracking.drop(columns=["inhalt_liter"], inplace=True)
    style_buckets_transaction.drop(columns=["inhalt_liter"], inplace=True)

    merge_gesamt = style_buckets_tracking.set_index(["uuid", "Untergruppe", "Farbe", "Geschmacksnote"]).add(style_buckets_transaction.set_index(["uuid", "Untergruppe", "Farbe", "Geschmacksnote"]), fill_value=0).reset_index()


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


    all_user_data_rot = merge_gesamt[(merge_gesamt["Untergruppe"] == 'Still') & (merge_gesamt["Farbe"] == 'Rot')].groupby(["uuid", "Geschmacksnote"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    all_user_data_weiss = merge_gesamt[(merge_gesamt["Untergruppe"] == 'Still') & (merge_gesamt["Farbe"] == 'Weiß')].groupby(["uuid", "Geschmacksnote"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    all_user_data_rose = merge_gesamt[(merge_gesamt["Untergruppe"] == 'Still') & (merge_gesamt["Farbe"] == 'Rosé')].groupby(["uuid", "Geschmacksnote"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    all_user_data_schaum = merge_gesamt[(merge_gesamt["Untergruppe"] == 'Schaumwein')].groupby(["uuid", "Geschmacksnote"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})

    all_user_data_rot.reset_index(inplace=True)
    all_user_data_weiss.reset_index(inplace=True)
    all_user_data_rose.reset_index(inplace=True)
    all_user_data_schaum.reset_index(inplace=True)

    all_user_data_rot["wilson_score_lb"] = all_user_data_rot.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    all_user_data_rot.reset_index(level=0, inplace=True)
    all_user_data_weiss["wilson_score_lb"] = all_user_data_weiss.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    all_user_data_weiss.reset_index(level=0, inplace=True)
    all_user_data_rose["wilson_score_lb"] = all_user_data_rose.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    all_user_data_rose.reset_index(level=0, inplace=True)
    all_user_data_schaum["wilson_score_lb"] = all_user_data_schaum.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    all_user_data_schaum.reset_index(level=0, inplace=True)

    ## Ab hier Geschmacksnote als Spalten
    farbe_rot = all_user_data_rot.pivot_table(index = ["uuid"], 
              columns = "Geschmacksnote" ,
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    farbe_weiss = all_user_data_weiss.pivot_table(index = ["uuid"],
                columns = "Geschmacksnote" ,
                values = "wilson_score_lb", 
                aggfunc = "sum", margins=False).fillna(0)
    farbe_rose = all_user_data_rose.pivot_table(index = ["uuid"], 
                columns = "Geschmacksnote" , 
                values = "wilson_score_lb", 
                aggfunc = "sum", margins=False).fillna(0)
    farbe_schaum = all_user_data_schaum.pivot_table(index = ["uuid"], 
                columns = "Geschmacksnote" ,
                values = "wilson_score_lb", 
                aggfunc = "sum", margins=False).fillna(0)

    ## Drop empty columns, "fruchtig-frisch" & "knackig-frisch" at Redwine and "fruchtig" & "griffig" at Schaumwein
    if "" in farbe_rot.columns:
        farbe_rot = farbe_rot.drop(columns=[""])
    if "fruchtig-frisch" in farbe_rot.columns:
        farbe_rot = farbe_rot.drop(columns=["fruchtig-frisch"])
    if "knackig-frisch" in farbe_rot.columns:
        farbe_rot = farbe_rot.drop(columns=["knackig-frisch"])

    if "" in farbe_weiss.columns:
        farbe_weiss = farbe_weiss.drop(columns=[""])
    if "fruchtig-harmonisch" in farbe_weiss.columns:
        farbe_weiss = farbe_weiss.drop(columns=["fruchtig-harmonisch"])

    if "" in farbe_rose.columns:
        farbe_rose = farbe_rose.drop(columns=[""])

    if "" in farbe_schaum.columns:
        farbe_schaum = farbe_schaum.drop(columns=[""])
    if "fruchtig" in farbe_schaum.columns:
        farbe_schaum = farbe_schaum.drop(columns=["fruchtig"])
    if "griffig" in farbe_schaum.columns:
        farbe_schaum = farbe_schaum.drop(columns=["griffig"])

    ## Relocate columns
    rot_style_buckets = farbe_rot[["ausgewogen", "weich", "fruchtig", "frisch", "griffig"]]
    weiss_style_buckets = farbe_weiss[["ausgewogen", "weich", "fruchtig", "fruchtig-frisch", "knackig-frisch"]]
    rose_style_buckets = farbe_rose[["ausgewogen", "fruchtig", "knackig-frisch", "fruchtig-frisch"]]
    schaum_style_buckets = farbe_schaum[["fruchtig-harmonisch", "fruchtig-frisch", "ausgewogen", "elegant"]]
    all_user_data_final = pd.concat([rot_style_buckets, weiss_style_buckets, rose_style_buckets, schaum_style_buckets], axis=1, keys=['Rot_Verteilung','Weiß_Verteilung','Rosé_Verteilung','Schaumwein_Verteilung'])
    all_user_data_final = all_user_data_final.round(4)
    all_user_data_final.fillna(0,inplace=True)

    ### Fake-Values dann mit dem allgemeinen Durchschnitt zu multiplizieren
    mean = all_user_data_final.mean()/all_user_data_final.mean().sum()
    # fake values
    all_user_data_final_copy = all_user_data_final.copy()
    rot_distr =   all_user_data_final.iloc[:,:5].fillna(0).copy()
    weiss_distr = all_user_data_final.iloc[:,5:10].fillna(0).copy()
    rose_distr =  all_user_data_final.iloc[:,10:14].fillna(0).copy()
    schw_distr =  all_user_data_final.iloc[:,14:].fillna(0).copy()

    min_rot_distr = rot_distr.mean(axis=1)
    min_weiss_distr = weiss_distr.mean(axis=1)
    min_rose_distr = rose_distr.mean(axis=1)
    min_schw_distr = schw_distr.mean(axis=1)

    rot_distr_mean = rot_distr.copy()
    rot_distr_mean[rot_distr_mean == 0] = 1
    rot_distr_mean = mean[:5] * rot_distr_mean

    weiss_distr_mean = weiss_distr.copy()
    weiss_distr_mean[weiss_distr_mean == 0] = 1
    weiss_distr_mean = mean[5:10] * weiss_distr_mean

    rose_distr_mean = rose_distr.copy()
    rose_distr_mean[rose_distr_mean == 0] = 1
    rose_distr_mean = mean[10:14] * rose_distr_mean

    schw_distr_mean = schw_distr.copy()
    schw_distr_mean[schw_distr_mean == 0] = 1
    schw_distr_mean = mean[14:] * schw_distr_mean

    # red empty, white empty, rose empty
    # .
    # .
    # .
    # red empty
    rot_distr.mask((rot_distr.sum(axis=1) == 0), rot_distr_mean.mul((min_rot_distr + min_weiss_distr + min_rose_distr + min_schw_distr)/4, axis=0),inplace = True)
    weiss_distr.mask((weiss_distr.sum(axis=1) == 0), weiss_distr_mean.mul((min_rot_distr + min_weiss_distr + min_rose_distr + min_schw_distr)/4, axis=0),inplace = True)
    rose_distr.mask((rose_distr.sum(axis=1) == 0), rose_distr_mean.mul((min_rot_distr + min_weiss_distr + min_rose_distr + min_schw_distr)/4, axis=0),inplace = True)
    schw_distr.mask((schw_distr.sum(axis=1) == 0), schw_distr_mean.mul((min_rot_distr + min_weiss_distr + min_rose_distr + min_schw_distr)/4, axis=0),inplace = True)

    all_user_data_final_copy.iloc[:,:5] = rot_distr
    all_user_data_final_copy.iloc[:,5:10] = weiss_distr
    all_user_data_final_copy.iloc[:,10:14] = rose_distr
    all_user_data_final_copy.iloc[:,14:] = schw_distr

    # Neighboring
    ## Table wieder auftrennen

    rot_verteilung = all_user_data_final_copy.iloc[:,:5]
    weiss_verteilung = all_user_data_final_copy.iloc[:,5:10]
    rose_verteilung = all_user_data_final_copy.iloc[:,10:14]
    schaum_verteilung = all_user_data_final_copy.iloc[:,14:]

    ### get different uuid's
    all_users = all_user_data_final.index.to_list()

    ## Create distance matrices for taste
    rot = np.array([[1, 0.8, 0.6, 0.8, 0.8],
                [0.8, 1, 0.6, 0.2, 0.4],
                [0.6, 0.6, 1, 0.2, 0.8],
                [0.8, 0.2, 0.2, 1, 0.6],
                [0.8, 0.4, 0.8, 0.6, 1]])

    weiss = np.array([[1, 0.8, 0.6, 0.4, 0.6],
                    [0.8, 1, 0.8, 0.4, 0.2],
                    [0.6, 0.8, 1, 0.8, 0.2],
                    [0.4, 0.4, 0.8, 1, 0.8],
                    [0.6, 0.2, 0.2, 0.8, 1]])

    rose = np.array([[1, 0.8, 0.6, 0.8],
                    [0.8, 1, 0.2, 0.6],
                    [0.6, 0.2, 1, 0.8],
                    [0.8, 0.6, 0.8, 1]])

    schaum = np.array([[1, 0.8, 0.8, 0.6],
                    [0.8, 1, 0.8, 0.4],
                    [0.8, 0.8, 1, 0.8],
                    [0.6, 0.4, 0.8, 1]])

    ## create data for rot
    rot_list = []
    for user in all_users:
        user_vector = rot_verteilung.loc[user,:].values
        sum = np.sum(user_vector)
        row = rot.dot(user_vector)
        row = np.insert(row, 0, user) # prepend element to numpy array
        rot_list.append(row)
    rot_distance_styles = pd.DataFrame(rot_list, columns=["uuid", "ausgewogen", "weich", "fruchtig", "frisch", "griffig"])
    rot_distance_styles["uuid"] = rot_distance_styles["uuid"].astype(np.int32)

    ## create data for weiss
    weiss_list = []
    for user in all_users:
        user_vector = weiss_verteilung.loc[user,:].values
        sum = np.sum(user_vector)
        row = weiss.dot(user_vector)
        row = np.insert(row, 0, user) # prepend element to numpy array
        weiss_list.append(row)
    weiss_distance_styles = pd.DataFrame(weiss_list, columns=["uuid", "ausgewogen", "weich", "fruchtig", "fruchtig-frisch", "knackig-frisch"])
    weiss_distance_styles["uuid"] = weiss_distance_styles["uuid"].astype(np.int32)

    ## create data for rose
    rose_list = []
    for user in all_users:
        user_vector = rose_verteilung.loc[user,:].values
        sum = np.sum(user_vector)
        row = rose.dot(user_vector)
        row = np.insert(row, 0, user) # prepend element to numpy array
        rose_list.append(row)
    rose_distance_styles = pd.DataFrame(rose_list, columns=["uuid", "ausgewogen", "fruchtig", "knackig-frisch", "fruchtig-frisch"])
    rose_distance_styles["uuid"] = rose_distance_styles["uuid"].astype(np.int32)

    ## create data for schaum
    schaum_list = []
    for user in all_users:
        user_vector = schaum_verteilung.loc[user,:].values
        sum = np.sum(user_vector)
        row = schaum.dot(user_vector)
        row = np.insert(row, 0, user) # prepend element to numpy array
        schaum_list.append(row)
    schaum_distance_styles = pd.DataFrame(schaum_list, columns=["uuid", "fruchtig-harmonisch", "fruchtig-frisch", "ausgewogen", "elegant"])
    schaum_distance_styles["uuid"] = schaum_distance_styles["uuid"].astype(np.int32)

    ### setze "uuid" für alle styles als index
    rot_distance_styles.set_index("uuid", inplace=True)
    weiss_distance_styles.set_index("uuid", inplace=True)
    rose_distance_styles.set_index("uuid", inplace=True)
    schaum_distance_styles.set_index("uuid", inplace=True)

    style_bucket_table_final = pd.concat([rot_distance_styles, weiss_distance_styles, rose_distance_styles, schaum_distance_styles], axis=1, keys=['Rot_Verteilung','Weiß_Verteilung','Rosé_Verteilung','Schaumwein_Verteilung'])
    style_bucket_table_final = style_bucket_table_final.round(5)

    ### catch values between 0 and 1
    style_bucket_table_final_rank = style_bucket_table_final.rank(axis= 1, ascending = False, method='dense')
    style_bucket_table_final_100 = (1 - style_bucket_table_final_rank/100) ** 3

    # style_bucket_table_final = style_bucket_table_final.apply(lambda x: 1 - np.exp(-x)).round(4)

    style_bucket_table_final_100.to_csv(final_path)