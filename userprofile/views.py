from django.shortcuts import render, render_to_response
from django.template import RequestContext
import urllib2
from django.http import HttpResponse
import json

"""
This function uses Steam's API to get Counter Strike Global Offensive inventory of steamID
sent to the function. steamID is a get param on the url.
"""
def showCSGOInventory(request, steamID):
    #Prepare api request
    apiRequest = urllib2.Request("http://steamcommunity.com/id/" + steamID + "/inventory/json/730/2/es", headers={"Accept-language" : "es"})
    #Executing api request and saving it as String (JSON format comes)
    jsondata = urllib2.urlopen(apiRequest).read()
    #Parsing json to Python Dict
    jsonDecoded = json.loads(jsondata)
    #Returns items description to render engine
    return render_to_response("inventory.html", {"items": jsonDecoded["rgDescriptions"]}, context_instance=RequestContext(request))

