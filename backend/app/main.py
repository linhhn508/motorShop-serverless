from a2wsgi import WSGIMiddleware
from mangum import Mangum

from app import create_app

app = create_app()
handler = Mangum(WSGIMiddleware(app), lifespan="off")
