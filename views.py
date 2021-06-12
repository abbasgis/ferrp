import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from ferrp.layers.gis_migration import get_table_schema
from ferrp.layers.models import Info
from ferrp.utils import DB_Query, Common_Utils, Model_Utils


class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()


def user_department_list(request):
    udlist = {}
    udlist['users'] = list(User.objects.all().values_list('id', 'username'))
    udlist['depts'] = list(Group.objects.all().values_list('id', 'name'))  # .values_list('id', flat=True) )
    res = json.dumps(udlist)
    return HttpResponse(res, content_type="application/json")


# def attribute_list(request):
#     table_name = request.GET.get("layername")
#     table_schema = get_table_schema(table_name)
#     return HttpResponse(json.dumps(table_schema),content_type="application/json")

def login_linkedin(request):
    redirect_uri = 'http://pnddch.info/indus_basin/social_user_profile/'
    # redirect_uri = 'http://localhost:52/indus_basin/social_user_profile/'
    client_id = '8151q7s39d7an5'
    client_secret = 'UTNsLBQRqSe7XcQH'
    url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&state=' + client_secret + '&scope=r_basicprofile'
    # url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=8151q7s39d7an5&redirect_uri=http://localhost:52/indus_basin/social_user_profile/&state=UTNsLBQRqSe7XcQH&scope=r_basicprofile'
    return HttpResponseRedirect(url)


def account_profile(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    if user and not user.has_usable_password():
        return redirect(reverse(set_new_password))
    messages.add_message(request, messages.SUCCESS, 'Login successful')
    # return render(request, "index.html", context={})
    return redirect(reverse('home_dch'))

# @receiver(user_logged_in)
# def user_signed_up_(request, user, sociallogin=None, **kwargs):
#     if sociallogin:
#         from allauth.account.models import EmailAddress
#         emails = EmailAddress.objects.filter(user=user, verified=False)
#         for email in emails:
#             email.verified=True
#             email.save()

def set_new_password(request):
    try:
        user = request.user
        if request.method == 'POST':
            form = SetPasswordForm(user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'User created succesfully')
                return redirect(reverse('home_dch'))
        else:
            form = SetPasswordForm(user)
            messages.add_message(request, messages.INFO, 'Please set your password for this P&DD DCH')
    except Exception as e:
        messages.add_message(render, messages.ERROR, 'Password cannot be set due to ' + str(e))
    return render(request, "login/set_password.html", context={"form": form})


def account_logout(request):
    redirect_path = '/'  # request.GET.get("next")
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout Successfully')
    return redirect(redirect_path)


def account_login(request):
    if request.method == 'POST':
        # return HttpResponse(
        #     content="ajax login requires HTTP POST",
        #     status=405,
        #     mimetype="text/plain"
        # )
        form = LoginForm(data=request.POST)
        redirect_path = request.GET.get("next")
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                msg = "bad credentials or disabled user",
                messages.add_message(request, messages.ERROR, msg)
                return redirect(redirect_path)
            else:
                login(request, user)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                messages.add_message(request, messages.SUCCESS, 'Login Successfully')
                return redirect(redirect_path)
        else:
            msg = "The form you submitted doesn't look like a username/password combo.",
            messages.add_message(request, messages.INFO, msg)
            return redirect(redirect_path)
    else:
        next = request.GET.get("next")
        if next is None: next = request.path
        return render(request, "login/login_page.html", {"next_page": next})


def user_department_list(request):
    udlist = {}
    udlist['users'] = list(User.objects.all().values_list('id', 'username'))
    udlist['depts'] = list(Group.objects.all().values_list('id', 'name'))  # .values_list('id', flat=True) )
    res = json.dumps(udlist)
    return HttpResponse(res, content_type="application/json")


def attribute_list(request):
    layer_name = request.GET.get("layername")
    layer_info = Info.objects.filter(layer_name=layer_name).first()
    if layer_info is not None:
        # table_schema = DB_Query.get_table_schema(layer_info.table_name,layer_info.app_label)

        table_schema = DB_Query.get_layer_table_description(layer_info, is_geom_included=False)
        # return HttpResponse(json.dumps(table_schema.cols), content_type="application/json")
        return JsonResponse(table_schema['cols'], safe=False)
    return HttpResponseBadRequest()


def attribute_distinct_value(request):
    layer_name = request.GET.get("layer_name")
    col_name = request.GET.get("column_name")
    layer_info = Info.objects.filter(layer_name=layer_name)[0]
    distinct_value = DB_Query.get_column_distinct_value(layer_info.table_name, col_name)
    # table_schema = get_table_schema(layer_info.table_name)
    return HttpResponse(json.dumps(distinct_value), content_type="application/json")


def raster_summary(request):
    layer_name = request.GET.get("layer_name")
    layer_info = Info.objects.filter(layer_name=layer_name)[0]
    # value_count = DB_Query.get_raster_valuecount(layer_info.table_name)
    stats = DB_Query.get_raster_summary("o_8_" + layer_info.table_name)
    return HttpResponse(json.dumps(stats), content_type="application/json")


def get_layer_info(request):
    layer_name = request.GET.get("layer_name")
    info = Info.objects.filter(layer_name=layer_name).get().__dict__
    layer_info = {'extent': info['extent'], 'title': info['name'], 'layerName': layer_name,
                  'layerType': info['layer_type'],
                  'geomType': info['geom_type']}
    # layerInfo['csrfToken'] = csrf_token
    # layerInfo['geomType'] = '{{ info.geom_type }}'
    # layerInfo.canDownload = '{{ can_download }}'
    # layerInfo.url = '{% url "wms_get_map" %}'
    # layerInfo.urlDownloadLayer = "{% url "
    # lyr_download
    # " %}";
    # layerInfo.urlDeleteLayer = "{% url "
    # lyr_delete
    # " %}";
    # layerInfo.urlSetLayerIcon = '{% url "set_layer_icon" %}';
    # layerInfo.urlLayerBrowser = '{% url "layer_browse" %}';
    # layerInfo.urlGetFeature = '{% url "get_feature" %}';


    return HttpResponse(json.dumps(layer_info), content_type="application/json")


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)


def model_fields_list(request):
    app_label = request.GET.get("appLabel")
    model_name = request.GET.get("modelName")
    field_list = Model_Utils.get_model_fields_list(app_label, model_name)
    return HttpResponse(json.dumps(field_list), content_type="application/json")
