from django.shortcuts import render, render_to_response
from django.template import RequestContext
import urllib2
from django.http import HttpResponse, JsonResponse
import json

"""
This function uses Steam's API to get Counter Strike Global Offensive inventory of steamID
sent to the function. steamID is a get param on the url.
"""
def showCSGOInventory(request, steamID):
    #Prepare api request
    apiRequest = urllib2.Request("http://steamcommunity.com/id/" + steamID + "/inventory/json/730/2", headers={"Accept-language" : "es"})
    #Executing api request and saving it as String (JSON format comes)
    jsondata = urllib2.urlopen(apiRequest).read()
    #Parsing json to Python Dict
    jsonDecoded = json.loads(jsondata)

    #Get and appends background color for item name
    options = list()
    for k, v in jsonDecoded["rgDescriptions"].iteritems():
        for k1 in v["tags"]:
            if k1.has_key("color"):
                v["background"] = k1["color"]
        if(v.has_key("market_actions")):
            v["actions"] = v.get("market_actions")[0]
        else:
            v["actions"] = False
        
 
    # DEV RETURN
    # return JsonResponse(options, safe=False)


    # Returns items description to render engine
    return render_to_response("inventory.html", {"items": jsonDecoded["rgDescriptions"]}, context_instance=RequestContext(request))

