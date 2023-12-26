from redis_database import redis
from pydantic import BaseModel
from redis_om import HashModel


# Pydantic model for FastAPI
class ProductModel(BaseModel):
    name: str
    price: float
    quantity: int

# Redis model for database operations
class ProductRedis(HashModel):
  name: str
  price: float
  quantity: int

  class Meta:
    database = redis