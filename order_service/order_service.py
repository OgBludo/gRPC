from concurrent import futures
import grpc
import order_pb2
import order_pb2_grpc
import uuid

orders = {}

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        order_id = str(uuid.uuid4())
        orders[order_id] = {
            "user_id": request.user_id,
            "product_ids": request.product_ids,
            "total_price": request.total_price,
            "status": "Created"
        }
        return order_pb2.OrderResponse(
            order_id=order_id, user_id=request.user_id,
            product_ids=request.product_ids, total_price=request.total_price,
            status="Created"
        )

    def GetOrder(self, request, context):
        order = orders.get(request.order_id)
        if not order:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return order_pb2.OrderResponse()
        return order_pb2.OrderResponse(
            order_id=request.order_id, user_id=order["user_id"],
            product_ids=order["product_ids"], total_price=order["total_price"],
            status=order["status"]
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port("[::]:5002")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
