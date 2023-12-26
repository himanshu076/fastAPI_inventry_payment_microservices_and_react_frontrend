from main import redis, OrderRedis, HashModel
import time

key = 'refund_order'
group = 'payment-group'

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
        order = OrderRedis.get(obj['pk'])
        if order:
          order.status = 'refunded'
          order.save()

  except Exception as e:
    print(str(e))
  time.sleep(1)