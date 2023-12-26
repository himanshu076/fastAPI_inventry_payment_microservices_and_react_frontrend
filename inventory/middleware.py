from main import app
from fastapi.middleware.cors import CORSMiddleware


# Adding middleware.
app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)