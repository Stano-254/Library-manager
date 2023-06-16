import json
import logging
import re
from uuid import UUID

from django.http import QueryDict

lgr = logging.getLogger(__name__)


def get_request_data(request):
    """
    Retrieve request data.
    @param request: The Django HttpRequest.
    @type request: WSGIRequest
    @return: The data from the request as a dict
    @rtype: QueryDict
    """
    try:
        data = None
        if request is not None:
            request_meta = getattr(request, 'META', {})
            request_method = getattr(request, 'method', None)
            if request_meta.get('CONTENT_TYPE', '') == 'application/json':
                data = json.loads(request.body)
            elif str(request_meta.get('CONTENT_TYPE', '')).startswith('multipart/form-data;'):
                # Form Data?
                data = request.POST.copy()
                data = data.dict()
            elif request_method == 'GET':
                data = request.GET.copy()
                data = data.dict()
            elif request_method == 'POST':
                data = request.POST.copy()
                data = data.dict()
            if not data:
                request_body = getattr(request, 'body', None)
                if request_body:
                    data = json.loads(request_body)
                else:
                    data = QueryDict()
            return data
    except Exception as e:
        lgr.exception(f"get_request_data Exception: {e}")
    return QueryDict()


def validate_uuid4(uuid_string):
    """
    Validate that a UUID string is in fact a valid uuid4.
    """
    # noinspection PyBroadException
    try:
        _ = UUID(uuid_string, version=4)
    except Exception:
        return False
    return True


def validate_name(name, min_length=2, max_length=50):
    """
    Checks if the provided name:
        - contains only alphabet characters
        - len(name) is within specified min_length and max_length
    :param name: name passed to be validated
    :type name: str
    :param min_length: minimum length of name
    :type min_length: int
    :param max_length: maximum length of name
    :type max_length: int
    :return: True if valid else False
    :rtype: bool
    """
    try:
        name = str(name).strip()
        if not re.match(r"(^[a-zA-Z\s]+$)", name):
            return False
        if min_length <= len(name) <= max_length:
            return True
    except Exception as e:
        lgr.error('validate_name: %s', e)
    return False
