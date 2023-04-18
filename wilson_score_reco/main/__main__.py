from src.load_and_prep import load_trackingevents, load_transaction
from src.add_bas_prod_view import add_bas_prod_view
from src.purchase import purchase
from src.repurchase import repurchase
from src.merge_results import merge_results
from src.price_buckets import create_price_buckets
import time

target_path = "csv_results/"
out_file = "price_buckets.csv"

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
print("Step_2: ratings for tracking and transaction")
##-----------------------------------------------------------------------------------
add_bas_prod_view_df = add_bas_prod_view(trackingevents_df)
purchase_df = purchase(transaction_df)
repurchase_df = repurchase(transaction_df)
merged_results = merge_results(add_bas_prod_view_df, purchase_df, repurchase_df)
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
create_price_buckets(merged_results, target_path + out_file)
##-----------------------------------------------------------------------------------    
print("Step_3 finished")
stop3 = time.time()
print("time elapsed: " + str(stop3 - start3))
##-----------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------
