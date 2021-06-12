from django.contrib import messages
# from linkedin import linkedin
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader

from ferrp.indus_basin.models import Social_User_Profile
from ferrp.maps.models import Map_Info


def account_profile(request):
    redirect_path = '/maps/create_map/'  # request.GET.get("next")
    map_obj = Map_Info.objects.filter(created_by=request.user)
    if map_obj.count() > 0:
        map_list = list(map_obj.values().order_by('-created_at'))
        map_name = map_list[0]['name']
        redirect_path = '/maps/view_map/?item_name=' + map_name
    messages.add_message(request, messages.SUCCESS, 'Login Successfully')
    return redirect(redirect_path)


def social_user_profile(request, template=loader.get_template('social_user_profile.html')):
    code = request.GET.get('code')
    # credentials = service_account.Credentials.from_service_account_file(
    #     'D://dchServerProj//ferrp//creadentials.json')
    state = request.GET.get('state')
    redirect_uri = 'http://pnddch.info/indus_basin/social_user_profile/'
    redirect_uri = 'http://localhost:52/indus_basin/social_user_profile/'
    client_id = '8151q7s39d7an5'
    client_secret = 'UTNsLBQRqSe7XcQH'
    grant_type = 'authorization_code'
    permission = (['r_basicprofile', 'r_emailaddress'])
    context = {'code': code, 'state': state, 'redirect_uri': redirect_uri, 'client_id': client_id,
               'client_secret': client_secret, 'grant_type': grant_type}
    authentication = linkedin.LinkedInAuthentication(
        client_id,
        client_secret,
        redirect_uri,
        linkedin.PERMISSIONS.enums.values()
    )
    authentication.authorization_code = code
    try:
        result = authentication.get_access_token()
        application = linkedin.LinkedInApplication(token=result.access_token)
        profile = application.get_profile()
        data = {'first_name': profile['firstName'], 'last_name': profile['lastName'],
                'account_heading': profile['headline'],
                'id_from_account': profile['id']}
        insert_profile_in_db(data, 'linkedin')
        if profile:
            url = 'http://pnddch.info/maps/view_map/?item_name=Indus%20Basin_20180916184941754244'
            url = 'http://localhost:52/maps/view_map/?item_name=Indus%20Basin_20180910180856806901'
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponseRedirect('/login/')


def insert_profile_in_db(profile, account_type):
    user = Social_User_Profile.objects.filter(id_from_account='', account_type=account_type)
    if user.count() == 0:
        sup = Social_User_Profile(first_name=profile['first_name'], last_name=profile['last_name'],
                                  account_heading=profile['account_heading'], account_type=account_type,
                                  id_from_account=profile['id_from_account'])
        sup.save(force_insert=True)
