import random
import time
import multiprocessing as mp
import pandas as pd

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd
import src.framework.handler as hd
import cade_analytics_client as cac


class CadeAnalyticsServer:

    def comunication(self):
        # AQUI É O MOCK DO CLIENTE TROCAR PELO CLIENTE REAL
        client = cac.CadeAnalyticsClient()
        yield client.get_data()

    def add_data(self, queue_data):
        while True:
            data = self.comunication()
            for d in data:
                queue_data.put(d)
                
            time.sleep(10)

    def run_simulation(self):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        reader = rd.Reader(n_threads=5, buffer_output=buffer_output)
        manager_data = mp.Manager()
        queue_data = manager_data.Queue()
        data_process = mp.Process(target=self.add_data, args=(queue_data, ))
        read_process = mp.Process(target=reader.read_threaded, args=(queue_data, ))

        data_process.start()
        read_process.start()
        
        managed_dict = manager.dict()
        managed_dict['views_per_item'] = pd.DataFrame()
        managed_dict['buys_per_item'] = pd.DataFrame()
        managed_dict['min_time_viewed'] = pd.Timestamp.max
        managed_dict['max_time_viewed'] = pd.Timestamp.min
        managed_dict['min_time_bought'] = pd.Timestamp.max
        managed_dict['max_time_bought'] = pd.Timestamp.min
        managed_dict['num_views'] = 0
        managed_dict['num_buys'] = 0
        managed_dict['avg_views_per_minute'] = 0
        managed_dict['avg_buys_per_minute'] = 0
        
        while True:
            handling_processes = []
            for _ in range(20):
                handling_processes.append(mp.Process(target=hd.Handler(data=buffer_output, managed_dict=managed_dict).handle_data))
                
            for p in handling_processes:
                p.start()
                
            for p in handling_processes:
                p.join()
            
            print(f"most viewed items:\n{managed_dict['views_per_item'].head()}")
            print(f"most bought items:\n{managed_dict['buys_per_item'].head()}")
            
            print(f"min time viewed: {managed_dict['min_time_viewed']}")
            print(f"max time viewed: {managed_dict['max_time_viewed']}")
            
            print(f"min time bought: {managed_dict['min_time_bought']}")
            print(f"max time bought: {managed_dict['max_time_bought']}")
            
            print(f"avg views per minute: {managed_dict['avg_views_per_minute']}")
            print(f"avg buys per minute: {managed_dict['avg_buys_per_minute']}")
    
        
        data_process.join()
        read_process.join()

if __name__ == "__main__":
    cas = CadeAnalyticsServer()
    cas.run_simulation()