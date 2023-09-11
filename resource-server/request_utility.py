import config
from authlete.dto.standard_introspection_request  import StandardIntrospectionRequest
from authlete.api.authlete_api_impl  import AuthleteApiImpl
from authlete.conf.authlete_configuration import AuthleteConfiguration
from authlete.dto.introspection_request  import IntrospectionRequest
from authlete.dto.introspection_action    import IntrospectionAction
import json

cnf = AuthleteConfiguration()
cnf.baseUrl = config.baseUrl
cnf.serviceApiKey         = config.serviceApiKey
cnf.serviceApiSecret      =  config.serviceApiSecret
authorization_server = AuthleteApiImpl(cnf)


def get_bearer_token(request):
    authorization_header = request.headers.get('Authorization')
    return None if authorization_header is None else authorization_header.strip("Bearer ")


def standard_introspection_request(token):
    introspection_req = StandardIntrospectionRequest()
    introspection_req.parameters = "token="+token

    #TODO check for netwrok failure, now assuming introspection_response.action == StandardIntrospectionAction.OK
    return json.loads(authorization_server.standardIntrospection(introspection_req).responseContent)


def is_valid(token):
    introspection_req = IntrospectionRequest()
    introspection_req.token = token
    try:
        introspection_response = authorization_server.introspection(introspection_req)
    except Exception:
        return False #TODO Check if the request has failed (at network level)

    return True if introspection_response.action == IntrospectionAction.OK else False

def authorization_check(request):
    token = get_bearer_token(request)
    return is_valid(token)
