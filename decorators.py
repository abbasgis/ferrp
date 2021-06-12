import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
# from django.shortcuts import redirect
# from django.urls import reverse
from django.views.defaults import bad_request

from ferrp.layers.models import Info
from ferrp.models import Items_Permission
from ferrp.utils import Common_Utils


def permission_required(permission_type, item_name_var, item_type):
    def real_decorator(function):
        def wrapper(request, *args, **kw):
            # if(len(args)>0):
            #     permission_type = str(args[0]).upper();
            # else:
            #     permission_type ='V'
            item_name = request.GET.get(item_name_var)

            result = False
            if request.user.is_authenticated() and request.user.is_superuser:
                result = True
            elif item_name == '' or item_name is None:
                result = False
            # if is_owner(request.user.username,item_name):
            #     result = True
            else:
                group_list = list(request.user.groups.values_list('name', flat=True))
                user_name = request.user.username
                if user_name == '': user_name = "Public"
                result = is_permission_available(user_name, group_list, [permission_type, 'O'], item_name, item_type)
            if result is False:
                msg = "403 Forbidden.You are not allowed to perform this action...",
                try:
                    url = request.META['HTTP_REFERER']
                except:
                    url = "/"  # None

                if url is not None:
                    if request.is_ajax():
                        # res = {"is_redirect": True, "url": url, "is_permission_denied":True,  msg: msg}
                        # response =  HttpResponse(json.dumps(res),content_type="application/json")
                        # response.status_code = 400
                        # return response
                        return bad_request(message=msg)
                    else:
                        messages.add_message(request, messages.ERROR, msg)
                        return HttpResponseRedirect(url)
                else:
                    raise PermissionDenied
            else:
                return function(request, *args, **kw)

        return wrapper

    return real_decorator


def is_permission_available(user_name, group_list, request_type_list, item_name, item_type):
    # user = request.user
    # group_list = list(request.user.groups.values_list('name', flat=True))
    # user_name = request.user.username
    entity_list = group_list
    entity_list.append(user_name)
    entity_list.append("Public")

    have_permission = len(list(Items_Permission.objects.filter(item_type=item_type, item_name=item_name,
                                                               entity_name__in=entity_list,
                                                               permission_type__in=request_type_list))) > 0
    return have_permission


def is_owner(user_name, item_name, item_type=Common_Utils.get_info_item_content_type('layers', 'info')):
    is_owner = len(list(Items_Permission.objects.filter(item_type=item_type, item_name=item_name,
                                                        entity_name=user_name, entity_type='U',
                                                        permission_type='O'))) > 0
    return is_owner


def can_download(user_name, item_name):
    if user_name == '': user_name = "Public"
    can_download = len(
        list(Items_Permission.objects.filter(item_name=item_name, entity_name=user_name, permission_type='D'))) > 0
    return can_download
