from concurrent import futures
import grpc
import review_pb2
import review_pb2_grpc
import uuid

reviews = {}

class ReviewService(review_pb2_grpc.ReviewServiceServicer):
    def AddReview(self, request, context):
        review_id = str(uuid.uuid4())
        review = {
            "user_id": request.user_id,
            "product_id": request.product_id,
            "review_text": request.review_text,
            "rating": request.rating,
        }
        reviews.setdefault(request.product_id, []).append(review)
        return review_pb2.ReviewResponse(review_id=review_id, message="Review added successfully")

    def GetReviews(self, request, context):
        product_reviews = reviews.get(request.product_id, [])
        return review_pb2.ReviewsResponse(reviews=[
            review_pb2.Review(
                review_id=str(uuid.uuid4()),
                user_id=review["user_id"],
                review_text=review["review_text"],
                rating=review["rating"]
            ) for review in product_reviews
        ])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    review_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewService(), server)
    server.add_insecure_port("[::]:5005")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
