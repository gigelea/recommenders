from src.load_and_prep import load_transaction, load_trackingevents
from src.herkunft_buckets_tracking import herkunft_buckets_tracking
from src.herkunft_buckets_transaction import herkunft_buckets_transaction
from src.merge_results import merge_gebiet_buckets
import sys
import time
import os
import pandas as pd

target_path = "csv_results/"
out_file = "gebiet_buckets_gesamt.csv"

tracking_results_path = "csv_results/gebiet_buckets_tracking.csv"
transaction_results_path = "csv_results/gebiet_buckets_transaction.csv"

start1 = time.time()
print("Step_1: load trackingevents")
#-----------------------------------------------------------------------------------
tracking_df = load_trackingevents()
transaction_df = load_transaction()
#-----------------------------------------------------------------------------------
print("Step_1 finished")
stop1 = time.time()
print("time elapsed: " + str(stop1 - start1))
print("--------------------------------------------")
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------
start4 = time.time()
print("Step_3: create gebiet_buckets for tracking and transaction")
##-----------------------------------------------------------------------------------

herkunft_buckets_tracking(tracking_df, tracking_results_path)
herkunft_buckets_transaction(transaction_df, transaction_results_path)

##-----------------------------------------------------------------------------------    
print("Step_3 finished")
stop4 = time.time()
print("time elapsed: " + str(stop4 - start4))
##-----------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------
start4 = time.time()
print("Step_4: merge gebiet_buckets")
##-----------------------------------------------------------------------------------

merge_gebiet_buckets(tracking_results_path, transaction_results_path, target_path + out_file)

##-----------------------------------------------------------------------------------    
print("Step_4 finished")
stop4 = time.time()
print("time elapsed: " + str(stop4 - start4))
##-----------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------