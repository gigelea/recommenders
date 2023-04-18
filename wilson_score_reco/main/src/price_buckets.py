#!/usr/bin/python

import pandas as pd
import numpy as np
import math
import scipy.stats as st

def create_price_buckets(merge_results, result_path_filename):
    
    # Damit alle buckets vertreten sind
    uuid = 5000007
    # merge_results.columns # make sure to catch every single stupid bucket
    catch_all_buckets = pd.DataFrame([[uuid, "", 1, "Weiß", "Still", 0, 0],
                                      [uuid, "", 7, "Weiß", "Still", 0, 0],
                                      [uuid, "", 9, "Weiß", "Still", 0, 0],
                                      [uuid, "", 11, "Weiß", "Still", 0, 0],
                                      [uuid, "", 13, "Weiß", "Still", 0, 0],
                                      [uuid, "", 16, "Weiß", "Still", 0, 0],
                                      [uuid, "", 19, "Weiß", "Still", 0, 0],
                                      [uuid, "", 23, "Weiß", "Still", 0, 0],
                                      [uuid, "", 30, "Weiß", "Still", 0, 0],
                                      [uuid, "", 40, "Weiß", "Still", 0, 0],
                                      [uuid, "", 50, "Weiß", "Still", 0, 0],
                                      [uuid, "", 70, "Weiß", "Still", 0, 0],
                                      [uuid, "", 100, "Weiß", "Still", 0, 0],
                                      [uuid, "", 180, "Weiß", "Still", 0, 0],
                                      [uuid, "", 300, "Weiß", "Still", 0, 0],
                                      [uuid, "", 1, "Rot", "Still", 0, 0], 
                                      [uuid, "", 7, "Rot", "Still", 0, 0],
                                      [uuid, "", 9, "Rot", "Still", 0, 0],
                                      [uuid, "", 11, "Rot", "Still", 0, 0],
                                      [uuid, "", 13, "Rot", "Still", 0, 0],
                                      [uuid, "", 16, "Rot", "Still", 0, 0],
                                      [uuid, "", 19, "Rot", "Still", 0, 0],
                                      [uuid, "", 23, "Rot", "Still", 0, 0],
                                      [uuid, "", 30, "Rot", "Still", 0, 0],
                                      [uuid, "", 40, "Rot", "Still", 0, 0],
                                      [uuid, "", 50, "Rot", "Still", 0, 0],
                                      [uuid, "", 70, "Rot", "Still", 0, 0],
                                      [uuid, "", 100, "Rot", "Still", 0, 0],
                                      [uuid, "", 180, "Rot", "Still", 0, 0],
                                      [uuid, "", 300, "Rot", "Still", 0, 0],
                                      [uuid, "", 1, "Rosé", "Still", 0, 0], 
                                      [uuid, "", 7, "Rosé", "Still", 0, 0],
                                      [uuid, "", 9, "Rosé", "Still", 0, 0],
                                      [uuid, "", 11, "Rosé", "Still", 0, 0],
                                      [uuid, "", 13, "Rosé", "Still", 0, 0],
                                      [uuid, "", 16, "Rosé", "Still", 0, 0],
                                      [uuid, "", 19, "Rosé", "Still", 0, 0],
                                      [uuid, "", 23, "Rosé", "Still", 0, 0],
                                      [uuid, "", 30, "Rosé", "Still", 0, 0],
                                      [uuid, "", 40, "Rosé", "Still", 0, 0],
                                      [uuid, "", 50, "Rosé", "Still", 0, 0],
                                      [uuid, "", 70, "Rosé", "Still", 0, 0],
                                      [uuid, "", 100, "Rosé", "Still", 0, 0],
                                      [uuid, "", 180, "Rosé", "Still", 0, 0],
                                      [uuid, "", 300, "Rosé", "Still", 0, 0],
                                      [uuid, "", 1, "", "Schaumwein", 0, 0], 
                                      [uuid, "", 7, "", "Schaumwein", 0, 0],
                                      [uuid, "", 9, "", "Schaumwein", 0, 0],
                                      [uuid, "", 11, "", "Schaumwein", 0, 0],
                                      [uuid, "", 13, "", "Schaumwein", 0, 0],
                                      [uuid, "", 16, "", "Schaumwein", 0, 0],
                                      [uuid, "", 19, "", "Schaumwein", 0, 0],
                                      [uuid, "", 23, "", "Schaumwein", 0, 0],
                                      [uuid, "", 30, "", "Schaumwein", 0, 0],
                                      [uuid, "", 40, "", "Schaumwein", 0, 0],
                                      [uuid, "", 50, "", "Schaumwein", 0, 0],
                                      [uuid, "", 70, "", "Schaumwein", 0, 0],
                                      [uuid, "", 100, "", "Schaumwein", 0, 0],
                                      [uuid, "", 180, "", "Schaumwein", 0, 0],
                                      [uuid, "", 300, "", "Schaumwein", 0, 0]
                                      ], columns=merge_results.columns)
    
    merge_results = pd.concat([merge_results, catch_all_buckets], ignore_index=True)
    
    merge_results["preis_buckets"] = pd.cut(merge_results["itemPrice"], [0,6.5,8.5,10.5,12.5,14.5,17.5,20.5,27,37,47,67,97,150,250,30606], include_lowest=True)
    
    # Aggregate factored number and positive number for each color into price_buckets
    merge_results_rot = merge_results[(merge_results["Untergruppe"] == 'Still') & (merge_results["Farbe"] == 'Rot')].groupby(["uuid", "preis_buckets"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    merge_results_weiss = merge_results[(merge_results["Untergruppe"] == 'Still') & (merge_results["Farbe"] == 'Weiß')].groupby(["uuid", "preis_buckets"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    merge_results_rose = merge_results[(merge_results["Untergruppe"] == 'Still') & (merge_results["Farbe"] == 'Rosé')].groupby(["uuid", "preis_buckets"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    merge_results_schaum = merge_results[(merge_results["Untergruppe"] == 'Schaumwein')].groupby(["uuid", "preis_buckets"]).aggregate({"factored_number": np.sum, "positive_number": np.sum})
    
    merge_results_rot.reset_index(inplace=True)
    merge_results_weiss.reset_index(inplace=True)
    merge_results_rose.reset_index(inplace=True)
    merge_results_schaum.reset_index(inplace=True)
    
    # Wilson-score Function
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
    
    merge_results_rot["wilson_score_lb"] = merge_results_rot.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    merge_results_rot.reset_index(level=0, inplace=True)
    
    merge_results_weiss["wilson_score_lb"] = merge_results_weiss.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    merge_results_weiss.reset_index(level=0, inplace=True)
    
    merge_results_rose["wilson_score_lb"] = merge_results_rose.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    merge_results_rose.reset_index(level=0, inplace=True)
    
    merge_results_schaum["wilson_score_lb"] = merge_results_schaum.apply(lambda x: wilson_lower_bound(x["positive_number"], x["factored_number"]), axis=1)
    merge_results_schaum.reset_index(level=0, inplace=True)
    
    # Ab hier die Preis-buckets als Spalten
    farbe_rot = merge_results_rot.pivot_table(index = ["uuid"], 
              columns = "preis_buckets" ,
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    
    farbe_weiss = merge_results_weiss.pivot_table(index = ["uuid"],
              columns = "preis_buckets" ,
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    
    farbe_rose = merge_results_rose.pivot_table(index = ["uuid"], 
              columns = "preis_buckets" , 
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    
    farbe_schaum = merge_results_schaum.pivot_table(index = ["uuid"], 
              columns = "preis_buckets" ,
              values = "wilson_score_lb", 
              aggfunc = "sum", margins=False).fillna(0)
    
    merge_results_final = pd.concat([farbe_rot, farbe_weiss, farbe_rose, farbe_schaum], axis=1, keys=['Rot_Verteilung','Weiß_Verteilung','Rosé_Verteilung','Schaumwein_Verteilung'])
    
    merge_results_final = merge_results_final.round(4)
    merge_results_final.fillna(0,inplace=True)
    
    # Um die Fake-Values dann mit dem allgemeinen Durchschnitt zu multiplizieren
    mean = merge_results_final.mean()/merge_results_final.mean().sum()
    
    # fake values
    
    merge_results_final_copy = merge_results_final.copy()
    rot_distr = merge_results_final['Rot_Verteilung'].fillna(0).copy()
    weiss_distr = merge_results_final['Weiß_Verteilung'].fillna(0).copy()
    rose_distr = merge_results_final['Rosé_Verteilung'].fillna(0).copy()
    schw_distr = merge_results_final['Schaumwein_Verteilung'].fillna(0).copy()

    # red empty, white empty, rose empty
    # .
    # .
    # .
    # red empty

    rot_distr.mask((rot_distr.sum(axis=1) == 0), mean["Rot_Verteilung"] * (rot_distr + weiss_distr + rose_distr)/4 ,inplace = True)
    weiss_distr.mask((weiss_distr.sum(axis=1) == 0), mean["Weiß_Verteilung"] * (rot_distr + weiss_distr + rose_distr)/4 ,inplace = True)
    rose_distr.mask((rose_distr.sum(axis=1) == 0), mean["Rosé_Verteilung"] * (rot_distr + weiss_distr + rose_distr)/4 ,inplace = True)


    merge_results_final_copy['Rot_Verteilung']  = rot_distr
    merge_results_final_copy['Weiß_Verteilung'] = weiss_distr
    merge_results_final_copy['Rosé_Verteilung'] = rose_distr

    # Neighboring für alle 4 Weinfarben
    x = merge_results_final_copy.copy()

    #rot
    merge_results_final_copy.iloc[:,0] = x.iloc[:,0].fillna(0) + x.iloc[:,1].fillna(0)/4 # Randspalten zuerst
    merge_results_final_copy.iloc[:,14] = x.iloc[:,14].fillna(0) + x.iloc[:,13].fillna(0)/4 # Randspalten zuerst
    for i in range (1,14):
        merge_results_final_copy.iloc[:,i] = x.iloc[:,i-1].fillna(0) /4 + x.iloc[:,i+1].fillna(0) /4 + x.iloc[:,i].fillna(0)

    # weiss
    merge_results_final_copy.iloc[:,15] = x.iloc[:,15].fillna(0) + x.iloc[:,16].fillna(0) /4  
    merge_results_final_copy.iloc[:,29] = x.iloc[:,29].fillna(0) + x.iloc[:,28].fillna(0) /4 
    for i in range (16,29):
        merge_results_final_copy.iloc[:,i] = x.iloc[:,i-1].fillna(0) /4 + x.iloc[:,i+1].fillna(0) /4 + x.iloc[:,i].fillna(0)

    # rose
    merge_results_final_copy.iloc[:,30] = x.iloc[:,30].fillna(0) + x.iloc[:,31].fillna(0) /4  
    merge_results_final_copy.iloc[:,44] = x.iloc[:,44].fillna(0) + x.iloc[:,43].fillna(0) /4 
    for i in range (31,44):
        merge_results_final_copy.iloc[:,i] = x.iloc[:,i-1].fillna(0) /4 + x.iloc[:,i+1].fillna(0) /4 + x.iloc[:,i].fillna(0)

    # schaum
    merge_results_final_copy.iloc[:,45] = x.iloc[:,41].fillna(0) + x.iloc[:,46].fillna(0) /4  
    merge_results_final_copy.iloc[:,59] = x.iloc[:,59].fillna(0) + x.iloc[:,58].fillna(0) /4 
    for i in range (46,59):
        merge_results_final_copy.iloc[:,i] = x.iloc[:,i-1].fillna(0) /4 + x.iloc[:,i+1].fillna(0) /4 + x.iloc[:,i].fillna(0)
    
    # 4. Zeile droppen
    merge_results_final_copy.columns = pd.MultiIndex.from_tuples(merge_results_final_copy.rename(columns={('', 'preis_buckets'): ('', '')}))
    
    merge_results_final_copy.reset_index(inplace=True)
    merge_results_final_copy_d = merge_results_final_copy.set_index('uuid')

    merge_results_final_rank = merge_results_final_copy_d.rank(axis= 1, ascending = False, method='dense')
    merge_results_final_rank_100 = 1 - merge_results_final_rank/100
    
    merge_results_final_rank_100.to_csv(result_path_filename)

    # return merge_results_final_rank_100