from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc
import uuid

users = {}

class UserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        user_id = str(uuid.uuid4())
        users[user_id] = {"name": request.name, "email": request.email}
        return user_pb2.UserResponse(user_id=user_id, name=request.name, email=request.email)

    def GetUser(self, request, context):
        user = users.get(request.user_id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UserResponse()
        return user_pb2.UserResponse(user_id=request.user_id, name=user["name"], email=user["email"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:5001")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
