from main import redis, ProductRedis, HashModel
import time

key = 'order_completed'
group = 'inventory-group'

class ProductRedis(HashModel):
  name: str
  price: float
  quantity: int

  class Meta:
    database = redis

try:
  redis.xgroup_create(key, group)
except:
  print('Group already exists!')

while True:
  try:
    results = redis.xreadgroup(group, key, {key: '>'}, None)

    if results != []:
      for result in results:
        obj = result[1][0][1]
        print('obj', obj)
        try:
          product = ProductRedis.get(obj['product_id'])
          print(product)
          product.quantity -= int(obj['quantity'])
          product.save()
        except:
          redis.xadd('refund_order', obj, '*')

  except Exception as e:
    print(str(e))
  time.sleep(1)