"""
Middle ware for authorization for users before they access specific resources
"""
from _main_.utils.massenergize_errors import NotAuthorizedError, CustomMassenergizeError, MassEnergizeAPIError
from _main_.utils.context import Context
from _main_.settings import SECRET_KEY
from firebase_admin import auth
import json, jwt
from sentry_sdk import capture_message


class MassenergizeJWTAuthMiddleware:

  # List of routes that do not require sign-in
  WHITLISTED_ROUTES = set([

  ])

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.

    response = self.get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response
  

  def _get_decoded_token(self, request) -> (dict, MassEnergizeAPIError):
    try:
      payload = jwt.decode(id_token, SECRET_KEY, algorithm='HS256')
      return payload, None
    except jwt.ExpiredSignatureError:
      msg = 'session_expired'
      return None, CustomMassenergizeError(msg)
    except jwt.DecodeError:
      msg = 'token_decode_error'
      return None, CustomMassenergizeError(msg)
    except jwt.InvalidTokenError:
      return None, CustomMassenergizeError('invalid_auth')


  def _get_clean_path(self, request):
    try:
      return request.path.split('/')[-1]
    except Exception:
      return request.path

  def process_view(self, request, view_func, *view_args, **view_kwargs):

    try:
      # add a context: (this will contain all info about 
      # the request body, this user's session info, etc)
      ctx = Context()

      #set request body
      ctx.set_request_body(request)

      path = self._get_clean_path(request)

      if path not in self.WHITLISTED_ROUTES:

        #extract JWT auth token
        token = request.COOKIES.get('token', None) 

        if token:
          decoded_token, err = self._get_decoded_token(token)
          if err:
            return err

          # at this point the user has an active session
          ctx.set_user_credentials(decoded_token)

        else:
          return CustomMassenergizeError("login_required")
        
      request.context = ctx

    except Exception as e:
      capture_message(str(e), level="error")
      return CustomMassenergizeError(e)


class RemoveHeaders:

  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    response['Server'] = ''
    return response

