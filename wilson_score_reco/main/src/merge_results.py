import pandas as pd
import numpy as np

def merge_results(add_bas_prod_view_df, purchase_df, repurchase_df):
    
    add_bas_prod_view_df.rename(columns={"itemid": "itemcode"}, inplace=True)

    add_bas_prod_view_df.drop(columns=["inhalt_liter"], inplace=True)
    purchase_df.drop(columns=["inhalt_liter"], inplace=True)
    repurchase_df.drop(columns=["inhalt_liter"], inplace=True)
    
    add_bas_prod_view_df.rename(columns={"actualGrossPrice": "itemPrice"}, inplace=True)
        
    # Mit dataframe.add() alle drei dataframes kombinieren
    merge_gesamt = purchase_df.set_index(["uuid", "itemcode", "itemPrice", "Untergruppe", "Farbe"]).add(repurchase_df.set_index(["uuid", "itemcode", "itemPrice", "Untergruppe", "Farbe"]), fill_value=0).reset_index()

    merge_gesamt = merge_gesamt.set_index(["uuid", "itemcode", "itemPrice", "Untergruppe", "Farbe"]).add(add_bas_prod_view_df.set_index(["uuid", "itemcode", "itemPrice", "Untergruppe", "Farbe"]), fill_value=0).reset_index()
    
    merge_gesamt = merge_gesamt.round(4)

    merge_gesamt["Farbe"] = merge_gesamt["Farbe"].map({0.0:"undefiniert", 1.0: "Weiß", 2.0: "Rosé", 3.0:"Rot"})
    
    return merge_gesamt