# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def root_route_handler(request):
    return web.Response(
        text="✅ MohammedDev-yt - Links Share Bot is Running!",
        content_type="text/plain"
    )

@routes.get("/health")
async def health(request):
    return web.json_response({
        "status": "ok",
        "service": "MD Links Share Bot"
    })

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #