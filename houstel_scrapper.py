import requests
from bs4 import BeautifulSoup
import json

def scrapper(url):
    hostel = {}
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    name_div = soup.find("div", class_ = "container hostel-container")

    try:
        lists = name_div.find_all("li")
        h_name = lists[4].get_text()
        hostel["name"] = h_name
        hostel["city"] = lists[2].get_text()
    except Exception as e:
        print("couldnt find name div")
    
    try:
        h_loc = name_div.find("p").get_text()
        hostel["location"] = h_loc
    except:
        print("couldnt find location div")
    
    try:
        description_div = soup.find("div", class_ = "col-lg-8")
        desc = description_div.find("p").get_text()

        fac_div = soup.find("div", class_ = "row")
        facil = desc + description_div.find("ul").get_text()
        sec_row = description_div.find_all("ul")
        description = facil + sec_row[1].get_text()
        hostel["description"] = description
    except:
        print("couldnt find description div")
    
    try:
        owner_div = soup.find("div", class_ = "warden-info my-3")
        owner_name = owner_div.find("p").get_text()
        hostel["owner_name"] = owner_name
    except:
        print("couldnt find owner div")
    
    try:
        price_div = soup.find("div", class_ = "d-flex flex-column h-100")
        price = price_div.find("li").get_text()
        hostel["price"] = price
    except:
        print("couldnt find price div")
    print(hostel)

    return hostel


names = []
url = "https://houstel.pk/pakistan/islamabad/hostels/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

divs = soup.find_all("div", class_ = "col-12 position-relative")
for div in divs:
   temp = (div.find("a")).get_text()
   names.append(temp)

formatted_hostels = []

for hostel in names:
    clean = hostel.strip().lower().replace('–', '-') 
    clean = clean.replace('(', '').replace(')', '')   
    clean = ' '.join(clean.split())                   
    clean = clean.replace(' ', '-')                   
    clean += '-islamabad'                             
    formatted_hostels.append(clean)

hostels = {"hostels" : []}

for hostel in formatted_hostels:
    complete_url = url+hostel
    data = scrapper(complete_url)
    hostels["hostels"].append(data)

with open("houstel.json", 'w') as f:
  json.dump(hostels, f, indent=4)

