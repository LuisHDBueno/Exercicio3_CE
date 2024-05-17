import multiprocessing as mp
import regex as re

class Reader():
    def __init__(self, n_threads=10, buffer_output: mp.Queue = None):
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
    def transform(data: str, sep = ","):
        """ Transform data into a list of columns.

        :param data: Data to be transformed.
        :type data: str
        :param sep: Separator for the data, defaults to ","
        :type sep: str, optional
        :return: List of columns.
        :rtype: list
        """
        data = data.split(sep)
        columns = []
        for col in data:
            if re.match(r"^\d+$", col):
                columns.append(int(col))
            elif re.match(r"^\d+\.\d+$", col):
                columns.append(float(col))
            else:
                columns.append(col)
        return columns

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
        while True:
            data = requests.get()
            data = data.split("\n")
            for line in data:
                colums = Reader.transform(line, sep)
                # fazer regex para verificar o formato dos dados
                buffer_output.put(colums)

    def read_threaded(self, requests: mp.Queue):
        """ Split the reading process into multiple threads.
        """
        for _ in range(self.n_threads):
            t = mp.Process(target=self.read, args=(self.buffer_output, requests))
            self.threads_list.append(t)
            t.start()
        for t in self.threads_list:
            t.join()


if __name__ == "__main__":
    reader = Reader(n_threads=4)
    manager = mp.Manager()
    buffer_output = manager.Queue()
    reader.read_threaded(buffer_output)