import grpc
from concurrent import futures
import datasender_pb2
import datasender_pb2_grpc

class CadeAnalyticsServer(datasender_pb2_grpc.DataSenderServicer):
    def Sender(self, request, context):
        result = request.data.upper()
        print(f"Received: {result}")
        #result = request.num1 + request.num2
        if result == "AAAAA":
            return datasender_pb2.ConfirmData(check=1)
        return datasender_pb2.ConfirmData(check=0)
        #return calculator_pb2.AddResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datasender_pb2_grpc.add_DataSenderServicer_to_server(CadeAnalyticsServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()