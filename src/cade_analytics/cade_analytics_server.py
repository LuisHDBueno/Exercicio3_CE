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

import grpc
import datasender_pb2
import datasender_pb2_grpc
from concurrent import futures

class CadeAnalyticsServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        datasender_pb2_grpc.add_DataSenderServicer_to_server(self, self.server)
        self.server.add_insecure_port('0.0.0.0:50051')  # Listen on all available network interfaces
        self.is_received = False
        self.data = None
        self.lock = mp.Lock()

    def Sender(self, request, context):
        print(f"Received data")
        received_data = request.data
        timestamp = request.begining
        print(f"Received data from {timestamp}")
        self.is_received = True
        self.lock.acquire()
        self.queue_time.put(timestamp)
        self.lock.release()
        self.queue_data.put(received_data)
        return datasender_pb2.ConfirmData(check=1)
            

    def run_simulation(self):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        reader = rd.Reader(n_threads=5, buffer_output=buffer_output)
        manager_data = mp.Manager()
        self.queue_data = manager_data.Queue()
        read_process = mp.Process(target=reader.read_threaded, args=(self.queue_data, ))
        self.queue_time = manager_data.Queue()
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
        
        time.sleep(2)
        
        self.server.start()  # Add this line to start the gRPC server
        
        while True:
            self.lock.acquire()
            total_timestamps = 0
            n = 0
            while not self.queue_time.empty():
                total_timestamps += float(self.queue_time.get())
                n+=1
            self.lock.release()
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

            now = time.time()
            if n==0:
                avg_time = 0
            else:
                avg_time = ((now*n)-total_timestamps) / n
            print(f"avg time of requests: {avg_time}")
    
if __name__ == "__main__":
    cas = CadeAnalyticsServer()
    cas.run_simulation()