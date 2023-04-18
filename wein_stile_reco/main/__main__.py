from src.load_and_prep import load_trackingevents, load_transaction
from src.style_buckets_tracking import create_tracking_style_buckets
from src.style_buckets_transaction import create_transaction_style_buckets
from src.merge_style_buckets import merge_style_buckets
import time

target_path = "csv_results/"
out_file = "style_buckets_gesamt.csv"

start1 = time.time()
print("Step_1: load transaction and trackingevents")
#-----------------------------------------------------------------------------------
trackingevents_df = load_trackingevents()
transaction_df = load_transaction()
#-----------------------------------------------------------------------------------
print("Step_1 finished")
stop1 = time.time()
print("time elapsed: " + str(stop1 - start1))
print("--------------------------------------------")
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------
start2 = time.time()
print("Step_2: create style_buckets for tracking and transaction")
##-----------------------------------------------------------------------------------
tracking_style_buckets = create_tracking_style_buckets(trackingevents_df)
transaction_style_buckets = create_transaction_style_buckets(transaction_df)
##-----------------------------------------------------------------------------------    
print("Step_2 finished")
stop2 = time.time()
print("time elapsed: " + str(stop2 - start2))
##-----------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------
start3 = time.time()
print("Step_3: merge style_buckets")
##-----------------------------------------------------------------------------------
merge_style_buckets(tracking_style_buckets, transaction_style_buckets, target_path + out_file)
##-----------------------------------------------------------------------------------    
print("Step_3 finished")
stop3 = time.time()
print("time elapsed: " + str(stop3 - start3))
##-----------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------