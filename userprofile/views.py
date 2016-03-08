from django.shortcuts import render, render_to_response
from django.template import RequestContext
import urllib2
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from userprofile.forms import NewUserForm
from userprofile.models import UserProfile
from steamauth import RedirectToSteamSignIn, GetSteamID64
from steamapi.settings import SOCIAL_AUTH_STEAM_API_KEY
"""
This function uses Steam's API to get Counter Strike Global Offensive inventory from steamID
sent to the function. steamID is a get param on the url.
"""
# @login_required
# def showOwnCSGOInventory(request):

#     steamID = request.user.userprofile.steamURL
#     #Prepare api request
#     apiRequest = urllib2.Request("http://steamcommunity.com/profiles/" + steamID + "/inventory/json/730/2", headers={"Accept-language" : "es"})
#     #Executing api request and saving it as String (JSON format comes)
#     jsondata = urllib2.urlopen(apiRequest).read()
#     #Parsing json to Python Dict
#     jsonDecoded = json.loads(jsondata)

#     is_inventory_visible = jsonDecoded.has_key("rgDescriptions")
#     #Get and appends actions list and background color to each item
#     # DEV options = list()
#     if is_inventory_visible:
#         for k, v in jsonDecoded["rgDescriptions"].iteritems():
#             for k1 in v["tags"]:
#                 if k1.has_key("color"):
#                     v["background"] = k1["color"]
#             if(v.has_key("market_actions")):
#                 v["actions"] = v.get("market_actions")[0]
#             else:
#                 v["actions"] = False
#         items = jsonDecoded["rgDescriptions"]
#     else:
#         items = False
 
#     # DEV RETURN
#     return JsonResponse(items, safe=False)


#     # Returns items description to render engine
#     return render_to_response("inventory.html", {"items": items}, context_instance=RequestContext(request))

@login_required
def showOwnCSGOInventory(request):

    steamID = request.user.userprofile.steamURL
    #Prepare api request
    apiRequest = urllib2.Request("https://api.steampowered.com/IEconItems_730/GetPlayerItems/v1/?format=json&key=" + SOCIAL_AUTH_STEAM_API_KEY +"&steamid=" + steamID)
    #Executing api request and saving it as String (JSON format comes)

    try:
        jsondata = urllib2.urlopen(apiRequest).read()
    except urllib2.HTTPError, e:
        return HttpResponse(e.code)
    except urllib2.URLError, e:
        return HttpResponse(e.args)
    

    #Parsing json to Python Dict
    jsonDecoded = json.loads(jsondata)

    
 
    # DEV RETURN
    return JsonResponse(jsonDecoded, safe=False)


    # Returns items description to render engine
    return render_to_response("inventory.html", {"items": items}, context_instance=RequestContext(request))

"""
This function provides registration feature to the platform.
"""
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            userprofile = UserProfile(user=new_user, steamURL=form.cleaned_data["steamURL"])
            userprofile.save()
            return HttpResponseRedirect("/inventory")
    else:
        form = NewUserForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def login(request):
    return RedirectToSteamSignIn('/process')

def LoginProcess(request):
    steamid = GetSteamID64(request.GET)
    if steamid == False:
        # login failed
        return redirect('/login_failed')
    else:
        # login success
        # do something with variable `steamid`
        return HttpResponse(steamid)