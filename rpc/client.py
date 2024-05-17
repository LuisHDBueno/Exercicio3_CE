import grpc
import calculator_pb2
import calculator_pb2_grpc

def get_string():
    strs = ["Arroz", "Barco", "Curva", "Dado", "Elefante"]
    return strs

def run(num):
    for i in range(num):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            palavra = ["Arroz", "Barco", "Curva", "Dado", "Elefante"]
            try:
                response = stub.Add(calculator_pb2.AddRequest(palavra=palavra[i]))
            except grpc.RpcError as e:
                print(e.details())
                raise e
        print(f"Result: {response.result}")

if __name__ == '__main__':
    num = int(input("Enter the number of times to run the client: "))
    run(num)