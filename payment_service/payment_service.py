from concurrent import futures
import grpc
import payment_pb2
import payment_pb2_grpc
import uuid

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    def ProcessPayment(self, request, context):
        transaction_id = str(uuid.uuid4())
        success = request.amount > 0  # Simple validation
        return payment_pb2.PaymentResponse(
            success=success,
            transaction_id=transaction_id if success else ""
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    server.add_insecure_port("[::]:5003")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
