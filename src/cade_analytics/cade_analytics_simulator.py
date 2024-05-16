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
    

if __name__ == "__main__":
    cas = CadeAnalyticsSimulator()
    manager = mp.Manager()
    buffer_output = manager.Queue()
    reader = rd.Reader(n_threads=4, buffer_output=buffer_output)
    manager_data = mp.Manager()
    queue_data = manager_data.Queue()
    mp.Process(target=reader.read_threaded, args=(queue_data,)).start()
    for data in cas.time_trigger(n=5, speed=1):
        for d in data:
            queue_data.put(d)
        while not buffer_output.empty():
            print(buffer_output.get())