from redis_om import get_redis_connection


redis = get_redis_connection(
  host='redis-14262.c301.ap-south-1-1.ec2.cloud.redislabs.com',
  port='14262',
  password='P408hgpvtwKv0CAcBEhoZCxRf1mbpY8X',
  decode_responses=True
)