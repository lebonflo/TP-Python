
# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------

from rich.traceback import install
install()



import aiohttp
import aiohttp_cors



from aiohttp import web



# Create Application with Middlewares
app = web.Application(
  middlewares=[
    # authMiddleware #authentification
  ],
  client_max_size=1024**3
)

from echo import app_echo
from tick import app_tick

app.add_subapp('/echo', app_echo)
app.add_subapp('/tick', app_tick)

# Configure CORS on all routes.
cors = aiohttp_cors.setup(app, defaults={
  "*": aiohttp_cors.ResourceOptions(
    # allow_credentials=True,
    expose_headers="*",
    allow_headers="*",
  )
})


for route in list(app.router.routes()):
  print(route)
  cors.add(route)



if __name__ == '__main__':
  web.run_app(app, port=8000)

