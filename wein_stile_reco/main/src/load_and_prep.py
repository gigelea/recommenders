import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import urllib3
urllib3.disable_warnings()
from sqlalchemy.sql import text
import os

today = date.today()
then = today - relativedelta(years = 2)
mysql_pw = os.getenv("MYSQL_PASSWORD")

engine = (f'mysql+pymysql://root:{mysql_pw}@localhost:3306/weinco_tables')

transaction_query = text('''
    select t1.docdate,
    t2.itemcode,
    t1.cardcode as uuid,
    t1.docnum as bookingNumber,
    t1.quantity,
    t1.bruttowert as itemPrice,
    t2.lstevlpric as single_itemPrice,
    t2.u_b1cw_inhliter as inhalt_liter,
    t2.u_b1cw_attributkat1 as Geschmacksnote,
    t2.u_b1cw_untergruppe as Untergruppe,
    t2.u_b1cw_attributkat2,
    t2.u_b1cw_attributkat3,
    t2.u_b1cw_farbe as Farbe
    FROM weinco_tables.transactions as t1

    inner join weinco_tables.items as t2 
    on t1.itemcode = t2.itemcode
    WHERE t1.cardcode BETWEEN '1000000' and '9999999'
    AND whscode NOT IN (101, 103, 105, 107, 109, 205, 301)
    AND t1.cardcode NOT IN ('5999999')
    AND docdate > (:date)
    AND t2.u_b1cw_artikelgruppe = 'Wein (aus Trauben)'

     ''')

tracking_query = text('''
    select t1.timestamp,
    t1.itemid,
    t1.uuid,
    t1.event_type,
    t1.actualGrossPrice,
    t2.u_b1cw_inhliter as inhalt_liter,
    t2.u_b1cw_attributkat1 as Geschmacksnote,
    t2.u_b1cw_untergruppe as Untergruppe,
    t2.u_b1cw_attributkat2,
    t2.u_b1cw_attributkat3,
    t2.u_b1cw_farbe as Farbe
    FROM weinco_tables.trackingevents t1

    join weinco_tables.items t2
    on t1.itemid = t2.itemcode
    WHERE event_type in ('addtobasket', 'productview')
	AND t2.U_B1CW_Artikelgruppe = 'Wein (aus Trauben)'
	AND t1.uuid between '1000000' AND '9999999'
	AND t1.uuid NOT IN ('5999999', '5e2bafe0fede462d.1572452043.2.1580903987.1580903180.')
    AND timestamp > (:date)

    ''')

def load_transaction():
    transaction = pd.read_sql_query(transaction_query, engine, params={"date": then})

    # docdate to datetime datatype
    transaction['docdate'] = pd.to_datetime(transaction['docdate'].copy()) # <---- slice of a copy warning

    return transaction

def load_trackingevents():
    trackingevents = pd.read_sql_query(tracking_query, engine, params={"date": then})
    trackingevents = trackingevents.drop_duplicates() # exakt doppelte zeilen droppen da durch einen bug product_views doppelt sind

    # docdate to datetime datatype
    trackingevents['timestamp'] = pd.to_datetime(trackingevents['timestamp'].copy()) # <---- slice of a copy warning
    return trackingevents