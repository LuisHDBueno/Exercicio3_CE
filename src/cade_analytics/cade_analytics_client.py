import random
import time
import multiprocessing as mp
import grpc
import datasender_pb2
import datasender_pb2_grpc

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def time_trigger(n:int = 100, speed:int = 1, server_address: str = '0.0.0.0:50051'):
    """ Triggers the client to send data to the server at a given speed. Runs indefinitely.
    
    Args:
        n (int): Number of data points to be sent
        speed (int): Time in seconds between each request
        server_address (str): Address of the server
    """
    while True:
        client = CadeAnalyticsClient(server_address=server_address)
        data = client.get_data(n)
        response = client.stub.Sender(datasender_pb2.SendData(data=data))
        time.sleep(speed)
        print(f"Client {os.getpid()} sent {n} data points with response: {response.check}")

class CadeAnalyticsClient:
    """ Client class to send data to the server.
    
    Attributes:
        path (str): Path to the data file
        data (list): List of data points
        channel (grpc.channel): gRPC channel object
        stub (grpc.stub): gRPC stub object
        
    Methods:
        get_data: Get n data points from the data file
        
    """
    def __init__(self, path: str = "data/cade_analytics_data.txt", server_address: str = '0.0.0.0:50051'):
        self.path = path
        with open(path, "r") as f:
            data = f.readlines()
            data = [line.strip() for line in data]
        self.data = data
        self.channel = grpc.insecure_channel(server_address, options=(('grpc.enable_http_proxy', 0),))
        self.stub = datasender_pb2_grpc.DataSenderStub(self.channel)
        print(self.channel)

    def get_data(self, n:int = 1000):
        """ Creates data message to be sent to the server.
        
        Args:
            n (int): Number of data points to be sent
            
        Returns:
            str: String with n datapoints
        """
        str_list = [random.choice(self.data) for _ in range(n)]
        unified_string = '\n'.join(str_list)
        return unified_string

if __name__ == "__main__":
    if os.environ.get('https_proxy'):
        del os.environ['https_proxy']
    if os.environ.get('http_proxy'):
        del os.environ['http_proxy']

    n_clients = 10
    server_address = '192.168.0.22:50051'  # Ip do servidor, precisa ser trocado
    client_process = []
    for i in range(n_clients):
        client_process.append(mp.Process(target=time_trigger, args=(10, 1, server_address)))
        client_process[i].start()
        print(f"Client {i} started")
    
    for i in range(n_clients):
        client_process[i].join()
        print(f"Client {i} finished")