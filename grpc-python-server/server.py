import sys
sys.path.insert(1, './generated/')
import logging
import grpc
import conn_pb2
import conn_pb2_grpc
from concurrent import futures
from google.protobuf.json_format import MessageToJson
import requests
from request_header_validator_interceptor import RequestHeaderValidatorInterceptor


class Deploy(conn_pb2_grpc.ClientCallServiceServicer):
    def RunDeploy(self, request, context):
        print("Running command: ", request.callInterface.command)
        if request.callInterface.command == "deploy-contract":
            resp = conn_pb2.ClientCallResponse(result="success")
            yield resp
        else:
            return
    
def serve():
    header_validator = RequestHeaderValidatorInterceptor(grpc.StatusCode.UNAUTHENTICATED, 'Access denied!')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(header_validator,))
    conn_pb2_grpc.add_ClientCallServiceServicer_to_server(Deploy(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("gRPC server listening on port 50053")
    server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig()
    serve()