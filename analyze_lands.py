import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['real_estate']
collection = db['land_listings']

# Fetch data from MongoDB
data = list(collection.find())
df = pd.DataFrame(data)

# Calculate price per square meter/acre
df['price_per_unit'] = df['price'] / df['area']

# Calculate the average price per square meter/acre for each location
avg_price_per_location = df.groupby('location')['price_per_unit'].mean().reset_index()
avg_price_per_location.columns = ['location', 'average_price_per_unit']

# Identify the top 5 most expensive locations
top_5_locations = avg_price_per_location.sort_values(by='average_price_per_unit', ascending=False).head(5)

# Define thresholds for categorization
cheap_threshold = df['price_per_unit'].quantile(0.33)
moderate_threshold = df['price_per_unit'].quantile(0.66)
expensive_threshold = df['price_per_unit'].max()


def categorize(price):
    if price <= cheap_threshold:
        return 'Cheap'
    elif price <= moderate_threshold:
        return 'Moderate'
    else:
        return 'Expensive'


# Apply categorization
df['category'] = df['price_per_unit'].apply(categorize)

# Update the MongoDB collection with the new field
for index, row in df.iterrows():
    collection.update_one({'_id': row['_id']}, {'$set': {'category': row['category']}})

# Generate the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='location', y='average_price_per_unit', data=top_5_locations)
plt.title('Average Price per Square Meter/Acre for Top 5 Most Expensive Locations')
plt.xlabel('Location')
plt.ylabel('Average Price per Unit')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_locations.png')
