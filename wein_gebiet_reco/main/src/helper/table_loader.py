from sqlalchemy.engine import create_engine
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import urllib3
urllib3.disable_warnings()
from sqlalchemy.sql import text
import os

class TableLoader(object):

    def __init__(self, sql_string, target_path, years = 2):
        self.sql_string = sql_string
        self.years = years
        self.target_path = target_path

    def load_table(self):

        now = datetime.datetime.now()
        then = now - relativedelta(years = self.years)

        now_str = now.strftime('%Y-%m-%d')
        now_str = now_str + 'T00:00:00.000Z'
        then_str = then.strftime('%Y-%m-%d')
        then_str = then_str + 'T00:00:00.000Z'

        print(now_str)
        print(then_str)

        engine = create_engine('druid+https://hw-druid-query.nip-base.svc.cluster.local:8082/druid/v2/sql?header=true', connect_args={'scheme': 'https', 'ssl_verify_cert': False})
        
        query = text(self.sql_string)
        query = query.bindparams(stop = now_str, start = then_str)

        dataframe_chunks = pd.read_sql_query(query, engine, chunksize = 10000)
        
         # exakt doppelte zeilen droppen da durch einen bug product_views doppelt sind
        
        if os.path.exists(self.target_path):
            os.remove(self.target_path)
            i = 0
            for chunk in dataframe_chunks:
                if i == 0:
                    chunk = chunk.drop_duplicates()
                    chunk.to_csv(self.target_path, mode = "a", index = False)
                else:
                    chunk = chunk.drop_duplicates()
                    chunk.to_csv(self.target_path, mode = "a", index = False, header = False)
                i += 1 
        else:
            i = 0
            for chunk in dataframe_chunks:
                if i == 0:
                    chunk = chunk.drop_duplicates()
                    chunk.to_csv(self.target_path, mode = "a", index = False)
                else:
                    chunk = chunk.drop_duplicates()
                    chunk.to_csv(self.target_path, mode = "a", index = False, header = False)
                i += 1   
