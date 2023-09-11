import json
import jsonpatch
from aiohttp import web, ClientSession, TCPConnector
import datetime
import request_utility
import token_cache


def get_rar_object(token):
    cached_rar = token_cache.get_cached_rar_object(token)#check the cache

    if cached_rar is not None:
         return cached_rar
    
    introspection_response = request_utility.standard_introspection_request(token) #introspect the token with AS
    
    if introspection_response is None:
        return web.json_response(data="Internal server error", status=500)


    if 'authorization_details' not in introspection_response: #check if there is a rar object associated with this token
         return None

    token_cache.cache_token(token, str(introspection_response['authorization_details'][0]))
    return introspection_response['authorization_details'][0]


async def api_proxy_middleware(app, handler):
    async def middleware(request):
        token = request_utility.get_bearer_token(request)

        if token is None:
            return await call_the_api(request, None)
        # introspection_response = request_utility.standard_introspection_request(token)
        
        # rar_object = None if 'authorization_details' not in introspection_response else introspection_response['authorization_details'][0]
        rar_object = get_rar_object(token)
        return await call_the_api(request, rar_object)

    return middleware

async def call_the_api(request, rar_object):
    async with ClientSession(connector=TCPConnector()) as session:
        backend_url = 'http://localhost:8080' 
        async with session.request(
            method=request.method,
            url=backend_url + request.path_qs,
            headers=request.headers,
            data=await request.read(),
            allow_redirects=False,
        ) as resp:
            response_json = await resp.text()
            headers = resp.headers.copy()
            del headers['Content-Type']
            if rar_object is None:
                return web.json_response(data=json.loads(response_json), status=resp.status)
            if request.path_qs != rar_object['path']:
                return web.json_response(data=json.loads(response_json), status=resp.status)
            if int(rar_object['access_timeout']) < datetime.datetime.timestamp(datetime.datetime.now()): 
                return web.json_response(data="403: Forbidden. Access timeout reached", status=403)
            
            response_json = response_json if 'patch' not in rar_object else jsonpatch.JsonPatch(rar_object['patch']).apply(json.loads(response_json))
            return web.json_response(data=response_json, status=resp.status)


app = web.Application(middlewares=[api_proxy_middleware])
web.run_app(app, port=8000)
