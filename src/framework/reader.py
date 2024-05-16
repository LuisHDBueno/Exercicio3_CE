import multiprocessing as mp

class Reader():
    def __init__(self, n_threads=1, buffer_output: mp.Queue = None):
        """ Reader class to read data from a source.

        :param n_threads: Number of threads for a reader, defaults to 1
        :type n_threads: int, optional
        :param buffer_output: Buffer for the output of the data, defaults to bf.Buffer(10)
        :type buffer_output: bf.Buffer, optional
        """        
        self.n_threads = n_threads
        if buffer_output is None:
            manager = mp.Manager()
            buffer_output = manager.Queue()
        self.buffer_output = buffer_output
        self.threads_list = []

    @staticmethod
    def read(buffer_output: mp.Queue, requests: mp.Queue, sep = ","):
        """ Read data from a source.

        :param buffer_output: Buffer for the output of the data.
        :type buffer_output: mp.Queue
        :param requests: Data to be read.
        :type requests: mp.Queue
        :param sep: Separator for the data, defaults to ","
        :type sep: str, optional
        """        
        while not requests.empty():
            data = requests.get()
            colums = data.split(sep)
            # fazer regex para verificar o formato dos dados
            buffer_output.put(colums)
        print("fazer regex")

    def read_threaded(self, requests: mp.Queue):
        """ Split the reading process into multiple threads.
        """
        for i in range(self.n_threads):
            t = mp.Process(target=self.read, args=(self.buffer_output, requests))
            self.threads_list.append(t)
            t.start()
        for t in self.threads_list:
            t.join()

if __name__ == "__main__":
    import random
    def randon_request(n = 100):
        manager = mp.Manager()
        requests = manager.Queue()
        for _ in range(n):
            requests.put(f"{random.randint(0, 100)},{random.randint(0, 100)}")
        return requests
    
    manager = mp.Manager()
    buffer_output = manager.Queue()
    reader = Reader(n_threads=4, buffer_output=buffer_output)
    reader.read_threaded(randon_request())
    for _ in range(4):
        data = buffer_output.get()
        print(data)

