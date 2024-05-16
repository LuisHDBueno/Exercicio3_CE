import random
import time
import multiprocessing as mp

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd

class CadeAnalyticsSimulator:
    def __init__(self, path: str = "data/cade_analytics_data.txt"):
        self.path = path
        with open(path, "r") as f:
            data = f.readlines()
            data = [line.strip() for line in data]
        self.data = data

    def get_data(self, n = 100):
        return [random.choice(self.data) for _ in range(n)]
    
    def time_trigger(self, n = 100, speed = 1):
        while True:
            data = self.get_data(n)
            yield data
            time.sleep(speed)
    
    
    def add_data(self, queue_data, buffer_output, n = 100, speed = 1):
        for data in self.time_trigger(n=n, speed=speed):
            for d in data:
                queue_data.put(d)
            while not buffer_output.empty():
                print(buffer_output.get())

        
    def run_simulation(self, n = 100, speed = 1):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        reader = rd.Reader(n_threads=4, buffer_output=buffer_output)
        manager_data = mp.Manager()
        queue_data = manager_data.Queue()
        data_process = mp.Process(target=self.add_data, args=(queue_data, buffer_output, n, speed))
        read_process = mp.Process(target=reader.read_threaded, args=(queue_data,))

        data_process.start()
        read_process.start()
        
        data_process.join()
        read_process.join()

if __name__ == "__main__":
    cas = CadeAnalyticsSimulator()
    cas.run_simulation(n=100, speed=1)
    