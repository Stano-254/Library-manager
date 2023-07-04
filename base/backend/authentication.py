import calendar
import logging
import token

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import re_path
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from base.backend.service import UserIdentityService, StateService
from base.backend.utils.utilities import get_request_data

lgr = logging.getLogger(__name__)


class Authentication(object):
    """ handles authentication for the application """

    @staticmethod
    @csrf_exempt
    def login(request):
        """
        handles login logic
        :param request:
        :return:
        """
        try:
            request_data = get_request_data(request)
            username = f"{request_data.get('username').strip()}"
            password = f"{request_data.get('password').strip()}"

            user = authenticate(username=username, password=password)
            if not user:
                return JsonResponse({'code': "500.000.301", "message": "user login failed"})
            # check token
            login(request, user)
            user_auth = UserIdentityService().filter(
                user=user, expires_at__gt=timezone.now(), state__name="Active").order_by('-date_created').first()
            if not user_auth:
                state_activation_pending = StateService().get(name="Activation Pending")
                user_auth = UserIdentityService().create(
                    user=user, source_ip=request_data.get('source_ip', None),
                    state=state_activation_pending)
            if user_auth:
                user_auth.extend()
                setattr(request, 'user', user)
                return JsonResponse({
                    "code": "100.000.000", 'data': {
                        'token': str(user_auth.token),
                        'expires_at': calendar.timegm(user_auth.expires_at.timetuple())
                    }
                })
            return JsonResponse({"code": "100.000.002"})
        except Exception as e:
            lgr.exception('token Exception: %s' % e)
            return JsonResponse({"code": "700.006.003"})
    @csrf_exempt
    def refresh_token(self, request):
        request_data = get_request_data(request)
        expired_token = request_data.get('expired_token')
        if not expired_token:
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            _, expired_token = authorization_header.split(' ')
        user_auth = UserIdentityService().filter(token=expired_token).first()
        user_auth.extend()
        user_auth.refresh_from_db()
        return JsonResponse({
            "code": "100.000.000", 'data': {
                'token': str(user_auth.token),
                'expires_at': calendar.timegm(user_auth.expires_at.timetuple())
            }
        })


urlpatterns = [
    re_path(r'login/', Authentication().login),
    re_path(r'refresh-token/', Authentication().refresh_token),
]
