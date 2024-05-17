import grpc
import calculator_pb2
import calculator_pb2_grpc

def get_string():
    strs = ["Arroz", "Barco", "Curva", "Dado", "Elefante"]
    return strs

def run(num):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        palavra = "aaaaA"
        num1=4
        num2=6
        try:
            response = stub.Add(calculator_pb2.AddRequest(num1=num1, num2=num2))
        except grpc.RpcError as e:
            print(e.details())
            raise e
    print(f"Result: {response.result}")

if __name__ == '__main__':
    num1 = input("Al: ")
    run(num1)