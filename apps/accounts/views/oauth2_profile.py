import waffle

import apps.logging.request_logger as logging

from collections import OrderedDict
from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.decorators import protected_resource
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from apps.capabilities.permissions import TokenHasProtectedCapability
from apps.fhir.bluebutton.models import Crosswalk
from apps.fhir.bluebutton.permissions import ApplicationActivePermission


def get_userinfo(user):
    """
    OIDC-style userinfo
    """
    data = OrderedDict()
    data['sub'] = user.username
    data['name'] = "%s %s" % (user.first_name, user.last_name)
    data['given_name'] = user.first_name
    data['family_name'] = user.last_name
    data['email'] = user.email
    data['iat'] = user.date_joined

    # Get the FHIR ID if its there
    fhir_id = get_fhir_id(user)
    if fhir_id:
        data['patient'] = fhir_id
        data['sub'] = fhir_id
    return data


@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
@permission_classes([ApplicationActivePermission, TokenHasProtectedCapability])
@protected_resource()
def openidconnect_userinfo(request, **kwargs):
    if request.path.startswith('/v2') and (not waffle.flag_is_active(request, 'bfd_v2_flag')):
        # TODO: waffle flag enforced, to be removed after v2 GA
        err = exceptions.NotFound("bfd_v2_flag not active.")
        waffle_event_logger = logging.getLogger(logging.AUDIT_WAFFLE_EVENT_LOGGER, request)
        log_dict = {"type": "v2_blocked",
                    "user": str(request.user) if request.user else None,
                    "path": request.path if request.path else None,
                    "app_id": request.auth.application.id if request.auth.application else None,
                    "app_name": str(request.auth.application.name) if request.auth.application else None,
                    "dev_id": str(request.auth.application.user.id) if request.auth.application else None,
                    "dev_name": str(request.auth.application.user.username) if request.auth.application else None,
                    "response_code": err.status_code,
                    "message": str(err)}
        log_dict.update(kwargs)
        waffle_event_logger.info(log_dict)

        raise err
    user = request.resource_owner
    data = get_userinfo(user)
    return JsonResponse(data)


def get_fhir_id(user):

    r = None
    if Crosswalk.objects.filter(user=user).exists():
        c = Crosswalk.objects.get(user=user)
        r = c.fhir_id
    return r
