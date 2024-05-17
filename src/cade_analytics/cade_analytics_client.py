import random
import time
import multiprocessing as mp
import grpc
import datasender_pb2
import datasender_pb2_grpc

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
        self.channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
        self.stub = datasender_pb2_grpc.DataSenderStub(self.channel)
        print(self.channel)

    def get_data(self, n:int = 100):
        str_list = [random.choice(self.data) for _ in range(n)]
        unified_string = '\n'.join(str_list)
        return unified_string
    
    def time_trigger(self, n:int = 100, speed:int = 1):
        #for i in range(10):
        data = self.get_data(n)
        response = self.stub.Sender(datasender_pb2.SendData(data=data))
        time.sleep(speed)
        print(f"Client {os.getpid()} sent {n} data points with response: {response.check}")

if __name__ == "__main__":
    if os.environ.get('https_proxy'):
        del os.environ['https_proxy']
    if os.environ.get('http_proxy'):
        del os.environ['http_proxy']

    n_clients = 2
    client_process = []
    for i in range(n_clients):
        client = CadeAnalyticsClient()
        client_process.append(mp.Process(target=client.time_trigger, args=(10, 1)))
        client_process[i].start()
        print(f"Client {i} started")
    
    for i in range(n_clients):
        client_process[i].join()
        print(f"Client {i} finished")