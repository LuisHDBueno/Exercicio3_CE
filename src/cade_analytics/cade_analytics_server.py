import random
import time
import multiprocessing as mp

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.framework.reader as rd
import cade_analytics_client as cac

import grpc
import datasender_pb2
import datasender_pb2_grpc
from concurrent import futures

class CadeAnalyticsServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        datasender_pb2_grpc.add_DataSenderServicer_to_server(self, self.server)
        self.server.add_insecure_port('[::]:50051')
        self.is_received = False

    def comunication(self):
        # AQUI É O MOCK DO CLIENTE TROCAR PELO CLIENTE REAL
        self.server.start()
        self.server.wait_for_termination()

    def Sender(self, request, context):
        print(f"Received data")
        self.received_data = request.data
        self.is_received = True
        self.queue_data.put(self.received_data)
        return datasender_pb2.ConfirmData(check=1)

    def add_data(self):
        self.comunication()
        """
        while True:
            if self.is_received:
                data = self.received_data
                for d in data:
                    self.queue_data.put(d)
                self.received = False
            else:
                time.sleep(0.5)"""
            

    def run_simulation(self):
        manager = mp.Manager()
        buffer_output = manager.Queue()
        reader = rd.Reader(n_threads=4, buffer_output=buffer_output)
        manager_data = mp.Manager()
        self.queue_data = manager_data.Queue()
        data_process = mp.Process(target=self.add_data, args=())
        read_process = mp.Process(target=reader.read_threaded, args=(self.queue_data, ))

        data_process.start()
        read_process.start()
        
        data_process.join()
        read_process.join()

if __name__ == "__main__":
    cas = CadeAnalyticsServer()
    cas.run_simulation()