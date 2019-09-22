from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import time

# Create your views here.

def index(request):
    now = time.localtime()
    time_now = time.strftime("%H:%M", now)
    msg = ""
    all_the_bus_infos = []
    urls = ["https://www.vrs.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=d2b20e66ff4314bef3148765ff9ca312",
            "https://www.vrs.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=bad4338506fbba04e76196b375a4b262",
            "https://www.vrs.de/index.php?eID=tx_vrsinfo_ass2_departuremonitor&i=a291d9a880842e293023ba8cf34e7aee"]
    headers = requests.utils.default_headers()
    headers.update({
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    })
    for url in urls:
        r = requests.get(url, headers)
        tries = 0
        while r.status_code != 200 and tries <= 5:
            r = requests.get(url, headers)
            tries = tries + 1
        if tries >= 5:
            msg = "Der Statuscode beträgt: " + str(r.status_code)
        raw_html = r.content
        bus_info = json.loads(raw_html)
        for i in range(0, len(bus_info["events"])):
            bus_info["events"][i]["departure"]["comes_in"] = round((bus_info["events"][i]["departure"]["timestamp"] - time.time()) / 60)
        all_the_bus_infos.append(bus_info)
    return render(request=request,
                  template_name="bus/index.html",
                  context={
                  "bus_info_erich": all_the_bus_infos[0], 
                  "bus_info_hymmen": all_the_bus_infos[1],
                  "bus_info_huegel": all_the_bus_infos[2], 
                  "msg": msg, 
                  "time_now": time_now})