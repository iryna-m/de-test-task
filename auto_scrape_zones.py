import requests
from bs4 import BeautifulSoup
import json

def scrape_zones(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    zones = {}

    # Assuming zones are listed in a specific structure; this needs to be adjusted based on the actual site structure
    zone_elements = soup.find_all('div', class_='zone')
    for zone in zone_elements:
        zone_name = zone.find('h2').text.strip()
        zone_description = zone.find('p').text.strip()
        zones[zone_name] = zone_description

    return zones

def main():
    links = [
        "https://www.codepublishing.com/WA/AirwayHeights/",
        "https://library.municode.com/wa/albion/codes/code_of_ordinances?nodeId=TIT16ZO_CH16.24REMOHODI",
        "https://algona.municipal.codes/",
        "https://anacortes.municipal.codes/",
        "https://library.municode.com/wa/arlington/codes/code_of_ordinances"
    ]

    all_zones = {}

    for link in links:
        print(f"Scraping {link}...")
        zones = scrape_zones(link)
        all_zones[link] = zones

    with open('zones.json', 'w') as json_file:
        json.dump(all_zones, json_file, indent=4)

    print("Scraping completed. Data saved to zones.json.")

if __name__ == "__main__":
    main()
