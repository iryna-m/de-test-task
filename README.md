# Land Listings Web Scraper

## Objective
This script scrapes land listings from a specified real estate website and stores the data in a MongoDB database.

## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `pymongo` library
- MongoDB

## Setup Instructions

### Step 1: Install Python Libraries
```bash
pip install requests beautifulsoup4 pymongo
```

### Step 2: Set Up MongoDB Database
1. Install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community) and follow the instructions.
2. Start the MongoDB server:
```bash
mongod
```

## Running the scraper

1. Ensure MongoDB is running.
2. Run the Python script:
```bash
python scrape_lands.py
```
3. Start MongoDB shell:
```bash
mongosh
```
4. When connected to `mongosh`, the following commands can be used to access data:
    - `show dbs`
    - `use real_estate`
    - `show collections`
    - `db.land_listings.find().pretty()`

## MongoDB Database Dump

### To create a MongoDB database dump of the scraped data, use the following command:
```bash
mongodump --db real_estate --collection land_listings --out dump/
```


# Land Data Analysis

## Objective
This script analyzes land data stored in a MongoDB database and performs the following operations:
- Calculates the average price per square meter/acre for each location.
- Identifies the top 5 most expensive locations based on the average price per square meter/acre.
- Categorizes the land listings into "Cheap", "Moderate", and "Expensive" based on their price per square meter/acre.
- Generates a bar chart showing the average price per square meter/acre for the top 5 most expensive locations.

## Requirements
- Python 3.x
- Pandas
- Matplotlib
- Seaborn
- Pymongo

You can install the required libraries using pip:
```bash
pip install pandas matplotlib seaborn pymongo
```

# Auto Scrape Zones

## Overview
This Python script scrapes zone information and their descriptions from a nested website structure. 
It collects data from specified URLs and outputs the information in a JSON file.

## Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation
Install the required libraries:

```sh
pip install requests beautifulsoup4
```
