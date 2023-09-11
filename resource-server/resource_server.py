import asyncio
from datetime import datetime
from aiohttp import web
import request_utility



async def user_info(request):
    if request_utility.authorization_check(request) is False:
        return  web.Response(body='{"401":"Unauthorized"}',status=401)

    example_user = [
        '{',
        '  "given_name":   "John",',
        '  "family_name":  "Doe",',
        '  "email":    "john.doe@example.com",',
        '  "dob":   "2001-10-02",',
        '  "gender": "M",',
        '  "occupations": "CEO at Awesome Org"',
        '}'
    ]

    content = '\n'.join(example_user)
    headers = {"Content-Type": "application/json"}
    response = web.Response(body=content, headers=headers)
    return response

async def docs(request):
    headers = {"Content-Type": "application/json"}
    with open("API-response-swagger.json",'r') as fp:
        content = fp.read()
        response = web.Response(body=content, headers=headers)
        return response

app = web.Application()
app.router.add_route("GET", "/userinfo", user_info)
app.router.add_route("GET", "/docs", docs)
web.run_app(app)
