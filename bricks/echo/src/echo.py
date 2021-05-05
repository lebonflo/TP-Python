
from aiohttp import  web

async def _echo_(request):
    try:
        # 0 : extract payload dict
        json = await request.json()

        #
        return web.json_response(dict(json=json))

    # $>
    except Exception as exp:
    # <!
        # !0 return what's wrong in string and the type of the exception should be enough to understand where you're wrong noobs
        return web.json_response({'err':{'str':str(exp),'typ':str(type(exp))}}, status=500)
#`< - - - - - - - - - - - -
