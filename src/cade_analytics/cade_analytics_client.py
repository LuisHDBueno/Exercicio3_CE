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
    """Class to handle the client of the cade analytics system.
    """
    def __init__(self, path: str = "data/cade_analytics_data.txt", server_address: str = '0.0.0.0:50051'):
        """Initialize the client.

        :param path: Path to the data file, defaults to "data/cade_analytics_data.txt"
        :type path: str, optional
        :param server_address: Address of the server, defaults to '
        :type server_address: str, optional
        """
        self.path = path
        with open(path, "r") as f:
            data = f.readlines()
            data = [line.strip() for line in data]
        self.data = data
        self.channel = grpc.insecure_channel(server_address, options=(('grpc.enable_http_proxy', 0),))
        self.stub = datasender_pb2_grpc.DataSenderStub(self.channel)
        print(self.channel)

    def get_data(self, n:int = 1000):
        """Get data from the client.

        :param n: Number of data points to get, defaults to 1000
        :type n: int, optional
        :return: Data points.
        :rtype: str
        """
        str_list = [random.choice(self.data) for _ in range(n)]
        unified_string = '\n'.join(str_list)
        return unified_string
    
def time_trigger(n:int = 100, speed:int = 1, server_address: str = '0.0.0.0:50051'):
    """Trigger the client to send data.

    :param n: Number of data points to send, defaults to 100
    :type n: int, optional
    :param speed: Speed of sending data, defaults to 1
    :type speed: int, optional
    :param server_address: Address of the server, defaults to '
    :type server_address: str, optional
    """
    while True:
        client = CadeAnalyticsClient(server_address=server_address)
        data = client.get_data(n)
        timestamp = str(time.time())
        response = client.stub.Sender(datasender_pb2.SendData(data=data, begining=timestamp))
        time.sleep(speed)
        print(f"Client {os.getpid()} sent {n} data points with response: {response.check}")

if __name__ == "__main__":
    if os.environ.get('https_proxy'):
        del os.environ['https_proxy']
    if os.environ.get('http_proxy'):
        del os.environ['http_proxy']

    n_clients = 20
    server_address = '192.168.0.71:50051'  # Ip do servidor, precisa ser trocado
    client_process = []
    for i in range(n_clients):
        client_process.append(mp.Process(target=time_trigger, args=(100, 1, server_address)))
        client_process[i].start()
        print(f"Client {i} started")
        time.sleep(50)
    
    for i in range(n_clients):
        client_process[i].join()
        print(f"Client {i} finished")