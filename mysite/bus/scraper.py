import requests
from datetime import datetime
from bs4 import BeautifulSoup

links = []
linien = []
zeiten = []
msg = ""

def give_bus_times():
    global links
    global linien
    global zeiten
    global msg
    links = []
    linien = []
    zeiten = []
    msg = ""
    current_date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    current_time = datetime.strftime(datetime.now(), "%H%%3A%M") #Example: 16%3A09 = 16:09
    haltestellen_ids = ["05315%3A11201"] # 05315%3A11201 = Köln-Hbf, add Numbers to scrape here
    haltestellen_namen = ["Köln-Hbf", ""] # has no uses yet


    def links_to_scrape(ids):
        for id in ids:
            links.append("https://www.vrs.de/fahrplan/fahrplanauskunft.html?tx_vrsinfo_pi_connection%5Brequest%5D=result&tx_vrsinfo_pi_connection%5BoriginName%5D=Köln&tx_vrsinfo_pi_connection%5BoriginId%5D=de%3A" + id + "&tx_vrsinfo_pi_connection%5BoriginType%5D=stop&tx_vrsinfo_pi_connection%5BdestinationName%5D=Bonn+Hbf&tx_vrsinfo_pi_connection%5BdestinationId%5D=de%3A05314%3A61101&tx_vrsinfo_pi_connection%5BdestinationType%5D=stop&tx_vrsinfo_pi_connection%5Bdate%5D=" + current_date + "&tx_vrsinfo_pi_connection%5Btime%5D=" + current_time + "&tx_vrsinfo_pi_connection%5BdepartureArrival%5D=departure")

    def scrape(url):
        """Scrape URLs to generate previews."""
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        r = requests.get(url, headers)
        tries = 0
        while r.status_code != 200 and tries <= 5:
            r = requests.get(url, headers)
            tries = tries + 1
        if tries >= 5:
            msg = "Der Statuscode beträgt: " + str(r.status_code)
        raw_html = r.content
        soup = BeautifulSoup(raw_html, 'html.parser')
        route_info = soup.find_all("div", class_="route-segments")
        for bus_lines_info_on_page in route_info:
            bus_line = bus_lines_info_on_page.find("div",{"title": "Linie"})
            bus_departure_time = bus_lines_info_on_page.find("div",{"title": "Abfahrt"})
            if bus_line is not None:
                linien.append(bus_line.get_text(" ", strip=True))
                zeiten.append(bus_departure_time.text)

    links_to_scrape(haltestellen_ids)

    for link in links:
       scrape(link)