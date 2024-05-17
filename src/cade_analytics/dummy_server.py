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
        self.queue_data = self.manager_data.Queue()
        self.read_process = mp.Process(target=self.reader.read_threaded, args=(self.queue_data, ))

        self.read_process.start()
        self.read_process.join()

    def Sender(self, request, context):
        print(f"Received data")
        result = request.data
        try:
            self.queue_data.put(result)
            return datasender_pb2.ConfirmData(check=1)
        except:
            return datasender_pb2.ConfirmData(check=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datasender_pb2_grpc.add_DataSenderServicer_to_server(CadeAnalyticsServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()