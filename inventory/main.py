from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

redis = get_redis_connection(
  host='redis-14262.c301.ap-south-1-1.ec2.cloud.redislabs.com',
  port='14262',
  password='P408hgpvtwKv0CAcBEhoZCxRf1mbpY8X',
  decode_responses=True
)

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


# @app.get("/")
# async def root():
#   return {"message": "Hello World"}

@app.get('/products')
def all():
  # return ProductRedis.all_pks()
  return [format(pk) for pk in ProductRedis.all_pks()]

def format(pk: str):
  product = ProductRedis.get(pk)
  product_details = {
    'id': product.pk,
    'name': product.name,
    'price': product.price,
    'quantity': product.quantity
  }
  return product_details

@app.post('/products')
def create(product: ProductModel):
  product_redis = ProductRedis(**product.model_dump())
  # product_redis.save()
  # return ProductModel(**product_redis.dict())
  return product_redis.save()

@app.get('/products/{pk}')
def get_product(pk: str):
  product_redis = ProductRedis.get(pk)
  if product_redis is None:
      raise HTTPException(status_code=404, detail="Product not found")
  return product_redis

@app.delete('/products/{pk}')
def delete(pk: str):
  return ProductRedis.delete(pk)