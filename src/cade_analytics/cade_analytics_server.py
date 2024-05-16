import random
import time
import multiprocessing as mp

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd
import cade_analytics_client as cac

class CadeAnalyticsServer:
    def time_trigger(self, n = 100, speed = 1):
        while True:
            data = self.get_data(n)
            yield data
            time.sleep(speed)
    
    def add_data(self, queue_data, data):
        for d in data:
            queue_data.put(d)

    def run_simulation(self, n = 100, speed = 1):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        reader = rd.Reader(n_threads=4, buffer_output=buffer_output)
        manager_data = mp.Manager()
        queue_data = manager_data.Queue()
        client = cac.CadeAnalyticsClient()
        data_process = mp.Process(target=self.add_data, args=(queue_data, client.time_trigger(n, speed)))
        read_process = mp.Process(target=reader.read_threaded, args=(queue_data, buffer_output))

        data_process.start()
        read_process.start()
        
        data_process.join()
        read_process.join()

if __name__ == "__main__":
    cas = CadeAnalyticsServer()
    cas.run_simulation(n=100, speed=1)
    