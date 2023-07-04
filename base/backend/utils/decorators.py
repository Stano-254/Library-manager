import json
from functools import WRAPPER_ASSIGNMENTS

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from six import wraps

from base.backend.service import UserIdentityService
from base.backend.utils.utilities import get_request_data


def user_login_required(view_func):
    """
    Checks if the request is from a valid user and the provided token is valid.
    """

    def wrapped_view(*args, **kwargs):
        """This method wraps the decorated method."""
        is_checked = False
        print(kwargs)
        for k in args:
            if isinstance(k, WSGIRequest):
                request_data = get_request_data(k)
                token = request_data.get("token", False)
                if token is False:
                    token = str(k.headers.get('Authorization', ""))
                    token = token[len("Bearer "):] if token.startswith("Bearer ") else token

                if token not in ["", False]:
                    is_checked = True
                    print("token",token)
                    user_auth = UserIdentityService().filter(
                        ~Q(user=None), token=token, expires_at__gt=timezone.now()).order_by('-date_created').first()
                    if not user_auth:
                        response = HttpResponse(
                            json.dumps({
                                'status': 'failed', 'message': 'Unauthorized. Invalid credentials.', 'code': '401'
                            }),
                            content_type='application/json', status=401)
                        response['WWW-Authenticate'] = 'Bearer realm=api'
                        return response
                    setattr(k, 'user', user_auth.user)
                    setattr(k, 'token', token)
                    user_auth.extend()
                else:
                    return JsonResponse({
                        'status': 'failed', 'message': 'Unauthorized. Authorization parameters not Found!',
                        'code': '401'
                    }, status=401)
        if not is_checked:
            response = HttpResponse(
                json.dumps({'status': 'failed', 'message': 'Unauthorized. Credentials not Provided.', 'code': '401'}),
                content_type='application/json', status=401)
            response['WWW-Authenticate'] = 'Bearer realm=api'
            return response
        return view_func(*args, **kwargs)

    # return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return wraps(view_func, assigned=WRAPPER_ASSIGNMENTS)(wrapped_view)
