from concurrent import futures
import grpc
import tracking_pb2
import tracking_pb2_grpc

order_statuses = {}

class TrackingService(tracking_pb2_grpc.TrackingServiceServicer):
    def UpdateOrderStatus(self, request, context):
        order_statuses[request.order_id] = request.status
        return tracking_pb2.StatusResponse(order_id=request.order_id, status=request.status)

    def GetOrderStatus(self, request, context):
        status = order_statuses.get(request.order_id, "Unknown")
        return tracking_pb2.StatusResponse(order_id=request.order_id, status=status)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tracking_pb2_grpc.add_TrackingServiceServicer_to_server(TrackingService(), server)
    server.add_insecure_port("[::]:5004")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
