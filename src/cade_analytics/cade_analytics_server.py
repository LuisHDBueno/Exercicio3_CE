import time
import multiprocessing as mp
import pandas as pd

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd
import src.framework.handler as hd

import grpc
import datasender_pb2
import datasender_pb2_grpc
from concurrent import futures

class CadeAnalyticsServer:
    """ Server class resposible for receiving data from clients and processing it.
    
    Attributes:
        server (grpc.server): gRPC server object
        data (str): Data received from clients
        
    Methods:
        Sender: Receives data from clients and puts it in the queue
        run_simulation: Starts the gRPC server and processes data
    """
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        datasender_pb2_grpc.add_DataSenderServicer_to_server(self, self.server)
        self.server.add_insecure_port('0.0.0.0:50051')  # Listen on all available network interfaces
        self.data = None

    def Sender(self, request, context):
        received_data = request.data
        self.queue_data.put(received_data)
        
        return datasender_pb2.ConfirmData(check=1)
        

    def run_simulation(self):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        self.queue_data = manager.Queue()
        
        reader = rd.Reader(n_threads=5, buffer_output=buffer_output)
        read_process = mp.Process(target=reader.read_threaded, args=(self.queue_data, ))
        read_process.start()
        
        # Initialize managed dictionary
        # This is the output dict for analytics
        managed_dict = manager.dict()
        managed_dict['views_per_item'] = pd.DataFrame()
        managed_dict['buys_per_item'] = pd.DataFrame()
        managed_dict['min_time_viewed'] = pd.Timestamp.max
        managed_dict['max_time_viewed'] = pd.Timestamp.min
        managed_dict['min_time_bought'] = pd.Timestamp.max
        managed_dict['max_time_bought'] = pd.Timestamp.min
        managed_dict['num_views'] = 10e-6 # Avoid division by zero
        managed_dict['num_buys'] = 10e-6 # Avoid division by zero
        managed_dict['avg_views_per_minute'] = 0
        managed_dict['avg_buys_per_minute'] = 0
        
        self.server.start()  # Start the gRPC server
        
        # Wait for the queue to have data
        time.sleep(3)
        
        # Run the analytics
        while True:
            handling_processes = []
            
            # Create 20 handler processes
            for _ in range(20):
                handling_processes.append(mp.Process(target=hd.Handler(data=buffer_output, managed_dict=managed_dict).handle_data))
                
            for p in handling_processes:
                p.start()
            
            # Handlers pop data from the buffer until it is empty,
            # after which they run the processing pipeline to the end
            for p in handling_processes:
                p.join()
            
            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Report the results
            print("===\n", f"most viewed items:\n{managed_dict['views_per_item'].head()}\n")
            print(f"most bought items:\n{managed_dict['buys_per_item'].head()}", end="\n\n")
            
            print(f"min time viewed: {managed_dict['min_time_viewed']}")
            print(f"max time viewed: {managed_dict['max_time_viewed']}", end="\n\n")
            
            print(f"min time bought: {managed_dict['min_time_bought']}")
            print(f"max time bought: {managed_dict['max_time_bought']}", end="\n\n")
            
            print(f"avg views per minute: {managed_dict['avg_views_per_minute']}")
            print(f"avg buys per minute: {managed_dict['avg_buys_per_minute']}", end="\n===\n")
    
if __name__ == "__main__":
    cas = CadeAnalyticsServer()
    cas.run_simulation()