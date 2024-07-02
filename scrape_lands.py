import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import random

# MongoDB setup
try:
    client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
    db = client['real_estate']
    collection = db['land_listings']
    client.server_info()  # Trigger exception if cannot connect to MongoDB
    print("Connected to MongoDB successfully.")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(f"Error: {err}")
    exit()

# Base URLs of the real estate website
base_url_first_page = 'https://www.aresproperties.com.cy/properties?PropertyID=&StatusID=&PropertyTypeID=&PropertySubTypeID=&DistrictID=&TownID=&ParishID=&PriceMIN=&PriceMAX=&AreaMIN=&AreaMAX=&NumberOfBedrooms=&NumberOfBaths=&HasPool=&StarRating=&PlanningType=&Location=&NumberOfBeds='
base_url_other_pages = 'https://www.aresproperties.com.cy/properties/page/'


def get_land_listings(page):
    if page == 1:
        url = base_url_first_page
    else:
        url = f'{base_url_other_pages}{page}?PropertyID=&StatusID=&PropertyTypeID=&PropertySubTypeID=&DistrictID=&TownID=&ParishID=&PriceMIN=&PriceMAX=&AreaMIN=&AreaMAX=&NumberOfBedrooms=&NumberOfBaths=&HasPool=&StarRating=&PlanningType=&Location=&NumberOfBeds='

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    retries = 2
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.exceptions.RequestException as e:
            print(f'Attempt {i + 1} failed: {e}')
            time.sleep(2 ** i + random.uniform(0, 1))

    raise Exception(f"No listings found on page {page}. Ending scrape.")


def parse_listing(listing):
    try:
        title = listing.find('li', class_='spotlight-list-text').find('strong').text.strip()
        price = listing.find('h3', class_='listing-price').text.strip()
        property_id_element = listing.find('li', text=lambda text: text and 'Property ID:' in text)
        property_id = property_id_element.text.split('Property ID:')[1].strip() if property_id_element else 'N/A'
        url = listing.find('a', class_='property-spotlight-image-link')['href']

        size = 'N/A'
        columns = listing.find_all('div', class_='listing-details-column-2')
        for column in columns:
            heading = column.find('div', class_='listing-details-heading-2').text.strip()
            if heading == 'Area':
                size = column.find('div', class_='listing-details-2').text.strip()
                break

        # Extract location from title
        location = 'N/A'
        if ' in ' in title:
            location = title.split(' in ')[-1].strip()
        elif '“' in title and '”, ' in title:
            location = title.split('”, ')[-1].strip()

        date = 'N/A'  # Placeholder if the date is not available

        return {
            'property_id': property_id,
            'title': title,
            'location': location,
            'price': price,
            'size': size,
            'date': date,
            'url': f'https://www.aresproperties.com.cy{url}'
        }
    except AttributeError:
        return None


def scrape_website():
    page = 1
    while True:
        soup = get_land_listings(page)
        listings = soup.find_all('div', class_='property-spotlight-tile')

        if not listings:
            break

        for listing in listings:
            data = parse_listing(listing)
            if data:
                # Check for existing document with the same property_id
                if collection.find_one({"property_id": data["property_id"]}):
                    print(f"Duplicate found for property_id: {data['property_id']}. Skipping insertion.")
                    continue

                print(f"Inserting data: {data}")  # Log the data being inserted
                result = collection.insert_one(data)
                print(f"Data inserted with ID: {result.inserted_id}")  # Log the inserted document ID

                # Verify that the data was inserted
                inserted_data = collection.find_one({"_id": result.inserted_id})
                if inserted_data:
                    print(f"Verified insertion: {inserted_data}")
                else:
                    print(f"Failed to verify insertion for ID: {result.inserted_id}")

        print(f'Scraped page {page} finished. Data inserted: {len(listings)}')  # Log the number of listings scraped
        page += 1

        time.sleep(random.uniform(1, 3))


if __name__ == '__main__':
    try:
        scrape_website()
        print('Scraping complete.')
    except Exception as e:
        print(f'Error: {e}')
