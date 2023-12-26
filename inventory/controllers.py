from fastapi import HTTPException

from main import app
from models import ProductModel, ProductRedis


# @app.get("/")
# async def root():
#   return {"message": "Hello World"}

@app.get('/products')
def all():
  return ProductModel.all_pks()

# @app.get('/products/{product_id}', response_model=ProductModel)
# def get_product(product_id: str):
#   product_redis = ProductRedis.get(product_id)
#   if product_redis is None:
#       raise HTTPException(status_code=404, detail="Product not found")
#   return ProductModel(**product_redis.model_dump())

# @app.post('/products')
# def create(product: ProductRedis):
#   breakpoint()
#   # product_redis = ProductRedis(**product.model_dump())
#   product.save()
#   return ProductModel(**product.model_dump())
