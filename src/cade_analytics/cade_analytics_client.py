import random
import time
import multiprocessing as mp

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd

class CadeAnalyticsClient:
    def __init__(self, path: str = "data/cade_analytics_data.txt"):
        self.path = path
        with open(path, "r") as f:
            data = f.readlines()
            data = [line.strip() for line in data]
        self.data = data

    def get_data(self, n:int = 10000):
        return [random.choice(self.data) for _ in range(n)]
    
    def time_trigger(self, n:int = 100, speed:int = 1):
        while True:
            data = self.get_data(n)
            yield data
            time.sleep(speed)
