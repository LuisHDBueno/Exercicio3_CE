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

class CadeAnalyticsServer(datasender_pb2_grpc.DataSenderServicer):
    def __init__(self):
        self.is_received = False
        self.manager = mp.Manager()
        self.buffer_output = self.manager.Queue()
        self.reader = rd.Reader(n_threads=4, buffer_output=self.buffer_output)
        self.manager_data = mp.Manager()
        queue_data = self.manager_data.Queue()
        self.data_process = mp.Process(target=self.add_data, args=(queue_data, ))
        self.read_process = mp.Process(target=self.reader.read_threaded, args=(queue_data, ))

        self.data_process.start()
        self.read_process.start()
        
        self.data_process.join()
        self.read_process.join()

    def Sender(self, request, context):
        result = request.data.upper()
        print(f"Received: {result}")
        if result == "AAAAA":
            return datasender_pb2.ConfirmData(check=1)
        return datasender_pb2.ConfirmData(check=0)
    
    def add_data(self, queue_data):
        while True:
            if self.is_received:
                data = self.received_data
                for d in data:
                    queue_data.put(d)
                self.received = False
            else:
                time.sleep(0.5)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datasender_pb2_grpc.add_DataSenderServicer_to_server(CadeAnalyticsServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()