import requests, time
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import HashModel, get_redis_connection
from starlette.requests import Request

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

# This should be different database but using same because of paid version.
redis = get_redis_connection(
  host='host',
  port='14262',
  password='pwd',
  decode_responses=True
)

class Order(BaseModel):
  product_id: str
  price: float
  fee: float
  total: float
  quantity: int
  status: str # pending, completed, refunded

class OrderRedis(HashModel):
  product_id: str
  price: float
  fee: float
  total: float
  quantity: int
  status: str # pending, completed, refunded

  class Meta:
    database: redis

@app.get('/orders/{pk}')
def get(pk: str):
  order = OrderRedis.get(pk)
  redis.xadd('refund_order', order, '*')
  return order


@app.post('/orders')
async def create(request: Request, background_task: BackgroundTasks):
  body = await request.json()
  req = requests.get('http://127.0.0.1:8000/products/%s' % body['id'])
  product = req.json()
  order = OrderRedis(
    product_id = body['id'],
    price = product['price'],
    fee = 0.2 * product['price'],
    total = 1.2 * product['price'],
    quantity = body['quantity'],
    status = 'pending',
  )
  order.save()
  background_task.add_task(order_completed, order)
  return order

def order_completed(order: OrderRedis):
  time.sleep(5)
  order.status = 'completed'
  order.save()
  redis.xadd('order_completed', order.dict(), '*')